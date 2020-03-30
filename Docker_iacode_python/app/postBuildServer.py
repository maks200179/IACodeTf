from subprocess import (Popen, PIPE)
import fileinput
#import logging
import jenkins
from loggingGlobal import loggingGlobal
from gitHubCopyRepository import gitHubCopyRepo
from configFileJson import configFileIni
import shlex
import time
import json
import sys 
import os
import re

class postBuildServer(configFileIni):
    def __init__(self):
        super(postBuildServer, self).__init__()
        self.logging = loggingGlobal()
        self.githubcopyrepo = gitHubCopyRepo()


    def setVarsToFunctionSelf(self,module):
        
        self.git_link = self.read_conf_file("Git", "ssh_link")
        self.iacode_module_name = 'iacode'

        self.terraform_data =  '%s/terraform/modules_data' %(self.detectFileDir())
        self.terraform_modules_data = '%s/%s' %(self.terraform_data,module)

        self.modules_work_space    = '%s/moduls/' % (self.detectFileDir())
        self.main_module_workspace = '%s/moduls/%s/%s' % (self.detectFileDir(),self.iacode_module_name,module)
        
        self.excluded_directoryes = 'certbot/log/*'

        self.fileRepoListToDeploy = '%s/repository_module_list.json' % (self.main_module_workspace)
        

    #aws creds from file
    def collectAWSCredentials(self):
        #make sure the file exist and collect aws creds
        filePatch         = '%s/moduls/kubernetes/aws_credentials.json' % (self.detectFileDir())
        if not os.path.isfile(filePatch):
            return False
        
        json_data              = self.fileGetContentsJson(filePatch)
        self.aws_region        = json_data["region"]
        self.aws_access_key    = json_data["access_key"]
        self.aws_secret_key    = json_data["secret_key"]
        
        if len(self.aws_region) == 0 or len(self.aws_access_key) == 0 or len(self.aws_secret_key) == 0 :
            return False 

    #aws creds from app  
    def getAwsCredsFromConfig(self):
        self.aws_region        = self.read_conf_file('AWS', 'region')
        self.aws_access_key    = self.read_conf_file('AWS', 'accesskey')
        self.aws_secret_key    = self.read_conf_file('AWS', 'secretkey')
        
        if len(self.aws_region) == 0 or len(self.aws_access_key) == 0 or len(self.aws_secret_key) == 0 :
            return False
        


    def exportEnvAwsCredentials(self):
            stdout_file = self.collectAWSCredentials()
            if stdout_file is False:
                #try to get from  config 
                stdout_config = self.getAwsCredsFromConfig()
            elif stdout_config is False:
                msg = 'App: The aws credential file not exist or cant find the json in root of repository and also cant read creds from config' 
                self.logging.writeLogWarning(msg)
                return msg
            
            
                
            os.environ["AWS_ACCESS_KEY_ID"]="%s"     %(self.aws_access_key)
            os.environ["AWS_SECRET_ACCESS_KEY"]="%s" %(self.aws_secret_key)
            os.environ["AWS_DEFAULT_REGION"]="%s"    %(self.aws_region)
            
            #print(os.environ["AWS_ACCESS_KEY_ID"])
            #print(os.environ["AWS_SECRET_ACCESS_KEY"])
            #print(os.environ["AWS_DEFAULT_REGION"])

            return True

    
   
    def collectRepoModulesData(self):
        repolist = []
        if os.path.isfile(self.fileRepoListToDeploy):
            json_data         = self.fileGetContentsJson(self.fileRepoListToDeploy)
            self.branch       = json_data["branch"]

            for key , val  in json_data.items():
                #print (val)
                #print (key)
                if  'repo' in key:
                    repolist.append(val)
            self.repolist = repolist

        else:
            return False




    def detectFileDir(self):
        dirname = os.path.dirname(os.path.abspath(__file__))
        return dirname


    def fileGetContentsJson(self,filename):
        with open(filename) as f:
            json_data   = json.loads(f.read())
            f.close()
            return json_data

    def fileGetContent(self,filename):
        with open(filename) as f:
            data = f.read()
            f.close()
            return data.strip()

    def fileWriteContent(self,content,file):
        file = open(file, "w")  # write mode
        file.write(content)
        file.close()



    def saveSwarmManagerToken(self,token):
        filename = "%s/manager_token.info" % self.terraform_modules_data
        if not os.path.isfile(filename):
            self.mainExecCMD('tochToken',filename)
        self.fileWriteContent(token,filename)


    def readSwarmManagerToken(self,module):
        
        filename = "%s/%s/manager_token.info" % (self.terraform_data, self.manager_module_name)
        if os.path.isfile(filename):
            return (self.fileGetContent(filename))
        else:
            msg = 'cant read the token file not exist or not finded '
            self.logging.writeLogCritical(msg)
            return False




    def collectModulData(self):
        #make sure the file exist otherwise module not installed and config not exist
        filePatch         = '%s/json.info' % self.terraform_modules_data
        if not os.path.isfile(filePatch):
            return False
        json_data                   = self.fileGetContentsJson(filePatch)
      
        self.server_ip              = json_data["ip"]



    def checkServerIfOnlineTimer(self):
        test = 0
        timeout = time.time() + 60 * 7  # 5 minutes from now
        while (self.mainExecCMD('cmdCheckServerOnline')) == '':
            time.sleep(7)
            if test == 15 or time.time() > timeout:
                return False
            test = test + 1
        return True




    
    def collectModulDataFromBase(self):
        #make sure the file exist otherwise module not installed and config not exist
        filePatch         = '%s/module_build_info.json' % self.main_module_workspace
        if not os.path.isfile(filePatch):
            msg = 'the config file module_build_info.json not exist in root of module '
            return msg
        json_data                   = self.fileGetContentsJson(filePatch)
        
        self.ssh_key_name                 = json_data["ssh_key_name"]
        self.network_module_name    = json_data["network_module_name"]
        self.user_name              = json_data["username"]
        self.swarm                  = "swarm" in json_data
        self.manager                = "manager" in json_data
        
        if "manager_module_name" in json_data:
            self.manager_module_name    = json_data["manager_module_name"]

        self.ssh_key_path = '%s/%s/%s' % (self.terraform_data, self.network_module_name , self.ssh_key_name)
        if not os.path.isfile(self.ssh_key_path):
            msg = 'the network module not installed please install it first'
            return msg
    
        return True
    
    
    
    
    
    
    def getGitConfigData(self):
        self.git_ssh_link = self.read_conf_file("Git", "ssh_link")
        self.git_ssh_key_path = self.read_conf_file('Git', 'SSH_Key_Path')
        self.git_ssh_branch = self.read_conf_file('Git', 'branch')
        self.git_repo_name = self.read_conf_file('Git', 'repository_name')
        self.deploy_git_key = self.read_conf_file('DeployGitInfo', 'ssh_key_path')
        
                
        if self.git_ssh_link is None  or self.git_ssh_link is False:
            msg = 'Cant read git section from config '
            self.logging.writeLogCritical(msg)
            print (msg)
            sys.exit(1)

            


    def copyTfMainModule(self):
        stdout = self.githubcopyrepo.updateTerraformMainModuleListConfig()
        return stdout


    def  copyRepoToServer(self):
        self.getGitConfigData()
        stdout = (self.githubcopyrepo.git_clone_repository(self.git_ssh_link, self.git_ssh_key_path, self.git_ssh_branch,self.git_repo_name))
        if stdout is False:
            msg = 'App: Cant copy repo check log'
            self.logging.writeLogWarning(msg)
            return msg
        else:
            return stdout
    
    def fileReplaseStr(self,filename,str_old,str_new):
        for line in fileinput.input([filename], inplace=True):
            if line.strip().startswith(str_old):
                line = str_new
            sys.stdout.write(line)

    def editConfigJobXML(self):
        filepath = '%s/configJobXML.xml' % (self.detectFileDir())
        filepathtmp = '%s/configJobXML.xml.tmp' % (self.detectFileDir())
        

        self.mainExecCMD('copyXML',filepath,filepathtmp)

        str_to_find = '<defaultValue>$server_ip</defaultValue>'
        str_to_put  = '<defaultValue>%s</defaultValue>' %(self.server_ip)  
        self.fileReplaseStr(filepathtmp, str_to_find, str_to_put)

        str_to_find = '<defaultValue>$server_token</defaultValue>'
        str_to_put  = '<defaultValue>%s</defaultValue>' %(self.fileGetContent(self.ssh_key_path))  
        self.fileReplaseStr(filepathtmp, str_to_find, str_to_put)
        


        return self.fileGetContent(filepathtmp)
        
    


    def mainBuildRemoveModule(self,command,module):
        self.setVarsToFunctionSelf(module)
        self.collectModulDataFromBase()
        

        if 'checkNetModuleIsCreated' in command:
            stdout = self.collectModulDataFromBase()
            return stdout

        elif 'collectModuleDataFromJsonAndCheckIfExist' in command:
            stdout = self.collectModulData()
            #stdout2 = self.collectModulDataFromBase()
            if stdout  is False:
                msg = 'App: The json data info file not exist after module applyed by terraform'
                self.logging.writeLogWarning(msg)
                return msg
            else:
                return True


        elif 'cmdCheckGitModulesToDeployAndCollectData' in command:
            stdout = self.collectRepoModulesData()
            #print (self.repolist)
            if stdout is False:
                msg = 'App: The module not contain git repositories to deploy'
                self.logging.writeLogWarning(msg)
                return msg
            else:
                return True


        # there is triger jenkins job to deploy content for services .
        
        elif 'cmdGitCloneModules' in command:
            stdout = self.mainExecCMD('mkdir','/var/www-data')
            #job_name = 'BuildAllAndSyncToStaging2Swarm'
            
            #job_data = self.j_server.get_job(job_name) 
            #prev_id = self.j_server.get_job_info(job_name)['lastBuild']['number']

            #self.j_server.reconfig_job(job_name,self.editConfigJobXML())
            #stdout = self.j_server.build_job(job_name, {'server_ip': self.server_ip})
            #wait for jenkins done the job 
            #while True:
            #    self.logging.writeLogWarning('Waiting for build to start...')
            #    if prev_id != self.j_server.get_job_info(job_name)['lastBuild']['number']:
            #        break
            #    time.sleep(3)
            #self.logging.writeLogWarning('Running...')
            #last_build = self.j_server.get_job_info(job_name)['lastBuild']['number']
            #while self.j_server.get_build_info(job_name,last_build)['building']:
            #    time.sleep(3)
            #self.logging.writeLogWarning(self.j_server.get_build_info(job_name,last_build)['result'])    
            




            if stdout is False:
                msg = 'App: The module not contain git repositories to deploy'
                self.logging.writeLogWarning(msg)
                return msg
            else:
                return ('%s') %(stdout)


        elif 'cmdCheckServerOnline' in command:
            stdout = self.checkServerIfOnlineTimer()
            if stdout is False:
                msg = 'App: Server Offline timeout'
                self.logging.writeLogWarning(msg)
                return msg
            else:
                return  True

        elif 'cmdRsync' in command:
            stdout = self.mainExecCMD('cmdRsync')
            return stdout

        elif 'cmdExecInstallEnv' in command:
            stdout = self.mainExecCMD('cmdExecInstallEnv',module)
            return stdout

        elif 'cmdExecDockerPs' in command:
            stdout = self.mainExecCMD('cmdExecDockerPs',module)
            return stdout

        elif 'checkIfSwarm' in command:
            if self.swarm is  True:
                return True
            else:
                return False

        elif 'checkIfManger' in command:
            if self.manager is  True:
                return True
            else:
                return False

        elif 'initSwarmManager' in command:
            stdout = self.mainExecCMD('initSwarmManager',module)
            if stdout != '':
                self.saveSwarmManagerToken(stdout)
                return stdout
            else:
                msg = 'the manager not returned tocken while init'
                self.logging.writeLogWarning(msg)
                return (msg)

        elif 'connectWorkerToManager' in command:
            token = (self.readSwarmManagerToken(module)).replace('cubeadm  join --token','')
            if token != '' and token is not False:
                stdout = self.mainExecCMD('connectWorkerToManager', module,token)
                return stdout
            else:
                msg = 'the manager not installed or token not exist please check log'
                self.logging.writeLogWarning(msg)
                return msg


        elif 'rebuildSwarmManager' in command:
            manager_module_name = self.network_module_name
            if manager_module_name is not False:
                #self.setVarsToFunctionSelf(manager_module_name)
                #self.collectModulData()
                #update module data on manager
                stdout_copy = self.mainExecCMD('cmdRsync')
                stdout_rebuild = self.mainExecCMD('rebuildSwarmManager', module)
                return '%s \n%s' %(stdout_copy,stdout_rebuild)
            else:
                msg = 'the manager not installed or token not exist please check log'
                self.logging.writeLogWarning(msg)
                return msg










    def mainExecCMD(self, command, param=None , param2=None):
        
        cmdCheckServerOnline      = """ ssh -o "StrictHostKeyChecking=no" -o "ConnectTimeout=2" -i "%s" "%s@%s" "uname -a" """ % (self.ssh_key_path, self.user_name, self.server_ip)
        cmdRsync                  = """ rsync   -c -arh -i --rsync-path "sudo rsync"  --info=COPY --info=REMOVE  --delete --no-times --no-perms --no-owner --no-group    "%s" -e "ssh -i %s -o "StrictHostKeyChecking=no""   "centos@%s:/var/" """ % (self.main_module_workspace, self.ssh_key_path, self.server_ip)
        cmdCopyModulesToServer    = """ rsync  -og -c -arh -i --rsync-path "sudo rsync"  --info=COPY --info=REMOVE  --delete  --usermap=:apache --groupmap=*:apache   "%s%s" -e "ssh -i %s -o "StrictHostKeyChecking=no""   "centos@%s:/var/www-data/" """ % (self.modules_work_space,param, self.ssh_key_path, self.server_ip)
        cmdExecInstallEnv         = """ ssh -o "StrictHostKeyChecking=no" -o "ConnectTimeout=2" -i "%s" "%s@%s" "sudo bash /var/%s/build.sh --docker_env yes" """ % (self.ssh_key_path, self.user_name, self.server_ip, param)
        cmdExecDockerPs           = """ ssh -o "StrictHostKeyChecking=no" -o "ConnectTimeout=2" -i "%s" "%s@%s" "cd /var/%s   && sudo docker ps -a --format 'table {{.Names}}\t{{.Status}}\t{{.RunningFor}}'" """ % (self.ssh_key_path, self.user_name, self.server_ip, param)
        cmdInitSwarmManager       = """ ssh -o "StrictHostKeyChecking=no" -o "ConnectTimeout=2" -i "%s" "%s@%s" "sudo bash /var/%s/build.sh  --set_host_name_master yes --install_kube yes --init_swarm_manager yes" """ % (self.ssh_key_path, self.user_name, self.server_ip, param)
        cmdTochToken              = """ touch %s """  % (param)
        cmdConnectWorkerToManager = """ ssh -o "StrictHostKeyChecking=no" -o "ConnectTimeout=2" -i "%s" "%s@%s" "sudo bash /var/%s/build.sh   --worker_connect_to_manager %s" """ % (self.ssh_key_path, self.user_name, self.server_ip,param,param2)
        cmdGetModuleNamesInstalled= """ ls %s """ % (self.terraform_data)
        cmdRebuildSwarmManager    = """ ssh -o "StrictHostKeyChecking=no" -o "ConnectTimeout=2" -i "%s" "%s@%s" "sudo bash /var/%s/build.sh --rebuild_swarm_manager yes" """ % (self.ssh_key_path, self.user_name, self.server_ip,param)
        cmdCpXML                  = """ cp -fr %s %s """  % (param, param2) 
        cmdMkdir                  = """ ssh -o "StrictHostKeyChecking=no" -o "ConnectTimeout=2" -i "%s" "%s@%s" "sudo mkdir -p  %s" """ % (self.ssh_key_path, self.user_name, self.server_ip,param)
        
        
        options = {'mkdir': cmdMkdir,'copyXML': cmdCpXML,'copyModulesToServer': cmdCopyModulesToServer,'rebuildSwarmManager': cmdRebuildSwarmManager,'getModuleNameInstalled': cmdGetModuleNamesInstalled,'connectWorkerToManager': cmdConnectWorkerToManager,'tochToken': cmdTochToken,'initSwarmManager': cmdInitSwarmManager,'cmdCheckServerOnline': cmdCheckServerOnline, 'cmdRsync': cmdRsync, 'cmdExecInstallEnv': cmdExecInstallEnv , 'cmdExecDockerPs': cmdExecDockerPs}

        if command in options:
            cmd = options[command]
            self.logging.writeLogWarning(cmd)
            stdout = self.cmdCommunicateOS(cmd)
            return stdout
        else:
            self.logging.writeLogCritical('no command defined in main cmd function post build server')
            return ("no command defined")



    def cmdCommunicateOS(self, command):




        p = Popen(shlex.split(command), stdin=PIPE, stdout=PIPE, stderr=PIPE)
        (stdout, stderr) = p.communicate()
        if p.returncode != 0 or stderr.decode('utf-8') != '':
            self.logging.writeLogWarning(("""'The command %s exited with error code  %s and error messege is %s '""") %(command,p.returncode,(stderr.decode('utf-8'))))
        return stdout.decode('utf-8')
