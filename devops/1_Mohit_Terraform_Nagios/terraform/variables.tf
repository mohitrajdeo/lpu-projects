variable "aws_region" {
  description = "AWS region for deployment (default Mumbai)"
  type        = string
  default     = "ap-south-1"
}

variable "environment" {
  description = "Environment identifier"
  type        = string
  default     = "production"
}

variable "vpc_cidr" {
  description = "CIDR block for the custom VPC"
  type        = string
  default     = "10.100.0.0/16"
}

variable "subnet_1_cidr" {
  description = "CIDR block for Public Subnet 1 (Web Portal)"
  type        = string
  default     = "10.100.1.0/24"
}

variable "subnet_2_cidr" {
  description = "CIDR block for Public Subnet 2 (Nagios Server)"
  type        = string
  default     = "10.100.2.0/24"
}

variable "instance_type" {
  description = "EC2 instance type (Free tier eligible)"
  type        = string
  default     = "t2.micro"
}

variable "ubuntu_ami_id" {
  description = "Ubuntu 24.04 LTS AMI ID in ap-south-1 (leave default for dynamic or override)"
  type        = string
  default     = "ami-0dee22c13ea7a9a67" # Ubuntu 24.04 LTS Mumbai AMI
}

variable "key_name" {
  description = "SSH key pair name for EC2 access"
  type        = string
  default     = "int333-devops-key"
}

variable "admin_cidr" {
  description = "Administrator CIDR permitted for SSH and Nagios Web Console"
  type        = string
  default     = "0.0.0.0/0"
}

