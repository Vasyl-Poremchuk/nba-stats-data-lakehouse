import sys
from enum import StrEnum

import boto3
import pyspark.sql.functions as F
import pyspark.sql.types as T
from awsglue.utils import getResolvedOptions
from awsglue.context import GlueContext
from awsglue.job import Job
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
    ],
)

CATALOG = args.get("catalog")
ICEBERG_S3_PATH = args.get("iceberg_s3_path")
BUCKET_NAME = args.get("bucket_name")
TEAMS_MAP_S3_PATH = args.get("teams_map_s3_path")


class TopPerformer(StrEnum):
    BY_POINTS = "top_performer_by_points"
    BY_REBOUNDS = "top_performer_by_rebounds"
    BY_ASSISTS = "top_performer_by_assists"
    BY_WIN_SHARES = "top_performer_by_win_shares"


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


class Retriever:
    def __init__(self, prefix: str) -> None:
        self.prefix = f"bronze/{prefix}"
        self._client_name = "s3"
        self._db_name_prefix = "silver_"

    def _get_s3_client(self) -> boto3.client:
        """Initialize an S3 client.

        :return: S3 client.
        """
        s3_client = boto3.client(self._client_name)

        return s3_client

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

                object_metadata = self.get_object_metadata(key=key)

                objects_metadata.append(object_metadata)

        return objects_metadata


class SeasonETL:
    def __init__(self, spark: SparkSession, s3_uri: str) -> None:
        self.spark = spark
        self.s3_uri = s3_uri

    def read_to_df(self) -> DataFrame:
        """Read a season file as a dataframe.

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
    def split_column(df: DataFrame, column: str) -> DataFrame:
        """Split the column into an array with 2 values, such as
        player and metric.

        :param df: Dataframe to use.
        :param column: A column to split.
        :return: Dataframe with divided values in the column.
        """
        df = df.withColumn(column, F.regexp_replace(column, r"\)", ""))

        df = df.withColumn(column, F.split(column, "\u00a0\\("))

        return df

    def split_columns(self, df: DataFrame) -> DataFrame:
        """Split all the necessary columns of the dataframe into arrays.

        :param df: Dataframe to use.
        :return: Dataframe with the divided columns.
        """
        df = self.split_column(df=df, column=TopPerformer.BY_ASSISTS)
        df = self.split_column(df=df, column=TopPerformer.BY_POINTS)
        df = self.split_column(df=df, column=TopPerformer.BY_REBOUNDS)
        df = self.split_column(df=df, column=TopPerformer.BY_WIN_SHARES)

        return df

    def add_team_abbr_column(self, df: DataFrame) -> DataFrame:
        """Add the team abbreviation column to the dataframe
        based on the team column values.

        :param df: Dataframe to use.
        :return: Dataframe with team abbreviation column added.
        """
        teams_map_df = self.get_teams_map_df()

        df = df.join(
            teams_map_df, on=df["champion"] == teams_map_df["team"], how="left"
        ).drop("team")

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

    def add_columns_sk(self, df: DataFrame) -> DataFrame:
        """Add surrogate columns to the dataframe.

        :param df: Dataframe to use.
        :return: Dataframe with surrogate keys added.
        """
        df = self.add_column_sk(df=df, column="team_abbr", column_sk="team_sk")
        df = self.add_column_sk(df=df, column="mvp", column_sk="mvp_sk")
        df = self.add_column_sk(
            df=df,
            column="rookie_of_the_year",
            column_sk="rookie_of_the_year_sk",
        )
        df = self.add_column_sk(df=df, column="season", column_sk="season_sk")

        return df

    def get_top_performer_df(
        self,
        df: DataFrame,
        top_performer_column: str,
        metric_column: str,
        data_type: T.IntegerType | T.FloatType,
    ) -> DataFrame:
        """Get the top performer data as a dataframe.

        :param df: Dataframe to use.
        :param top_performer_column: A column of the top performer
            metric.
        :param metric_column: A column name of the metric value.
        :param data_type: Data type to use.
        :return: Dataframe with the top performer values.
        """
        df = df.select("season_sk", "season", top_performer_column)

        df = df.withColumn("player", F.col(top_performer_column)[0])
        df = df.withColumn(
            metric_column, F.col(top_performer_column)[1].cast(data_type)
        )

        df = df.drop(top_performer_column)

        df = self.add_column_sk(df=df, column="player", column_sk="player_sk")

        return df

    def get_top_performer_dfs(self, df: DataFrame) -> list[DataFrame]:
        """Get top performer data as a list of dataframes.

        :param df: Dataframe to use.
        :return: List of top performer dataframes.
        """
        top_performer_by_points_df = self.get_top_performer_df(
            df=df,
            top_performer_column=TopPerformer.BY_POINTS,
            metric_column="points",
            data_type=T.IntegerType(),
        )
        top_performer_by_rebounds_df = self.get_top_performer_df(
            df=df,
            top_performer_column=TopPerformer.BY_REBOUNDS,
            metric_column="rebounds",
            data_type=T.IntegerType(),
        )
        top_performer_by_assists_df = self.get_top_performer_df(
            df=df,
            top_performer_column=TopPerformer.BY_ASSISTS,
            metric_column="assists",
            data_type=T.IntegerType(),
        )
        top_performer_by_win_shares_df = self.get_top_performer_df(
            df=df,
            top_performer_column=TopPerformer.BY_WIN_SHARES,
            metric_column="win_shares",
            data_type=T.FloatType(),
        )

        top_performer_dfs = [
            top_performer_by_points_df,
            top_performer_by_rebounds_df,
            top_performer_by_assists_df,
            top_performer_by_win_shares_df,
        ]

        return top_performer_dfs

    @staticmethod
    def drop_columns(df: DataFrame) -> DataFrame:
        """Drop top performer columns from the dataframe.

        :param df: Dataframe to use.
        :return: Dataframe with the dropped columns.
        """
        df = df.drop(
            TopPerformer.BY_POINTS,
            TopPerformer.BY_REBOUNDS,
            TopPerformer.BY_ASSISTS,
            TopPerformer.BY_WIN_SHARES,
        )

        return df

    def is_table_exist(self, table_path: str) -> bool:
        """Check whether the table exists.

        :param table_path: A name of the table to check.
        :return: True if table exists, otherwise False.
        """
        is_exist = self.spark.catalog.tableExists(table_path)

        return is_exist

    def write_to_iceberg(
        self, df: DataFrame, catalog: str, db_name: str, table_name: str
    ) -> None:
        """Write the dataframe to the Iceberg table.

        :param df: Dataframe to write.
        :param catalog: Logical catalog name.
        :param db_name: The database name registered in AWS Glue.
        :param table_name: The table name that will be stored
            in the Iceberg format.
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
    """Run the conference stats ETL job.

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

    retriever = Retriever(prefix="seasons")

    objects_metadata = retriever.get_objects_metadata()

    for object_metadata in objects_metadata:
        s3_uri = object_metadata.get("s3_uri")
        db_name = object_metadata.get("db_name")
        table_name = object_metadata.get("table_name")

        season_etl = SeasonETL(spark=spark, s3_uri=s3_uri)

        season_df = season_etl.read_to_df()
        season_df = season_etl.split_columns(df=season_df)
        season_df = season_etl.add_team_abbr_column(df=season_df)
        season_df = season_etl.add_columns_sk(df=season_df)

        top_performer_dfs = season_etl.get_top_performer_dfs(df=season_df)
        (
            top_performer_by_points_df,
            top_performer_by_rebounds,
            top_performer_by_assists,
            top_performer_by_win_shares,
        ) = top_performer_dfs
        season_df = season_etl.drop_columns(df=season_df)

        season_etl.write_to_iceberg(
            df=season_df,
            catalog=CATALOG,
            db_name=db_name,
            table_name=table_name,
        )
        season_etl.write_to_iceberg(
            df=top_performer_by_points_df,
            catalog=CATALOG,
            db_name=db_name,
            table_name=TopPerformer.BY_POINTS,
        )
        season_etl.write_to_iceberg(
            df=top_performer_by_rebounds,
            catalog=CATALOG,
            db_name=db_name,
            table_name=TopPerformer.BY_REBOUNDS,
        )
        season_etl.write_to_iceberg(
            df=top_performer_by_assists,
            catalog=CATALOG,
            db_name=db_name,
            table_name=TopPerformer.BY_ASSISTS,
        )
        season_etl.write_to_iceberg(
            df=top_performer_by_win_shares,
            catalog=CATALOG,
            db_name=db_name,
            table_name=TopPerformer.BY_WIN_SHARES,
        )

    job.commit()


# Execute the job.
run()
