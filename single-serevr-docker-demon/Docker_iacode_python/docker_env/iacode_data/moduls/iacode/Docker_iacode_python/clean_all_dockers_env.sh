#!/bin/bash

set -x

docker stop $(docker ps -a -q)
docker rm $(docker ps -a -q)


docker volume prune -f
docker system prune -a  -f 
 

docker rmi $(docker images -q)


systemctl stop docker
rm -rf /var/lib/docker/overlay2/*
systemctl start  docker 


