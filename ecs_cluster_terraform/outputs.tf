output "alb_dns_name" {
  description = "ALB DNS name (use in browser)"
  value       = aws_lb.alb.dns_name
}
