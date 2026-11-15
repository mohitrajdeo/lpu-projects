# Compute Instances: Private Nodes & Nagios
resource "aws_instance" "app_node_1" {
  ami                    = var.ubuntu_ami_id
  instance_type          = var.instance_type
  subnet_id              = aws_subnet.private_1.id
  vpc_security_group_ids = [aws_security_group.app_sg.id]

  tags = { Name = "int333-app-node-1" }
}

resource "aws_instance" "app_node_2" {
  ami                    = var.ubuntu_ami_id
  instance_type          = var.instance_type
  subnet_id              = aws_subnet.private_2.id
  vpc_security_group_ids = [aws_security_group.app_sg.id]

  tags = { Name = "int333-app-node-2" }
}

resource "aws_instance" "nagios_server" {
  ami                         = var.ubuntu_ami_id
  instance_type               = var.instance_type
  subnet_id                   = aws_subnet.public_1.id
  vpc_security_group_ids      = [aws_security_group.nagios_sg.id]
  associate_public_ip_address = true

  tags = { Name = "int333-saif-nagios-server" }
}

