#!/bin/bash
#set -x



while [[ ${1:0:2} == '--' ]] && [[ $# -ge 2 ]] ; do
    [[ $1 == '--docker_env' ]] && { docker_env="yes"; };
    [[ $1 == '--docker_compose_up' ]] && { docker_compose_up="yes"; };
    [[ $1 == '--init_swarm_manager' ]] && { init_swarm_manager="${2}"; };
    [[ $1 == '--rebuild_swarm_manager' ]] && { rebuild_swarm_manager="${2}"; };
    [[ $1 == '--install_db_crone_tab' ]] && { install_db_crone="${2}"; };
    [[ $1 == '--install_kube' ]] && { install_kube="${2}"; };
    [[ $1 == '--check_cluster_up' ]] && { check_cluster_up="${2}"; };
    [[ $1 == '--get_token' ]] && { get_token="${2}"; };
    [[ $1 == '--set_host_name_master' ]] && { set_host_name_master="${2}"; };
    [[ $1 == '--worker_connect_to_manager' ]] && { ipaddr="${2}"; manager_token="${3}"; discovery_token="${4}"; };
        shift 2 || break
done







    DIR=$(dirname "$(readlink -f "$0")")


    if [[ $docker_env == "yes" ]] ; then

    
        installed=$(yum list installed | grep docker-ce.x86_64)

        if [[ -z $installed  ]] ; then 
            sudo yum install -y yum-utils device-mapper-persistent-data lvm2 >/dev/null 2>&1
            sudo yum-config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo >/dev/null 2>&1
            sudo yum install -y docker-ce-19.03.5-3.el7.x86_64 docker-ce-cli-19.03.5-3.el7.x86_64 containerd.io-1.2.10-3.2.el7.x86_64  >/dev/null 2>&1
            systemctl enable docker   >/dev/null 2>&1
            systemctl start docker  >/dev/null 2>&1
            sudo docker version
        fi

        if [[ ! -f /usr/local/bin/docker-compose ]] ||  [[ ! -f /usr/bin/docker-compose ]] ; then

            #curl -L "https://github.com/docker/compose/releases/download/1.23.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
            curl -L "https://github.com/docker/compose/releases/download/1.25.4/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose >/dev/null 2>&1
            chmod +x /usr/local/bin/docker-compose >/dev/null 2>&1
            ln -s /usr/local/bin/docker-compose /usr/bin/docker-compose >/dev/null 2>&1
            sudo docker-compose --version  >/dev/null 2>&1

        fi
        
        
        if [[ ! -d /etc/docker  ]]  ||  [[ ! -f /etc/docker/daemon.json ]] ; then
            sudo mkdir /etc/docker
            #sudo mkdir /etc/docker
            # Setup daemon.
            cat > /etc/docker/daemon.json <<EOF
            {
              "exec-opts": ["native.cgroupdriver=systemd"],
              "log-driver": "json-file",
              "log-opts": {
                "max-size": "100m"
              },
              "storage-driver": "overlay2",
              "storage-opts": [
                "overlay2.override_kernel_check=true"
              ]
            }
EOF

            mkdir -p /etc/systemd/system/docker.service.d

            # Restart Docker
            systemctl daemon-reload
            systemctl restart docker
     
        fi

        
    fi



    if  [[ $install_kube == "yes" ]] ; then
        if  [[ ! -z $(yum list installed | grep docker-ce.x86_64) ]] && [[ ! -z $(docker-compose --version) ]] ; then
            #add kubernetes repo
            
            sudo yum install -y tcpdump                 >/dev/null 2>&1
            #sudo bash /var/Docker_iacode_python/build.sh
            if [[ ! -d /var/Docker_iacode_python ]] ; then
                sudo cp -fr  /var/single-serevr-docker-demon/Docker_iacode_python /var/
                sudo bash /var/Docker_iacode_python/build.sh
                
                
            
            fi    
            
            
            

            if [[ ! -z $(docker exec -it awscli sh -c "test -f ~/.aws/credentials   && echo 'Exists'") ]] ; then
                sudo docker exec awscli  aws eks --region us-east-2  update-kubeconfig --name test-eks-9chRfdVG
                sudo docker cp  awscli:/root/.kube/config /
                sudo docker cp  /config  kubectl:/root/.kube/config
                sudo docker exec  kubectl kubectl get pods -A
                
            
            fi    
                
                
        fi
        
    fi






    if  [[ $set_host_name_master == "yes" ]] ; then
        if  [[ ! -z $(yum list installed | grep docker-ce.x86_64) ]] && [[ ! -z $(docker-compose --version) ]] ; then
        
                sudo hostnamectl set-hostname infrastracture-node-cli                               
                ipaddr=$(sudo curl --fail --silent --show-error http://169.254.169.254/latest/meta-data/local-ipv4) 
                echo "${ipaddr}" "master-node" >> /etc/hosts                            
            
                sudo sed -i '/swap/d' /etc/fstab                                        
                sudo swapoff -a                                                         
                sudo echo '1' > /proc/sys/net/bridge/bridge-nf-call-iptables            
                
                
        fi
        
    fi




    if  [[ $get_token == "yes" ]] ; then
        if  [[ ! -z $(yum list installed | grep docker-ce.x86_64) ]] && [[ ! -z $(docker-compose --version) ]] ; then
        
                echo "no token" >/dev/null 2>&1
                
        fi
        
    fi




    if  [[ $check_cluster_up == "yes" ]] ; then
        if  [[ ! -z $(yum list installed | grep docker-ce.x86_64) ]] && [[ ! -z $(docker-compose --version) ]] ; then
                 #sudo whoami
                 #whoami
                 echo 'check_cluster_up_no_in_use'
                
        fi
        
    fi




    if  [[ ! -z ${manager_token}  ]] ; then
        if  [[ ! -z $(yum list installed | grep docker-ce.x86_64) ]] && [[ ! -z $(docker-compose --version) ]] ; then
            
            sudo hostnamectl set-hostname worker-node                                   
            ipaddres=$(sudo curl --fail --silent --show-error http://169.254.169.254/latest/meta-data/local-ipv4)     
            echo "${ipaddres}" "worker-node" >> /etc/hosts                                  
            sudo mkdir /mnt/data{0..10}
            sudo kubeadm join "${ipaddr}" --token "${manager_token}"  --discovery-token-ca-cert-hash  "${discovery_token}"                   
                
        fi
        
    fi
     
    
    if  [[ $init_swarm_manager == "yes"  ]] ; then
        if  [[ ! -z $(yum list installed | grep docker-ce.x86_64) ]] && [[ ! -z $(docker-compose --version) ]] ; then
            
            #sudo docker swarm init  | grep 'docker swarm join --token'
            

            sudo kubeadm init --service-cidr=10.10.0.0/24  --pod-network-cidr=10.244.0.0/16  | grep "Your Kubernetes control-plane has initialized"  
            
             
            #for root
            mkdir -p $HOME/.kube                                                                                                 
            sudo yes | cp -i /etc/kubernetes/admin.conf $HOME/.kube/config                        
            sudo chown $(id -u):$(id -g) $HOME/.kube/config                                                
            export KUBECONFIG="$HOME/.kube/config"                              
            #sudo bash -c "KUBECONFIG='$HOME/.kube/config'"
            #export KUBECONFIG=$HOME/.kube/config                                            3>&1 1>/dev/null 2>&3
            
            sudo mkdir /mnt/data{0..10}
            
            
            #for root 
            #sudo export KUBECONFIG=/etc/kubernetes/admin.conf
            
            

            
            sudo kubectl apply -f https://raw.githubusercontent.com/coreos/flannel/2140ac876ef134e0ed5af15c65e414cf26827915/Documentation/kube-flannel.yml > /dev/null 
            
            sudo kubectl taint nodes --all node-role.kubernetes.io/master-
            #sudo kubectl apply -f https://raw.githubusercontent.com/coreos/flannel/master/Documentation/kube-flannel.yml > /dev/null 
            #sudo kubectl apply -f https://docs.projectcalico.org/v3.11/manifests/calico.yaml
            #sudo kubectl create rolebinding -n kube-system configmaps --role=extension-apiserver-authentication-reader --serviceaccount=kube-system:cloud-controller-manager
           
            
        else 
            
            echo "docker-compose or docker not  installed on target server check logs."
                
        fi
        
    fi
    
    
    
