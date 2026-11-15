# EC2 Compute Provisioning: Nagios Core Observability Server
resource "aws_instance" "nagios_server" {
  ami                    = var.ubuntu_ami_id
  instance_type          = var.instance_type
  subnet_id              = aws_subnet.public_subnet_2.id
  vpc_security_group_ids = [aws_security_group.nagios_sg.id]
  key_name               = var.key_name

  user_data = templatefile("${path.module}/scripts/nagios_userdata.sh", {
    monitored_target_ip = aws_instance.web_portal.private_ip
  })

  root_block_device {
    volume_size           = 20
    volume_type           = "gp3"
    delete_on_termination = true
    tags = {
      Name = "int333-nagios-server-disk"
    }
  }

  tags = {
    Name = "int333-nagios-monitoring-server"
    Role = "Central Continuous Observability Daemon"
  }

  depends_on = [aws_instance.web_portal]
}

# Elastic IP for Nagios Monitoring Server
resource "aws_eip" "nagios_eip" {
  instance = aws_instance.nagios_server.id
  domain   = "vpc"

  tags = {
    Name = "int333-nagios-eip"
  }
}

