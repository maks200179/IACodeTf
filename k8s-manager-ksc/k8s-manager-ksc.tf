provider "aws" {
  region      =  var.region
 
}

locals {
  cluster_name = "test-eks-9chRfdVG"
  domain_name  = "xmaxfr.com"
  key_name = "kubernetes_test_ssh_acess_key"
}

resource "tls_private_key" "kubernetes_test_key" {
  algorithm = "RSA"
  rsa_bits  = 4096
}

resource "aws_key_pair" "generated_key" {
  key_name   = local.key_name
  public_key = "${tls_private_key.kubernetes_test_key.public_key_openssh}"
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
  name = module.my-cluster.cluster_id
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




module "eks-node-group-a" {
  source = "umotif-public/eks-node-group/aws"

  
  create_iam_role = false

  cluster_name                  = module.my-cluster.cluster_id
  node_role_arn                 = aws_iam_role.main.arn
  subnet_ids                    = [module.vpc.public_subnets[0]]
  

  desired_size = 1
  min_size     = 1
  max_size     = 2

  instance_types = ["t2.micro"]

  ec2_ssh_key = local.key_name

  kubernetes_labels = {
    lifecycle = "OnDemand"
    az        = data.aws_availability_zones.available.names[0]
  }

  tags = {
    Environment = "test"
  }
}    
  
  
  
module "eks-node-group-b" {
  source = "umotif-public/eks-node-group/aws"

  
  create_iam_role = false

  cluster_name                  = module.my-cluster.cluster_id
  node_role_arn                 = aws_iam_role.main.arn
  subnet_ids                    = [module.vpc.public_subnets[1]]
  

  desired_size = 1
  min_size     = 1
  max_size     = 2

  instance_types = ["t2.micro"]

  ec2_ssh_key = local.key_name

  kubernetes_labels = {
    lifecycle = "OnDemand"
    az        = data.aws_availability_zones.available.names[1]
  }

  tags = {
    Environment = "test"
  }
}      

  
  
  
module "eks-node-group-c" {
  source = "umotif-public/eks-node-group/aws"

 
  create_iam_role = false

  cluster_name                  = module.my-cluster.cluster_id
  node_role_arn                 = aws_iam_role.main.arn
  subnet_ids                    = [module.vpc.public_subnets[2]]
  

  desired_size = 1
  min_size     = 1
  max_size     = 2

  instance_types = ["t2.micro"]

  ec2_ssh_key = local.key_name

  kubernetes_labels = {
    lifecycle = "OnDemand"
    az        = data.aws_availability_zones.available.names[2]
  }

  tags = {
    Environment = "test"
  }
}        
