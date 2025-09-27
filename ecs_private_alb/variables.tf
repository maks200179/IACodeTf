variable "region" {
  description = "AWS region to deploy to"
  type        = string
  default     = "us-east-1"
}

variable "vpc_cidr" {
  description = "CIDR block for the VPC"
  type        = string
  default     = "10.0.0.0/16"
}

variable "enable_https" {
  description = "Enable HTTPS listener on ALB. Set true only after you have a valid ACM certificate ARN."
  type        = bool
  default     = true
}

variable "acm_certificate_arn" {
  description = "Existing ACM certificate ARN in the same region as the ALB. Required when enable_https = true."
  type        = string
  default     = ""
}

variable "service_desired_count" {
  description = "Number of desired tasks"
  type        = number
  default     = 1
}

variable "container_image" {
  description = "Container image to run"
  type        = string
  default     = "nginx:stable"
}

variable "container_port" {
  description = "Container port to expose"
  type        = number
  default     = 80
}
