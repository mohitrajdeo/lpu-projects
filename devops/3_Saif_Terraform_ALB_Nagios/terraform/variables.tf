variable "aws_region" { default = "ap-south-1" }
variable "vpc_cidr" { default = "10.200.0.0/16" }
variable "public_subnet_1_cidr" { default = "10.200.1.0/24" }
variable "public_subnet_2_cidr" { default = "10.200.2.0/24" }
variable "private_subnet_1_cidr" { default = "10.200.10.0/24" }
variable "private_subnet_2_cidr" { default = "10.200.20.0/24" }
variable "instance_type" { default = "t2.micro" }
variable "ubuntu_ami_id" { default = "ami-0dee22c13ea7a9a67" }

