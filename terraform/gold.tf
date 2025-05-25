# ================================================================================
# GOLD LAYER.
# Glue Jobs, databases, & related resources for business-ready analytics data.
# ================================================================================

# Upload Glue Job scripts to S3.
resource "aws_s3_object" "gold_layer_gold_etl" {
  bucket       = aws_s3_bucket.glue_jobs.bucket
  key          = "gold/gold_etl.py"
  source       = "${path.module}/../src/gold/gold_etl.py"
  etag         = filemd5("${path.module}/../src/gold/gold_etl.py")
  content_type = "text/x-python"
}

resource "aws_s3_object" "gold_layer_dq_rules" {
  for_each = fileset("${path.module}/../src/gold/dq_rules", "**")

  bucket = aws_s3_bucket.glue_jobs.bucket
  key    = "gold/dq_rules/${each.value}"
  source = "${path.module}/../src/gold/dq_rules/${each.value}"
  etag   = filemd5("${path.module}/../src/gold/dq_rules/${each.value}")
}

# Create AWS Glue Catalog DBs.
resource "aws_glue_catalog_database" "gold_layer_seasons_catalog_db" {
  name = var.gold_layer_seasons_db
}

resource "aws_glue_catalog_database" "gold_layer_champions_catalog_db" {
  name = var.gold_layer_champions_db
}

resource "aws_glue_catalog_database" "gold_layer_mvps_catalog_db" {
  name = var.gold_layer_mvps_db
}

resource "aws_glue_catalog_database" "gold_layer_rookies_catalog_db" {
  name = var.gold_layer_rookies_db
}

resource "aws_glue_catalog_database" "gold_layer_conferences_catalog_db" {
  name = var.gold_layer_conferences_db
}

resource "aws_glue_catalog_database" "gold_layer_divisions_catalog_db" {
  name = var.gold_layer_divisions_db
}

resource "aws_glue_catalog_database" "gold_layer_teams_catalog_db" {
  name = var.gold_layer_teams_db
}

resource "aws_glue_catalog_database" "gold_layer_arenas_catalog_db" {
  name = var.gold_layer_arenas_db
}

resource "aws_glue_catalog_database" "gold_layer_players_catalog_db" {
  name = var.gold_layer_players_db
}

resource "aws_glue_catalog_database" "gold_layer_rosters_catalog_db" {
  name = var.gold_layer_rosters_db
}

resource "aws_glue_catalog_database" "gold_layer_top_performers_by_assists_catalog_db" {
  name = var.gold_layer_top_performers_by_assists_db
}

resource "aws_glue_catalog_database" "gold_layer_top_performers_by_points_catalog_db" {
  name = var.gold_layer_top_performers_by_points_db
}

resource "aws_glue_catalog_database" "gold_layer_top_performers_by_rebounds_catalog_db" {
  name = var.gold_layer_top_performers_by_rebounds_db
}

resource "aws_glue_catalog_database" "gold_layer_top_performers_by_win_shares_catalog_db" {
  name = var.gold_layer_top_performers_by_win_shares_db
}

resource "aws_glue_catalog_database" "gold_layer_conferences_stats_catalog_db" {
  name = var.gold_layer_conferences_stats_db
}

resource "aws_glue_catalog_database" "gold_layer_teams_per_game_stats_catalog_db" {
  name = var.gold_layer_teams_per_game_stats_db
}

resource "aws_glue_catalog_database" "gold_layer_teams_total_stats_catalog_db" {
  name = var.gold_layer_teams_total_stats_db
}

resource "aws_glue_catalog_database" "gold_layer_teams_per_100_possessions_stats_catalog_db" {
  name = var.gold_layer_teams_per_100_possessions_stats_db
}

resource "aws_glue_catalog_database" "gold_layer_teams_advanced_stats_catalog_db" {
  name = var.gold_layer_teams_advanced_stats_db
}

resource "aws_glue_catalog_database" "gold_layer_teams_shooting_stats_catalog_db" {
  name = var.gold_layer_teams_shooting_stats_db
}

resource "aws_glue_catalog_database" "gold_layer_opponents_per_game_stats_catalog_db" {
  name = var.gold_layer_opponents_per_game_stats_db
}

resource "aws_glue_catalog_database" "gold_layer_opponents_total_stats_catalog_db" {
  name = var.gold_layer_opponents_total_stats_db
}

resource "aws_glue_catalog_database" "gold_layer_opponents_per_100_possessions_stats_catalog_db" {
  name = var.gold_layer_opponents_per_100_possessions_stats_db
}

resource "aws_glue_catalog_database" "gold_layer_opponents_shooting_stats_catalog_db" {
  name = var.gold_layer_opponents_shooting_stats_db
}

resource "aws_glue_catalog_database" "gold_layer_regular_season_players_per_game_stats_catalog_db" {
  name = var.gold_layer_regular_season_players_per_game_stats_db
}

resource "aws_glue_catalog_database" "gold_layer_regular_season_players_total_stats_catalog_db" {
  name = var.gold_layer_regular_season_players_total_stats_db
}

resource "aws_glue_catalog_database" "gold_layer_regular_season_players_per_36_minutes_stats_catalog_db" {
  name = var.gold_layer_regular_season_players_per_36_minutes_stats_db
}

resource "aws_glue_catalog_database" "gold_layer_regular_season_players_per_100_possessions_stats_catalog_db" {
  name = var.gold_layer_regular_season_players_per_100_possessions_stats_db
}

resource "aws_glue_catalog_database" "gold_layer_regular_season_players_advanced_stats_catalog_db" {
  name = var.gold_layer_regular_season_players_advanced_stats_db
}

resource "aws_glue_catalog_database" "gold_layer_regular_season_players_adjusted_shooting_stats_catalog_db" {
  name = var.gold_layer_regular_season_players_adjusted_shooting_stats_db
}

resource "aws_glue_catalog_database" "gold_layer_regular_season_players_shooting_stats_catalog_db" {
  name = var.gold_layer_regular_season_players_shooting_stats_db
}

resource "aws_glue_catalog_database" "gold_layer_regular_season_players_play_by_play_stats_catalog_db" {
  name = var.gold_layer_regular_season_players_play_by_play_stats_db
}

resource "aws_glue_catalog_database" "gold_layer_playoffs_players_per_game_stats_catalog_db" {
  name = var.gold_layer_playoffs_players_per_game_stats_db
}

resource "aws_glue_catalog_database" "gold_layer_playoffs_players_total_stats_catalog_db" {
  name = var.gold_layer_playoffs_players_total_stats_db
}

resource "aws_glue_catalog_database" "gold_layer_playoffs_players_per_36_minutes_stats_catalog_db" {
  name = var.gold_layer_playoffs_players_per_36_minutes_stats_db
}

resource "aws_glue_catalog_database" "gold_layer_playoffs_players_per_100_possessions_stats_catalog_db" {
  name = var.gold_layer_playoffs_players_per_100_possessions_stats_db
}

resource "aws_glue_catalog_database" "gold_layer_playoffs_players_advanced_stats_catalog_db" {
  name = var.gold_layer_playoffs_players_advanced_stats_db
}

resource "aws_glue_catalog_database" "gold_layer_playoffs_players_adjusted_shooting_stats_catalog_db" {
  name = var.gold_layer_playoffs_players_adjusted_shooting_stats_db
}

resource "aws_glue_catalog_database" "gold_layer_playoffs_players_shooting_stats_catalog_db" {
  name = var.gold_layer_playoffs_players_shooting_stats_db
}

resource "aws_glue_catalog_database" "gold_layer_playoffs_players_play_by_play_stats_catalog_db" {
  name = var.gold_layer_playoffs_players_play_by_play_stats_db
}

resource "aws_glue_catalog_database" "gold_layer_players_salaries_catalog_db" {
  name = var.gold_layer_players_salaries_db
}

resource "aws_glue_catalog_database" "gold_layer_arenas_stats_catalog_db" {
  name = var.gold_layer_arenas_stats_db
}

# IAM role for AWS Glue Job.
resource "aws_iam_role" "gold_layer_gold_etl_glue_job_role" {
  name = "gold-layer-gold-etl-glue-job-role"

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

# Create AWS Glue Job.
resource "aws_glue_job" "gold_layer_gold_etl_glue_job" {
  name              = "gold-layer-gold-etl-glue-job"
  glue_version      = var.glue_jobs_version
  role_arn          = aws_iam_role.gold_layer_gold_etl_glue_job_role.arn
  max_retries       = var.glue_jobs_max_retries
  timeout           = var.glue_jobs_timeout
  worker_type       = var.glue_jobs_worker_type
  number_of_workers = var.glue_jobs_number_of_workers

  command {
    script_location = "s3://${aws_s3_bucket.glue_jobs.bucket}/gold/gold_etl.py"
    python_version  = var.glue_jobs_python_version
  }

  default_arguments = {
    "--contiouns-log-logGroup"           = aws_cloudwatch_log_group.gold_layer_gold_etl_log_group.name
    "--enable-continuous-cloudwatch-log" = "true"
    "--enable-continuous-log-filter"     = "true"
    "--catalog"                          = var.glue_catalog
    "--iceberg_s3_path"                  = "s3://${var.nba_data_lakehouse_bucket_name}/gold"
    "--glue_jobs_bucket_name"            = var.glue_jobs_bucket_name
    "--dq_rules_prefix"                  = "gold/dq_rules"
  }
}

# Create CloudWatch Log group.
resource "aws_cloudwatch_log_group" "gold_layer_gold_etl_log_group" {
  name = "/aws/glue/gold-layer-gold-etl-glue-job"

  retention_in_days = 30
}

# IAM policy for S3 access.
resource "aws_iam_policy" "gold_layer_s3_access_policy" {
  name = "gold-layer-s3-access-policy"

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
            "arn:aws:s3:::${var.glue_jobs_bucket_name}/gold/*",
            "arn:aws:s3:::${var.nba_data_lakehouse_bucket_name}",
            "arn:aws:s3:::${var.nba_data_lakehouse_bucket_name}/silver/*",
            "arn:aws:s3:::${var.nba_data_lakehouse_bucket_name}/gold/*",
          ]
        }
      ]
    }
  )
}

# IAM policy for Glue operations.
resource "aws_iam_policy" "gold_layer_glue_policy" {
  name = "gold-layer-glue-policy"

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

# Attach S3 policy to Glue role.
resource "aws_iam_role_policy_attachment" "gold_layer_gold_etl_s3_access_policy_attachment" {
  role       = aws_iam_role.gold_layer_gold_etl_glue_job_role.name
  policy_arn = aws_iam_policy.gold_layer_s3_access_policy.arn
}

# Attach Glue policy to Glue role.
resource "aws_iam_role_policy_attachment" "gold_layer_gold_etl_glue_policy_attachment" {
  role       = aws_iam_role.gold_layer_gold_etl_glue_job_role.name
  policy_arn = aws_iam_policy.gold_layer_glue_policy.arn
}
