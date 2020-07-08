
data "template_file" "json_config" {
    
    template = <<EOF
{
    "endpoint": "${module.eks.cluster_endpoint}",
    "securitygroup": "${module.eks.cluster_security_group_id}",
    "kubectl_config": "${module.eks.kubeconfig}",
    "config_map_aws_auth": "${module.eks.config_map_aws_auth}"
}
}
EOF
}



