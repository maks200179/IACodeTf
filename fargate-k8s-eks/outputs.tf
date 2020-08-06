data "template_file" "json_config" {
    
    template = <<EOF
{
    "endpoint": "${data.aws_eks_cluster.example.endpoint}",
    "securitygroup": "${data.aws_eks_cluster.example.security_group_id}",
    "kubectl_config": "${data.aws_eks_cluster.example.kubeconfig}"
    
}
EOF
}



resource "local_file" "environment1" {
    content = "${data.template_file.json_config.rendered}"
    filename = "../terraform/modules_data/fargate-k8s-eks/json.secret"
    file_permission = "0400"
}  
