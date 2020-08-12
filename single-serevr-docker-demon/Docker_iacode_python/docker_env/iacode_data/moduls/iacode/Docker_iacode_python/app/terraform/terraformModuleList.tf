module "docker_compose_env_production_openvpn" {
  source = "../moduls/all_bash/docker_compose_env_production_openvpn"
}

 module "docker_compose_env_production_jenkins" {
  source = "../moduls/all_bash/docker_compose_env_production_jenkins"
} 


module "aws_production_network_terraform_conf" {
  source = "../moduls/all_bash/aws_production_network_terraform_conf"
} 
  

module "aws_staging_network_terraform_conf" {
  source = "../moduls/all_bash/aws_staging_network_terraform_conf"
}

module "docker_compose_env_staging" {
  source = "../moduls/all_bash/docker_compose_env_staging"
} 
  
 module "docker_compose_env_production_server_swarm_manager" {
  source = "../moduls/all_bash/docker_compose_env_production_server_swarm_manager"
}   

module "docker_compose_env_production_server_swarm_worker1" {
  source = "../moduls/all_bash/docker_compose_env_production_server_swarm_worker1"
}   
