terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }

  backend "s3" {
    bucket       = "nba-data-lakehouse-terraform-state"
    key          = "terraform.tfstate"
    region       = "us-east-1"
    encrypt      = true
    use_lockfile = true
  }
}

provider "aws" {
  region = var.aws_region
}

# S3 bucket for storing Medallion layers.
resource "aws_s3_bucket" "nba_data_lakehouse_bucket" {
  bucket = var.nba_data_lakehouse_bucket_name
}

resource "aws_s3_object" "medallion_layers" {
  for_each = toset(
    [
      "bronze/",
      "silver/",
      "gold/"
    ]
  )

  bucket = aws_s3_bucket.nba_data_lakehouse_bucket.id
  key    = each.value
}

# IAM role for Lambda function.
resource "aws_iam_role" "bronze_layer_lambda_role" {
  name = "bronze-layer-lambda-role"

  assume_role_policy = jsonencode(
    {
      Version = "2012-10-17"
      Statement = [
        {
          Action = "sts:AssumeRole"
          Effect = "Allow"
          Principal = {
            Service = "lambda.amazonaws.com"
          }
        }
      ]
    }
  )
}

# Lambda function to load data into the bronze layer.
resource "aws_lambda_function" "bronze_layer_trigger" {
  function_name = "bronze-layer-trigger"
  role          = aws_iam_role.bronze_layer_lambda_role.arn
  handler       = "lambda_func.load_into_bronze_layer_handler"
  runtime       = "python3.12"
  timeout       = 240
  memory_size   = var.bronze_layer_task_memory_size

  filename         = data.archive_file.bronze_layer_lambda_code.output_path
  source_code_hash = data.archive_file.bronze_layer_lambda_code.output_base64sha256

  depends_on = [aws_cloudwatch_log_group.bronze_layer_log_group]

  ephemeral_storage {
    size = var.bronze_layer_task_storage
  }
}

data "archive_file" "bronze_layer_lambda_code" {
  type        = "zip"
  source_file = "${path.module}/lambda/lambda_func.py"
  output_path = "${path.module}/lambda/lambda_func.zip"
}

# IAM policy for interacting with S3 bucket objects.
resource "aws_iam_policy" "bronze_layer_s3_access_policy" {
  name        = "bronze-layer-s3-access-policy"
  description = "Allow Lambda function to load source objects into the bronze layer"

  policy = jsonencode(
    {
      Version = "2012-10-17"
      Statement = [
        {
          Effect = "Allow"
          Action = [
            "s3:ListBucket",
            "s3:GetObject",
            "s3:PutObject"
          ]
          Resource = [
            "arn:aws:s3:::nba-data-stats",
            "arn:aws:s3:::nba-data-stats/processed/*",
            "arn:aws:s3:::${var.nba_data_lakehouse_bucket_name}",
            "arn:aws:s3:::${var.nba_data_lakehouse_bucket_name}/bronze/*"
          ]
        }
      ]
    }
  )
}

resource "aws_iam_role_policy_attachment" "bronze_layer_s3_access_policy_attachment" {
  role       = aws_iam_role.bronze_layer_lambda_role.name
  policy_arn = aws_iam_policy.bronze_layer_s3_access_policy.arn
}

resource "aws_cloudwatch_log_group" "bronze_layer_log_group" {
  name = "/aws/lambda/bronze-layer-trigger"

  retention_in_days = 30
}

resource "aws_iam_policy" "bronze_layer_log_policy" {
  name        = "brzone_layer_log_policy"
  description = "Allow Lambda function to write logs into CloudWatch"

  policy = jsonencode(
    {
      Version = "2012-10-17"
      Statement = [
        {
          Effect = "Allow"
          Action = [
            "logs:CreateLogGroup",
            "logs:CreateLogStream",
            "logs:PutLogEvents"
          ]
          Resource = "arn:aws:logs:*:*:*"
        }
      ]
    }
  )
}

resource "aws_iam_role_policy_attachment" "bronze_layer_log_policy_attachment" {
  role       = aws_iam_role.bronze_layer_lambda_role.name
  policy_arn = aws_iam_policy.bronze_layer_log_policy.arn
}

# EventBridge rule for scheduled loading (once per year).
resource "aws_cloudwatch_event_rule" "bronze_layer_event_trigger" {
  name                = "bronze-layer-event-trigger"
  description         = "Trigger loading objects into the bronze layer"
  schedule_expression = "cron(0 0 2 11 ? *)" # Run at midnight on November 2nd
}

resource "aws_cloudwatch_event_target" "bronze_layer_event_target" {
  rule      = aws_cloudwatch_event_rule.bronze_layer_event_trigger.name
  target_id = "InvokeLambda"
  arn       = aws_lambda_function.bronze_layer_trigger.arn
}

resource "aws_lambda_permission" "bronze_layer_allow_event_bridge" {
  statement_id  = "AllowExecutionFromEventBrindge"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.bronze_layer_trigger.function_name
  principal     = "events.amazonaws.com"
  source_arn    = aws_cloudwatch_event_rule.bronze_layer_event_trigger.arn
}

# S3 bucket for storing AWS Glue Jobs.
resource "aws_s3_bucket" "glue_jobs" {
  bucket = var.glue_jobs_bucket_name
}

resource "aws_s3_object" "silver_layer_season_etl" {
  bucket       = aws_s3_bucket.glue_jobs.bucket
  key          = "silver/season_etl.py"
  source       = "${path.module}/../src/silver/season_etl.py"
  etag         = filemd5("${path.module}/../src/silver/season_etl.py")
  content_type = "text/x-python"
}

resource "aws_s3_object" "silver_layer_conference_etl" {
  bucket       = aws_s3_bucket.glue_jobs.bucket
  key          = "silver/conference_etl.py"
  source       = "${path.module}/../src/silver/conference_etl.py"
  etag         = filemd5("${path.module}/../src/silver/conference_etl.py")
  content_type = "text/x-python"
}

resource "aws_s3_object" "silver_layer_conference_stats_etl" {
  bucket       = aws_s3_bucket.glue_jobs.bucket
  key          = "silver/conference_stats_etl.py"
  source       = "${path.module}/../src/silver/conference_stats_etl.py"
  etag         = filemd5("${path.module}/../src/silver/conference_stats_etl.py")
  content_type = "text/x-python"
}

resource "aws_s3_object" "silver_layer_team_stats_etl" {
  bucket       = aws_s3_bucket.glue_jobs.bucket
  key          = "silver/team_stats_etl.py"
  source       = "${path.module}/../src/silver/team_stats_etl.py"
  etag         = filemd5("${path.module}/../src/silver/team_stats_etl.py")
  content_type = "text/x-python"
}

resource "aws_s3_object" "silver_layer_player_stats_etl" {
  bucket       = aws_s3_bucket.glue_jobs.bucket
  key          = "silver/player_stats_etl.py"
  source       = "${path.module}/../src/silver/player_stats_etl.py"
  etag         = filemd5("${path.module}/../src/silver/player_stats_etl.py")
  content_type = "text/x-python"
}

resource "aws_s3_object" "silver_layer_teams_map" {
  bucket = aws_s3_bucket.glue_jobs.bucket
  key    = "silver/map/teams_map.json"
  source = "${path.module}/../src/silver/map/teams_map.json"
  etag   = filemd5("${path.module}/../src/silver/map/teams_map.json")
}

# Create AWS Glue Catalog DBs.
resource "aws_glue_catalog_database" "silver_layer_seasons_glue_catalog_db" {
  name = var.silver_layer_seasons_db
}

resource "aws_glue_catalog_database" "silver_layer_conferences_catalog_db" {
  name = var.silver_layer_conferences_db
}

resource "aws_glue_catalog_database" "silver_layer_conferences_stats_catalog_db" {
  name = var.silver_layer_conferences_stats_db
}

resource "aws_glue_catalog_database" "silver_layer_teams_stats_catalog_db" {
  name = var.silver_layer_teams_stats_db
}

resource "aws_glue_catalog_database" "silver_layer_players_stats_catalog_db" {
  name = var.silver_layer_players_stats_db
}

# IAM roles for AWS Glue jobs.
resource "aws_iam_role" "silver_layer_season_etl_glue_job_role" {
  name = "silver-layer-season-etl-glue-job-role"

  assume_role_policy = jsonencode(
    {
      Version = "2012-10-17"
      Statement = [
        {
          Action = "sts:AssumeRole"
          Effect = "Allow"
          Principal = {
            Service = "glue.amazonaws.com"
          }
        }
      ]
    }
  )
}

resource "aws_iam_role" "silver_layer_conference_etl_glue_job_role" {
  name = "silver-layer-conference-etl-glue-job-role"

  assume_role_policy = jsonencode(
    {
      Version = "2012-10-17"
      Statement = [
        {
          Action = "sts:AssumeRole"
          Effect = "Allow"
          Principal = {
            Service = "glue.amazonaws.com"
          }
        }
      ]
    }
  )
}

resource "aws_iam_role" "silver_layer_conference_stats_etl_glue_job_role" {
  name = "silver-layer-conference-stats-elt-glue-job-role"

  assume_role_policy = jsonencode(
    {
      Version = "2012-10-17"
      Statement = [
        {
          Action = "sts:AssumeRole"
          Effect = "Allow"
          Principal = {
            Service = "glue.amazonaws.com"
          }
        }
      ]
    }
  )
}

resource "aws_iam_role" "silver_layer_team_stats_etl_glue_job_role" {
  name = "silver-layer-team-stats-etl-glue-job-role"

  assume_role_policy = jsonencode(
    {
      Version = "2012-10-17"
      Statement = [
        {
          Action = "sts:AssumeRole"
          Effect = "Allow"
          Principal = {
            Service = "glue.amazonaws.com"
          }
        }
      ]
    }
  )
}

resource "aws_iam_role" "silver_layer_player_stats_etl_glue_job_role" {
  name = "silver-layer-player-stats-etl-glue-job-role"

  assume_role_policy = jsonencode(
    {
      Version = "2012-10-17"
      Statement = [
        {
          Action = "sts:AssumeRole"
          Effect = "Allow"
          Principal = {
            Service = "glue.amazonaws.com"
          }
        }
      ]
    }
  )
}

# Create AWS Glue jobs.
resource "aws_glue_job" "silver_layer_season_etl_glue_job" {
  name              = "silver-layer-season-etl-glue-job"
  glue_version      = var.glue_jobs_version
  role_arn          = aws_iam_role.silver_layer_season_etl_glue_job_role.arn
  max_retries       = var.glue_jobs_max_retries
  timeout           = var.glue_jobs_timeout
  worker_type       = var.glue_jobs_worker_type
  number_of_workers = var.glue_jobs_number_of_workers

  command {
    script_location = "s3://${aws_s3_bucket.glue_jobs.bucket}/silver/season_etl.py"
    python_version  = var.glue_jobs_python_version
  }

  default_arguments = {
    "--continuous-log-logGroup"          = aws_cloudwatch_log_group.silver_layer_season_etl_log_group.name
    "--enable-continuous-cloudwatch-log" = "true"
    "--enable-continuous-log-filter"     = "true"
    "--catalog"                          = var.glue_catalog
    "--iceberg_s3_path"                  = "s3://${var.nba_data_lakehouse_bucket_name}/silver"
    "--bucket_name"                      = var.nba_data_lakehouse_bucket_name
    "--teams_map_s3_path"                = "s3://${var.glue_jobs_bucket_name}/silver/map/teams_map.json"
  }
}

resource "aws_glue_job" "silver_layer_conference_etl_glue_job" {
  name              = "silver-layer-conference-etl-glue-job"
  glue_version      = var.glue_jobs_version
  role_arn          = aws_iam_role.silver_layer_conference_etl_glue_job_role.arn
  max_retries       = var.glue_jobs_max_retries
  timeout           = var.glue_jobs_timeout
  worker_type       = var.glue_jobs_worker_type
  number_of_workers = var.glue_jobs_number_of_workers

  command {
    script_location = "s3://${aws_s3_bucket.glue_jobs.bucket}/silver/conference_etl.py"
    python_version  = var.glue_jobs_python_version
  }

  default_arguments = {
    "--continous-log-logGroup"          = aws_cloudwatch_log_group.silver_layer_conference_etl_log_group.name
    "--enable-continous-cloudwatch-log" = "true"
    "--enable-continous-log-filter"     = "true"
    "--catalog"                         = var.glue_catalog
    "--iceberg_s3_path"                 = "s3://${var.nba_data_lakehouse_bucket_name}/silver"
    "--bucket_name"                     = var.nba_data_lakehouse_bucket_name
    "--teams_map_s3_path"               = "s3://${var.glue_jobs_bucket_name}/silver/map/teams_map.json"
  }
}

resource "aws_glue_job" "silver_layer_conference_stats_etl_glue_job" {
  name              = "silver-layer-conference-stats-etl-glue-job"
  glue_version      = var.glue_jobs_version
  role_arn          = aws_iam_role.silver_layer_conference_stats_etl_glue_job_role.arn
  max_retries       = var.glue_jobs_max_retries
  timeout           = var.glue_jobs_timeout
  worker_type       = var.glue_jobs_worker_type
  number_of_workers = var.glue_jobs_number_of_workers

  command {
    script_location = "s3://${aws_s3_bucket.glue_jobs.bucket}/silver/conference_stats_etl.py"
    python_version  = var.glue_jobs_python_version
  }

  default_arguments = {
    "--continous-log-logGroup"          = aws_cloudwatch_log_group.silver_layer_conference_stats_etl_log_group.name
    "--enable-continous-cloudwatch-log" = "true"
    "--enable-continous-log-filter"     = "true"
    "--catalog"                         = var.glue_catalog
    "--iceberg_s3_path"                 = "s3://${var.nba_data_lakehouse_bucket_name}/silver"
    "--bucket_name"                     = var.nba_data_lakehouse_bucket_name
    "--teams_map_s3_path"               = "s3://${var.glue_jobs_bucket_name}/silver/map/teams_map.json"
  }
}

resource "aws_glue_job" "silver_layer_team_stats_etl_glue_job" {
  name              = "silvery-layer-team-stats-etl-glue-job"
  glue_version      = var.glue_jobs_version
  role_arn          = aws_iam_role.silver_layer_team_stats_etl_glue_job_role.arn
  max_retries       = var.glue_jobs_max_retries
  worker_type       = var.glue_jobs_worker_type
  number_of_workers = var.glue_jobs_number_of_workers

  command {
    script_location = "s3://${aws_s3_bucket.glue_jobs.bucket}/silver/team_stats_etl.py"
    python_version  = var.glue_jobs_python_version
  }

  default_arguments = {
    "--continous-log-logGroup"          = aws_cloudwatch_log_group.silver_layer_team_stats_etl_log_group.name
    "--enable-continous-cloudwatch-log" = "true"
    "--enable-continuous-log-filter"    = "true"
    "--catalog"                         = var.glue_catalog
    "--iceberg_s3_path"                 = "s3://${var.nba_data_lakehouse_bucket_name}/silver"
    "--bucket_name"                     = var.nba_data_lakehouse_bucket_name
  }
}

resource "aws_glue_job" "silver_layer_player_stats_etl_glue_job" {
  name              = "silver-layer-player-stats-etl-glue-job"
  glue_version      = var.glue_jobs_version
  role_arn          = aws_iam_role.silver_layer_player_stats_etl_glue_job_role.arn
  max_retries       = var.glue_jobs_max_retries
  worker_type       = var.glue_jobs_worker_type
  number_of_workers = var.glue_jobs_number_of_workers

  command {
    script_location = "s3://${aws_s3_bucket.glue_jobs.bucket}/silver/player_stats_etl.py"
    python_version  = var.glue_jobs_python_version
  }

  default_arguments = {
    "--continous-log-logGroup"          = aws_cloudwatch_log_group.silver_layer_player_stats_etl_log_group.name
    "--enable-continous-cloudwatch-log" = "true"
    "--enable-continous-log-filter"     = "true"
    "--catalog"                         = var.glue_catalog
    "--iceberg_s3_path"                 = "s3://${var.nba_data_lakehouse_bucket_name}/silver"
    "--bucket_name"                     = var.nba_data_lakehouse_bucket_name
  }
}

# IAM policy for interacting with S3 bucket objects.
resource "aws_iam_policy" "silver_layer_s3_access_policy" {
  name = "silver-layer-s3-access-policy"

  policy = jsonencode(
    {
      Version = "2012-10-17"
      Statement = [
        {
          Effect = "Allow"
          Action = [
            "s3:ListBucket",
            "s3:GetObject",
            "s3:PutObject"
          ]
          Resource = [
            "arn:aws:s3:::${var.glue_jobs_bucket_name}",
            "arn:aws:s3:::${var.glue_jobs_bucket_name}/silver/*",
            "arn:aws:s3:::${var.nba_data_lakehouse_bucket_name}",
            "arn:aws:s3:::${var.nba_data_lakehouse_bucket_name}/bronze/*",
            "arn:aws:s3:::${var.nba_data_lakehouse_bucket_name}/silver/*",
          ]
        }
      ]
    }
  )
}

resource "aws_iam_policy" "silver_layer_glue_policy" {
  name = "silver-layer-glue-policy"

  policy = jsonencode(
    {
      Version = "2012-10-17"
      Statement = [
        {
          Effect = "Allow"
          Action = [
            "glue:GetJob",
            "glue:GetJobs",
            "glue:StartJobRun",
            "glue:GetJobRun",
            "glue:GetJobRuns",
            "glue:GetTable",
            "glue:GetTables",
            "glue:CreateTable",
            "glue:UpdateTable",
            "glue:DeleteTable",
            "glue:GetDatabase",
            "glue:GetDatabases",
            "glue:CreatePartition",
            "glue:GetPartition",
            "glue:GetPartitions",
            "glue:DeletePartition",
            "glue:DeletePartition",
            "glue:BatchCreatePartition"
          ]
          Resource = "*"
        }
      ]
    }
  )
}

resource "aws_iam_role_policy_attachment" "silver_layer_season_etl_s3_access_policy_attachment" {
  role       = aws_iam_role.silver_layer_season_etl_glue_job_role.name
  policy_arn = aws_iam_policy.silver_layer_s3_access_policy.arn
}

resource "aws_iam_role_policy_attachment" "silver_layer_conference_etl_s3_access_policy_attachment" {
  role       = aws_iam_role.silver_layer_conference_etl_glue_job_role.name
  policy_arn = aws_iam_policy.silver_layer_s3_access_policy.arn
}

resource "aws_iam_role_policy_attachment" "silver_layer_conference_stats_etl_s3_access_policy_attachment" {
  role       = aws_iam_role.silver_layer_conference_stats_etl_glue_job_role.name
  policy_arn = aws_iam_policy.silver_layer_s3_access_policy.arn
}

resource "aws_iam_role_policy_attachment" "silver_layer_team_stats_etl_s3_access_policy_attachment" {
  role       = aws_iam_role.silver_layer_team_stats_etl_glue_job_role.name
  policy_arn = aws_iam_policy.silver_layer_s3_access_policy.arn
}

resource "aws_iam_role_policy_attachment" "silver_layer_player_stats_etl_s3_access_policy_attachment" {
  role       = aws_iam_role.silver_layer_player_stats_etl_glue_job_role.name
  policy_arn = aws_iam_policy.silver_layer_s3_access_policy.arn
}

resource "aws_iam_role_policy_attachment" "silver_layer_season_etl_glue_policy_attachment" {
  role       = aws_iam_role.silver_layer_season_etl_glue_job_role.name
  policy_arn = aws_iam_policy.silver_layer_glue_policy.arn
}

resource "aws_iam_role_policy_attachment" "silver_layer_conference_etl_glue_policy_attachment" {
  role       = aws_iam_role.silver_layer_conference_etl_glue_job_role.name
  policy_arn = aws_iam_policy.silver_layer_glue_policy.arn
}

resource "aws_iam_role_policy_attachment" "silver_layer_conference_stats_etl_glue_policy_attachment" {
  role       = aws_iam_role.silver_layer_conference_stats_etl_glue_job_role.name
  policy_arn = aws_iam_policy.silver_layer_glue_policy.arn
}

resource "aws_iam_role_policy_attachment" "silver_layer_team_stats_elt_glue_policy_attachment" {
  role       = aws_iam_role.silver_layer_team_stats_etl_glue_job_role.name
  policy_arn = aws_iam_policy.silver_layer_glue_policy.arn
}

resource "aws_iam_role_policy_attachment" "silver_layer_player_stats_etl_glue_policy_attachment" {
  role       = aws_iam_role.silver_layer_player_stats_etl_glue_job_role.name
  policy_arn = aws_iam_policy.silver_layer_glue_policy.arn
}

resource "aws_cloudwatch_log_group" "silver_layer_season_etl_log_group" {
  name = "/aws/glue/silver-layer-season-etl-glue-job"

  retention_in_days = 30
}

resource "aws_cloudwatch_log_group" "silver_layer_conference_etl_log_group" {
  name = "/aws/glue/silver-layer-conference-etl-glue-job"

  retention_in_days = 30
}

resource "aws_cloudwatch_log_group" "silver_layer_conference_stats_etl_log_group" {
  name = "/aws/glue/silver-layer-conference-stats-etl-glue-job"

  retention_in_days = 30
}

resource "aws_cloudwatch_log_group" "silver_layer_team_stats_etl_log_group" {
  name = "/aws/glue/silver-layer-team-stats-etl-glue-job"

  retention_in_days = 30
}

resource "aws_cloudwatch_log_group" "silver_layer_player_stats_etl_log_group" {
  name = "/aws/glue/silver-layer-player-stats-etl-glue-job"

  retention_in_days = 30
}
