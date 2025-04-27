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
