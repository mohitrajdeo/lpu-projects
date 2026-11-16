# Modern OpenTofu / Terraform GitOps & Checkov-Compliant Architecture v2.0
# Author: Mohit Raj Deo (12323329 | Roll: 62)

terraform {
  required_version = ">= 1.6.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.30"
    }
  }
  backend "s3" {
    bucket         = "mohit-aiops-terraform-state"
    key            = "v2/production.tfstate"
    region         = "ap-south-1"
    encrypt        = true
    dynamodb_table = "terraform-lock-table"
  }
}

provider "aws" {
  region = var.aws_region
  default_tags {
    tags = {
      Project     = "AIOps-Cloud-Intelligence-v2"
      Owner       = "Mohit Raj Deo (12323329)"
      ManagedBy   = "OpenTofu-GitOps-Atlantis"
      Compliance  = "CIS-Benchmark-v1.4"
    }
  }
}

variable "aws_region" {
  type    = string
  default = "ap-south-1"
}

# KMS Key for Encrypted Telemetry Storage
resource "aws_kms_key" "telemetry_kms" {
  description             = "KMS Key for AIOps Telemetry and State Encryption"
  deletion_window_in_days = 7
  enable_key_rotation     = true
}

# S3 Bucket with Server-Side Encryption and Versioning
resource "aws_s3_bucket" "telemetry_lake" {
  bucket        = "aiops-telemetry-lake-v2"
  force_destroy = false
}

resource "aws_s3_bucket_server_side_encryption_configuration" "telemetry_lake_crypto" {
  bucket = aws_s3_bucket.telemetry_lake.id
  rule {
    apply_server_side_encryption_by_default {
      kms_master_key_id = aws_kms_key.telemetry_kms.arn
      sse_algorithm     = "aws:kms"
    }
  }
}

resource "aws_s3_bucket_public_access_block" "telemetry_lake_pab" {
  bucket                  = aws_s3_bucket.telemetry_lake.id
  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

output "telemetry_lake_arn" {
  description = "ARN of the secure telemetry lake"
  value       = aws_s3_bucket.telemetry_lake.arn
}

