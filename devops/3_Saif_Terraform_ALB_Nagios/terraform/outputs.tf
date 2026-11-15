output "alb_dns_name" {
  description = "Public DNS name of the Application Load Balancer"
  value       = aws_lb.external_alb.dns_name
}

output "nagios_public_ip" {
  description = "Public IP of Nagios monitoring server"
  value       = aws_instance.nagios_server.public_ip
}

