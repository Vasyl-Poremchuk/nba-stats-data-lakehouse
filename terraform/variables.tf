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
  default     = 60
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
