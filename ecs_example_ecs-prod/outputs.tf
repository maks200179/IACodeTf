data "template_file" "json_config" {
    
    template = <<EOF
{
    "endpoint": "${aws_ecs_cluster.main.cluster_endpoint}",
    "securitygroup": "${aws_ecs_cluster.main.cluster_security_group_id}",
    "kubectl_config": "${aws_ecs_cluster.main.kubeconfig}"
    
}
EOF
}



resource "local_file" "environment1" {
    content = "${data.template_file.json_config.rendered}"
    filename = "../terraform/modules_data/ecs_example_ecs-prod/json.secret"
    file_permission = "0400"
}  
