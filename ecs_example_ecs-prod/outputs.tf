data "template_file" "json_config" {
    
    template = <<EOF
{
    "endpoint": "${module.my-cluster.cluster_endpoint}",
    "securitygroup": "${module.my-cluster.cluster_security_group_id}",
    "kubectl_config": "${module.my-cluster.kubeconfig}"
    
}
EOF
}



resource "local_file" "environment1" {
    content = "${data.template_file.json_config.rendered}"
    filename = "../terraform/modules_data/ecs_example_ecs-prod/json.secret"
    file_permission = "0400"
}  
