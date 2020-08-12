module "aws_kubernetes_test_network_terraform_conf" {
  source = "../moduls/iacode/aws_kubernetes_test_network_terraform_conf"
} 
  
 module "docker_compose_env_kubernetes_test_server_kubernetes_manager" {
  source = "../moduls/iacode/docker_compose_env_kubernetes_test_server_kubernetes_manager"
}  

 module "docker_compose_env_kubernetes_test_server_kubernetes_worker1" {
  source = "../moduls/iacode/docker_compose_env_kubernetes_test_server_kubernetes_worker1"
}  

 module "k8s-manager-ksc" {
  source = "../moduls/iacode/k8s-manager-ksc"
} 

 module "fargate-k8s-eks" {
  source = "../moduls/iacode/fargate-k8s-eks"
} 

