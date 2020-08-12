

provider "aws" {}




resource "aws_iam_role" "prof-example" {
  name = "eks-fargate-profile-example"

  assume_role_policy = jsonencode({
    Statement = [{
      Action = "sts:AssumeRole"
      Effect = "Allow"
      Principal = {
        Service = "eks-fargate-pods.amazonaws.com"
      }
    }]
    Version = "2012-10-17"
  })
}

resource "aws_iam_role_policy_attachment" "prof-example-AmazonEKSFargatePodExecutionRolePolicy" {
  policy_arn = "arn:aws:iam::aws:policy/AmazonEKSFargatePodExecutionRolePolicy"
  role       = aws_iam_role.prof-example.name
}




resource "aws_eks_fargate_profile" "example" {
  cluster_name           = aws_eks_cluster.example.name
  fargate_profile_name   = "example"
  pod_execution_role_arn = aws_iam_role.prof-example.arn
  subnet_ids             = [aws_subnet.example1.id,aws_subnet.example2.id]

  selector {
    namespace = "example"
  }

  selector {
    namespace = "kube-system"
  }
  
  selector {
    namespace = "default"
  }
}
