provider "aws" {
  version = ">= 2.28.1"
  region  = var.region
}

locals {
  cluster_name = "test-eks-${random_string.suffix.result}"
}

data "aws_availability_zones" "available" {
}
module "eks" {
  source = "cookpad/eks/aws"
  version = "~> 1.14"

  cluster_name       = "hal-9000"
  cidr_block         = "10.4.0.0/16"
  availability_zones = ["us-east-1a", "us-east-1b", "us-east-1c"]
}
