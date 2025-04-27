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
