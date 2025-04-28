import sys

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
    ],
)

CATALOG = args.get("catalog")
ICEBERG_S3_PATH = args.get("iceberg_s3_path")
BUCKET_NAME = args.get("bucket_name")

STATS_TYPE_MAP = {
    "playoffs_adjusted_shooting_stats": "adjusted_shooting",
    "playoffs_advanced_stats": "advanced",
    "playoffs_per_36_minutes_stats": "per_36_minutes",
    "playoffs_per_100_possessions_stats": "per_100_possessions",
    "playoffs_per_game_stats": "per_game",
    "playoffs_play_by_play_stats": "play_by_play",
    "playoffs_shooting_stats": "shooting",
    "playoffs_total_stats": "total",
    "regular_season_adjusted_shooting_stats": "adjusted_shooting",
    "regular_season_advanced_stats": "advanced",
    "regular_season_per_36_minutes_stats": "per_36_minutes",
    "regular_season_per_100_possessions_stats": "per_100_possessions",
    "regular_season_per_game_stats": "per_game",
    "regular_season_play_by_play_stats": "play_by_play",
    "regular_season_shooting_stats": "shooting",
    "regular_season_total_stats": "total",
    "rosters": "rosters",
    "salaries": "salaries",
}


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


class TeamStatsETL:
    def __init__(self, spark: SparkSession, s3_uri: str) -> None:
        self.spark = spark
        self.s3_uri = s3_uri

    def read_to_df(self) -> DataFrame:
        """Read a team stats file as a dataframe.

        :return: Dataframe.
        """
        df = self.spark.read.parquet(self.s3_uri)

        return df

    @staticmethod
    def update_percentage_column(df: DataFrame, column: str) -> DataFrame:
        """Update the percentage column by multiplying by 100 and
        rounding it to 1 decimal places.

        :param df: Dataframe to use.
        :param column: A column to update.
        :return: Dataframe with updated column.
        """
        df = df.withColumn(column, F.round(F.col(column) * 100, 1))

        return df

    def update_percentage_columns(
        self, df: DataFrame, stats_type: str
    ) -> DataFrame:
        """Update the percentage columns.

        :param df: Dataframe to use.
        :param stats_type: Stats type.
        :return: Dataframe with updated columns.
        """
        if stats_type == "adjusted_shooting":
            df = self.update_percentage_column(
                df=df, column="field_goal_percentage"
            )
            df = self.update_percentage_column(
                df=df, column="2_point_field_goal_percentage"
            )
            df = self.update_percentage_column(
                df=df, column="3_point_field_goal_percentage"
            )
            df = self.update_percentage_column(
                df=df, column="effective_field_goal_percentage"
            )
            df = self.update_percentage_column(
                df=df, column="free_throw_percentage"
            )
            df = self.update_percentage_column(
                df=df, column="true_shooting_percentage"
            )

        elif stats_type == "advanced":
            df = self.update_percentage_column(
                df=df, column="true_shooting_percentage"
            )

        elif stats_type in [
            "per_36_minutes",
            "per_100_possessions",
            "per_game",
        ]:
            df = self.update_percentage_column(
                df=df, column="field_goal_percentage"
            )
            df = self.update_percentage_column(
                df=df, column="3_point_field_goal_percentage"
            )
            df = self.update_percentage_column(
                df=df, column="2_point_field_goal_percentage"
            )
            df = self.update_percentage_column(
                df=df, column="effective_field_goal_percentage"
            )
            df = self.update_percentage_column(
                df=df, column="free_throw_percentage"
            )

        elif stats_type == "shooting":
            df = self.update_percentage_column(
                df=df, column="field_goal_percentage"
            )
            df = self.update_percentage_column(
                df=df, column="2_point_field_goal_attempts_percentage"
            )
            df = self.update_percentage_column(
                df=df, column="0_3_ft_field_goal_attempts_percentage"
            )
            df = self.update_percentage_column(
                df=df, column="3_10_ft_field_goal_attempts_percentage"
            )
            df = self.update_percentage_column(
                df=df, column="10_16_ft_field_goal_attempts_percentage"
            )
            df = self.update_percentage_column(
                df=df, column="16_ft_3_point_field_goal_attempts_percentage"
            )
            df = self.update_percentage_column(
                df=df, column="3_point_field_goal_attempts_percentage"
            )
            df = self.update_percentage_column(
                df=df, column="2_point_field_goal_percentage"
            )
            df = self.update_percentage_column(
                df=df, column="0_3_ft_field_goal_percentage"
            )
            df = self.update_percentage_column(
                df=df, column="3_10_ft_field_goal_percentage"
            )
            df = self.update_percentage_column(
                df=df, column="10_16_ft_field_goal_percentage"
            )
            df = self.update_percentage_column(
                df=df, column="16_ft_3_point_field_goal_percentage"
            )
            df = self.update_percentage_column(
                df=df, column="3_point_field_goal_percentage"
            )
            df = self.update_percentage_column(
                df=df, column="2_point_assisted_field_goal_percentage"
            )
            df = self.update_percentage_column(
                df=df, column="3_point_assisted_field_goal_percentage"
            )
            df = self.update_percentage_column(
                df=df, column="field_goal_dunk_attempts_percentage"
            )
            df = self.update_percentage_column(
                df=df, column="3_point_field_goal_from_corner_percentage"
            )
            df = self.update_percentage_column(
                df=df,
                column="3_point_field_goal_attempts_from_corner_percentage",
            )

        elif stats_type == "total":
            df = self.update_percentage_column(
                df=df, column="field_goal_percentage"
            )
            df = self.update_percentage_column(
                df=df, column="3_point_field_goal_percentage"
            )
            df = self.update_percentage_column(
                df=df, column="2_point_field_goal_percentage"
            )
            df = self.update_percentage_column(
                df=df, column="effective_field_goal_percentage"
            )
            df = self.update_percentage_column(
                df=df, column="free_throw_percentage"
            )

        return df

    @staticmethod
    def rename_column(df: DataFrame) -> DataFrame:
        """Rename the `team` column to the `team_abbr` one.

        :param df: Dataframe to use.
        :return: Dataframe with renamed column.
        """
        df = df.withColumnRenamed("team", "team_abbr")

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

    @staticmethod
    def update_team_abbr_values(df: DataFrame) -> DataFrame:
        """Update the `team_abbr` column values.

        :param df: Dataframe to use.
        :return: Dataframe with updated column values.
        """
        df = df.withColumn(
            "team_abbr",
            F.when(F.col("team_abbr") == "CHH", F.lit("CHO")).otherwise(
                F.col("team_abbr")
            ),
        )

        return df

    @staticmethod
    def update_data_types(df: DataFrame, stats_type: str) -> DataFrame:
        """Update data types of columns.

        :param df: Dataframe to use.
        :param stats_type: Stats type.
        :return: Dataframe with updated column data types.
        """
        if stats_type == "adjusted_shooting":
            df = df.withColumn("rank", F.col("rank").cast(T.IntegerType()))
            df = df.withColumn("age", F.col("age").cast(T.IntegerType()))
            df = df.withColumn("games", F.col("games").cast(T.IntegerType()))
            df = df.withColumn(
                "games_started", F.col("games_started").cast(T.IntegerType())
            )
            df = df.withColumn(
                "minutes_played", F.col("minutes_played").cast(T.IntegerType())
            )
            df = df.withColumn(
                "adjusted_field_goal",
                F.col("adjusted_field_goal").cast(T.IntegerType()),
            )
            df = df.withColumn(
                "adjusted_2_point_field_goal",
                F.col("adjusted_2_point_field_goal").cast(T.IntegerType()),
            )
            df = df.withColumn(
                "adjusted_3_point_field_goal",
                F.col("adjusted_3_point_field_goal").cast(T.IntegerType()),
            )
            df = df.withColumn(
                "adjusted_effective_field_goal",
                F.col("adjusted_effective_field_goal").cast(T.IntegerType()),
            )
            df = df.withColumn(
                "adjusted_free_throw",
                F.col("adjusted_free_throw").cast(T.IntegerType()),
            )
            df = df.withColumn(
                "adjusted_true_shooting",
                F.col("adjusted_true_shooting").cast(T.IntegerType()),
            )
            df = df.withColumn(
                "adjusted_free_throw_attempt",
                F.col("adjusted_free_throw_attempt").cast(T.IntegerType()),
            )
            df = df.withColumn(
                "adjusted_3_point_attempt",
                F.col("adjusted_3_point_attempt").cast(T.IntegerType()),
            )

        elif stats_type == "advanced":
            df = df.withColumn("rank", F.col("rank").cast(T.IntegerType()))
            df = df.withColumn("age", F.col("age").cast(T.IntegerType()))
            df = df.withColumn("games", F.col("games").cast(T.IntegerType()))
            df = df.withColumn(
                "games_started", F.col("games_started").cast(T.IntegerType())
            )
            df = df.withColumn(
                "minutes_played", F.col("minutes_played").cast(T.IntegerType())
            )

        elif stats_type == "per_36_minutes":
            df = df.withColumn("rank", F.col("rank").cast(T.IntegerType()))
            df = df.withColumn("age", F.col("age").cast(T.IntegerType()))
            df = df.withColumn("games", F.col("games").cast(T.IntegerType()))
            df = df.withColumn(
                "games_started", F.col("games_started").cast(T.IntegerType())
            )
            df = df.withColumn(
                "minutes_played", F.col("minutes_played").cast(T.IntegerType())
            )

        elif stats_type == "per_100_possessions":
            df = df.withColumn("rank", F.col("rank").cast(T.IntegerType()))
            df = df.withColumn("age", F.col("age").cast(T.IntegerType()))
            df = df.withColumn("games", F.col("games").cast(T.IntegerType()))
            df = df.withColumn(
                "games_started", F.col("games_started").cast(T.IntegerType())
            )
            df = df.withColumn(
                "minutes_played", F.col("minutes_played").cast(T.IntegerType())
            )
            df = df.withColumn(
                "offensive_rating",
                F.col("offensive_rating").cast(T.IntegerType()),
            )
            df = df.withColumn(
                "defensive_rating",
                F.col("defensive_rating").cast(T.IntegerType()),
            )

        elif stats_type == "per_game":
            df = df.withColumn("rank", F.col("rank").cast(T.IntegerType()))
            df = df.withColumn("age", F.col("age").cast(T.IntegerType()))
            df = df.withColumn("games", F.col("games").cast(T.IntegerType()))
            df = df.withColumn(
                "games_started", F.col("games_started").cast(T.IntegerType())
            )

        elif stats_type == "play_by_play":
            df = df.withColumn("rank", F.col("rank").cast(T.IntegerType()))
            df = df.withColumn("age", F.col("age").cast(T.IntegerType()))
            df = df.withColumn("games", F.col("games").cast(T.IntegerType()))
            df = df.withColumn(
                "games_started", F.col("games_started").cast(T.IntegerType())
            )
            df = df.withColumn(
                "minutes_played", F.col("minutes_played").cast(T.IntegerType())
            )
            df = df.withColumn(
                "turnovers_by_bad_pass",
                F.col("turnovers_by_bad_pass").cast(T.IntegerType()),
            )
            df = df.withColumn(
                "lost_ball_turnovers",
                F.col("lost_ball_turnovers").cast(T.IntegerType()),
            )
            df = df.withColumn(
                "shooting_fouls", F.col("shooting_fouls").cast(T.IntegerType())
            )
            df = df.withColumn(
                "offensive_fouls",
                F.col("offensive_fouls").cast(T.IntegerType()),
            )
            df = df.withColumn(
                "shooting_fouls_drawn",
                F.col("shooting_fouls_drawn").cast(T.IntegerType()),
            )
            df = df.withColumn(
                "offensive_fouls_drawn",
                F.col("offensive_fouls_drawn").cast(T.IntegerType()),
            )
            df = df.withColumn(
                "point_generated_by_assists",
                F.col("point_generated_by_assists").cast(T.IntegerType()),
            )
            df = df.withColumn(
                "fouled_field_goals",
                F.col("fouled_field_goals").cast(T.IntegerType()),
            )
            df = df.withColumn(
                "blocked_field_goal_attempts",
                F.col("blocked_field_goal_attempts").cast(T.IntegerType()),
            )

        elif stats_type == "shooting":
            df = df.withColumn("rank", F.col("rank").cast(T.IntegerType()))
            df = df.withColumn("age", F.col("age").cast(T.IntegerType()))
            df = df.withColumn("games", F.col("games").cast(T.IntegerType()))
            df = df.withColumn(
                "games_started", F.col("games_started").cast(T.IntegerType())
            )
            df = df.withColumn(
                "minutes_played", F.col("minutes_played").cast(T.IntegerType())
            )
            df = df.withColumn(
                "number_of_made_dunk_attempts",
                F.col("number_of_made_dunk_attempts").cast(T.IntegerType()),
            )
            df = df.withColumn(
                "heave_attempts", F.col("heave_attempts").cast(T.IntegerType())
            )
            df = df.withColumn(
                "heaves_made", F.col("heaves_made").cast(T.IntegerType())
            )

        elif stats_type == "total":
            df = df.withColumn("rank", F.col("rank").cast(T.IntegerType()))
            df = df.withColumn("age", F.col("age").cast(T.IntegerType()))
            df = df.withColumn("games", F.col("games").cast(T.IntegerType()))
            df = df.withColumn(
                "games_started", F.col("games_started").cast(T.IntegerType())
            )
            df = df.withColumn(
                "minutes_played", F.col("minutes_played").cast(T.IntegerType())
            )
            df = df.withColumn(
                "field_goals", F.col("field_goals").cast(T.IntegerType())
            )
            df = df.withColumn(
                "field_goal_attempts",
                F.col("field_goal_attempts").cast(T.IntegerType()),
            )
            df = df.withColumn(
                "3_point_field_goals",
                F.col("3_point_field_goals").cast(T.IntegerType()),
            )
            df = df.withColumn(
                "3_point_field_goal_attempts",
                F.col("3_point_field_goal_attempts").cast(T.IntegerType()),
            )
            df = df.withColumn(
                "2_point_field_goals",
                F.col("2_point_field_goals").cast(T.IntegerType()),
            )
            df = df.withColumn(
                "2_point_field_goal_attempts",
                F.col("2_point_field_goal_attempts").cast(T.IntegerType()),
            )
            df = df.withColumn(
                "free_throws", F.col("free_throws").cast(T.IntegerType())
            )
            df = df.withColumn(
                "free_throw_attempts",
                F.col("free_throw_attempts").cast(T.IntegerType()),
            )
            df = df.withColumn(
                "offensive_rebounds",
                F.col("offensive_rebounds").cast(T.IntegerType()),
            )
            df = df.withColumn(
                "defensive_rebounds",
                F.col("defensive_rebounds").cast(T.IntegerType()),
            )
            df = df.withColumn(
                "total_rebounds", F.col("total_rebounds").cast(T.IntegerType())
            )
            df = df.withColumn(
                "assists", F.col("assists").cast(T.IntegerType())
            )
            df = df.withColumn("steals", F.col("steals").cast(T.IntegerType()))
            df = df.withColumn("blocks", F.col("blocks").cast(T.IntegerType()))
            df = df.withColumn(
                "turnovers", F.col("turnovers").cast(T.IntegerType())
            )
            df = df.withColumn(
                "personal_fouls", F.col("personal_fouls").cast(T.IntegerType())
            )
            df = df.withColumn("points", F.col("points").cast(T.IntegerType()))
            df = df.withColumn(
                "triple_doubles", F.col("triple_doubles").cast(T.IntegerType())
            )

        elif stats_type == "rosters":
            df = df.withColumn(
                "birth_date",
                F.to_date(F.col("birth_date"), format="MMMM d, yyyy"),
            )

        elif stats_type == "salaries":
            df = df.withColumn("rank", F.col("rank").cast(T.IntegerType()))

        return df

    @staticmethod
    def update_awards_values(df: DataFrame) -> DataFrame:
        """Replace the `null` values with the `No Awards` values for the
        `awards` column.

        :param df: Dataframe to use.
        :return: Dataframe with update awards values.
        """
        if "awards" not in df.columns:
            return df

        df = df.withColumn(
            "awards",
            F.when(F.col("awards").isNull(), F.lit("No Awards")).otherwise(
                F.col("awards")
            ),
        )

        return df

    @staticmethod
    def update_salary_values(df: DataFrame) -> DataFrame:
        """Remove the `$` sign from the salary values and
        update their data types.

        :param df: Dataframe to use.
        :return: Dataframe with updated salary values.
        """
        df = df.withColumn(
            "salary", F.regexp_replace(F.col("salary"), "\\$", "")
        )
        df = df.withColumn(
            "salary",
            F.regexp_replace(F.col("salary"), ",", "").cast(T.IntegerType()),
        )

        return df

    @staticmethod
    def update_country_of_birth_values(df: DataFrame) -> DataFrame:
        """Remove the 1st part of the country before the empty space
        character.

        :param df: Dataframe to use.
        :return: Dataframe with updated country values.
        """
        df = df.withColumn(
            "country_of_birth", F.split(F.col("country_of_birth"), " ")[1]
        )

        return df

    def add_columns_sk(self, df: DataFrame) -> DataFrame:
        """Add surrogate columns to the dataframe.

        :param df: Dataframe to use.
        :return: Dataframe with surrogate keys added.
        """
        df = self.add_column_sk(df=df, column="team_abbr", column_sk="team_sk")
        df = self.add_column_sk(df=df, column="season", column_sk="season_sk")
        df = self.add_column_sk(df=df, column="player", column_sk="player_sk")

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

    retriever = Retriever(prefix="teams_stats")

    objects_metadata = retriever.get_objects_metadata()

    for object_metadata in objects_metadata:
        s3_uri = object_metadata.get("s3_uri")
        db_name = object_metadata.get("db_name")
        table_name = object_metadata.get("table_name")

        stats_type = STATS_TYPE_MAP.get(table_name)

        team_stats_etl = TeamStatsETL(spark=spark, s3_uri=s3_uri)

        team_stats_df = team_stats_etl.read_to_df()
        team_stats_df = team_stats_etl.rename_column(df=team_stats_df)
        team_stats_df = team_stats_etl.update_team_abbr_values(
            df=team_stats_df
        )
        team_stats_df = team_stats_etl.update_awards_values(df=team_stats_df)

        if stats_type == "rosters":
            team_stats_df = team_stats_etl.update_country_of_birth_values(
                df=team_stats_df
            )

        elif stats_type == "salaries":
            team_stats_df = team_stats_etl.update_salary_values(
                df=team_stats_df
            )

        else:
            team_stats_df = team_stats_etl.update_percentage_columns(
                df=team_stats_df, stats_type=stats_type
            )

        team_stats_df = team_stats_etl.update_data_types(
            df=team_stats_df, stats_type=stats_type
        )

        team_stats_df = team_stats_etl.add_columns_sk(df=team_stats_df)

        team_stats_etl.write_to_iceberg(
            df=team_stats_df,
            catalog=CATALOG,
            db_name=db_name,
            table_name=table_name,
        )

    job.commit()


# Execute the job.
run()
