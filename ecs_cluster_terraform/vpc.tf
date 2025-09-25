resource "aws_vpc" "this" {
  cidr_block = var.vpc_cidr
  tags = { Name = "demo-vpc" }
}

resource "aws_internet_gateway" "gw" {
  vpc_id = aws_vpc.this.id
  tags   = { Name = "demo-igw" }
}

resource "aws_subnet" "public" {
  count                   = length(var.public_subnets)
  vpc_id                  = aws_vpc.this.id
  cidr_block              = var.public_subnets[count.index]
  map_public_ip_on_launch = true
  availability_zone       = data.aws_availability_zones.available.names[count.index]
  tags = { Name = "demo-public-${count.index}" }
}

data "aws_availability_zones" "available" {
  state = "available"
}
