# Security Group for Nagios Observability Server
resource "aws_security_group" "nagios_sg" {
  name        = "int333-nagios-sg"
  description = "Security rules for central Nagios Core monitoring server"
  vpc_id      = aws_vpc.devops_vpc.id

  # Apache CGI Dashboard Access
  ingress {
    description = "Nagios Web Console Ingress"
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = [var.admin_cidr]
  }

  # SSH Management
  ingress {
    description = "SSH Admin Access"
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = [var.admin_cidr]
  }

  # Outbound Probing & Updates
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "int333-nagios-security-group"
  }
}

# Security Group for Web Portal and Code Execution Server
resource "aws_security_group" "web_sg" {
  name        = "int333-web-portal-sg"
  description = "Security boundaries for Developer Portal and Backend Code Runner"
  vpc_id      = aws_vpc.devops_vpc.id

  # Public Web Ingress
  ingress {
    description = "HTTP Public Ingress"
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    description = "HTTPS Public Ingress"
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  # Deep Observability: Port 9010 restricted strictly to Nagios Security Group
  ingress {
    description     = "Backend Code Execution Service Probing from Nagios"
    from_port       = 9010
    to_port         = 9010
    protocol        = "tcp"
    security_groups = [aws_security_group.nagios_sg.id]
  }

  # ICMP Echo Ping for Latency Check from Nagios
  ingress {
    description     = "ICMP Echo Probing from Nagios"
    from_port       = -1
    to_port         = -1
    protocol        = "icmp"
    security_groups = [aws_security_group.nagios_sg.id]
  }

  # SSH Management
  ingress {
    description = "SSH Admin Access"
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = [var.admin_cidr]
  }

  # Outbound Access for Package Repositories
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "int333-web-portal-security-group"
  }
}

