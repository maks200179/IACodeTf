# InfrastractureAsCode




```
To run it inside docker run build.sh. 


To run app:

Connect to docker via ssh port 52 with X server.
Run the file after sessiion established with X server. 
cd /usr/src/iacode/ && python3  MainWindowsIac.py 

or:

ssh -X  root@docker_host_ip -p 72 'cd /usr/src/iac/ && python3  MainWindowsIac.py'
```
