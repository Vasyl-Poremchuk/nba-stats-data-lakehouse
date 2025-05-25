# ================================================================================
# BRONZE LAYER.
# Lambda function & related resource for raw data ingestion.
# ================================================================================

# Lambda deployment package.
data "archive_file" "bronze_layer_lambda_code" {
  type        = "zip"
  source_file = "${path.module}/lambda/lambda_func.py"
  output_path = "${path.module}/lambda/lambda_func.zip"
}

# CloudWatch Log Group for Lambda.
resource "aws_cloudwatch_log_group" "bronze_layer_log_group" {
  name = "/aws/lambda/bronze-layer-trigger"

  retention_in_days = 30
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

# Lambda function for bronze layer data ingestion.
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

# IAM policy for S3 access.
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

# IAM policy for CloudWatch Logs.
resource "aws_iam_policy" "bronze_layer_log_policy" {
  name        = "bronze_layer_log_policy"
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

# Attach S3 policy to Lambda role.
resource "aws_iam_role_policy_attachment" "bronze_layer_s3_access_policy_attachment" {
  role       = aws_iam_role.bronze_layer_lambda_role.name
  policy_arn = aws_iam_policy.bronze_layer_s3_access_policy.arn
}

# Attach CloudWatch policy to Lambda role.
resource "aws_iam_role_policy_attachment" "bronze_layer_log_policy_attachment" {
  role       = aws_iam_role.bronze_layer_lambda_role.name
  policy_arn = aws_iam_policy.bronze_layer_log_policy.arn
}
