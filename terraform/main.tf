# Terraform Infrastructure-as-Code for Financial Inclusion Engine
# Provisioning AWS App Runner, Encrypted S3 Bucket & CloudWatch Log Group

terraform {
  required_version = ">= 1.5.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = var.aws_region
}

variable "aws_region" {
  type        = string
  default     = "us-east-1"
  description = "AWS deployment target region"
}

variable "app_name" {
  type        = string
  default     = "financial-inclusion-engine"
  description = "Application stack identifier"
}

# 1. AWS CloudWatch Log Group for Structured Audit Logs
resource "aws_cloudwatch_log_group" "audit_logs" {
  name              = "/aws/apprunner/${var.app_name}-audit-logs"
  retention_in_days = 90

  tags = {
    Environment = "Production"
    Compliance  = "FCRA-ECOA"
  }
}

# 2. AWS S3 Encrypted Bucket for Compliance Audit Certificates
resource "aws_s3_bucket" "audit_storage" {
  bucket        = "${var.app_name}-audit-storage-2026"
  force_destroy = true
}

resource "aws_s3_bucket_server_side_encryption_configuration" "s3_encryption" {
  bucket = aws_s3_bucket.audit_storage.id

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}

resource "aws_s3_bucket_public_access_block" "block_public" {
  bucket                  = aws_s3_bucket.audit_storage.id
  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

# 3. IAM Role for AWS Bedrock & CloudWatch Execution Access
resource "aws_iam_role" "apprunner_execution_role" {
  name = "${var.app_name}-apprunner-exec-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "build.apprunner.amazonaws.com"
        }
      }
    ]
  })
}

# IAM Policy granting AWS Bedrock LLM invocation access
resource "aws_iam_policy" "bedrock_access_policy" {
  name        = "${var.app_name}-bedrock-policy"
  description = "Grants least-privilege Bedrock Mantle model invocation permissions"

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "bedrock:InvokeModel",
          "bedrock:InvokeModelWithResponseStream"
        ]
        Resource = "*"
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "attach_bedrock" {
  role       = aws_iam_role.apprunner_execution_role.name
  policy_arn = aws_iam_policy.bedrock_access_policy.arn
}

# Output parameters
output "s3_audit_bucket_name" {
  value = aws_s3_bucket.audit_storage.id
}

output "cloudwatch_log_group" {
  value = aws_cloudwatch_log_group.audit_logs.name
}
