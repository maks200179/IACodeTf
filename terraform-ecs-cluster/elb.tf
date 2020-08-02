## ALB

resource "aws_alb" "frankly_internal_alb" {
    name = "frankly-internal-alb"
    internal = false
    security_groups = ["${aws_security_group.frankly_internal_alb_sg.id}"]
    subnets = ["${aws_subnet.frankly_public_subnet_a.id}", "${aws_subnet.frankly_public_subnet_b.id}"]
}

resource "aws_alb_listener" "frankly_alb_listener" {
    load_balancer_arn = "${aws_alb.frankly_internal_alb.arn}"

    port = "8080"
    protocol = "HTTP"

    default_action {
        target_group_arn = "${aws_alb_target_group.frankly_internal_target_group.arn}"
        type = "forward"
    }
}

## Target Group

resource "aws_alb_target_group" "frankly_internal_target_group" {
    name = "internal-target-group"
    port = 8080
    protocol = "HTTP"
    vpc_id = "${aws_vpc.frankly_vpc.id}"

    health_check {
        healthy_threshold = 5
        unhealthy_threshold = 2
        timeout = 5
    }
}

## IAM

resource "aws_iam_role" "frankly_ec2_role" {
  name               = "franklyec2role"
  assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": "sts:AssumeRole",
      "Principal": {
        "Service": "ec2.amazonaws.com"
      },
      "Effect": "Allow",
      "Sid": ""
    }
  ]
}
EOF
}

resource "aws_iam_role" "frankly_ecs_role" {
  name = "frankly_ecs_role"

  assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": "sts:AssumeRole",
      "Principal": {
        "Service": "ecs.amazonaws.com"
      },
      "Effect": "Allow",
      "Sid": ""
    }
  ]
}
EOF
}

# aggresively add permissions...
resource "aws_iam_policy" "frankly_ecs_policy" {
  name        = "frankly_ecs_policy"
  description = "A test policy"

  policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": [
        "ec2:*",
        "ecs:*",
        "ecr:*",
        "autoscaling:*",
        "elasticloadbalancing:*",
        "application-autoscaling:*",
        "logs:*",
        "tag:*",
        "resource-groups:*"
      ],
      "Effect": "Allow",
      "Resource": "*"
    }
  ]
}
EOF
}

resource "aws_iam_role_policy_attachment" "frankly_ecs_attach" {
  role       = "${aws_iam_role.frankly_ecs_role.name}"
  policy_arn = "${aws_iam_policy.frankly_ecs_policy.arn}"
}

## ECS

resource "aws_ecs_cluster" "frankly_ec2" {
    name = "frankly_ec2_cluster"
}

resource "aws_ecs_task_definition" "frankly_ecs_task" {
  family                = "service"
  container_definitions = "${file("terraform/task-definitions/search.json")}"

  volume {
    name      = "service-storage"

    docker_volume_configuration {
      scope         = "shared"
      autoprovision = true
    }
  }

  placement_constraints {
    type       = "memberOf"
    expression = "attribute:ecs.availability-zone in [us-east-2]"
  }
}

resource "aws_ecs_service" "frankly_ecs_service" {
  name            = "frankly_ecs_service"
  cluster         = "${aws_ecs_cluster.frankly_ec2.id}"
  task_definition = "${aws_ecs_task_definition.frankly_ecs_task.arn}"
  desired_count   = 2
  iam_role        = "${aws_iam_role.frankly_ecs_role.arn}"
  depends_on      = ["aws_iam_role.frankly_ecs_role", "aws_alb.frankly_internal_alb", "aws_alb_target_group.frankly_internal_target_group"]

  # network_configuration = {
  #   subnets = ["${aws_subnet.frankly_private_subnet_a.id}", "${aws_subnet.frankly_private_subnet_b}"]
  #   security_groups = ["${aws_security_group.frankly_internal_alb_sg}", "${aws_security_group.frankly_service_sg}"]
  #   # assign_public_ip = true
  # }

  ordered_placement_strategy {
    type  = "binpack"
    field = "cpu"
  }

  load_balancer {
    target_group_arn = "${aws_alb_target_group.frankly_internal_target_group.arn}"
    container_name   = "search-svc"
    container_port   = 8080
  }

  placement_constraints {
    type       = "memberOf"
    expression = "attribute:ecs.availability-zone in [us-east-2]"
  }
}
