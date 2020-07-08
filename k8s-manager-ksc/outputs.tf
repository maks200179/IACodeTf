
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
    content = "${data.template_file.json_config}"
    filename = "../terraform/modules_data/k8s-manager-ksc/json.info"
    file_permission = "0400"
}  

