provider "aws" {}

locals {
  my_ip        = ["213.57.87.195/32","35.158.209.228/32","35.158.99.12/32"]
  subnet_cidr  = ["10.1.0.0/16"]
}


//get vpc infrastracture id 
data "aws_vpc" "infrastracture-vpc" {
  tags = {
    Name = "infrastracture-vpc"
  }
}



//get subnet id
data "aws_subnet_ids" "infrastracture-subnet" {
  vpc_id = "${data.aws_vpc.infrastracture-vpc.id}"
  tags = {
    Name = "infrastracture-subnet"
  }
}



 
  
  
  
// create a security group for ssh access to the linux systems
resource "aws_security_group" "infrastracture-kubernetes_manager-sg-ssh" {
  name        = "infrastracture-kubernetes_manager-sg-ssh"
  description = "Allow SSH inbound traffic"
  vpc_id      = "${data.aws_vpc.infrastracture-vpc.id}"
 
 
  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
  
 
  // allow access to the internet
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
 
  tags = {
    Name = "infrastracture-kubernetes_manager-sg-ssh"
  }
}


  
// create a security group for ssh access for local subnets
resource "aws_security_group" "infrastracture-kubernetes_manager-sg-ssh-local" {
  name        = "infrastracture-kubernetes_manager-sg-ssh-local"
  description = "Allow SSH inbound traffic"
  vpc_id      = "${data.aws_vpc.infrastracture-vpc.id}"
 
  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = local.subnet_cidr
  }
  
  
  tags = {
    Name = "infrastracture-kubernetes_manager-sg-ssh-local"
  }
}
  
  

  
 

  
// create  CentOS linux instances
resource "aws_instance" "i-centos-linux-kubernetes_manager_infrastracture" {
  ami                         = "ami-0f2b4fc905b0bd1f1"
  instance_type               = "t2.medium"
  key_name                    = "infrastracture_ssh_acess_key"
  vpc_security_group_ids      = [
                                 "${aws_security_group.infrastracture-kubernetes_manager-sg-ssh.id}",
                                 "${aws_security_group.infrastracture-kubernetes_manager-sg-ssh-local.id}"

                                ]
  count                       = "1"
  subnet_id                   = "${sort(data.aws_subnet_ids.infrastracture-subnet.ids)[0]}"
  associate_public_ip_address = "true"
 
  root_block_device { 
    volume_size           = "10"
    volume_type           = "gp2"
    delete_on_termination = "true"
  }
 
  tags = { 
    Name = "i-centos-linux-kubernetes_manager_infrastracture"
  }
}
 


  
  
  

  
  

  

data "template_file" "json_config" {
    count    = "1"
    template = <<EOF
{
    "ip": "${sort(aws_instance.i-centos-linux-kubernetes_manager_infrastracture.*.public_ip)[count.index]}"
}
EOF
}

resource "local_file" "environment1" {
    count    = "1"
    content = "${data.template_file.json_config.*.rendered[count.index]}"
    filename = "../terraform/modules_data/docker_compose_env_infrastracture_server_kubernetes_manager/json.info"
    file_permission = "0400"
}  
  
