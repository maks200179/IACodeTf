output "alb_dns_name" {
  description = "Public DNS name of the ALB"
  value       = aws_lb.alb.dns_name
}

output "ecs_cluster_name" {
  description = "Name of the ECS cluster"
  value       = aws_ecs_cluster.this.name
}

output "service_name" {
  description = "Name of the ECS service"
  value       = aws_ecs_service.app.name
}