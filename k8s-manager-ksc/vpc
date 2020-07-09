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
