# ================================================================================
# SILVER LAYER.
# Glue jobs, databases, & related resources for data cleaning & transformation.
# ================================================================================

# Upload Glue Job scripts to S3.
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

# Upload supporting files (teams mapping file & data quality files).
resource "aws_s3_object" "silver_layer_teams_map" {
  bucket = aws_s3_bucket.glue_jobs.bucket
  key    = "silver/map/teams_map.json"
  source = "${path.module}/../src/silver/map/teams_map.json"
  etag   = filemd5("${path.module}/../src/silver/map/teams_map.json")
}

resource "aws_s3_object" "silver_layer_dq_rules" {
  for_each = fileset("${path.module}/../src/silver/dq_rules", "**")

  bucket = aws_s3_bucket.glue_jobs.bucket
  key    = "silver/dq_rules/${each.value}"
  source = "${path.module}/../src/silver/dq_rules/${each.value}"
  etag   = filemd5("${path.module}/../src/silver/dq_rules/${each.value}")
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

# IAM roles for AWS Glue Jobs.
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
  name = "silver-layer-conference-stats-etl-glue-job-role"

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

# Create AWS Glue Jobs.
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
    "--glue_jobs_bucket_name"            = var.glue_jobs_bucket_name
    "--dq_rules_prefix"                  = "silver/dq_rules"
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
    "--continuous-log-logGroup"          = aws_cloudwatch_log_group.silver_layer_conference_etl_log_group.name
    "--enable-continuous-cloudwatch-log" = "true"
    "--enable-continuous-log-filter"     = "true"
    "--catalog"                          = var.glue_catalog
    "--iceberg_s3_path"                  = "s3://${var.nba_data_lakehouse_bucket_name}/silver"
    "--bucket_name"                      = var.nba_data_lakehouse_bucket_name
    "--teams_map_s3_path"                = "s3://${var.glue_jobs_bucket_name}/silver/map/teams_map.json"
    "--glue_jobs_bucket_name"            = var.glue_jobs_bucket_name
    "--dq_rules_prefix"                  = "silver/dq_rules"
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
    "--continuous-log-logGroup"          = aws_cloudwatch_log_group.silver_layer_conference_stats_etl_log_group.name
    "--enable-continuous-cloudwatch-log" = "true"
    "--enable-continuous-log-filter"     = "true"
    "--catalog"                          = var.glue_catalog
    "--iceberg_s3_path"                  = "s3://${var.nba_data_lakehouse_bucket_name}/silver"
    "--bucket_name"                      = var.nba_data_lakehouse_bucket_name
    "--teams_map_s3_path"                = "s3://${var.glue_jobs_bucket_name}/silver/map/teams_map.json"
    "--glue_jobs_bucket_name"            = var.glue_jobs_bucket_name
    "--dq_rules_prefix"                  = "silver/dq_rules"
  }
}

resource "aws_glue_job" "silver_layer_team_stats_etl_glue_job" {
  name              = "silver-layer-team-stats-etl-glue-job"
  glue_version      = var.glue_jobs_version
  role_arn          = aws_iam_role.silver_layer_team_stats_etl_glue_job_role.arn
  max_retries       = var.glue_jobs_max_retries
  timeout           = var.glue_jobs_timeout
  worker_type       = var.glue_jobs_worker_type
  number_of_workers = var.glue_jobs_number_of_workers

  command {
    script_location = "s3://${aws_s3_bucket.glue_jobs.bucket}/silver/team_stats_etl.py"
    python_version  = var.glue_jobs_python_version
  }

  default_arguments = {
    "--continuous-log-logGroup"          = aws_cloudwatch_log_group.silver_layer_team_stats_etl_log_group.name
    "--enable-continuous-cloudwatch-log" = "true"
    "--enable-continuous-log-filter"     = "true"
    "--catalog"                          = var.glue_catalog
    "--iceberg_s3_path"                  = "s3://${var.nba_data_lakehouse_bucket_name}/silver"
    "--bucket_name"                      = var.nba_data_lakehouse_bucket_name
    "--glue_jobs_bucket_name"            = var.glue_jobs_bucket_name
    "--dq_rules_prefix"                  = "silver/dq_rules"
  }
}

resource "aws_glue_job" "silver_layer_player_stats_etl_glue_job" {
  name              = "silver-layer-player-stats-etl-glue-job"
  glue_version      = var.glue_jobs_version
  role_arn          = aws_iam_role.silver_layer_player_stats_etl_glue_job_role.arn
  max_retries       = var.glue_jobs_max_retries
  timeout           = var.glue_jobs_timeout
  worker_type       = var.glue_jobs_worker_type
  number_of_workers = var.glue_jobs_number_of_workers

  command {
    script_location = "s3://${aws_s3_bucket.glue_jobs.bucket}/silver/player_stats_etl.py"
    python_version  = var.glue_jobs_python_version
  }

  default_arguments = {
    "--continuous-log-logGroup"          = aws_cloudwatch_log_group.silver_layer_player_stats_etl_log_group.name
    "--enable-continuous-cloudwatch-log" = "true"
    "--enable-continuous-log-filter"     = "true"
    "--catalog"                          = var.glue_catalog
    "--iceberg_s3_path"                  = "s3://${var.nba_data_lakehouse_bucket_name}/silver"
    "--bucket_name"                      = var.nba_data_lakehouse_bucket_name
    "--glue_jobs_bucket_name"            = var.glue_jobs_bucket_name
    "--dq_rules_prefix"                  = "silver/dq_rules"
  }
}

# Create CloudWatch Log groups.
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

# IAM policy for S3 access.
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

# IAM policy for Glue operations.
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
            "glue:BatchCreatePartition",
            "glue:CreateDataQualityRuleset",
            "glue:DeleteDataQualityRuleset",
            "glue:GetDataQualityRuleset",
            "glue:ListDataQualityRulesets",
            "glue:UpdateDataQualityRuleset",
            "glue:GetDataQualityResult",
            "glue:ListDataQualityResults"
          ]
          Resource = "*"
        }
      ]
    }
  )
}

# Attach S3 policies to Glue roles.
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

# Attach Glue policies to Glue roles.
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

resource "aws_iam_role_policy_attachment" "silver_layer_team_stats_etl_glue_policy_attachment" {
  role       = aws_iam_role.silver_layer_team_stats_etl_glue_job_role.name
  policy_arn = aws_iam_policy.silver_layer_glue_policy.arn
}

resource "aws_iam_role_policy_attachment" "silver_layer_player_stats_etl_glue_policy_attachment" {
  role       = aws_iam_role.silver_layer_player_stats_etl_glue_job_role.name
  policy_arn = aws_iam_policy.silver_layer_glue_policy.arn
}
