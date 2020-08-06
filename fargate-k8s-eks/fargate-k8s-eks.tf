

provider "aws" {}

resource "aws_eks_fargate_profile" "example" {
  cluster_name           = aws_eks_cluster.example.name
  fargate_profile_name   = "example"
  pod_execution_role_arn = aws_iam_role.example.arn
  subnet_ids             = [aws_subnet.example1.id,aws_subnet.example2.id]

  selector {
    namespace = "example"
  }
}
