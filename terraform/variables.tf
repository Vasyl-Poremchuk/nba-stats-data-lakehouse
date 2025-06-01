variable "aws_region" {
  description = "The AWS region to deploy resources"
  type        = string
  default     = "us-east-1"
}

variable "nba_data_lakehouse_bucket_name" {
  description = "Name for the S3 bucket to store Medallion layers"
  type        = string
  default     = "nba-data-lakehouse"
}

variable "bronze_layer_task_memory_size" {
  description = "Memory for the Lambda function in MB"
  type        = number
  default     = 2048 # 2 GB
}

variable "bronze_layer_task_storage" {
  description = "Storage for the Lambda function in MB"
  type        = number
  default     = 2048 # 2 GB
}

variable "glue_jobs_bucket_name" {
  description = "Name for the S3 bucket to store AWS Glue Jobs"
  type        = string
  default     = "nba-data-lakehouse-glue-jobs"
}

variable "glue_jobs_version" {
  description = "Version of the AWS Glue Jobs"
  type        = string
  default     = "5.0"
}

variable "glue_jobs_max_retries" {
  description = "The max number of retries of AWS Glue Jobs"
  type        = number
  default     = 0
}

variable "glue_jobs_timeout" {
  description = "The max minutes to keep a session for AWS Glue Jobs"
  type        = number
  default     = 120
}

variable "glue_jobs_worker_type" {
  description = "Worker type to use for AWS Glue Jobs"
  type        = string
  default     = "G.1X"
}

variable "glue_jobs_number_of_workers" {
  description = "The max number of workers to use for AWS Glue Jobs"
  type        = number
  default     = 4
}

variable "glue_jobs_python_version" {
  description = "Python version of the AWS Glue Jobs"
  type        = string
  default     = "3"
}

variable "glue_catalog" {
  description = "Name for the AWS Glue Catalog"
  type        = string
  default     = "glue_catalog"
}

variable "silver_layer_seasons_db" {
  description = "Name for the AWS Glue Catalog DB of seasons"
  type        = string
  default     = "silver_seasons"
}

variable "silver_layer_conferences_db" {
  description = "Name of the AWS Glue Catalog DB of conferences"
  type        = string
  default     = "silver_conferences"
}

variable "silver_layer_conferences_stats_db" {
  description = "Name of the AWS Glue Catalog DB of conferences stats"
  type        = string
  default     = "silver_conferences_stats"
}

variable "silver_layer_teams_stats_db" {
  description = "Name of the AWS Glue Catalog DB of teams stats"
  type        = string
  default     = "silver_teams_stats"
}

variable "silver_layer_players_stats_db" {
  description = "Name of the AWS Glue Catalog DB of players stats"
  type        = string
  default     = "silver_players_stats"
}

variable "gold_layer_seasons_db" {
  description = "Name of the AWS Glue Catalog DB of seasons"
  type        = string
  default     = "gold_seasons"
}

variable "gold_layer_champions_db" {
  description = "Name of the AWS Glue Catalog DB of champions"
  type        = string
  default     = "gold_champions"
}

variable "gold_layer_mvps_db" {
  description = "Name of the AWS Glue Catalog DB of MVPs"
  type        = string
  default     = "gold_mvps"
}

variable "gold_layer_rookies_db" {
  description = "Name of the AWS Glue Catalog DB of rookies"
  type        = string
  default     = "gold_rookies"
}

variable "gold_layer_conferences_db" {
  description = "Name of the AWS Glue Catalog DB of conferences"
  type        = string
  default     = "gold_conferences"
}

variable "gold_layer_divisions_db" {
  description = "Name of the AWS Glue Catalog DB of divisions"
  type        = string
  default     = "gold_divisions"
}

variable "gold_layer_teams_db" {
  description = "Name of the AWS Glue Catalog DB of teams"
  type        = string
  default     = "gold_teams"
}

variable "gold_layer_arenas_db" {
  description = "Name of the AWS Glue Catalog DB of arenas"
  type        = string
  default     = "gold_arenas"
}

variable "gold_layer_players_db" {
  description = "Name of the AWS Glue Catalog DB of players"
  type        = string
  default     = "gold_players"
}

variable "gold_layer_rosters_db" {
  description = "Name of the AWS Glue Catalog DB of rosters"
  type        = string
  default     = "gold_rosters"
}

variable "gold_layer_top_performers_by_assists_db" {
  description = "Name of the AWS Glue Catalog DB of the top performers by assists"
  type        = string
  default     = "gold_top_performers_by_assists"
}

variable "gold_layer_top_performers_by_points_db" {
  description = "Name of the AWS Glue Catalog DB of the top performers by points"
  type        = string
  default     = "gold_top_performers_by_points"
}

variable "gold_layer_top_performers_by_rebounds_db" {
  description = "Name of the AWS Glue Catalog DB of the top performers by rebounds"
  type        = string
  default     = "gold_top_performers_by_rebounds"
}

variable "gold_layer_top_performers_by_win_shares_db" {
  description = "Name of the AWS Glue Catalog DB of the top performers by win shares"
  type        = string
  default     = "gold_top_performers_by_win_shares"
}

variable "gold_layer_conferences_stats_db" {
  description = "Name of the AWS Glue Catalog DB of conferences stats"
  type        = string
  default     = "gold_conferences_stats"
}

variable "gold_layer_teams_per_game_stats_db" {
  description = "Name of the AWS Glue Catalog DB of teams per game stats"
  type        = string
  default     = "gold_teams_per_game_stats"
}

variable "gold_layer_teams_total_stats_db" {
  description = "Name of the AWS Glue Catalog DB of teams total stats"
  type        = string
  default     = "gold_teams_total_stats"
}

variable "gold_layer_teams_per_100_possessions_stats_db" {
  description = "Name of the AWS Glue Catalog DB of teams per 100 possessions stats"
  type        = string
  default     = "gold_teams_per_100_possessions_stats"
}

variable "gold_layer_teams_advanced_stats_db" {
  description = "Name of the AWS Glue Catalog DB of teams advanced stats"
  type        = string
  default     = "gold_teams_advanced_stats"
}

variable "gold_layer_teams_shooting_stats_db" {
  description = "Name of the AWS Glue Catalog DB of teams shooting stats"
  type        = string
  default     = "gold_teams_shooting_stats"
}

variable "gold_layer_opponents_per_game_stats_db" {
  description = "Name of the AWS Glue Catalog DB of opponents per game stats"
  type        = string
  default     = "gold_opponents_per_game_stats"
}

variable "gold_layer_opponents_total_stats_db" {
  description = "Name of the AWS Glue Catalog DB of opponents total stats"
  type        = string
  default     = "gold_opponents_total_stats"
}

variable "gold_layer_opponents_per_100_possessions_stats_db" {
  description = "Name of the AWS Glue Catalog DB of opponents per 100 possessions stats"
  type        = string
  default     = "gold_opponents_per_100_possessions_stats"
}

variable "gold_layer_opponents_shooting_stats_db" {
  description = "Name of the AWS Glue Catalog DB of opponents shooting stats"
  type        = string
  default     = "gold_opponents_shooting_stats"
}

variable "gold_layer_regular_season_players_per_game_stats_db" {
  description = "Name of the AWS Glue Catalog DB of regular season players per game stats"
  type        = string
  default     = "gold_regular_season_players_per_game_stats"
}

variable "gold_layer_regular_season_players_total_stats_db" {
  description = "Name of the AWS Glue Catalog DB of regular season players total stats"
  type        = string
  default     = "gold_regular_season_players_total_stats"
}

variable "gold_layer_regular_season_players_per_36_minutes_stats_db" {
  description = "Name of the AWS Glue Catalog DB of regular season players per 36 minutes stats"
  type        = string
  default     = "gold_regular_season_players_per_36_minutes_stats"
}

variable "gold_layer_regular_season_players_per_100_possessions_stats_db" {
  description = "Name of the AWS Glue Catalog DB of regular season players per 100 possessions stats"
  type        = string
  default     = "gold_regular_season_players_per_100_possessions_stats"
}

variable "gold_layer_regular_season_players_advanced_stats_db" {
  description = "Name of the AWS Glue Catalog DB of regular season players advanced stats"
  type        = string
  default     = "gold_regular_season_players_advanced_stats"
}

variable "gold_layer_regular_season_players_adjusted_shooting_stats_db" {
  description = "Name of the AWS Glue Catalog DB of regular season players adjusted shooting stats"
  type        = string
  default     = "gold_regular_season_players_adjusted_shooting_stats"
}

variable "gold_layer_regular_season_players_shooting_stats_db" {
  description = "Name of the AWS Glue Catalog DB of regular season players shooting stats"
  type        = string
  default     = "gold_regular_season_players_shooting_stats"
}
variable "gold_layer_regular_season_players_play_by_play_stats_db" {
  description = "Name of the AWS Glue Catalog DB of regular season players play by play stats"
  type        = string
  default     = "gold_regular_season_players_play_by_play_stats"
}

variable "gold_layer_playoffs_players_per_game_stats_db" {
  description = "Name of the AWS Glue Catalog DB of playoffs players per game stats"
  type        = string
  default     = "gold_playoffs_players_per_game_stats"
}

variable "gold_layer_playoffs_players_total_stats_db" {
  description = "Name of the AWS Glue Catalog DB of playoffs players total stats"
  type        = string
  default     = "gold_playoffs_players_total_stats"
}

variable "gold_layer_playoffs_players_per_36_minutes_stats_db" {
  description = "Name of the AWS Glue Catalog DB of playoffs players per 36 minutes stats"
  type        = string
  default     = "gold_playoffs_players_per_36_minutes_stats"
}

variable "gold_layer_playoffs_players_per_100_possessions_stats_db" {
  description = "Name of the AWS Glue Catalog DB of playoffs players per 100 possessions stats"
  type        = string
  default     = "gold_playoffs_players_per_100_possessions_stats"
}

variable "gold_layer_playoffs_players_advanced_stats_db" {
  description = "Name of the AWS Glue Catalog DB of playoffs players advanced stats"
  type        = string
  default     = "gold_playoffs_players_advanced_stats"
}

variable "gold_layer_playoffs_players_adjusted_shooting_stats_db" {
  description = "Name of the AWS Glue Catalog DB of playoffs players adjusted shooting stats"
  type        = string
  default     = "gold_playoffs_players_adjusted_shooting_stats"
}

variable "gold_layer_playoffs_players_shooting_stats_db" {
  description = "Name of the AWS Glue Catalog DB of playoffs players shooting stats"
  type        = string
  default     = "gold_playoffs_players_shooting_stats"
}
variable "gold_layer_playoffs_players_play_by_play_stats_db" {
  description = "Name of the AWS Glue Catalog DB of playoffs players play by play stats"
  type        = string
  default     = "gold_playoffs_players_play_by_play_stats"
}

variable "gold_layer_players_salaries_db" {
  description = "Name of the AWS Glue Catalog DB of players salaries"
  type        = string
  default     = "gold_players_salaries"
}

variable "gold_layer_arenas_stats_db" {
  description = "Name of the AWS Glue Catalog DB of arenas stats"
  type        = string
  default     = "gold_arenas_stats"
}
