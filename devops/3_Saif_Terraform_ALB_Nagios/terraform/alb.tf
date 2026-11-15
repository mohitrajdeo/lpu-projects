# Application Load Balancer Manifest
resource "aws_lb" "external_alb" {
  name               = "int333-saif-alb"
  internal           = false
  load_balancer_type = "application"
  security_groups    = [aws_security_group.alb_sg.id]
  subnets            = [aws_subnet.public_1.id, aws_subnet.public_2.id]

  tags = { Name = "int333-external-alb" }
}

resource "aws_lb_target_group" "app_tg" {
  name     = "int333-app-target-group"
  port     = 80
  protocol = "HTTP"
  vpc_id   = aws_vpc.multi_tier_vpc.id

  health_check {
    path                = "/health"
    healthy_threshold   = 2
    unhealthy_threshold = 3
    timeout             = 3
    interval            = 15
  }
}

resource "aws_lb_listener" "http" {
  load_balancer_arn = aws_lb.external_alb.arn
  port              = 80
  protocol          = "HTTP"

  default_action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.app_tg.arn
  }
}

# Attach App Nodes to Target Group
resource "aws_lb_target_group_attachment" "node1" {
  target_group_arn = aws_lb_target_group.app_tg.arn
  target_id        = aws_instance.app_node_1.id
  port             = 80
}

resource "aws_lb_target_group_attachment" "node2" {
  target_group_arn = aws_lb_target_group.app_tg.arn
  target_id        = aws_instance.app_node_2.id
  port             = 80
}

