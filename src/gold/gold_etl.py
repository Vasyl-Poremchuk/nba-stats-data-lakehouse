import sys

import boto3
import pyspark.sql.functions as F
from awsglue.utils import getResolvedOptions
from awsglue.context import GlueContext
from awsglue.dynamicframe import DynamicFrame
from awsglue.job import Job
from awsglue.transforms import SelectFromCollection
from awsgluedq.transforms import EvaluateDataQuality
from pyspark import SparkConf, SparkContext
from pyspark.sql import DataFrame, SparkSession


args = getResolvedOptions(
    sys.argv,
    [
        "JOB_NAME",
        "catalog",
        "iceberg_s3_path",
        "glue_jobs_bucket_name",
        "dq_rules_prefix",
    ],
)

CATALOG = args.get("catalog")
ICEBERG_S3_PATH = args.get("iceberg_s3_path")
GLUE_JOBS_BUCKET_NAME = args.get("glue_jobs_bucket_name")
DQ_RULES_PREFIX = args.get("dq_rules_prefix")

DQ_COLUMNS_TO_DROP = [
    "DataQualityRulesPass",
    "DataQualityRulesFail",
    "DataQualityRulesSkip",
    "DataQualityEvaluationResult",
]

TABLES_MAP = {
    "seasons": ("gold_seasons", "dim_season"),
    "champions": ("gold_champions", "dim_champion"),
    "mvps": ("gold_mvps", "dim_mvp"),
    "rookies": ("gold_rookies", "dim_rookie"),
    "conferences": ("gold_conferences", "dim_conference"),
    "divisions": ("gold_divisions", "dim_division"),
    "teams": ("gold_teams", "dim_team"),
    "arenas": ("gold_arenas", "dim_arena"),
    "players": ("gold_players", "dim_player"),
    "rosters": ("gold_rosters", "dim_roster"),
    "top_performers_by_assists": (
        "gold_top_performers_by_assists",
        "fact_top_performer_by_assists",
    ),
    "top_performers_by_points": (
        "gold_top_performers_by_points",
        "fact_top_performer_by_points",
    ),
    "top_performers_by_rebounds": (
        "gold_top_performers_by_rebounds",
        "fact_top_performer_by_rebounds",
    ),
    "top_performers_by_win_shares": (
        "gold_top_performers_by_win_shares",
        "fact_top_performer_by_win_shares",
    ),
    "conferences_stats": ("gold_conferences_stats", "fact_conference_stats"),
    "teams_per_game_stats": (
        "gold_teams_per_game_stats",
        "fact_team_per_game_stats",
    ),
    "teams_total_stats": ("gold_teams_total_stats", "fact_team_total_stats"),
    "teams_per_100_possessions_stats": (
        "gold_teams_per_100_possessions_stats",
        "fact_team_per_100_possessions_stats",
    ),
    "teams_advanced_stats": (
        "gold_teams_advanced_stats",
        "fact_team_advanced_stats",
    ),
    "teams_shooting_stats": (
        "gold_teams_shooting_stats",
        "fact_team_shooting_stats",
    ),
    "opponents_per_game_stats": (
        "gold_opponents_per_game_stats",
        "fact_opponent_per_game_stats",
    ),
    "opponents_total_stats": (
        "gold_opponents_total_stats",
        "fact_opponent_total_stats",
    ),
    "opponents_per_100_possessions_stats": (
        "gold_opponents_per_100_possessions_stats",
        "fact_opponent_per_100_possessions_stats",
    ),
    "opponents_shooting_stats": (
        "gold_opponents_shooting_stats",
        "fact_opponent_shooting_stats",
    ),
    "regular_season_players_per_game_stats": (
        "gold_regular_season_players_per_game_stats",
        "fact_regular_season_player_per_game_stats",
    ),
    "regular_season_players_total_stats": (
        "gold_regular_season_players_total_stats",
        "fact_regular_season_player_total_stats",
    ),
    "regular_season_players_per_36_minutes_stats": (
        "gold_regular_season_players_per_36_minutes_stats",
        "fact_regular_season_player_per_36_minutes_stats",
    ),
    "regular_season_players_per_100_possessions_stats": (
        "gold_regular_season_players_per_100_possessions_stats",
        "fact_regular_season_player_per_100_possessions_stats",
    ),
    "regular_season_players_advanced_stats": (
        "gold_regular_season_players_advanced_stats",
        "fact_regular_season_player_advanced_stats",
    ),
    "regular_season_players_adjusted_shooting_stats": (
        "gold_regular_season_players_adjusted_shooting_stats",
        "fact_regular_season_player_adjusted_shooting_stats",
    ),
    "regular_season_players_shooting_stats": (
        "gold_regular_season_players_shooting_stats",
        "fact_regular_season_player_shooting_stats",
    ),
    "regular_season_players_play_by_play_stats": (
        "gold_regular_season_players_play_by_play_stats",
        "fact_regular_season_player_play_by_play_stats",
    ),
    "playoffs_players_per_game_stats": (
        "gold_playoffs_players_per_game_stats",
        "fact_playoffs_player_per_game_stats",
    ),
    "playoffs_players_total_stats": ("", "fact_playoffs_player_total_stats"),
    "playoffs_players_per_36_minutes_stats": (
        "gold_playoffs_players_per_36_minutes_stats",
        "fact_playoffs_player_per_36_minutes_stats",
    ),
    "playoffs_players_per_100_possessions_stats": (
        "gold_playoffs_players_per_100_possessions_stats",
        "fact_playoffs_player_per_100_possessions_stats",
    ),
    "playoffs_players_advanced_stats": (
        "gold_playoffs_players_advanced_stats",
        "fact_playoffs_player_advanced_stats",
    ),
    "playoffs_players_adjusted_shooting_stats": (
        "gold_playoffs_players_adjusted_shooting_stats",
        "fact_playoffs_player_adjusted_shooting_stats",
    ),
    "playoffs_players_shooting_stats": (
        "gold_playoffs_players_shooting_stats",
        "fact_playoffs_player_shooting_stats",
    ),
    "playoffs_players_play_by_play_stats": (
        "gold_playoffs_players_play_by_play_stats",
        "fact_playoffs_player_play_by_play_stats",
    ),
    "players_salaries": ("gold_players_salaries", "fact_player_salaries"),
    "arenas_stats": ("gold_arenas_stats", "fact_arena_stats"),
}


def set_spark_iceberg_conf(catalog: str, iceberg_s3_path: str) -> SparkConf:
    """Setting up Spark configurations

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


class GoldETL:
    def __init__(self, spark: SparkSession) -> None:
        self.spark = spark
        self._version = "2"
        self._format = "parquet"

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

    @staticmethod
    def _quarantine_table_name(table_name: str) -> str:
        """Get the quarantine table name.

        :param table_name: A table name to use.
        :return: Quarantine table name.
        """
        quarantine_table_name = f"{table_name}_quarantine"

        return quarantine_table_name

    def get_metadata(self, key: str) -> tuple[str, str, str, str]:
        """Get the DB name, table name, quarantine table name,
        and data quality rules.

        :param key: The key of the `TABLES_MAP` constant.
        :return: Metadata.
        """
        db_name, table_name = TABLES_MAP.get(key)
        quarantine_table_name = self._quarantine_table_name(
            table_name=table_name
        )

        dq = DQ(db_name=db_name, table_name=table_name)
        dq_rules = dq.get_dq_rules()

        return db_name, table_name, quarantine_table_name, dq_rules

    def get_query(self, db_name: str, table_name, df: DataFrame) -> str:
        """Get the SQL query to write the data.

        :param db_name: The database name registered in AWS Glue.
        :param table_name: The table name that will be stored in
            the Iceberg format.
        :param df: Dataframe to use.
        :return: SQL query.
        """
        query = f"""
        CREATE TABLE IF NOT EXISTS {CATALOG}.{db_name}.{table_name}
        USING iceberg
        TBLPROPERTIES (
            'format-version' =  '{self._version}',
            'write.format.default' = '{self._format}'
        )
        AS
        SELECT
            *
        FROM
            {df};
        """

        return query

    def write_to_dim_season(self, glue_context: GlueContext) -> None:
        """Write the selected data to the `dim_season` table.

        :param glue_context: AWS Glue context.
        :return: None.
        """
        db_name, table_name, quarantine_table_name, dq_rules = (
            self.get_metadata(key="seasons")
        )

        select_query = f"""
        SELECT
            s.season_sk,
            s.season,
            s.league,
            c.year,
            c.conference_sk
        FROM
            {CATALOG}.silver_seasons.seasons AS s
        INNER JOIN
            {CATALOG}.silver_conferences.conferences AS c
        ON
            s.season_sk = c.season_sk;
        """

        df = self.spark.sql(select_query)
        dyf = self.get_dyf(
            df=df,
            glue_context=glue_context,
            db_name=db_name,
            table_name=table_name,
        )

        passed_df, failed_df = self.evaluate_dyf(
            dyf=dyf, dq_rules=dq_rules, db_name=db_name, table_name=table_name
        )

        query = self.get_query(
            db_name=db_name, table_name=table_name, df=passed_df
        )
        quarantine_query = self.get_query(
            db_name=db_name, table_name=quarantine_table_name, df=failed_df
        )

        self.spark.sql(query)
        self.spark.sql(quarantine_query)

    def write_to_dim_champion(self, glue_context: GlueContext) -> None:
        """Write the selected data to the `dim_champion` table.

        :param glue_context: AWS Glue context.
        :return: None.
        """
        db_name, table_name, quarantine_table_name, dq_rules = (
            self.get_metadata(key="champions")
        )

        select_query = f"""
        SELECT
            season_sk,
            team_sk,
            champion
        FROM
            {CATALOG}.silver_seasons.seasons;
        """

        df = self.spark.sql(select_query)
        dyf = self.get_dyf(
            df=df,
            glue_context=glue_context,
            db_name=db_name,
            table_name=table_name,
        )

        passed_df, failed_df = self.evaluate_dyf(
            dyf=dyf, dq_rules=dq_rules, db_name=db_name, table_name=table_name
        )

        query = self.get_query(
            db_name=db_name, table_name=table_name, df=passed_df
        )
        quarantine_query = self.get_query(
            db_name=db_name, table_name=quarantine_table_name, df=failed_df
        )

        self.spark.sql(query)
        self.spark.sql(quarantine_query)

    def write_to_dim_mvp(self, glue_context: GlueContext) -> None:
        """Write the selected data to the `dim_mvp` table.

        :param glue_context: AWS Glue context.
        :return: None.
        """
        db_name, table_name, quarantine_table_name, dq_rules = (
            self.get_metadata(key="mvps")
        )

        select_query = f"""
        SELECT
            season_sk,
            mvp_sk,
            mvp
        FROM
            {CATALOG}.silver_seasons.seasons;
        """

        df = self.spark.sql(select_query)
        dyf = self.get_dyf(
            df=df,
            glue_context=glue_context,
            db_name=db_name,
            table_name=table_name,
        )

        passed_df, failed_df = self.evaluate_dyf(
            dyf=dyf, dq_rules=dq_rules, db_name=db_name, table_name=table_name
        )

        query = self.get_query(
            db_name=db_name, table_name=table_name, df=passed_df
        )
        quarantine_query = self.get_query(
            db_name=db_name, table_name=quarantine_table_name, df=failed_df
        )

        self.spark.sql(query)
        self.spark.sql(quarantine_query)

    def write_to_dim_rookie(self, glue_context: GlueContext) -> None:
        """Write the selected data to the `dim_rookie` table.

        :param glue_context: AWS Glue context.
        :return: None.
        """
        db_name, table_name, quarantine_table_name, dq_rules = (
            self.get_metadata(key="rookies")
        )

        select_query = f"""
        SELECT
            season_sk,
            rookie_of_the_year_sk,
            rookie_of_the_year
        FROM
            {CATALOG}.silver_seasons.seasons;
        """

        df = self.spark.sql(select_query)
        dyf = self.get_dyf(
            df=df,
            glue_context=glue_context,
            db_name=db_name,
            table_name=table_name,
        )

        passed_df, failed_df = self.evaluate_dyf(
            dyf=dyf, dq_rules=dq_rules, db_name=db_name, table_name=table_name
        )

        query = self.get_query(
            db_name=db_name, table_name=table_name, df=passed_df
        )
        quarantine_query = self.get_query(
            db_name=db_name, table_name=quarantine_table_name, df=failed_df
        )

        self.spark.sql(query)
        self.spark.sql(quarantine_query)

    def write_to_dim_conference(self, glue_context: GlueContext) -> None:
        """Write the selected data to the `dim_conference` table.

        :param glue_context: AWS Glue context.
        :return: None.
        """
        db_name, table_name, quarantine_table_name, dq_rules = (
            self.get_metadata(key="conferences")
        )

        select_query = f"""
        SELECT
            conference_sk,
            conference,
            division_sk
        FROM
            {CATALOG}.silver_conferences.conferences;
        """

        df = self.spark.sql(select_query)
        dyf = self.get_dyf(
            df=df,
            glue_context=glue_context,
            db_name=db_name,
            table_name=table_name,
        )

        passed_df, failed_df = self.evaluate_dyf(
            dyf=dyf, dq_rules=dq_rules, db_name=db_name, table_name=table_name
        )

        query = self.get_query(
            db_name=db_name, table_name=table_name, df=passed_df
        )
        quarantine_query = self.get_query(
            db_name=db_name, table_name=quarantine_table_name, df=failed_df
        )

        self.spark.sql(query)
        self.spark.sql(quarantine_query)

    def write_to_dim_division(self, glue_context: GlueContext) -> None:
        """Write the selected data to the `dim_division` table.

        :param glue_context: AWS Glue context.
        :return: None.
        """
        db_name, table_name, quarantine_table_name, dq_rules = (
            self.get_metadata(key="divisions")
        )

        select_query = f"""
        SELECT
            division_sk,
            division,
            team_sk
        FROM
            {CATALOG}.silver_conferences.conferences;
        """

        df = self.spark.sql(select_query)
        dyf = self.get_dyf(
            df=df,
            glue_context=glue_context,
            db_name=db_name,
            table_name=table_name,
        )

        passed_df, failed_df = self.evaluate_dyf(
            dyf=dyf, dq_rules=dq_rules, db_name=db_name, table_name=table_name
        )

        query = self.get_query(
            db_name=db_name, table_name=table_name, df=passed_df
        )
        quarantine_query = self.get_query(
            db_name=db_name, table_name=quarantine_table_name, df=failed_df
        )

        self.spark.sql(query)
        self.spark.sql(quarantine_query)

    def write_to_dim_team(self, glue_context: GlueContext) -> None:
        """Write the selected data to the `dim_team` table.

        :param glue_context: AWS Glue context.
        :return: None.
        """
        db_name, table_name, quarantine_table_name, dq_rules = (
            self.get_metadata(key="teams")
        )

        select_query = f"""
        SELECT
            c.team_sk,
            c.team,
            c.team_abbr,
            ats.arena_sk
        FROM
            {CATALOG}.silver_conferences.conferences AS c
        INNER JOIN
            {CATALOG}.silver_conferences_stats.advanced_teams_stats AS ats
        ON
            c.team_sk = ats.team_sk
            AND c.season_sk = ats.season_sk
        WHERE
            ats.arena_sk IS NOT NULL;
        """

        df = self.spark.sql(select_query)
        dyf = self.get_dyf(
            df=df,
            glue_context=glue_context,
            db_name=db_name,
            table_name=table_name,
        )

        passed_df, failed_df = self.evaluate_dyf(
            dyf=dyf, dq_rules=dq_rules, db_name=db_name, table_name=table_name
        )

        query = self.get_query(
            db_name=db_name, table_name=table_name, df=passed_df
        )
        quarantine_query = self.get_query(
            db_name=db_name, table_name=quarantine_table_name, df=failed_df
        )

        self.spark.sql(query)
        self.spark.sql(quarantine_query)

    def write_to_dim_arena(self, glue_context: GlueContext) -> None:
        """Write selected data to the `dim_arena` table.

        :param glue_context: AWS Glue context.
        :return: None.
        """
        db_name, table_name, quarantine_table_name, dq_rules = (
            self.get_metadata(key="arenas")
        )

        select_query = f"""
        SELECT
            arena_sk,
            arena
        FROM
            {CATALOG}.silver_conferences_stats.advanced_teams_stats
        WHERE
            arena_sk IS NOT NULL;
        """

        df = self.spark.sql(select_query)
        dyf = self.get_dyf(
            df=df,
            glue_context=glue_context,
            db_name=db_name,
            table_name=table_name,
        )

        passed_df, failed_df = self.evaluate_dyf(
            dyf=dyf, dq_rules=dq_rules, db_name=db_name, table_name=table_name
        )

        query = self.get_query(
            db_name=db_name, table_name=table_name, df=passed_df
        )
        quarantine_query = self.get_query(
            db_name=db_name, table_name=quarantine_table_name, df=failed_df
        )

        self.spark.sql(query)
        self.spark.sql(quarantine_query)

    def write_to_dim_player(self, glue_context: GlueContext) -> None:
        """Write the selected data to the `dim_player` table.

        :param glue_context: AWS Glue context.
        :return: None.
        """
        db_name, table_name, quarantine_table_name, dq_rules = (
            self.get_metadata(key="players")
        )

        select_query = f"""
        SELECT
            player_sk,
            player,
            shooting_hand,
            high_schools,
            picked_team,
            draft_round,
            draft_pick,
            overall_draft_pick,
            draft_year,
            nba_debut
        FROM
            {CATALOG}.silver_players_stats.players_stats;
        """

        df = self.spark.sql(select_query)
        dyf = self.get_dyf(
            df=df,
            glue_context=glue_context,
            db_name=db_name,
            table_name=table_name,
        )

        passed_df, failed_df = self.evaluate_dyf(
            dyf=dyf, dq_rules=dq_rules, db_name=db_name, table_name=table_name
        )

        query = self.get_query(
            db_name=db_name, table_name=table_name, df=passed_df
        )
        quarantine_query = self.get_query(
            db_name=db_name, table_name=quarantine_table_name, df=failed_df
        )

        self.spark.sql(query)
        self.spark.sql(quarantine_query)

    def write_to_dim_roster(self, glue_context: GlueContext) -> None:
        """Write the selected data to the `dim_roster` table.

        :param glue_context: AWS Glue context.
        :return: None.
        """
        db_name, table_name, quarantine_table_name, dq_rules = (
            self.get_metadata(key="rosters")
        )

        select_query = f"""
        SELECT
            r.season_sk,
            r.team_sk,
            r.player_sk,
            r.player,
            r.uniform_number,
            r.position,
            r.height,
            r.weight,
            r.birth_date,
            r.country_of_birth,
            r.years_experience,
            r.college,
            rsts.awards AS regular_season_awards,
            pts.awards AS playoffs_awards
        FROM
            {CATALOG}.silver_teams_stats.rosters AS r
        INNER JOIN
            {CATALOG}.silver_teams_stats.regular_season_total_stats AS rsts
        ON
            r.season_sk = rsts.season_sk
            AND r.team_sk = rsts.team_sk
            AND r.player_sk = rsts.player_sk
        INNER JOIN
            {CATALOG}.silver_teams_stats.playoffs_total_stats AS pts
        ON
            r.season_sk = pts.season_sk
            AND r.team_sk = pts.team_sk
            AND r.player_sk = pts.player_sk;
        """

        df = self.spark.sql(select_query)
        dyf = self.get_dyf(
            df=df,
            glue_context=glue_context,
            db_name=db_name,
            table_name=table_name,
        )

        passed_df, failed_df = self.evaluate_dyf(
            dyf=dyf, dq_rules=dq_rules, db_name=db_name, table_name=table_name
        )

        query = self.get_query(
            db_name=db_name, table_name=table_name, df=passed_df
        )
        quarantine_query = self.get_query(
            db_name=db_name, table_name=quarantine_table_name, df=failed_df
        )

        self.spark.sql(query)
        self.spark.sql(quarantine_query)

    def write_to_fact_top_performer_by_assists(
        self, glue_context: GlueContext
    ) -> None:
        """Write the selected data to the
        `fact_top_performer_by_assists` table.

        :param glue_context: AWS Glue context.
        :return: None.
        """
        db_name, table_name, quarantine_table_name, dq_rules = (
            self.get_metadata(key="top_performers_by_assists")
        )

        select_query = f"""
        SELECT
            season_sk,
            player_sk,
            assists
        FROM
            {CATALOG}.silver_seasons.top_performer_by_assists;
        """

        df = self.spark.sql(select_query)
        dyf = self.get_dyf(
            df=df,
            glue_context=glue_context,
            db_name=db_name,
            table_name=table_name,
        )

        passed_df, failed_df = self.evaluate_dyf(
            dyf=dyf, dq_rules=dq_rules, db_name=db_name, table_name=table_name
        )

        query = self.get_query(
            db_name=db_name, table_name=table_name, df=passed_df
        )
        quarantine_query = self.get_query(
            db_name=db_name, table_name=quarantine_table_name, df=failed_df
        )

        self.spark.sql(query)
        self.spark.sql(quarantine_query)

    def write_to_fact_top_performer_by_points(
        self, glue_context: GlueContext
    ) -> None:
        """Write the selected data to the
        `fact_top_performer_by_points` table.

        :param glue_context: AWS Glue context.
        :return: None.
        """
        db_name, table_name, quarantine_table_name, dq_rules = (
            self.get_metadata(key="top_performers_by_points")
        )

        select_query = f"""
        SELECT
            season_sk,
            player_sk,
            points
        FROM
            {CATALOG}.silver_seasons.top_performer_by_points;
        """

        df = self.spark.sql(select_query)
        dyf = self.get_dyf(
            df=df,
            glue_context=glue_context,
            db_name=db_name,
            table_name=table_name,
        )

        passed_df, failed_df = self.evaluate_dyf(
            dyf=dyf, dq_rules=dq_rules, db_name=db_name, table_name=table_name
        )

        query = self.get_query(
            db_name=db_name, table_name=table_name, df=passed_df
        )
        quarantine_query = self.get_query(
            db_name=db_name, table_name=quarantine_table_name, df=failed_df
        )

        self.spark.sql(query)
        self.spark.sql(quarantine_query)

    def write_to_fact_top_performer_by_rebounds(
        self, glue_context: GlueContext
    ) -> None:
        """Write the selected data to the
        `fact_top_performer_by_rebounds` table.

        :param glue_context: AWS Glue context.
        :return: None.
        """
        db_name, table_name, quarantine_table_name, dq_rules = (
            self.get_metadata(key="top_performers_by_rebounds")
        )

        select_query = f"""
        SELECT
            season_sk,
            player_sk,
            rebounds
        FROM
            {CATALOG}.silver_seasons.top_performer_by_rebounds;
        """

        df = self.spark.sql(select_query)
        dyf = self.get_dyf(
            df=df,
            glue_context=glue_context,
            db_name=db_name,
            table_name=table_name,
        )

        passed_df, failed_df = self.evaluate_dyf(
            dyf=dyf, dq_rules=dq_rules, db_name=db_name, table_name=table_name
        )

        query = self.get_query(
            db_name=db_name, table_name=table_name, df=passed_df
        )
        quarantine_query = self.get_query(
            db_name=db_name, table_name=quarantine_table_name, df=failed_df
        )

        self.spark.sql(query)
        self.spark.sql(quarantine_query)

    def write_to_fact_top_performer_by_win_shares(
        self, glue_context: GlueContext
    ) -> None:
        """Write the selected data to the
        `fact_top_performer_by_win_shares` table.

        :param glue_context: AWS Glue context.
        :return: None.
        """
        db_name, table_name, quarantine_table_name, dq_rules = (
            self.get_metadata(key="top_performers_by_win_shares")
        )

        select_query = f"""
        SELECT
            season_sk,
            player_sk,
            win_shares
        FROM
            {CATALOG}.silver_seasons.top_performer_by_win_shares;
        """

        df = self.spark.sql(select_query)
        dyf = self.get_dyf(
            df=df,
            glue_context=glue_context,
            db_name=db_name,
            table_name=table_name,
        )

        passed_df, failed_df = self.evaluate_dyf(
            dyf=dyf, dq_rules=dq_rules, db_name=db_name, table_name=table_name
        )

        query = self.get_query(
            db_name=db_name, table_name=table_name, df=passed_df
        )
        quarantine_query = self.get_query(
            db_name=db_name, table_name=quarantine_table_name, df=failed_df
        )

        self.spark.sql(query)
        self.spark.sql(quarantine_query)

    def write_to_fact_conference_stats(
        self, glue_context: GlueContext
    ) -> None:
        """Write the selected data to the `fact_conference_stats` table.

        :param glue_context: AWS Glue context.
        :return: None.
        """
        db_name, table_name, quarantine_table_name, dq_rules = (
            self.get_metadata(key="conferences_stats")
        )

        select_query = f"""
        SELECT
            season_sk,
            conference_sk,
            division_sk,
            team_sk,
            wins,
            losses,
            wins_loss_percentage,
            games_behind,
            points_per_game,
            opponent_points_per_game,
            simple_rating_system,
            is_playoff_team
        FROM
            {CATALOG}.silver_conferences.conferences;
        """

        df = self.spark.sql(select_query)
        dyf = self.get_dyf(
            df=df,
            glue_context=glue_context,
            db_name=db_name,
            table_name=table_name,
        )

        passed_df, failed_df = self.evaluate_dyf(
            dyf=dyf, dq_rules=dq_rules, db_name=db_name, table_name=table_name
        )

        query = self.get_query(
            db_name=db_name, table_name=table_name, df=passed_df
        )
        quarantine_query = self.get_query(
            db_name=db_name, table_name=quarantine_table_name, df=failed_df
        )

        self.spark.sql(query)
        self.spark.sql(quarantine_query)

    def write_to_fact_team_per_game_stats(
        self, glue_context: GlueContext
    ) -> None:
        """Write the selected data to the
        `fact_team_per_game_stats` table.

        :param glue_context: AWS Glue context.
        :return: None.
        """
        db_name, table_name, quarantine_table_name, dq_rules = (
            self.get_metadata(key="teams_per_game_stats")
        )

        select_query = f"""
        SELECT
            season_sk,
            team_sk,
            rank,
            games,
            minutes_played,
            field_goals,
            field_goal_attempts,
            field_goal_percentage,
            3_point_field_goals,
            3_point_field_goal_attempts,
            3_point_field_goal_percentage,
            2_point_field_goals,
            2_point_field_goal_attempts,
            2_point_field_goal_percentage,
            free_throws,
            free_throw_attempts,
            free_throw_percentage,
            offensive_rebounds,
            defensive_rebounds,
            total_rebounds,
            assists,
            steals,
            blocks,
            turnovers,
            personal_fouls,
            points,
            is_playoff_team
        FROM
            {CATALOG}.silver_conferences_stats.per_game_teams_stats
        WHERE
            is_team_stats = TRUE;
        """

        df = self.spark.sql(select_query)
        dyf = self.get_dyf(
            df=df,
            glue_context=glue_context,
            db_name=db_name,
            table_name=table_name,
        )

        passed_df, failed_df = self.evaluate_dyf(
            dyf=dyf, dq_rules=dq_rules, db_name=db_name, table_name=table_name
        )

        query = self.get_query(
            db_name=db_name, table_name=table_name, df=passed_df
        )
        quarantine_query = self.get_query(
            db_name=db_name, table_name=quarantine_table_name, df=failed_df
        )

        self.spark.sql(query)
        self.spark.sql(quarantine_query)

    def write_to_fact_team_total_stats(
        self, glue_context: GlueContext
    ) -> None:
        """Write the selected data to the `fact_team_total_stats` table.

        :param glue_context: AWS Glue context.
        :return: None.
        """
        db_name, table_name, quarantine_table_name, dq_rules = (
            self.get_metadata(key="teams_total_stats")
        )

        select_query = f"""
        SELECT
            season_sk,
            team_sk,
            rank,
            games,
            minutes_played,
            field_goals,
            field_goal_attempts,
            field_goal_percentage,
            3_point_field_goals,
            3_point_field_goal_attempts,
            3_point_field_goal_percentage,
            2_point_field_goals,
            2_point_field_goal_attempts,
            2_point_field_goal_percentage,
            free_throws,
            free_throw_attempts,
            free_throw_percentage,
            offensive_rebounds,
            defensive_rebounds,
            total_rebounds,
            assists,
            steals,
            blocks,
            turnovers,
            personal_fouls,
            points,
            is_playoff_team
        FROM
            {CATALOG}.silver_conferences_stats.total_teams_stats
        WHERE
            is_team_stats = TRUE;
        """

        df = self.spark.sql(select_query)
        dyf = self.get_dyf(
            df=df,
            glue_context=glue_context,
            db_name=db_name,
            table_name=table_name,
        )

        passed_df, failed_df = self.evaluate_dyf(
            dyf=dyf, dq_rules=dq_rules, db_name=db_name, table_name=table_name
        )

        query = self.get_query(
            db_name=db_name, table_name=table_name, df=passed_df
        )
        quarantine_query = self.get_query(
            db_name=db_name, table_name=quarantine_table_name, df=failed_df
        )

        self.spark.sql(query)
        self.spark.sql(quarantine_query)

    def write_to_fact_team_per_100_possessions_stats(
        self, glue_context: GlueContext
    ) -> None:
        """Write the selected data to the
        `fact_team_per_100_possessions_stats` table.

        :param glue_context: AWS Glue context.
        :return: None.
        """
        db_name, table_name, quarantine_table_name, dq_rules = (
            self.get_metadata(key="teams_per_100_possessions_stats")
        )

        select_query = f"""
        SELECT
            season_sk,
            team_sk,
            rank,
            games,
            minutes_played,
            field_goals,
            field_goal_attempts,
            field_goal_percentage,
            3_point_field_goals,
            3_point_field_goal_attempts,
            3_point_field_goal_percentage,
            2_point_field_goals,
            2_point_field_goal_attempts,
            2_point_field_goal_percentage,
            free_throws,
            free_throw_attempts,
            free_throw_percentage,
            offensive_rebounds,
            defensive_rebounds,
            total_rebounds,
            assists,
            steals,
            blocks,
            turnovers,
            personal_fouls,
            points,
            is_playoff_team
        FROM
            {CATALOG}.silver_conferences_stats.per_100_possessions_teams_stats
        WHERE
            is_team_stats = TRUE;
        """

        df = self.spark.sql(select_query)
        dyf = self.get_dyf(
            df=df,
            glue_context=glue_context,
            db_name=db_name,
            table_name=table_name,
        )

        passed_df, failed_df = self.evaluate_dyf(
            dyf=dyf, dq_rules=dq_rules, db_name=db_name, table_name=table_name
        )

        query = self.get_query(
            db_name=db_name, table_name=table_name, df=passed_df
        )
        quarantine_query = self.get_query(
            db_name=db_name, table_name=quarantine_table_name, df=failed_df
        )

        self.spark.sql(query)
        self.spark.sql(quarantine_query)

    def write_to_fact_team_advanced_stats(
        self, glue_context: GlueContext
    ) -> None:
        """Write the selected data to the
        `fact_team_advanced_stats` table.

        :param glue_context: AWS Glue context.
        :return: None.
        """
        db_name, table_name, quarantine_table_name, dq_rules = (
            self.get_metadata(key="teams_shooting_stats")
        )

        select_query = f"""
        SELECT
            season_sk,
            team_sk,
            rank,
            average_age,
            wins,
            losses,
            pythagorean_wins,
            pythagorean_losses,
            margin_of_victory,
            strength_of_schedule,
            simple_rating_system,
            offensive_rating,
            defensive_rating,
            net_rating,
            pace_factor,
            free_throw_attempt_rate,
            3_point_attempt_rate,
            true_shooting_percentage,
            off_effective_field_goal_percentage,
            off_turnover_percentage,
            off_offensive_rebound_percentage,
            off_free_throws_per_field_goal_attempt,
            dff_opponent_effective_field_goal_percentage,
            dff_opponent_turnover_percentage,
            dff_defensive_rebound_percentage,
            dff_opponent_free_throws_per_field_goal_attempt,
            is_playoff_team
        FROM
            {CATALOG}.silver_conferences_stats.advanced_teams_stats
        WHERE
            is_team_stats = TRUE;
        """

        df = self.spark.sql(select_query)
        dyf = self.get_dyf(
            df=df,
            glue_context=glue_context,
            db_name=db_name,
            table_name=table_name,
        )

        passed_df, failed_df = self.evaluate_dyf(
            dyf=dyf, dq_rules=dq_rules, db_name=db_name, table_name=table_name
        )

        query = self.get_query(
            db_name=db_name, table_name=table_name, df=passed_df
        )
        quarantine_query = self.get_query(
            db_name=db_name, table_name=quarantine_table_name, df=failed_df
        )

        self.spark.sql(query)
        self.spark.sql(quarantine_query)

    def write_to_fact_team_shooting_stats(
        self, glue_context: GlueContext
    ) -> None:
        """Write the selected data to the
        `fact_team_shooting_stats` table.

        :param glue_context: AWS Glue context.
        :return: None.
        """
        db_name, table_name, quarantine_table_name, dq_rules = (
            self.get_metadata(key="teams_shooting_stats")
        )

        select_query = f"""
        SELECT
            season_sk,
            team_sk,
            rank,
            games,
            minutes_played,
            field_goal_percentage,
            average_distance_of_field_goal_attempts,
            2_point_field_goal_attempts_percentage,
            0_3_ft_field_goal_attempts_percentage,
            3_10_ft_field_goal_attempts_percentage,
            10_16_ft_field_goal_attempts_percentage,
            16_ft_3_point_field_goal_attempts_percentage,
            3_point_field_goal_attempts_percentage,
            2_point_field_goal_percentage,
            0_3_ft_field_goal_percentage,
            3_10_ft_field_goal_percentage,
            10_16_ft_field_goal_percentage,
            16_ft_3_point_field_goal_percentage,
            3_point_field_goal_percentage,
            2_point_assisted_field_goal_percentage,
            3_point_assisted_field_goal_percentage,
            field_goal_dunk_attempts_percentage,
            field_goal_dunk,
            3_point_field_goal_from_corner_percentage,
            3_point_field_goal_attempts_from_corner_percentage,
            heave_attempts,
            field_goal_layups,
            is_playoff_team,
            field_goal_layup_attempts_percentage,
            heaves_made
        FROM
            {CATALOG}.silver_conferences_stats.shooting_teams_stats
        WHERE
            is_team_stats = TRUE;
        """

        df = self.spark.sql(select_query)
        dyf = self.get_dyf(
            df=df,
            glue_context=glue_context,
            db_name=db_name,
            table_name=table_name,
        )

        passed_df, failed_df = self.evaluate_dyf(
            dyf=dyf, dq_rules=dq_rules, db_name=db_name, table_name=table_name
        )

        query = self.get_query(
            db_name=db_name, table_name=table_name, df=passed_df
        )
        quarantine_query = self.get_query(
            db_name=db_name, table_name=quarantine_table_name, df=failed_df
        )

        self.spark.sql(query)
        self.spark.sql(quarantine_query)

    def write_to_fact_opponent_per_game_stats(
        self, glue_context: GlueContext
    ) -> None:
        """Write the selected data to the
        `fact_opponent_per_game_stats` table.

        :param glue_context: AWS Glue context.
        :return: None.
        """
        db_name, table_name, quarantine_table_name, dq_rules = (
            self.get_metadata(key="opponents_per_game_stats")
        )

        select_query = f"""
        SELECT
            season_sk,
            team_sk,
            rank,
            games,
            minutes_played,
            field_goals,
            field_goal_attempts,
            field_goal_percentage,
            3_point_field_goals,
            3_point_field_goal_attempts,
            3_point_field_goal_percentage,
            2_point_field_goals,
            2_point_field_goal_attempts,
            2_point_field_goal_percentage,
            free_throws,
            free_throw_attempts,
            free_throw_percentage,
            offensive_rebounds,
            defensive_rebounds,
            total_rebounds,
            assists,
            steals,
            blocks,
            turnovers,
            personal_fouls,
            points,
            is_playoff_team
        FROM
            {CATALOG}.silver_conferences_stats.per_game_opponents_stats
        WHERE
            is_team_stats = FALSE;
        """

        df = self.spark.sql(select_query)
        dyf = self.get_dyf(
            df=df,
            glue_context=glue_context,
            db_name=db_name,
            table_name=table_name,
        )

        passed_df, failed_df = self.evaluate_dyf(
            dyf=dyf, dq_rules=dq_rules, db_name=db_name, table_name=table_name
        )

        query = self.get_query(
            db_name=db_name, table_name=table_name, df=passed_df
        )
        quarantine_query = self.get_query(
            db_name=db_name, table_name=quarantine_table_name, df=failed_df
        )

        self.spark.sql(query)
        self.spark.sql(quarantine_query)

    def write_to_fact_opponent_total_stats(
        self, glue_context: GlueContext
    ) -> None:
        """Write the selected data to the
        `fact_opponent_total_stats` table.

        :param glue_context: AWS Glue context.
        :return: None.
        """
        db_name, table_name, quarantine_table_name, dq_rules = (
            self.get_metadata(key="opponents_total_stats")
        )

        select_query = f"""
        SELECT
            season_sk,
            team_sk,
            rank,
            games,
            minutes_played,
            field_goals,
            field_goal_attempts,
            field_goal_percentage,
            3_point_field_goals,
            3_point_field_goal_attempts,
            3_point_field_goal_percentage,
            2_point_field_goals,
            2_point_field_goal_attempts,
            2_point_field_goal_percentage,
            free_throws,
            free_throw_attempts,
            free_throw_percentage,
            offensive_rebounds,
            defensive_rebounds,
            total_rebounds,
            assists,
            steals,
            blocks,
            turnovers,
            personal_fouls,
            points,
            is_playoff_team
        FROM
            {CATALOG}.silver_conferences_stats.total_opponents_stats
        WHERE
            is_team_stats = FALSE;
        """

        df = self.spark.sql(select_query)
        dyf = self.get_dyf(
            df=df,
            glue_context=glue_context,
            db_name=db_name,
            table_name=table_name,
        )

        passed_df, failed_df = self.evaluate_dyf(
            dyf=dyf, dq_rules=dq_rules, db_name=db_name, table_name=table_name
        )

        query = self.get_query(
            db_name=db_name, table_name=table_name, df=passed_df
        )
        quarantine_query = self.get_query(
            db_name=db_name, table_name=quarantine_table_name, df=failed_df
        )

        self.spark.sql(query)
        self.spark.sql(quarantine_query)

    def write_to_fact_opponent_per_100_possessions_stats(
        self, glue_context: GlueContext
    ) -> None:
        """Write the selected data to the
        `fact_opponent_per_100_possessions_stats` table.

        :param glue_context: AWS Glue context.
        :return: None.
        """
        db_name, table_name, quarantine_table_name, dq_rules = (
            self.get_metadata(key="opponents_per_100_possessions_stats")
        )

        select_query = f"""
        SELECT
            season_sk,
            team_sk,
            rank,
            games,
            minutes_played,
            field_goals,
            field_goal_attempts,
            field_goal_percentage,
            3_point_field_goals,
            3_point_field_goal_attempts,
            3_point_field_goal_percentage,
            2_point_field_goals,
            2_point_field_goal_attempts,
            2_point_field_goal_percentage,
            free_throws,
            free_throw_attempts,
            free_throw_percentage,
            offensive_rebounds,
            defensive_rebounds,
            total_rebounds,
            assists,
            steals,
            blocks,
            turnovers,
            personal_fouls,
            points,
            is_playoff_team
        FROM
            {CATALOG}.silver_conferences_stats.per_100_possessions_opponents_stats
        WHERE
            is_team_stats = FALSE;
        """

        df = self.spark.sql(select_query)
        dyf = self.get_dyf(
            df=df,
            glue_context=glue_context,
            db_name=db_name,
            table_name=table_name,
        )

        passed_df, failed_df = self.evaluate_dyf(
            dyf=dyf, dq_rules=dq_rules, db_name=db_name, table_name=table_name
        )

        query = self.get_query(
            db_name=db_name, table_name=table_name, df=passed_df
        )
        quarantine_query = self.get_query(
            db_name=db_name, table_name=quarantine_table_name, df=failed_df
        )

        self.spark.sql(query)
        self.spark.sql(quarantine_query)

    def write_to_fact_opponent_shooting_stats(
        self, glue_context: GlueContext
    ) -> None:
        """Write the selected data to the
        `fact_opponent_shooting_stats` table.

        :param glue_context: AWS Glue context.
        :return: None.
        """
        db_name, table_name, quarantine_table_name, dq_rules = (
            self.get_metadata(key="opponents_shooting_stats")
        )

        select_query = f"""
        SELECT
            season_sk,
            team_sk,
            rank,
            games,
            minutes_played,
            field_goal_percentage,
            average_distance_of_field_goal_attempts,
            2_point_field_goal_attempts_percentage,
            0_3_ft_field_goal_attempts_percentage,
            3_10_ft_field_goal_attempts_percentage,
            10_16_ft_field_goal_attempts_percentage,
            16_ft_3_point_field_goal_attempts_percentage,
            3_point_field_goal_attempts_percentage,
            2_point_field_goal_percentage,
            0_3_ft_field_goal_percentage,
            3_10_ft_field_goal_percentage,
            10_16_ft_field_goal_percentage,
            16_ft_3_point_field_goal_percentage,
            3_point_field_goal_percentage,
            2_point_assisted_field_goal_percentage,
            3_point_assisted_field_goal_percentage,
            field_goal_dunk_attempts_percentage,
            field_goal_dunk,
            3_point_field_goal_from_corner_percentage,
            3_point_field_goal_attempts_from_corner_percentage,
            is_playoff_team,
            field_goal_layup_attempts_percentage,
            field_goal_layups
        FROM
            {CATALOG}.silver_conferences_stats.shooting_opponents_stats
        WHERE
            is_team_stats = FALSE;
        """

        df = self.spark.sql(select_query)
        dyf = self.get_dyf(
            df=df,
            glue_context=glue_context,
            db_name=db_name,
            table_name=table_name,
        )

        passed_df, failed_df = self.evaluate_dyf(
            dyf=dyf, dq_rules=dq_rules, db_name=db_name, table_name=table_name
        )

        query = self.get_query(
            db_name=db_name, table_name=table_name, df=passed_df
        )
        quarantine_query = self.get_query(
            db_name=db_name, table_name=quarantine_table_name, df=failed_df
        )

        self.spark.sql(query)
        self.spark.sql(quarantine_query)

    def write_to_fact_regular_season_player_per_game_stats(
        self, glue_context: GlueContext
    ) -> None:
        """Write the selected data to the
        `fact_regular_season_player_per_game_stats` table.

        :param glue_context: AWS Glue context.
        :return: None.
        """
        db_name, table_name, quarantine_table_name, dq_rules = (
            self.get_metadata(key="regular_season_players_per_game_stats")
        )

        select_query = f"""
        SELECT
            season_sk,
            team_sk,
            player_sk,
            rank,
            games,
            games_started,
            minutes_played,
            field_goals,
            field_goal_attempts,
            field_goal_percentage,
            3_point_field_goals,
            3_point_field_goal_attempts,
            3_point_field_goal_percentage,
            2_point_field_goals,
            2_point_field_goal_attempts,
            2_point_field_goal_percentage,
            effective_field_goal_percentage,
            free_throws,
            free_throw_attempts,
            free_throw_percentage,
            offensive_rebounds,
            defensive_rebounds,
            total_rebounds,
            assists,
            steals,
            blocks,
            turnovers,
            personal_fouls,
            points
        FROM
            {CATALOG}.silver_teams_stats.regular_season_per_game_stats;
        """

        df = self.spark.sql(select_query)
        dyf = self.get_dyf(
            df=df,
            glue_context=glue_context,
            db_name=db_name,
            table_name=table_name,
        )

        passed_df, failed_df = self.evaluate_dyf(
            dyf=dyf, dq_rules=dq_rules, db_name=db_name, table_name=table_name
        )

        query = self.get_query(
            db_name=db_name, table_name=table_name, df=passed_df
        )
        quarantine_query = self.get_query(
            db_name=db_name, table_name=quarantine_table_name, df=failed_df
        )

        self.spark.sql(query)
        self.spark.sql(quarantine_query)

    def write_to_fact_regular_season_player_total_stats(
        self, glue_context: GlueContext
    ) -> None:
        """Write the selected data to the
        `fact_regular_season_player_total_stats` table.

        :param glue_context: AWS Glue context.
        :return: None.
        """
        db_name, table_name, quarantine_table_name, dq_rules = (
            self.get_metadata(key="regular_season_players_total_stats")
        )

        select_query = f"""
        SELECT
            season_sk,
            team_sk,
            player_sk,
            rank,
            games,
            games_started,
            minutes_played,
            field_goals,
            field_goal_attempts,
            field_goal_percentage,
            3_point_field_goals,
            3_point_field_goal_attempts,
            3_point_field_goal_percentage,
            2_point_field_goals,
            2_point_field_goal_attempts,
            2_point_field_goal_percentage,
            effective_field_goal_percentage,
            free_throws,
            free_throw_attempts,
            free_throw_percentage,
            offensive_rebounds,
            defensive_rebounds,
            total_rebounds,
            assists,
            steals,
            blocks,
            turnovers,
            personal_fouls,
            points,
            triple_doubles
        FROM
            {CATALOG}.silver_teams_stats.regular_season_total_stats;
        """

        df = self.spark.sql(select_query)
        dyf = self.get_dyf(
            df=df,
            glue_context=glue_context,
            db_name=db_name,
            table_name=table_name,
        )

        passed_df, failed_df = self.evaluate_dyf(
            dyf=dyf, dq_rules=dq_rules, db_name=db_name, table_name=table_name
        )

        query = self.get_query(
            db_name=db_name, table_name=table_name, df=passed_df
        )
        quarantine_query = self.get_query(
            db_name=db_name, table_name=quarantine_table_name, df=failed_df
        )

        self.spark.sql(query)
        self.spark.sql(quarantine_query)

    def write_to_fact_regular_season_player_per_36_minutes_stats(
        self, glue_context: GlueContext
    ) -> None:
        """Write the selected data to the
        `fact_regular_season_player_per_36_minutes` table.

        :param glue_context: AWS Glue context.
        :return: None.
        """
        db_name, table_name, quarantine_table_name, dq_rules = (
            self.get_metadata(
                key="regular_season_players_per_36_minutes_stats"
            )
        )

        select_query = f"""
        SELECT
            season_sk,
            team_sk,
            player_sk,
            rank,
            games,
            games_started,
            minutes_played,
            field_goals,
            field_goal_attempts,
            field_goal_percentage,
            3_point_field_goals,
            3_point_field_goal_attempts,
            3_point_field_goal_percentage,
            2_point_field_goals,
            2_point_field_goal_attempts,
            2_point_field_goal_percentage,
            effective_field_goal_percentage,
            free_throws,
            free_throw_attempts,
            free_throw_percentage,
            offensive_rebounds,
            defensive_rebounds,
            total_rebounds,
            assists,
            steals,
            blocks,
            turnovers,
            personal_fouls,
            points
        FROM
            {CATALOG}.silver_teams_stats.regular_season_per_36_minutes_stats;
        """

        df = self.spark.sql(select_query)
        dyf = self.get_dyf(
            df=df,
            glue_context=glue_context,
            db_name=db_name,
            table_name=table_name,
        )

        passed_df, failed_df = self.evaluate_dyf(
            dyf=dyf, dq_rules=dq_rules, db_name=db_name, table_name=table_name
        )

        query = self.get_query(
            db_name=db_name, table_name=table_name, df=passed_df
        )
        quarantine_query = self.get_query(
            db_name=db_name, table_name=quarantine_table_name, df=failed_df
        )

        self.spark.sql(query)
        self.spark.sql(quarantine_query)

    def write_to_fact_regular_season_player_per_100_possessions_stats(
        self, glue_context: GlueContext
    ) -> None:
        """Write the selected data to the
        `fact_regular_season_player_per_100_possessions` table.

        :param glue_context: AWS Glue context.
        :return: None.
        """
        db_name, table_name, quarantine_table_name, dq_rules = (
            self.get_metadata(
                key="regular_season_players_per_100_possessions_stats"
            )
        )

        select_query = f"""
        SELECT
            season_sk,
            team_sk,
            player_sk,
            rank,
            games,
            games_started,
            minutes_played,
            field_goals,
            field_goal_attempts,
            field_goal_percentage,
            3_point_field_goals,
            3_point_field_goal_attempts,
            3_point_field_goal_percentage,
            2_point_field_goals,
            2_point_field_goal_attempts,
            2_point_field_goal_percentage,
            effective_field_goal_percentage,
            free_throws,
            free_throw_attempts,
            free_throw_percentage,
            offensive_rebounds,
            defensive_rebounds,
            total_rebounds,
            assists,
            steals,
            blocks,
            turnovers,
            personal_fouls,
            points,
            offensive_rating,
            defensive_rating
        FROM
            {CATALOG}.silver_teams_stats.regular_season_per_100_possessions_stats;
        """

        df = self.spark.sql(select_query)
        dyf = self.get_dyf(
            df=df,
            glue_context=glue_context,
            db_name=db_name,
            table_name=table_name,
        )

        passed_df, failed_df = self.evaluate_dyf(
            dyf=dyf, dq_rules=dq_rules, db_name=db_name, table_name=table_name
        )

        query = self.get_query(
            db_name=db_name, table_name=table_name, df=passed_df
        )
        quarantine_query = self.get_query(
            db_name=db_name, table_name=quarantine_table_name, df=failed_df
        )

        self.spark.sql(query)
        self.spark.sql(quarantine_query)

    def write_to_fact_regular_season_player_advanced_stats(
        self, glue_context: GlueContext
    ) -> None:
        """Write the selected data to the
        `fact_regular_season_player_advanced` table.

        :param glue_context: AWS Glue context.
        :return: None.
        """
        db_name, table_name, quarantine_table_name, dq_rules = (
            self.get_metadata(key="regular_season_players_advanced_stats")
        )

        select_query = f"""
        SELECT
            season_sk,
            team_sk,
            player_sk,
            rank,
            games,
            games_started,
            minutes_played,
            player_efficiency_rating,
            true_shooting_percentage,
            3_point_attempt_rate,
            free_throw_attempt_rate,
            offensive_rebound_percentage,
            defensive_rebound_percentage,
            total_rebound_percentage,
            assist_percentage,
            steal_percentage,
            block_percentage,
            turnovers_percentage,
            usage_percentage,
            offensive_win_shares,
            defensive_win_shares,
            win_shares,
            win_shares_per_48_minutes,
            offensive_box_plus_minus,
            defensive_box_plus_minus,
            box_plus_minus,
            value_over_replacement_player
        FROM
            {CATALOG}.silver_teams_stats.regular_season_advanced_stats;
        """

        df = self.spark.sql(select_query)
        dyf = self.get_dyf(
            df=df,
            glue_context=glue_context,
            db_name=db_name,
            table_name=table_name,
        )

        passed_df, failed_df = self.evaluate_dyf(
            dyf=dyf, dq_rules=dq_rules, db_name=db_name, table_name=table_name
        )

        query = self.get_query(
            db_name=db_name, table_name=table_name, df=passed_df
        )
        quarantine_query = self.get_query(
            db_name=db_name, table_name=quarantine_table_name, df=failed_df
        )

        self.spark.sql(query)
        self.spark.sql(quarantine_query)

    def write_to_fact_regular_season_player_adjusted_shooting_stats(
        self, glue_context: GlueContext
    ) -> None:
        """Write the selected data to the
        `fact_regular_season_player_adjusted_shooting_stats` table.

        :param glue_context: AWS Glue context.
        :return: None.
        """
        db_name, table_name, quarantine_table_name, dq_rules = (
            self.get_metadata(
                key="regular_season_players_adjusted_shooting_stats"
            )
        )

        select_query = f"""
        SELECT
            season_sk,
            team_sk,
            player_sk,
            rank,
            games,
            games_started,
            minutes_played,
            field_goal_percentage,
            2_point_field_goal_percentage,
            3_point_field_goal_percentage,
            effective_field_goal_percentage,
            free_throw_percentage,
            true_shooting_percentage,
            free_throw_attempt_rate,
            3_point_attempt_rate,
            adjusted_field_goal,
            adjusted_2_point_field_goal,
            adjusted_effective_field_goal,
            adjusted_free_throw,
            adjusted_true_shooting,
            adjusted_free_throw_attempt,
            adjusted_3_point_attempt,
            points_added_by_field_goal_shooting,
            points_added_by_overall_shooting
        FROM
            {CATALOG}.silver_teams_stats.regular_season_adjusted_shooting_stats;
        """

        df = self.spark.sql(select_query)
        dyf = self.get_dyf(
            df=df,
            glue_context=glue_context,
            db_name=db_name,
            table_name=table_name,
        )

        passed_df, failed_df = self.evaluate_dyf(
            dyf=dyf, dq_rules=dq_rules, db_name=db_name, table_name=table_name
        )

        query = self.get_query(
            db_name=db_name, table_name=table_name, df=passed_df
        )
        quarantine_query = self.get_query(
            db_name=db_name, table_name=quarantine_table_name, df=failed_df
        )

        self.spark.sql(query)
        self.spark.sql(quarantine_query)

    def write_to_fact_regular_season_player_shooting_stats(
        self, glue_context: GlueContext
    ) -> None:
        """Write the selected data to the
        `fact_regular_season_player_shooting_stats` table.

        :param glue_context: AWS Glue context.
        :return: None.
        """
        db_name, table_name, quarantine_table_name, dq_rules = (
            self.get_metadata(key="regular_season_players_shooting_stats")
        )

        select_query = f"""
        SELECT
            season_sk,
            team_sk,
            player_sk,
            rank,
            games,
            games_started,
            minutes_played,
            field_goal_percentage,
            average_distance_of_field_goal_attempts,
            2_point_field_goal_attempts_percentage,
            0_3_ft_field_goal_attempts_percentage,
            3_10_ft_field_goal_attempts_percentage,
            10_16_ft_field_goal_attempts_percentage,
            16_ft_3_point_field_goal_attempts_percentage,
            3_point_field_goal_attempts_percentage,
            2_point_field_goal_percentage,
            0_3_ft_field_goal_percentage,
            3_10_ft_field_goal_percentage,
            10_16_ft_field_goal_percentage,
            16_ft_3_point_field_goal_percentage,
            3_point_field_goal_percentage,
            2_point_assisted_field_goal_percentage,
            3_point_assisted_field_goal_percentage,
            field_goal_dunk_attempts_percentage,
            number_of_made_dunk_attempts,
            3_point_field_goal_from_corner_percentage,
            3_point_field_goal_attempts_from_corner_percentage,
            heave_attempts,
            heaves_made
        FROM
            {CATALOG}.silver_teams_stats.regular_season_shooting_stats;
        """

        df = self.spark.sql(select_query)
        dyf = self.get_dyf(
            df=df,
            glue_context=glue_context,
            db_name=db_name,
            table_name=table_name,
        )

        passed_df, failed_df = self.evaluate_dyf(
            dyf=dyf, dq_rules=dq_rules, db_name=db_name, table_name=table_name
        )

        query = self.get_query(
            db_name=db_name, table_name=table_name, df=passed_df
        )
        quarantine_query = self.get_query(
            db_name=db_name, table_name=quarantine_table_name, df=failed_df
        )

        self.spark.sql(query)
        self.spark.sql(quarantine_query)

    def write_to_fact_regular_season_player_play_by_play_stats(
        self, glue_context: GlueContext
    ) -> None:
        """Write the selected data to the
        `fact_regular_season_player_play_by_play` table.

        :param glue_context: AWS Glue context.
        :return: None.
        """
        db_name, table_name, quarantine_table_name, dq_rules = (
            self.get_metadata(key="regular_season_players_play_by_play_stats")
        )

        select_query = f"""
        SELECT
            season_sk,
            team_sk,
            player_sk,
            rank,
            games,
            games_started,
            minutes_played,
            point_guard_percentage,
            shooting_guard_percentage,
            small_forward_percentage,
            power_forward_percentage,
            center_percentage,
            plus_minus_per_100_possessions_on_court,
            plus_minus_net_per_100_possessions,
            turnovers_by_bad_pass,
            lost_ball_turnovers,
            shooting_fouls,
            offensive_fouls,
            shooting_fouls_drawn,
            offensive_fouls_drawn,
            point_generated_by_assists,
            fouled_field_goals,
            blocked_field_goal_attempts
        FROM
            {CATALOG}.silver_teams_stats.regular_season_play_by_play_stats;
        """

        df = self.spark.sql(select_query)
        dyf = self.get_dyf(
            df=df,
            glue_context=glue_context,
            db_name=db_name,
            table_name=table_name,
        )

        passed_df, failed_df = self.evaluate_dyf(
            dyf=dyf, dq_rules=dq_rules, db_name=db_name, table_name=table_name
        )

        query = self.get_query(
            db_name=db_name, table_name=table_name, df=passed_df
        )
        quarantine_query = self.get_query(
            db_name=db_name, table_name=quarantine_table_name, df=failed_df
        )

        self.spark.sql(query)
        self.spark.sql(quarantine_query)

    def write_to_fact_playoffs_player_per_game_stats(
        self, glue_context: GlueContext
    ) -> None:
        """Write the selected data to the
        `fact_playoffs_player_per_game` table.

        :param glue_context: AWS Glue context.
        :return: None.
        """
        db_name, table_name, quarantine_table_name, dq_rules = (
            self.get_metadata(key="playoffs_players_per_game_stats")
        )

        select_query = f"""
        SELECT
            season_sk,
            team_sk,
            player_sk,
            rank,
            games,
            games_started,
            minutes_played,
            field_goals,
            field_goal_attempts,
            field_goal_percentage,
            3_point_field_goals,
            3_point_field_goal_attempts,
            3_point_field_goal_percentage,
            2_point_field_goals,
            2_point_field_goal_attempts,
            2_point_field_goal_percentage,
            effective_field_goal_percentage,
            free_throws,
            free_throw_attempts,
            free_throw_percentage,
            offensive_rebounds,
            defensive_rebounds,
            total_rebounds,
            assists,
            steals,
            blocks,
            turnovers,
            personal_fouls,
            points
        FROM
            {CATALOG}.silver_teams_stats.playoffs_per_game_stats;
        """

        df = self.spark.sql(select_query)
        dyf = self.get_dyf(
            df=df,
            glue_context=glue_context,
            db_name=db_name,
            table_name=table_name,
        )

        passed_df, failed_df = self.evaluate_dyf(
            dyf=dyf, dq_rules=dq_rules, db_name=db_name, table_name=table_name
        )

        query = self.get_query(
            db_name=db_name, table_name=table_name, df=passed_df
        )
        quarantine_query = self.get_query(
            db_name=db_name, table_name=quarantine_table_name, df=failed_df
        )

        self.spark.sql(query)
        self.spark.sql(quarantine_query)

    def write_to_fact_playoffs_player_total_stats(
        self, glue_context: GlueContext
    ) -> None:
        """Write the selected data to the
        `fact_playoffs_player_total_stats` table.

        :param glue_context: AWS Glue context.
        :return: None.
        """
        db_name, table_name, quarantine_table_name, dq_rules = (
            self.get_metadata(key="playoffs_players_total_stats")
        )

        select_query = f"""
        SELECT
            season_sk,
            team_sk,
            player_sk,
            rank,
            games,
            games_started,
            minutes_played,
            field_goals,
            field_goal_attempts,
            3_point_field_goal_attempts,
            3_point_field_goal_percentage,
            2_point_field_goals,
            2_point_field_goal_attempts,
            2_point_field_goal_percentage,
            effective_field_goal_percentage,
            free_throws,
            free_throw_attempts,
            free_throw_percentage,
            offensive_rebounds,
            defensive_rebounds,
            total_rebounds,
            assists,
            steals,
            blocks,
            turnovers,
            personal_fouls,
            points,
            triple_doubles
        FROM
            {CATALOG}.silver_teams_stats.playoffs_total_stats;
        """

        df = self.spark.sql(select_query)
        dyf = self.get_dyf(
            df=df,
            glue_context=glue_context,
            db_name=db_name,
            table_name=table_name,
        )

        passed_df, failed_df = self.evaluate_dyf(
            dyf=dyf, dq_rules=dq_rules, db_name=db_name, table_name=table_name
        )

        query = self.get_query(
            db_name=db_name, table_name=table_name, df=passed_df
        )
        quarantine_query = self.get_query(
            db_name=db_name, table_name=quarantine_table_name, df=failed_df
        )

        self.spark.sql(query)
        self.spark.sql(quarantine_query)

    def write_to_fact_playoffs_player_per_36_minutes_stats(
        self, glue_context: GlueContext
    ) -> None:
        """Write the selected data to the
        `fact_playoffs_player_per_game` table.

        :param glue_context: AWS Glue context.
        :return: None.
        """
        db_name, table_name, quarantine_table_name, dq_rules = (
            self.get_metadata(key="playoffs_players_per_36_minutes_stats")
        )

        select_query = f"""
        SELECT
            season_sk,
            team_sk,
            player_sk,
            rank,
            games,
            games_started,
            minutes_played,
            field_goals,
            field_goal_attempts,
            field_goal_percentage,
            3_point_field_goals,
            3_point_field_goal_attempts,
            3_point_field_goal_percentage,
            2_point_field_goals,
            2_point_field_goal_attempts,
            2_point_field_goal_percentage,
            effective_field_goal_percentage,
            free_throws,
            free_throw_attempts,
            free_throw_percentage,
            offensive_rebounds,
            defensive_rebounds,
            total_rebounds,
            assists,
            steals,
            blocks,
            turnovers,
            personal_fouls,
            points
        FROM
            {CATALOG}.silver_teams_stats.playoffs_per_36_minutes_stats;
        """

        df = self.spark.sql(select_query)
        dyf = self.get_dyf(
            df=df,
            glue_context=glue_context,
            db_name=db_name,
            table_name=table_name,
        )

        passed_df, failed_df = self.evaluate_dyf(
            dyf=dyf, dq_rules=dq_rules, db_name=db_name, table_name=table_name
        )

        query = self.get_query(
            db_name=db_name, table_name=table_name, df=passed_df
        )
        quarantine_query = self.get_query(
            db_name=db_name, table_name=quarantine_table_name, df=failed_df
        )

        self.spark.sql(query)
        self.spark.sql(quarantine_query)

    def write_to_fact_playoffs_player_per_100_possessions_stats(
        self, glue_context: GlueContext
    ) -> None:
        """Write the selected data to the
        `fact_playoffs_player_per_game` table.

        :param glue_context: AWS Glue context.
        :return: None.
        """
        db_name, table_name, quarantine_table_name, dq_rules = (
            self.get_metadata(key="playoffs_players_per_100_possessions_stats")
        )

        select_query = f"""
        SELECT
            season_sk,
            team_sk,
            player_sk,
            rank,
            games,
            games_started,
            minutes_played,
            field_goals,
            field_goal_attempts,
            field_goal_percentage,
            3_point_field_goals,
            3_point_field_goal_attempts,
            3_point_field_goal_percentage,
            2_point_field_goals,
            2_point_field_goal_attempts,
            2_point_field_goal_percentage,
            effective_field_goal_percentage,
            free_throws,
            free_throw_attempts,
            free_throw_percentage,
            offensive_rebounds,
            defensive_rebounds,
            total_rebounds,
            assists,
            steals,
            blocks,
            turnovers,
            personal_fouls,
            points,
            offensive_rating,
            defensive_rating
        FROM
            {CATALOG}.silver_teams_stats.playoffs_per_100_possessions_stats;
        """

        df = self.spark.sql(select_query)
        dyf = self.get_dyf(
            df=df,
            glue_context=glue_context,
            db_name=db_name,
            table_name=table_name,
        )

        passed_df, failed_df = self.evaluate_dyf(
            dyf=dyf, dq_rules=dq_rules, db_name=db_name, table_name=table_name
        )

        query = self.get_query(
            db_name=db_name, table_name=table_name, df=passed_df
        )
        quarantine_query = self.get_query(
            db_name=db_name, table_name=quarantine_table_name, df=failed_df
        )

        self.spark.sql(query)
        self.spark.sql(quarantine_query)

    def write_to_fact_playoffs_player_advanced_stats(
        self, glue_context: GlueContext
    ) -> None:
        """Write the selected data to the
        `fact_playoffs_player_per_game` table.

        :param glue_context: AWS Glue context.
        :return: None.
        """
        db_name, table_name, quarantine_table_name, dq_rules = (
            self.get_metadata(key="playoffs_players_advanced_stats")
        )

        select_query = f"""
        SELECT
            season_sk,
            team_sk,
            player_sk,
            rank,
            games,
            games_started,
            minutes_played,
            player_efficiency_rating,
            true_shooting_percentage,
            3_point_attempt_rate,
            free_throw_attempt_rate,
            offensive_rebound_percentage,
            defensive_rebound_percentage,
            total_rebound_percentage,
            assist_percentage,
            steal_percentage,
            block_percentage,
            turnovers_percentage,
            usage_percentage,
            offensive_win_shares,
            defensive_win_shares,
            win_shares,
            win_shares_per_48_minutes,
            offensive_box_plus_minus,
            defensive_box_plus_minus,
            box_plus_minus,
            value_over_replacement_player
        FROM
            {CATALOG}.silver_teams_stats.playoffs_advanced_stats;
        """

        df = self.spark.sql(select_query)
        dyf = self.get_dyf(
            df=df,
            glue_context=glue_context,
            db_name=db_name,
            table_name=table_name,
        )

        passed_df, failed_df = self.evaluate_dyf(
            dyf=dyf, dq_rules=dq_rules, db_name=db_name, table_name=table_name
        )

        query = self.get_query(
            db_name=db_name, table_name=table_name, df=passed_df
        )
        quarantine_query = self.get_query(
            db_name=db_name, table_name=quarantine_table_name, df=failed_df
        )

        self.spark.sql(query)
        self.spark.sql(quarantine_query)

    def write_to_fact_playoffs_player_adjusted_shooting_stats(
        self, glue_context: GlueContext
    ) -> None:
        """Write the selected data to the
        `fact_playoffs_player_per_game` table.

        :param glue_context: AWS Glue context.
        :return: None.
        """
        db_name, table_name, quarantine_table_name, dq_rules = (
            self.get_metadata(key="playoffs_players_adjusted_shooting_stats")
        )

        select_query = f"""
        SELECT
            season_sk,
            team_sk,
            player_sk,
            rank,
            games,
            games_started,
            minutes_played,
            field_goal_percentage,
            2_point_field_goal_percentage,
            3_point_field_goal_percentage,
            effective_field_goal_percentage,
            free_throw_percentage,
            true_shooting_percentage,
            free_throw_attempt_rate,
            3_point_attempt_rate,
            adjusted_field_goal,
            adjusted_2_point_field_goal,
            adjusted_3_point_field_goal,
            adjusted_effective_field_goal,
            adjusted_free_throw,
            adjusted_true_shooting,
            adjusted_free_throw_attempt,
            adjusted_3_point_attempt
        FROM
            {CATALOG}.silver_teams_stats.playoffs_adjusted_shooting_stats;
        """

        df = self.spark.sql(select_query)
        dyf = self.get_dyf(
            df=df,
            glue_context=glue_context,
            db_name=db_name,
            table_name=table_name,
        )

        passed_df, failed_df = self.evaluate_dyf(
            dyf=dyf, dq_rules=dq_rules, db_name=db_name, table_name=table_name
        )

        query = self.get_query(
            db_name=db_name, table_name=table_name, df=passed_df
        )
        quarantine_query = self.get_query(
            db_name=db_name, table_name=quarantine_table_name, df=failed_df
        )

        self.spark.sql(query)
        self.spark.sql(quarantine_query)

    def write_to_fact_playoffs_player_shooting_stats(
        self, glue_context: GlueContext
    ) -> None:
        """Write the selected data to the
        `fact_playoffs_player_per_game` table.

        :param glue_context: AWS Glue context.
        :return: None.
        """
        db_name, table_name, quarantine_table_name, dq_rules = (
            self.get_metadata(key="playoffs_players_shooting_stats")
        )

        select_query = f"""
        SELECT
            season_sk,
            team_sk,
            player_sk,
            rank,
            games,
            games_started,
            minutes_played,
            field_goal_percentage,
            average_distance_of_field_goal_attempts,
            2_point_field_goal_attempts_percentage,
            0_3_ft_field_goal_attempts_percentage,
            3_10_ft_field_goal_attempts_percentage,
            10_16_ft_field_goal_attempts_percentage,
            16_ft_3_point_field_goal_attempts_percentage,
            3_point_field_goal_attempts_percentage,
            2_point_field_goal_percentage,
            0_3_ft_field_goal_percentage,
            3_10_ft_field_goal_percentage,
            10_16_ft_field_goal_percentage,
            16_ft_3_point_field_goal_percentage,
            3_point_field_goal_percentage,
            2_point_assisted_field_goal_percentage,
            3_point_assisted_field_goal_percentage,
            field_goal_dunk_attempts_percentage,
            number_of_made_dunk_attempts,
            3_point_field_goal_from_corner_percentage,
            3_point_field_goal_attempts_from_corner_percentage,
            heave_attempts,
            heaves_made
        FROM
            {CATALOG}.silver_teams_stats.playoffs_shooting_stats;
        """

        df = self.spark.sql(select_query)
        dyf = self.get_dyf(
            df=df,
            glue_context=glue_context,
            db_name=db_name,
            table_name=table_name,
        )

        passed_df, failed_df = self.evaluate_dyf(
            dyf=dyf, dq_rules=dq_rules, db_name=db_name, table_name=table_name
        )

        query = self.get_query(
            db_name=db_name, table_name=table_name, df=passed_df
        )
        quarantine_query = self.get_query(
            db_name=db_name, table_name=quarantine_table_name, df=failed_df
        )

        self.spark.sql(query)
        self.spark.sql(quarantine_query)

    def write_to_fact_playoffs_player_play_by_play_stats(
        self, glue_context: GlueContext
    ) -> None:
        """Write the selected data to the
        `fact_playoffs_player_per_game` table.

        :param glue_context: AWS Glue context.
        :return: None.
        """
        db_name, table_name, quarantine_table_name, dq_rules = (
            self.get_metadata(key="playoffs_players_play_by_play_stats")
        )

        select_query = f"""
        SELECT
            season_sk,
            team_sk,
            player_sk,
            rank,
            games,
            games_started,
            minutes_played,
            point_guard_percentage,
            shooting_guard_percentage,
            small_forward_percentage,
            power_forward_percentage,
            center_percentage,
            plus_minus_per_100_possessions_on_court,
            plus_minus_net_per_100_possessions,
            turnovers_by_bad_pass,
            lost_ball_turnovers,
            shooting_fouls,
            offensive_fouls,
            shooting_fouls_drawn,
            offensive_fouls_drawn,
            point_generated_by_assists,
            fouled_field_goals,
            blocked_field_goal_attempts
        FROM
            {CATALOG}.silver_teams_stats.playoffs_play_by_play_stats;
        """

        df = self.spark.sql(select_query)
        dyf = self.get_dyf(
            df=df,
            glue_context=glue_context,
            db_name=db_name,
            table_name=table_name,
        )

        passed_df, failed_df = self.evaluate_dyf(
            dyf=dyf, dq_rules=dq_rules, db_name=db_name, table_name=table_name
        )

        query = self.get_query(
            db_name=db_name, table_name=table_name, df=passed_df
        )
        quarantine_query = self.get_query(
            db_name=db_name, table_name=quarantine_table_name, df=failed_df
        )

        self.spark.sql(query)
        self.spark.sql(quarantine_query)

    def write_to_fact_player_salaries(self, glue_context: GlueContext) -> None:
        """Write the selected data to the
        `fact_player_salaries_per_game` table.

        :param glue_context: AWS Glue context.
        :return: None.
        """
        db_name, table_name, quarantine_table_name, dq_rules = (
            self.get_metadata(key="players_salaries")
        )

        select_query = f"""
        SELECT
            season_sk,
            team_sk,
            player_sk,
            rank,
            salary
        FROM
            {CATALOG}.silver_teams_stats.salaries;
        """

        df = self.spark.sql(select_query)
        dyf = self.get_dyf(
            df=df,
            glue_context=glue_context,
            db_name=db_name,
            table_name=table_name,
        )

        passed_df, failed_df = self.evaluate_dyf(
            dyf=dyf, dq_rules=dq_rules, db_name=db_name, table_name=table_name
        )

        query = self.get_query(
            db_name=db_name, table_name=table_name, df=passed_df
        )
        quarantine_query = self.get_query(
            db_name=db_name, table_name=quarantine_table_name, df=failed_df
        )

        self.spark.sql(query)
        self.spark.sql(quarantine_query)

    def write_to_fact_arena_stats(self, glue_context: GlueContext) -> None:
        """Write the selected data to the `fact_arena_stats` table.

        :param glue_context: AWS Glue context.
        :return: None.
        """
        db_name, table_name, quarantine_table_name, dq_rules = (
            self.get_metadata(key="arenas_stats")
        )

        select_query = f"""
        SELECT
            season_sk,
            team_sk,
            arena_sk,
            attendance,
            attendance_per_game
        FROM
            {CATALOG}.silver_conferences_stats.advanced_teams_stats
        WHERE
            arena_sk IS NOT NULL;
        """

        df = self.spark.sql(select_query)
        dyf = self.get_dyf(
            df=df,
            glue_context=glue_context,
            db_name=db_name,
            table_name=table_name,
        )

        passed_df, failed_df = self.evaluate_dyf(
            dyf=dyf, dq_rules=dq_rules, db_name=db_name, table_name=table_name
        )

        query = self.get_query(
            db_name=db_name, table_name=table_name, df=passed_df
        )
        quarantine_query = self.get_query(
            db_name=db_name, table_name=quarantine_table_name, df=failed_df
        )

        self.spark.sql(query)
        self.spark.sql(quarantine_query)


def run() -> None:
    """Run the gold ETL pipeline.

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

    gold_etl = GoldETL(spark=spark)

    gold_etl.write_to_dim_season(glue_context=glue_context)
    gold_etl.write_to_dim_champion(glue_context=glue_context)
    gold_etl.write_to_dim_mvp(glue_context=glue_context)
    gold_etl.write_to_dim_rookie(glue_context=glue_context)
    gold_etl.write_to_dim_conference(glue_context=glue_context)
    gold_etl.write_to_dim_division(glue_context=glue_context)
    gold_etl.write_to_dim_team(glue_context=glue_context)
    gold_etl.write_to_dim_arena(glue_context=glue_context)
    gold_etl.write_to_dim_player(glue_context=glue_context)
    gold_etl.write_to_dim_roster(glue_context=glue_context)
    gold_etl.write_to_fact_top_performer_by_assists(glue_context=glue_context)
    gold_etl.write_to_fact_top_performer_by_points(glue_context=glue_context)
    gold_etl.write_to_fact_top_performer_by_rebounds(glue_context=glue_context)
    gold_etl.write_to_fact_top_performer_by_win_shares(
        glue_context=glue_context
    )
    gold_etl.write_to_fact_conference_stats(glue_context=glue_context)
    gold_etl.write_to_fact_team_per_game_stats(glue_context=glue_context)
    gold_etl.write_to_fact_team_total_stats(glue_context=glue_context)
    gold_etl.write_to_fact_team_per_100_possessions_stats(
        glue_context=glue_context
    )
    gold_etl.write_to_fact_team_advanced_stats(glue_context=glue_context)
    gold_etl.write_to_fact_team_shooting_stats(glue_context=glue_context)
    gold_etl.write_to_fact_opponent_per_game_stats(glue_context=glue_context)
    gold_etl.write_to_fact_opponent_total_stats(glue_context=glue_context)
    gold_etl.write_to_fact_opponent_per_100_possessions_stats(
        glue_context=glue_context
    )
    gold_etl.write_to_fact_opponent_shooting_stats(glue_context=glue_context)
    gold_etl.write_to_fact_regular_season_player_per_game_stats(
        glue_context=glue_context
    )
    gold_etl.write_to_fact_regular_season_player_total_stats(
        glue_context=glue_context
    )
    gold_etl.write_to_fact_regular_season_player_per_36_minutes_stats(
        glue_context=glue_context
    )
    gold_etl.write_to_fact_regular_season_player_per_100_possessions_stats(
        glue_context=glue_context
    )
    gold_etl.write_to_fact_regular_season_player_advanced_stats(
        glue_context=glue_context
    )
    gold_etl.write_to_fact_regular_season_player_adjusted_shooting_stats(
        glue_context=glue_context
    )
    gold_etl.write_to_fact_regular_season_player_shooting_stats(
        glue_context=glue_context
    )
    gold_etl.write_to_fact_regular_season_player_play_by_play_stats(
        glue_context=glue_context
    )
    gold_etl.write_to_fact_playoffs_player_per_game_stats(
        glue_context=glue_context
    )
    gold_etl.write_to_fact_playoffs_player_total_stats(
        glue_context=glue_context
    )
    gold_etl.write_to_fact_playoffs_player_per_36_minutes_stats(
        glue_context=glue_context
    )
    gold_etl.write_to_fact_playoffs_player_per_100_possessions_stats(
        glue_context=glue_context
    )
    gold_etl.write_to_fact_playoffs_player_advanced_stats(
        glue_context=glue_context
    )
    gold_etl.write_to_fact_playoffs_player_adjusted_shooting_stats(
        glue_context=glue_context
    )
    gold_etl.write_to_fact_playoffs_player_shooting_stats(
        glue_context=glue_context
    )
    gold_etl.write_to_fact_playoffs_player_play_by_play_stats(
        glue_context=glue_context
    )
    gold_etl.write_to_fact_player_salaries(glue_context=glue_context)
    gold_etl.write_to_fact_arena_stats(glue_context=glue_context)

    job.commit()


# Execute the job.
run()
