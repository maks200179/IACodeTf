#!/bin/bash
set -x


DIR=$(dirname "$(readlink -f "$0")")




if  [[ ! -f /iacode_data_data/MainWindowsIac.py ]] || [[ ! -d  /iacode_data_data ]] ; then
    #echo 'not'
    mkdir /iacode_data_data
    cp -fr "${DIR}"/app/* /iacode_data/
    
		
else 
		echo "clean installation not detected old configuration persist, so the  current code will be keeped .   The iacode_data folder is  /iacode_data_data and exist"
		
fi

	
git_dir="/iacode_data/.git"
if [[ -d ${git_dir} ]]; then 
    rm -fr "${git_dir}"
    echo "git dir removed"
fi	
	
	
if [[ ! $(docker ps -a | grep 'iacode') ]] ; then
    docker-compose  -f "${DIR}"/docker_env/docker-compose.yml up -d --build	
else 
    docker-compose  -f "${DIR}"/docker_env/docker-compose.yml up -d --build	
fi
