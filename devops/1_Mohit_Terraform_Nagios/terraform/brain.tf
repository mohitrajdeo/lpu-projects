# EC2 Compute Provisioning: Developer Web Portal & Backend Code Execution Node
resource "aws_instance" "web_portal" {
  ami                    = var.ubuntu_ami_id
  instance_type          = var.instance_type
  subnet_id              = aws_subnet.public_subnet_1.id
  vpc_security_group_ids = [aws_security_group.web_sg.id]
  key_name               = var.key_name

  user_data = file("${path.module}/scripts/web_portal_userdata.sh")

  root_block_device {
    volume_size           = 20
    volume_type           = "gp3"
    delete_on_termination = true
    tags = {
      Name = "int333-web-portal-disk"
    }
  }

  tags = {
    Name = "int333-web-portal-server"
    Role = "Application Tier & Code Execution Engine"
  }
}

# Elastic IP for Web Portal Server
resource "aws_eip" "web_portal_eip" {
  instance = aws_instance.web_portal.id
  domain   = "vpc"

  tags = {
    Name = "int333-web-portal-eip"
  }
}

