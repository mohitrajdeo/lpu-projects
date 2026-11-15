output "vpc_id" {
  description = "The ID of the custom VPC"
  value       = aws_vpc.devops_vpc.id
}

output "web_portal_public_ip" {
  description = "Public Elastic IP of Developer Web Portal"
  value       = aws_eip.web_portal_eip.public_ip
}

output "web_portal_url" {
  description = "Public URL to access the Developer Web Portal"
  value       = "http://${aws_eip.web_portal_eip.public_ip}"
}

output "code_execution_endpoint" {
  description = "Code execution service endpoint (via Nginx proxy)"
  value       = "http://${aws_eip.web_portal_eip.public_ip}/api/execute"
}

output "nagios_public_ip" {
  description = "Public Elastic IP of Nagios Continuous Monitoring Server"
  value       = aws_eip.nagios_eip.public_ip
}

output "nagios_web_console_url" {
  description = "Authenticated URL for Nagios Core Web Management Dashboard"
  value       = "http://${aws_eip.nagios_eip.public_ip}/nagios"
}

output "nagios_credentials" {
  description = "Default credentials for Nagios Core web console"
  value       = "Username: nagiosadmin | Password: int333devopspassword"
}

