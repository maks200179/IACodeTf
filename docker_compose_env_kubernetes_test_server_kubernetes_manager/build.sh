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
        
        sudo mkdir /etc/docker
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

       # mkdir -p /etc/systemd/system/docker.service.d

        # Restart Docker
        #systemctl daemon-reload
        #systemctl restart docker
     
        

        
    fi



    if  [[ $install_kube == "yes" ]] ; then
        if  [[ ! -z $(yum list installed | grep docker-ce.x86_64) ]] && [[ ! -z $(docker-compose --version) ]] ; then
            #add kubernetes repo
            cat <<EOF > /etc/yum.repos.d/kubernetes.repo
[kubernetes]
name=Kubernetes
baseurl=https://packages.cloud.google.com/yum/repos/kubernetes-el7-x86_64
enabled=1
gpgcheck=1
repo_gpgcheck=1
gpgkey=https://packages.cloud.google.com/yum/doc/yum-key.gpg https://packages.cloud.google.com/yum/doc/rpm-package-key.gpg
EOF
        
            sudo yum install -y kubelet kubeadm kubectl >/dev/null 2>&1
            sudo systemctl enable kubelet               >/dev/null 2>&1
            sudo systemctl start kubelet                >/dev/null 2>&1
            sudo yum install -y tcpdump                 >/dev/null 2>&1
                
                
        fi
        
    fi






    if  [[ $set_host_name_master == "yes" ]] ; then
        if  [[ ! -z $(yum list installed | grep docker-ce.x86_64) ]] && [[ ! -z $(docker-compose --version) ]] ; then
        
                sudo hostnamectl set-hostname master-node                               
                ipaddr=$(sudo curl --fail --silent --show-error http://169.254.169.254/latest/meta-data/local-ipv4) 
                echo "${ipaddr}" "master-node" >> /etc/hosts                            
            
                sudo sed -i '/swap/d' /etc/fstab                                        
                sudo swapoff -a                                                         
                sudo echo '1' > /proc/sys/net/bridge/bridge-nf-call-iptables            
                
                
        fi
        
    fi




    if  [[ $get_token == "yes" ]] ; then
        if  [[ ! -z $(yum list installed | grep docker-ce.x86_64) ]] && [[ ! -z $(docker-compose --version) ]] ; then
        
                sudo kubeadm token create --print-join-command | grep 'kubeadm join'
                
        fi
        
    fi




    if  [[ $check_cluster_up == "yes" ]] ; then
        if  [[ ! -z $(yum list installed | grep docker-ce.x86_64) ]] && [[ ! -z $(docker-compose --version) ]] ; then
                 #sudo whoami
                 #whoami
                 su root
                 export KUBECONFIG="$HOME/.kube/config"
                 echo $KUBECONFIG
                 ls -lsa $HOME/
                 sudo su - root -c
                 #echo $HOME
                 #sudo -s
                 sudo kubectl cluster-info  | egrep --color  'Kubernetes master' 3>&1 1>/dev/null 2>&3 | sed 's/\x1b\[[0-9;]*m//g' 
                
        fi
        
    fi




    if  [[ ! -z ${manager_token}  ]] ; then
        if  [[ ! -z $(yum list installed | grep docker-ce.x86_64) ]] && [[ ! -z $(docker-compose --version) ]] ; then
            
            sudo hostnamectl set-hostname worker-node                                   
            ipaddres=$(sudo curl --fail --silent --show-error http://169.254.169.254/latest/meta-data/local-ipv4)     
            echo "${ipaddres}" "worker-node" >> /etc/hosts                                  
            
            sudo kubeadm join "${ipaddr}" --token "${manager_token}"  --discovery-token-ca-cert-hash  "${discovery_token}"                   
                
        fi
        
    fi
     
    
    if  [[ $init_swarm_manager == "yes"  ]] ; then
        if  [[ ! -z $(yum list installed | grep docker-ce.x86_64) ]] && [[ ! -z $(docker-compose --version) ]] ; then
            
            #sudo docker swarm init  | grep 'docker swarm join --token'
            

            sudo kubeadm init --node-name=$(hostname -f) --pod-network-cidr=10.244.0.0/16  | grep "Your Kubernetes control-plane has initialized" | sed 's/\x1b\[[0-9;]*m//g' 
            
            #for root
            mkdir -p $HOME/.kube                                              > /dev/null                                                   
            sudo yes | cp -i /etc/kubernetes/admin.conf $HOME/.kube/config    > /dev/null                    
            sudo chown $(id -u):$(id -g) $HOME/.kube/config                   > /dev/null                             
            export KUBECONFIG="$HOME/.kube/config"                            > /dev/null  
            #sudo bash -c "KUBECONFIG='$HOME/.kube/config'"
            #export KUBECONFIG=$HOME/.kube/config                                            3>&1 1>/dev/null 2>&3
            
            #for root 
            #sudo export KUBECONFIG=/etc/kubernetes/admin.conf
            
            #for --pod-network-cidr=10.244.0.0/16
            #sudo kubectl apply -f https://raw.githubusercontent.com/coreos/flannel/2140ac876ef134e0ed5af15c65e414cf26827915/Documentation/kube-flannel.yml
            
            #sudo kubectl apply -f https://raw.githubusercontent.com/coreos/flannel/master/Documentation/kube-flannel.yml > /dev/null 
            #sudo kubectl apply -f https://docs.projectcalico.org/v3.11/manifests/calico.yaml
            #sudo kubectl create rolebinding -n kube-system configmaps --role=extension-apiserver-authentication-reader --serviceaccount=kube-system:cloud-controller-manager
                
        else 
            
            echo "docker-compose or docker not  installed on target server check logs."
                
        fi
        
    fi
    
    
    if [[ $rebuild_swarm_manager == "yes" ]] ; then
        if  [[ ! -z $(yum list installed | grep docker-ce.x86_64) ]] && [[ ! -z $(docker-compose --version) ]] ; then
        #base image build and push
        #sudo docker-compose -f "${DIR}"/docker-compose_base_images.yml build 3>&1 1>/dev/null 2>&3
        #sudo docker-compose -f "${DIR}"/docker-compose_base_images.yml push 3>&1 1>/dev/null 2>&3
        
        #build all other images
        #sudo docker-compose -f "${DIR}"/docker-compose.full.yml build 3>&1 1>/dev/null 2>&3
        #sudo docker-compose -f "${DIR}"/docker-compose.full.yml push 3>&1 1>/dev/null 2>&3
        
        sudo mkdir -p /mysql_data
        sudo mkdir -p /mysql_conf/dbbackup
        sudo mkdir -p /mysql_conf/log
        
        #deploy stack 
        #sudo docker stack deploy --prune --resolve-image always --with-registry-auth  --compose-file "${DIR}"/docker-compose.yml stackdemo 
        
        #restore database 
        #sudo  bash "${DIR}"/db_mysql5.6/conf/crone_copy_last_db_backup_from_s3.sh 2>/dev/null 
        
        fi
    fi
