provider "aws" {
  region      =  var.region
 
}

locals {
  cluster_name = "test-eks-9chRfdVG"
  domain_name  = "xmaxfr.com"
}

resource "random_string" "suffix" {
  length  = 8
  special = false
}


resource "aws_security_group" "all_worker_mgmt" {
  name_prefix = "all_worker_management"
  vpc_id      = module.vpc.vpc_id

  ingress {
    from_port = 22
    to_port   = 22
    protocol  = "tcp"

    cidr_blocks = [
      "10.0.0.0/8",
      "172.16.0.0/12",
      "192.168.0.0/16",
    ]
  }
}

resource "aws_security_group" "worker_group_mgmt_one" {
  name_prefix = "worker_group_mgmt_one"
  vpc_id      = module.vpc.vpc_id

  ingress {
    from_port = 80
    to_port   = 80
    protocol  = "tcp"
    cidr_blocks = ["10.0.0.0/8"]
  }

  ingress {
    from_port = 22
    to_port   = 22
    protocol  = "tcp"
    cidr_blocks = ["10.0.0.0/8"]
  }
}

  

  
resource "aws_security_group" "worker_group_mgmt_two" {
  name_prefix = "worker_group_mgmt_two"
  vpc_id      = module.vpc.vpc_id

  ingress {
    from_port = 80
    to_port   = 80
    protocol  = "tcp"

    cidr_blocks = ["192.168.0.0/16"]
  }
  
    
  ingress {
    from_port = 22
    to_port   = 22
    protocol  = "tcp"

    cidr_blocks = ["192.168.0.0/16"]
  }
}




data "aws_eks_cluster" "cluster" {
  enabled_cluster_log_types = []
  name                      = module.my-cluster.cluster_id
  role_arn                  = aws_iam_role.cluster.arn
  
  vpc_config {
    subnet_ids              = flatten([module.vpc.public_subnets, module.vpc.private_subnets])
    security_group_ids      = [aws_security_group.all_worker_mgmt.id]
    endpoint_private_access = "true"
    endpoint_public_access  = "true"
  }
}

  
data "aws_eks_cluster_auth" "cluster" {
  name = module.my-cluster.cluster_id
}  

data "aws_availability_zones" "available" {
}


  
  
provider "kubernetes" {
  host                   = data.aws_eks_cluster.cluster.endpoint
  cluster_ca_certificate = base64decode(data.aws_eks_cluster.cluster.certificate_authority.0.data)
  token                  = data.aws_eks_cluster_auth.cluster.token
  load_config_file       = false
  version                = "~> 1.9"
  
}

  
    
  
module "vpc" {
  source  = "terraform-aws-modules/vpc/aws"
  version = "2.6.0"

  name                 = "test-vpc"
  cidr                 = "10.0.0.0/16"
  azs                  = data.aws_availability_zones.available.names
  private_subnets      = ["10.0.1.0/24", "10.0.2.0/24", "10.0.3.0/24"]
  public_subnets       = ["10.0.4.0/24", "10.0.5.0/24", "10.0.6.0/24"]
  enable_nat_gateway   = true
  single_nat_gateway   = true
  enable_dns_hostnames = true

  public_subnet_tags = {
    "kubernetes.io/cluster/${local.cluster_name}" = "shared"
    "kubernetes.io/role/elb"                      = "1"
  }

  private_subnet_tags = {
    "kubernetes.io/cluster/${local.cluster_name}" = "shared"
    "kubernetes.io/role/internal-elb"             = "1"
  }
}
  
  


### OIDC config
resource "aws_iam_openid_connect_provider" "cluster" {
  client_id_list  = ["sts.amazonaws.com"]
  thumbprint_list = ["9E99A48A9960B14926BB7F3B02E22DA2B0AB7280"]
  url             = data.aws_eks_cluster.cluster.identity.0.oidc.0.issuer
}


    
    
    
#####
# EKS Cluster
#####

module "my-cluster" {
  source          = "terraform-aws-modules/eks/aws"
  cluster_name    = local.cluster_name
  cluster_version = "1.17"
  subnets         = module.vpc.public_subnets
  vpc_id          = module.vpc.vpc_id



  
  worker_additional_security_group_ids = [aws_security_group.all_worker_mgmt.id]
  map_roles                            = var.map_roles
  map_users                            = var.map_users
  map_accounts                         = var.map_accounts
}    


resource "aws_iam_role" "cluster" {
  name = "eks-cluster-role"

  assume_role_policy = <<POLICY
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Service": "eks.amazonaws.com"
      },
      "Action": "sts:AssumeRole"
    }
  ]
}
POLICY
}

resource "aws_iam_role_policy_attachment" "cluster_AmazonEKSClusterPolicy" {
  policy_arn = "arn:aws:iam::aws:policy/AmazonEKSClusterPolicy"
  role       = aws_iam_role.cluster.name
}

resource "aws_iam_role_policy_attachment" "cluster_AmazonEKSServicePolicy" {
  policy_arn = "arn:aws:iam::aws:policy/AmazonEKSServicePolicy"
  role       = aws_iam_role.cluster.name
}

#####
# EKS Node Group per availability zone
# If you are running a stateful application across multiple Availability Zones that is backed by Amazon EBS volumes and using the Kubernetes Cluster Autoscaler,
# you should configure multiple node groups, each scoped to a single Availability Zone. In addition, you should enable the --balance-similar-node-groups feature.
#
# In this setup you can configure a single IAM Role that is attached to multiple node groups.
#####

resource "aws_iam_role" "main" {
  name = "eks-managed-group-node-role"

  assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": "sts:AssumeRole",
      "Principal": {
        "Service": "ec2.amazonaws.com"
      },
      "Effect": "Allow"
    }
  ]
}
EOF
}

resource "aws_iam_role_policy_attachment" "main_AmazonEKSWorkerNodePolicy" {
  policy_arn = "arn:aws:iam::aws:policy/AmazonEKSWorkerNodePolicy"
  role       = aws_iam_role.main.name
}

resource "aws_iam_role_policy_attachment" "main_AmazonEKS_CNI_Policy" {
  policy_arn = "arn:aws:iam::aws:policy/AmazonEKS_CNI_Policy"
  role       = aws_iam_role.main.name
}

resource "aws_iam_role_policy_attachment" "main_AmazonEC2ContainerRegistryReadOnly" {
  policy_arn = "arn:aws:iam::aws:policy/AmazonEC2ContainerRegistryReadOnly"
  role       = aws_iam_role.main.name
}

module "eks-node-group-a" {
  source = "umotif-public/eks-node-group/aws"

  enabled         = true
  create_iam_role = false

  cluster_name  = module.my-cluster.name
  node_role_arn = aws_iam_role.main.arn
  subnet_ids    = [module.vpc.public_subnets]

  desired_size = 2
  min_size     = 2
  max_size     = 2

  instance_types = ["t2.micro"]

  ec2_ssh_key = "eks-test"

  kubernetes_labels = {
    lifecycle = "OnDemand"
    az        = data.aws_availability_zones.available.names
  }

  tags = {
    Environment = "test"
  }
}    
