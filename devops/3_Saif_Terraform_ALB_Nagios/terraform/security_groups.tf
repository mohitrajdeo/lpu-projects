# ALB Security Group (Public Ingress)
resource "aws_security_group" "alb_sg" {
  name        = "int333-alb-sg"
  description = "Allows public web traffic to ALB"
  vpc_id      = aws_vpc.multi_tier_vpc.id

  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

# Private Application Nodes Security Group
resource "aws_security_group" "app_sg" {
  name        = "int333-private-app-sg"
  description = "Allows HTTP strictly from ALB, NRPE strictly from Nagios"
  vpc_id      = aws_vpc.multi_tier_vpc.id

  ingress {
    description     = "HTTP from ALB"
    from_port       = 80
    to_port         = 80
    protocol        = "tcp"
    security_groups = [aws_security_group.alb_sg.id]
  }

  ingress {
    description     = "NRPE from Nagios"
    from_port       = 5666
    to_port         = 5666
    protocol        = "tcp"
    security_groups = [aws_security_group.nagios_sg.id]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

# Nagios Monitoring Server Security Group
resource "aws_security_group" "nagios_sg" {
  name        = "int333-saif-nagios-sg"
  description = "Nagios Dashboard access and outbound monitoring"
  vpc_id      = aws_vpc.multi_tier_vpc.id

  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

