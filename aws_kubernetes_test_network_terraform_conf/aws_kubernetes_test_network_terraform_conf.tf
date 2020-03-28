
provider "aws" {}


locals {
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



resource "local_file" "kubernetes_test_key_pem" {
    content     = tls_private_key.kubernetes_test_key.private_key_pem
    filename = "../terraform/modules_data/aws_kubernetes_test_network_terraform_conf/kubernetes_test_ssh_key.pem"
    file_permission = "0400"
}




// create the virtual private network
resource "aws_vpc" "kubernetes_test-vpc" {
  cidr_block = "10.0.0.0/16"
  enable_dns_hostnames = true
  enable_dns_support = true
 
  tags = {
    Name = "kubernetes_test-vpc"
  }
}


// create the internet gateway
resource "aws_internet_gateway" "kubernetes_test-igw" {
  vpc_id = "${aws_vpc.kubernetes_test-vpc.id}"
 
  tags = {
    Name = "kubernetes_test-igw"
  }
}


// create a dedicated subnet
resource "aws_subnet" "kubernetes_test-subnet" {
  vpc_id            = "${aws_vpc.kubernetes_test-vpc.id}"
  cidr_block        = "10.0.1.0/24"
  availability_zone = "us-east-2a"
 
  tags = {
    Name = "kubernetes_test-subnet"
  }
}



// create routing table which points to the internet gateway
resource "aws_route_table" "kubernetes_test-route" {
  vpc_id = "${aws_vpc.kubernetes_test-vpc.id}"
 
  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = "${aws_internet_gateway.kubernetes_test-igw.id}"
  }
 
  tags = {
    Name = "kubernetes_test-igw"
  }
}


// associate the routing table with the subnet
resource "aws_route_table_association" "subnet-association" {
  subnet_id      = "${aws_subnet.kubernetes_test-subnet.id}"
  route_table_id = "${aws_route_table.kubernetes_test-route.id}"
}


#module data
data "template_file" "json_config" {
    
    template = <<EOF
{
    "stage"             : "kubernetes_test",
    "module_name"       : "aws_kubernetes_test_network_terraform_conf",
    "network_module"    : "True"
}
EOF
}

resource "local_file" "module_info" {
    
    content = "${data.template_file.json_config.rendered}"
    filename = "../terraform/modules_data/aws_kubernetes_test_network_terraform_conf/json.info"
    file_permission = "0400"
}  

