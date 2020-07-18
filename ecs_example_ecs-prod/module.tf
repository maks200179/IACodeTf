## This Template creates the infrastructure
## with bastion host
##

module "main-vpc" {
  source     = "../../modules/vpc"
  ENV        = "${var.ENV}"                    #productEnv
  AWS_REGION = "${var.AWS_REGION}"
  VPC_NAME   = "${var.VPC_NAME}"               #productID
  az1        = "${var.AWS_REGION}a"
  az2        = "${var.AWS_REGION}b"
}

module "bastion" {
  source         = "../../modules/bastion"
  ENV            = "${var.ENV}"
  AWS_REGION     = "${var.AWS_REGION}"
  VPC_NAME       = "${var.VPC_NAME}"                     #productID
  vpc_id         = "${module.main-vpc.vpc_id}"           #productVPC
  public_subnets = "${module.main-vpc.public_subnets-1}"
  keyname        = "bastion-key"                         #Key name
  pubkey         = "ssh-rsa xxxxxxxxxxxxxxxxxxxxxxx"     #public key
}
## This templates creates the Application Loadblancer and 
## setup the ECS Cluster
##

module "alb" {
  source               = "../../modules/loadblancer/application_loadblancer"
  ENV                  = "dev" # Product Environment
  VPC_NAME             = "fusion" # Product Name
  appname              = "ecs-demo" # Application Name
  vpc_id               = "${module.main-vpc.vpc_id}"
  public-subnet-1      = "${module.main-vpc.public_subnets-1}"
  public-subnet-2      = "${module.main-vpc.public_subnets-2}"
  certificate_arn      = "xxxxxxxxxxxxxxxxxxxxxxxx"
}

module "ecs" {
  source               = "../../modules/ecs"
  ENV                  = "prod" # Product Environment
  VPC_NAME             = "fusion" # Product Name
  vpc_id               = "${module.main-vpc.vpc_id}"
  public-subnet-1      = "${module.main-vpc.public_subnets-1}"
  public-subnet-2      = "${module.main-vpc.public_subnets-2}"
  appname              = "ecs-demo" # Application Name
  min_size             = "1" # default 1, Minimum no of Instance node (ASG)
  max_size             = "4" # default 4, Maximum no of Instance node (ASG)
  desired_capacity     = "2" # default 2, number of Amazon EC2 instances that should be running
  keyname              = "ecskey"# key Name
  pubkey               = "ssh-rsa xxxxxxxxxxxxxxxxxxxxxxxxxxxxx" # Public key
  instance_type        = "t2.micro" # default t2.micro
  iam_instance_profile = "${module.IAM.instance_profile}"
  applicationPort      = "80" # Application port no (for security group)
  iam_role             = "${module.IAM.iam_role}"
  target_group         = "${module.alb.tagetGroup}"
  container_name       = "demo-ecs-container" # Container Name
  container_port       = "80"
  ecs_task_family      = "nginx" # Task defination name
  container_definitions= "${file("container_definition.json")}"
  desired_count        = "2" # default 1
  launch_type          = "EC2" # valid values are EC2 and FARGATE, default is EC2
  iam_policy_name      = "ecs-policy"     #Policy Name
  iam_instance_profile = "ecs-profile"    # Instance profile Name
  iam_role             = "fusion-prod-ecs" # Role Name
}
