#!/bin/bash

#set -x



clear


while [[ ${1:0:2} == '--' ]] && [[ $# -ge 1 ]] ; do
    [[ $1 == '--docker_env' ]] && { docker_env="yes"; };
    [[ $1 == '--monitor' ]] && { monitor="yes"; };
    [[ $1 == '--help' ]] && { help="yes"; };
    shift 2 || break
done


if [[ ! -z $help ]]
	then
	{
	echo "use --docker_env install docker envirement"
	}
fi

if [[ ! -z $docker_env ]]
	then
	{
	installed=$(yum list installed | grep docker.x86_64)
    if [[ -z $installed  ]] ; then 
		yum -y install docker
		systemctl enable docker
		systemctl start docker
	fi 
    if [[ ! -f /usr/local/bin/docker-compose ]] ||  [[ ! -f /usr/bin/docker-compose ]] ; then
	
		#curl -L "https://github.com/docker/compose/releases/download/1.23.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
		curl -L "https://github.com/docker/compose/releases/download/1.25.0-rc2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
		chmod +x /usr/local/bin/docker-compose
		ln -s /usr/local/bin/docker-compose /usr/bin/docker-compose
		docker-compose --version
		
	fi



	}


fi




