import sys

import boto3
import pyspark.sql.functions as F
from awsglue.utils import getResolvedOptions
from awsglue.context import GlueContext
from awsglue.dynamicframe import DynamicFrame
from awsglue.job import Job
from awsglue.transforms import SelectFromCollection
from awsgluedq.transforms import EvaluateDataQuality
from botocore.paginate import PageIterator
from pyspark import SparkConf
from pyspark.context import SparkContext
from pyspark.sql import DataFrame, SparkSession


args = getResolvedOptions(
    sys.argv,
    [
        "JOB_NAME",
        "catalog",
        "iceberg_s3_path",
        "bucket_name",
        "teams_map_s3_path",
        "glue_jobs_bucket_name",
        "dq_rules_prefix",
    ],
)

CATALOG = args.get("catalog")
ICEBERG_S3_PATH = args.get("iceberg_s3_path")
BUCKET_NAME = args.get("bucket_name")
TEAMS_MAP_S3_PATH = args.get("teams_map_s3_path")
GLUE_JOBS_BUCKET_NAME = args.get("glue_jobs_bucket_name")
DQ_RULES_PREFIX = args.get("dq_rules_prefix")

DQ_COLUMNS_TO_DROP = [
    "DataQualityRulesPass",
    "DataQualityRulesFail",
    "DataQualityRulesSkip",
    "DataQualityEvaluationResult",
]


def set_spark_iceberg_conf(catalog: str, iceberg_s3_path: str) -> SparkConf:
    """Setting up Spark configurations.

    :param catalog: A catalog name.
    :param iceberg_s3_path: S3 path to Iceberg warehouse.
    :return: Configurations.
    """
    conf_list = [
        (
            f"spark.sql.catalog.{catalog}",
            "org.apache.iceberg.spark.SparkCatalog",
        ),
        (f"spark.sql.catalog.{catalog}.warehouse", iceberg_s3_path),
        (
            f"spark.sql.catalog.{catalog}.catalog-impl",
            "org.apache.iceberg.aws.glue.GlueCatalog",
        ),
        (
            f"spark.sql.catalog.{catalog}.io-impl",
            "org.apache.iceberg.aws.s3.S3FileIO",
        ),
    ]

    spark_conf = SparkConf().setAll(conf_list)

    return spark_conf


class S3Client:
    def __init__(self) -> None:
        self._client_name = "s3"

    def _get_s3_client(self) -> boto3.client:
        """Initialize an S3 client.

        :return: S3 client.
        """
        s3_client = boto3.client(self._client_name)

        return s3_client


class Retriever(S3Client):
    def __init__(self, prefix: str) -> None:
        super().__init__()
        self.prefix = f"bronze/{prefix}"
        self._db_name_prefix = "silver_"

    def get_pages(self) -> PageIterator:
        """Get a list of pages as objects metadata.

        :return: List of pages.
        """
        s3_client = self._get_s3_client()

        paginator = s3_client.get_paginator("list_objects_v2")
        pages = paginator.paginate(Bucket=BUCKET_NAME, Prefix=self.prefix)

        return pages

    @staticmethod
    def get_table_name(filename: str) -> str:
        """Get a table name from the specified filename.

        :param filename: A filename.
        :return: Extracted table name.
        """
        table_name = filename.replace(".parquet", "").replace("-", "_")

        return table_name

    def get_object_metadata(self, key: str) -> dict[str, str]:
        """Get an object metadata from the specified key.

        :param key: A key from which to extract object metadata.
        :return: Extracted object metadata.
        """
        values = key.split("/")

        table_name = self.get_table_name(filename=values[-1])
        db_name = None

        if len(values) == 4:
            db_name = f"{self._db_name_prefix}{values[-3]}"

        elif len(values) == 3:
            db_name = f"{self._db_name_prefix}{values[-2]}"

        object_metadata = {
            "s3_uri": f"s3://{BUCKET_NAME}/{key}",
            "db_name": db_name,
            "table_name": table_name,
        }

        return object_metadata

    def get_objects_metadata(self) -> list[dict[str, str]]:
        """Get a list of objects metadata.

        :return: List of objects metadata.
        """
        pages = self.get_pages()

        objects_metadata = []

        for page in pages:
            for obj in page.get("Contents", []):
                key = obj.get("Key")

                if not key.endswith(f"{self.prefix.split('/')[-1]}.parquet"):
                    continue

                object_metadata = self.get_object_metadata(key=key)

                objects_metadata.append(object_metadata)

        return objects_metadata


class DQ(S3Client):
    def __init__(self, db_name: str, table_name: str) -> None:
        super().__init__()
        self.db_name = db_name
        self.table_name = table_name

    def _get_dq_rules_key(self) -> str:
        """Get the key to the data quality rules file.

        :return: DQ rules key.
        """
        dq_rules_key = (
            f"{DQ_RULES_PREFIX}/{self.db_name}.{self.table_name}.txt"
        )

        return dq_rules_key

    def get_dq_rules(self) -> str:
        """Get a list of data quality rules.

        :return: DQ rules.
        """
        s3_client = self._get_s3_client()
        dq_rules_key = self._get_dq_rules_key()

        response = s3_client.get_object(
            Bucket=GLUE_JOBS_BUCKET_NAME, Key=dq_rules_key
        )

        body = response.get("Body")
        dq_rules = body.read().decode("utf-8")

        return dq_rules


class ConferenceETL:
    def __init__(self, spark: SparkSession, s3_uri: str) -> None:
        self.spark = spark
        self.s3_uri = s3_uri

    def read_to_df(self) -> DataFrame:
        """Read a conference file as a dataframe.

        :return: Dataframe.
        """
        df = self.spark.read.parquet(self.s3_uri)

        return df

    def get_teams_map_df(self) -> DataFrame:
        """Read a teams mapping file as a dataframe.

        :return: Dataframe.
        """
        df = self.spark.read.json(TEAMS_MAP_S3_PATH)

        return df

    @staticmethod
    def update_wins_loss_percentage_values(df: DataFrame) -> DataFrame:
        """Update the `wins_loss_percentage` column values
        by multiplying them by 100.

        :param df: Dataframe to use.
        :return: Dataframe with updated `wins_loss_percentage`
            column values.
        """
        df = df.withColumn(
            "wins_loss_percentage",
            F.round(F.col("wins_loss_percentage") * 100, 1),
        )

        return df

    def add_team_abbr_column(self, df: DataFrame) -> DataFrame:
        """Add the team abbreviation column to the dataframe
        based on the team column values.

        :param df: Dataframe to use.
        :return: Dataframe with team abbreviation column added.
        """
        teams_map_df = self.get_teams_map_df()

        df = df.join(teams_map_df, on="team", how="left")

        return df

    @staticmethod
    def add_column_sk(df: DataFrame, column: str, column_sk: str) -> DataFrame:
        """Add a surrogate column based on the specified column.

        :param df: Dataframe to use.
        :param column: A column to hash.
        :param column_sk: Surrogate column name.
        :return: Dataframe with surrogate key added.
        """
        df = df.withColumn(column_sk, F.md5(column))

        return df

    def add_sk_columns(self, df: DataFrame) -> DataFrame:
        """Add surrogate columns to the dataframe.

        :param df: Dataframe to use.
        :return: Dataframe with surrogate keys added.
        """
        df = self.add_column_sk(df=df, column="season", column_sk="season_sk")
        df = self.add_column_sk(
            df=df, column="conference", column_sk="conference_sk"
        )
        df = self.add_column_sk(
            df=df, column="division", column_sk="division_sk"
        )
        df = self.add_column_sk(df=df, column="team_abbr", column_sk="team_sk")

        return df

    def is_table_exist(self, table_path: str) -> bool:
        """Check whether the table exists.

        :param table_path: A name of the table to check.
        :return: True if table exists, otherwise False.
        """
        is_exist = self.spark.catalog.tableExists(table_path)

        return is_exist

    @staticmethod
    def get_dyf(
        df: DataFrame, glue_context: GlueContext, db_name: str, table_name: str
    ) -> DynamicFrame:
        """Get a dynamic frame from the Spark dataframe.

        :param df: Dataframe to use.
        :param glue_context: AWS Glue context.
        :param db_name: The database name registered in AWS Glue.
        :param table_name: The table name that will be stored in
            the Iceberg format.
        :return: DynamicFrame.
        """
        dyf = DynamicFrame.fromDF(
            dataframe=df,
            glue_ctx=glue_context,
            name=f"{db_name}__{table_name}_dyf",
        )

        return dyf

    @staticmethod
    def evaluate_dyf(
        dyf: DynamicFrame, dq_rules: str, db_name: str, table_name: str
    ) -> tuple[DataFrame, DataFrame]:
        """Evaludate the dynamic frame against the data quality rulues.

        :param dyf: Dynamic frame for evaluation.
        :param dq_rules: Data quality rules.
        :param db_name: The database name registered in AWS Glue.
        :param table_name: The table name that will be stored in
            the Iceberg format.
        :return: Dataframes with `Passed` and `Failed` statuses.
        """
        dq_multiframe = EvaluateDataQuality().process_rows(
            frame=dyf,
            ruleset=dq_rules,
            publishing_options={
                "dataQualityEvaluationContext": f"{db_name}__{table_name}",
                "enableDataQualityCloudWatchMetrics": False,
                "enableDataQualityResultsPublishing": False,
            },
            additional_options={"performanceTuning.caching": "CACHE_NOTHING"},
        )

        dq_row_level_outcomes = SelectFromCollection.apply(
            dfc=dq_multiframe,
            key="rowLevelOutcomes",
        )
        dq_row_level_outcomes_df = dq_row_level_outcomes.toDF()

        passed_df = dq_row_level_outcomes_df.filter(
            F.col("DataQualityEvaluationResult") == "Passed"
        )
        passed_df = passed_df.drop(*DQ_COLUMNS_TO_DROP)

        failed_df = dq_row_level_outcomes_df.filter(
            F.col("DataQualityEvaluationResult") == "Failed"
        )

        return passed_df, failed_df

    def write_to_iceberg(
        self, df: DataFrame, catalog: str, db_name: str, table_name: str
    ) -> None:
        """Write the dataframe to the Iceberg table.

        :param df: Dataframe to write.
        :param catalog: Logical catalog name.
        :param db_name: The database name registered in AWS Glue.
        :param table_name: The table name that will be stored in
            the Iceberg format.
        :return: None.
        """
        table_path = f"{catalog}.{db_name}.{table_name}"

        is_exist = self.is_table_exist(table_path=table_path)

        if not is_exist:
            df.writeTo(table_path).using("iceberg").partitionedBy(
                F.col("season")
            ).create()
        else:
            df.writeTo(table_path).using("iceberg").overwritePartitions()


def run() -> None:
    """Run the conference ETL pipeline.

    :return: None.
    """
    conf = set_spark_iceberg_conf(
        catalog=CATALOG, iceberg_s3_path=ICEBERG_S3_PATH
    )
    sc = SparkContext(conf=conf)
    glue_context = GlueContext(sc)
    spark = glue_context.spark_session
    job = Job(glue_context)
    job.init(args["JOB_NAME"], args)

    retriever = Retriever(prefix="conferences")

    objects_metadata = retriever.get_objects_metadata()

    for object_metadata in objects_metadata:
        s3_uri = object_metadata.get("s3_uri")
        db_name = object_metadata.get("db_name")
        table_name = object_metadata.get("table_name")

        dq = DQ(db_name=db_name, table_name=table_name)
        dq_rules = dq.get_dq_rules()

        conference_etl = ConferenceETL(spark=spark, s3_uri=s3_uri)

        conference_df = conference_etl.read_to_df()
        conference_df = conference_etl.add_team_abbr_column(df=conference_df)
        conference_df = conference_etl.update_wins_loss_percentage_values(
            df=conference_df
        )
        conference_df = conference_etl.add_sk_columns(df=conference_df)

        conference_dyf = conference_etl.get_dyf(
            df=conference_df,
            glue_context=glue_context,
            db_name=db_name,
            table_name=table_name,
        )
        passed_conference_df, failed_conference_df = (
            conference_etl.evaluate_dyf(
                dyf=conference_dyf,
                dq_rules=dq_rules,
                db_name=db_name,
                table_name=table_name,
            )
        )

        conference_etl.write_to_iceberg(
            df=passed_conference_df,
            catalog=CATALOG,
            db_name=db_name,
            table_name=table_name,
        )

        conference_etl.write_to_iceberg(
            df=failed_conference_df,
            catalog=CATALOG,
            db_name=db_name,
            table_name=f"{table_name}_quarantine",
        )

    job.commit()


# Execute the job.
run()
