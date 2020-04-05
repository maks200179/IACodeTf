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
resource "aws_security_group" "kubernetes_test-kubernetes_manager-sg-ssh" {
  name        = "kubernetes_test-kubernetes_manager-sg-ssh"
  description = "Allow SSH inbound traffic"
  vpc_id      = "${data.aws_vpc.kubernetes_test-vpc.id}"
 
 
  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = local.my_ip
  }
  
  ingress {
    from_port   = 6443
    to_port     = 6443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
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
    Name = "kubernetes_test-kubernetes_manager-sg-ssh"
  }
}


  
// create a security group for ssh access for local subnets
resource "aws_security_group" "kubernetes_test-kubernetes_manager-sg-ssh-local" {
  name        = "kubernetes_test-kubernetes_manager-sg-ssh-local"
  description = "Allow SSH inbound traffic"
  vpc_id      = "${data.aws_vpc.kubernetes_test-vpc.id}"
 
  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = local.subnet_cidr
  }
  
  ingress {
    from_port   = 959
    to_port     = 959
    protocol    = "udp"
    cidr_blocks = local.subnet_cidr
  } 
  
  ingress {
    from_port   = 68
    to_port     = 68
    protocol    = "udp"
    cidr_blocks = local.subnet_cidr
  } 
  
  ingress {
    from_port   = 111
    to_port     = 111
    protocol    = "udp"
    cidr_blocks = local.subnet_cidr
  } 
  
  ingress {
    from_port   = 8472
    to_port     = 8472
    protocol    = "udp"
    cidr_blocks = local.subnet_cidr
  } 
  
  ingress {
    from_port   = 323
    to_port     = 323
    protocol    = "udp"
    cidr_blocks = local.subnet_cidr
  } 
  
  tags = {
    Name = "kubernetes_test-kubernetes_manager-sg-ssh-local"
  }
}
  
  
// create a security group for docker kubernetes access 
resource "aws_security_group" "kubernetes_test-kubernetes_manager-sg-kubernetes" {
  name        = "kubernetes_test-kubernetes_manager-sg-kubernetes"
  description = "Allow kubernetes inbound traffic"
  vpc_id      = "${data.aws_vpc.kubernetes_test-vpc.id}"
 
  ingress {
    from_port   = 6443
    to_port     = 6443
    protocol    = "tcp"
    cidr_blocks = local.subnet_cidr
  }
  
  ingress {
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = local.subnet_cidr
  }

 
  tags = {
    Name = "kubernetes_test-kubernetes_manager-sg-kubernetes"
  }
} 
  

// create a security group for docker kubernetes registry 
resource "aws_security_group" "kubernetes_test-kubernetes_manager-sg-kubernetes-registry" {
  name        = "kubernetes_test-kubernetes_manager-sg-sg-kubernetes-registry"
  description = "Allow kubernetes-registry inbound traffic"
  vpc_id      = "${data.aws_vpc.kubernetes_test-vpc.id}"
 
  ingress {
    from_port   = 2379
    to_port     = 2379
    protocol    = "tcp"
    cidr_blocks = local.subnet_cidr
  }
  
  ingress {
    from_port   = 2376
    to_port     = 2376
    protocol    = "tcp"
    cidr_blocks = local.subnet_cidr
  }
  
  ingress {
    from_port   = 8472
    to_port     = 8472
    protocol    = "tcp"
    cidr_blocks = local.subnet_cidr
  }
  
  ingress {
    from_port   = 9135
    to_port     = 9135
    protocol    = "tcp"
    cidr_blocks = local.subnet_cidr
  }
 
  tags = {
    Name = "kubernetes_test-kubernetes_manager-sg-kubernetes-registry"
  }
}   

  
  
  
// create a security group for docker kubernetes registry 
resource "aws_security_group" "kubernetes_test-kubernetes_manager-sg-kubernetes-2376" {
  name        = "kubernetes_test-kubernetes_manager-sg-kubernetes-2376"
  description = "Allow kubernetes-2376 inbound traffic"
  vpc_id      = "${data.aws_vpc.kubernetes_test-vpc.id}"
 
  ingress {
    from_port   = 2380
    to_port     = 2380
    protocol    = "tcp"
    cidr_blocks = local.subnet_cidr
  }
 
  ingress {
    from_port   = 2381
    to_port     = 2381
    protocol    = "tcp"
    cidr_blocks = local.subnet_cidr
  }
  
  ingress {
    from_port   = 8472
    to_port     = 8472
    protocol    = "udp"
    cidr_blocks = local.subnet_cidr
  }
 
  ingress {
    from_port   = 8285
    to_port     = 8285
    protocol    = "udp"
    cidr_blocks = local.subnet_cidr
  }
  
  tags = {
    Name = "kubernetes_test-kubernetes_manager-sg-kubernetes-2376"
  }
}  
  
  
  
  
// create a security group for docker kubernetes registry 
resource "aws_security_group" "kubernetes_test-kubernetes_manager-sg-kubernetes-7946" {
  name        = "kubernetes_test-kubernetes_manager-sg-kubernetes-7946"
  description = "Allow kubernetes-7946 inbound traffic"
  vpc_id      = "${data.aws_vpc.kubernetes_test-vpc.id}"
 
  ingress {
    from_port   = 10250
    to_port     = 10250
    protocol    = "tcp"
    cidr_blocks = local.subnet_cidr
  }
 
 
  tags = {
    Name = "kubernetes_test-kubernetes_manager-sg-kubernetes-7946"
  }
}  
  
  
// create a security group for docker kubernetes registry 
resource "aws_security_group" "kubernetes_test-kubernetes_manager-sg-kubernetes-4789" {
  name        = "kubernetes_test-kubernetes_manager-sg-kubernetes-4789"
  description = "Allow kubernetes-4789 inbound traffic"
  vpc_id      = "${data.aws_vpc.kubernetes_test-vpc.id}"
 
  ingress {
    from_port   = 10251
    to_port     = 10251
    protocol    = "tcp"
    cidr_blocks = local.subnet_cidr
  }
  ingress {
    from_port   = 10252
    to_port     = 10252
    protocol    = "tcp"
    cidr_blocks = local.subnet_cidr
  }
  ingress {
    from_port   = 10255
    to_port     = 10255
    protocol    = "tcp"
    cidr_blocks = local.subnet_cidr
  }
 
 
  tags = {
    Name = "kubernetes_test-kubernetes_manager-sg-kubernetes-4789"
  }
}    

  
// create  CentOS linux instances
resource "aws_instance" "i-centos-linux-kubernetes_manager_kubernetes_test" {
  ami                         = "ami-0f2b4fc905b0bd1f1"
  instance_type               = "t2.medium"
  key_name                    = "kubernetes_test_ssh_acess_key"
  vpc_security_group_ids      = [
                                 "${aws_security_group.kubernetes_test-kubernetes_manager-sg-ssh.id}",
                                 "${aws_security_group.kubernetes_test-kubernetes_manager-sg-ssh-local.id}",
                                 "${aws_security_group.kubernetes_test-kubernetes_manager-sg-kubernetes.id}",
                                 "${aws_security_group.kubernetes_test-kubernetes_manager-sg-kubernetes-registry.id}",
                                 "${aws_security_group.kubernetes_test-kubernetes_manager-sg-kubernetes-2376.id}",
                                 "${aws_security_group.kubernetes_test-kubernetes_manager-sg-kubernetes-7946.id}",
                                 "${aws_security_group.kubernetes_test-kubernetes_manager-sg-kubernetes-4789.id}"
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
    Name = "i-centos-linux-kubernetes_manager_kubernetes_test"
  }
}
 


  
  
  

  
  

  

data "template_file" "json_config" {
    count    = "1"
    template = <<EOF
{
    "ip": "${sort(aws_instance.i-centos-linux-kubernetes_manager_kubernetes_test.*.public_ip)[count.index]}"
}
EOF
}

resource "local_file" "environment1" {
    count    = "1"
    content = "${data.template_file.json_config.*.rendered[count.index]}"
    filename = "../terraform/modules_data/docker_compose_env_kubernetes_test_server_kubernetes_manager/json.info"
    file_permission = "0400"
}  
  
