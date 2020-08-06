data "template_file" "json_config" {
    
    template = <<EOF
{
    "endpoint": "${aws_eks_cluster.example.endpoint}",
    "securitygroup": "${aws_eks_cluster.example.security_group_id}",
    "kubectl_config": "${aws_eks_cluster.example.cluster_kubeconfig}",
    "cert"          : "${aws_eks_cluster.example.certificate_authority[0].data}"
    
}
EOF
}



resource "local_file" "environment1" {
    content = "${data.template_file.json_config.rendered}"
    filename = "../terraform/modules_data/fargate-k8s-eks/json.secret"
    file_permission = "0400"
}  
