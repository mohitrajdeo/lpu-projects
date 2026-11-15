# Multi-Tier AWS VPC for Saif Siddique (12308813)
resource "aws_vpc" "multi_tier_vpc" {
  cidr_block           = var.vpc_cidr
  enable_dns_hostnames = true
  enable_dns_support   = true

  tags = {
    Name  = "int333-saif-vpc"
    Owner = "Saif Siddique (12308813)"
  }
}

resource "aws_internet_gateway" "igw" {
  vpc_id = aws_vpc.multi_tier_vpc.id
  tags   = { Name = "int333-saif-igw" }
}

# Public Subnets (ALB Ingress)
resource "aws_subnet" "public_1" {
  vpc_id                  = aws_vpc.multi_tier_vpc.id
  cidr_block              = var.public_subnet_1_cidr
  availability_zone       = "${var.aws_region}a"
  map_public_ip_on_launch = true
  tags                    = { Name = "int333-public-subnet-1" }
}

resource "aws_subnet" "public_2" {
  vpc_id                  = aws_vpc.multi_tier_vpc.id
  cidr_block              = var.public_subnet_2_cidr
  availability_zone       = "${var.aws_region}b"
  map_public_ip_on_launch = true
  tags                    = { Name = "int333-public-subnet-2" }
}

# Private Subnets (Isolated Compute)
resource "aws_subnet" "private_1" {
  vpc_id            = aws_vpc.multi_tier_vpc.id
  cidr_block        = var.private_subnet_1_cidr
  availability_zone = "${var.aws_region}a"
  tags              = { Name = "int333-private-subnet-1" }
}

resource "aws_subnet" "private_2" {
  vpc_id            = aws_vpc.multi_tier_vpc.id
  cidr_block        = var.private_subnet_2_cidr
  availability_zone = "${var.aws_region}b"
  tags              = { Name = "int333-private-subnet-2" }
}

# Public Route Table
resource "aws_route_table" "public_rt" {
  vpc_id = aws_vpc.multi_tier_vpc.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.igw.id
  }

  tags = { Name = "int333-public-rt" }
}

resource "aws_route_table_association" "pub1" {
  subnet_id      = aws_subnet.public_1.id
  route_table_id = aws_route_table.public_rt.id
}

resource "aws_route_table_association" "pub2" {
  subnet_id      = aws_subnet.public_2.id
  route_table_id = aws_route_table.public_rt.id
}

