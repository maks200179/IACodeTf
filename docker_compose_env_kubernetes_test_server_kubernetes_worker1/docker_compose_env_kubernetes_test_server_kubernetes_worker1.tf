provider "aws" {}

locals {
  my_ip        = ["213.57.87.195/32","35.158.209.228/32","35.158.99.12/32"]
  subnet_cidr  = ["10.0.0.0/16"]
}


//get vpc kubernetes_test id 
data "aws_vpc" "kubernetes_test-vpc" {
  tags = {
    Name = "kubernetes_test-vpc"
  }
}



//get subnet id
data "aws_subnet_ids" "kubernetes_test-subnet" {
  vpc_id = "${data.aws_vpc.kubernetes_test-vpc.id}"
  tags = {
    Name = "kubernetes_test-subnet"
  }
}



 
  
  
  
// create a security group for ssh access to the linux systems
resource "aws_security_group" "kubernetes_test-kubernetes_worker1-sg-ssh" {
  name        = "kubernetes_test-kubernetes_worker1-sg-ssh"
  description = "Allow SSH inbound traffic"
  vpc_id      = "${data.aws_vpc.kubernetes_test-vpc.id}"
 
 
  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = local.my_ip
  }
  
  ingress {
    from_port   = 80
    to_port     = 80
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
    Name = "kubernetes_test-kubernetes_worker1-sg-ssh"
  }
}


  
// create a security group for ssh access on local subnets
resource "aws_security_group" "kubernetes_test-kubernetes_worker1-sg-ssh-local" {
  name        = "kubernetes_test-kubernetes_worker1-sg-ssh-local"
  description = "Allow SSH inbound traffic"
  vpc_id      = "${data.aws_vpc.kubernetes_test-vpc.id}"
 
  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = local.subnet_cidr
  }
 

 
  tags = {
    Name = "kubernetes_test-kubernetes_worker1-sg-ssh-local"
  }
}
  
  

  

 

  
  
  

  
  
  
  
 
  
  
// create a security group for docker kubernetes registry 
resource "aws_security_group" "kubernetes_test-kubernetes_worker1-sg-kubernetes-4789" {
  name        = "kubernetes_test-kubernetes_worker1-sg-kubernetes-4789"
  description = "Allow kubernetes-4789 inbound traffic"
  vpc_id      = "${data.aws_vpc.kubernetes_test-vpc.id}"
 
  ingress {
    from_port   = 10250
    to_port     = 10250
    protocol    = "tcp"
    cidr_blocks = local.subnet_cidr
  }


  ingress {
    from_port   = 30000
    to_port     = 32767
    protocol    = "tcp"
    cidr_blocks = local.subnet_cidr
  }
 
 
  tags = {
    Name = "kubernetes_test-kubernetes_worker1-sg-kubernetes-4789"
  }
}    

  
// create  CentOS linux instances
resource "aws_instance" "i-centos-linux-kubernetes_worker1_kubernetes_test" {
  ami                         = "ami-0f2b4fc905b0bd1f1"
  instance_type               = "t2.medium"
  key_name                    = "kubernetes_test_ssh_acess_key"
  vpc_security_group_ids      = [
                                 "${aws_security_group.kubernetes_test-kubernetes_worker1-sg-ssh.id}",
                                 "${aws_security_group.kubernetes_test-kubernetes_worker1-sg-ssh-local.id}",
                                 "${aws_security_group.kubernetes_test-kubernetes_worker1-sg-kubernetes-4789.id}"
                                ]
  count                       = "1"
  subnet_id                   = "${sort(data.aws_subnet_ids.kubernetes_test-subnet.ids)[0]}"
  associate_public_ip_address = "true"
 
  root_block_device { 
    volume_size           = "10"
    volume_type           = "gp2"
    delete_on_termination = "true"
  }
 
  tags = { 
    Name = "i-centos-linux-kubernetes_worker1_kubernetes_test"
  }
}
 


  
  
  

  
  

  

data "template_file" "json_config" {
    count    = "1"
    template = <<EOF
{
    "ip": "${sort(aws_instance.i-centos-linux-kubernetes_worker1_kubernetes_test.*.public_ip)[count.index]}"
}
EOF
}

resource "local_file" "environment1" {
    count    = "1"
    content = "${data.template_file.json_config.*.rendered[count.index]}"
    filename = "../terraform/modules_data/docker_compose_env_kubernetes_test_server_kubernetes_worker1/json.info"
    file_permission = "0400"
}  
  
