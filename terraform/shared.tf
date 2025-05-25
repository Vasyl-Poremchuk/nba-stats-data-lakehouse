# ================================================================================
# SHARED RESOURCES.
# S3 bucket & common resources used across multiple layers.
# ================================================================================

# S3 bucket for storing Medallion layers (Bronze, Silver, & Gold).
resource "aws_s3_bucket" "nba_data_lakehouse_bucket" {
  bucket = var.nba_data_lakehouse_bucket_name
}

# Create folder structure for Medallion architecture.
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

# S3 bucket for storing AWS Glue Jobs code.
resource "aws_s3_bucket" "glue_jobs" {
  bucket = var.glue_jobs_bucket_name
}
