# AWS WAFv2 Security Automation & Layer 7 Defense v2.0
# Author: Saif Siddique (12308813 | Roll: 44)

resource "aws_wafv2_web_acl" "alb_security_guard" {
  name        = "saif-alb-wafv2-production"
  description = "Enterprise WAFv2 with AWS Managed Core Rule Set and Layer-7 Rate Limiter"
  scope       = "REGIONAL"

  default_action {
    allow {}
  }

  visibility_config {
    cloudwatch_metrics_enabled = true
    metric_name                = "SaifAlbWafMetric"
    sampled_requests_enabled   = true
  }

  # Rule 1: AWS Managed Common Rule Set (CRS)
  rule {
    name     = "AWSManagedRulesCommonRuleSet"
    priority = 1

    override_action {
      none {}
    }

    statement {
      managed_rule_group_statement {
        name        = "AWSManagedRulesCommonRuleSet"
        vendor_name = "AWS"
      }
    }

    visibility_config {
      cloudwatch_metrics_enabled = true
      metric_name                = "AWSManagedRulesCommonRuleSetMetric"
      sampled_requests_enabled   = true
    }
  }

  # Rule 2: SQL Injection Rule Set
  rule {
    name     = "AWSManagedRulesSQLiRuleSet"
    priority = 2

    override_action {
      none {}
    }

    statement {
      managed_rule_group_statement {
        name        = "AWSManagedRulesSQLiRuleSet"
        vendor_name = "AWS"
      }
    }

    visibility_config {
      cloudwatch_metrics_enabled = true
      metric_name                = "AWSManagedRulesSQLiRuleSetMetric"
      sampled_requests_enabled   = true
    }
  }

  # Rule 3: IP Rate Limiting (Block more than 500 requests per 5 minutes per IP)
  rule {
    name     = "RateLimitPerIp"
    priority = 3

    action {
      block {}
    }

    statement {
      rate_based_statement {
        limit              = 500
        aggregate_key_type = "IP"
      }
    }

    visibility_config {
      cloudwatch_metrics_enabled = true
      metric_name                = "RateLimitPerIpMetric"
      sampled_requests_enabled   = true
    }
  }
}

