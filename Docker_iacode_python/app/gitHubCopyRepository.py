
from configFileJson import configFileIni
from loggingGlobal import loggingGlobal
import sys,os
import subprocess




class gitHubCopyRepo(configFileIni):
    def __init__(self):
        super(gitHubCopyRepo, self).__init__()
        self.logging = loggingGlobal()

    def setVarsToFunctionSelf(self):
        self.repository_workspace = '%s/moduls/%s' % (self.detectFileDir(),'iacode')
        self.terraform_dir = '%s/terraform' % (self.detectFileDir())


    def detectFileDir(self):
        dirname = os.path.dirname(os.path.abspath(__file__))
        return dirname

    def git_clone_repository(self,ssh_url,ssh_key,branch,reponame):
        self.git_link = ssh_url
        self.git_key_path = ssh_key
        self.git_branch = branch
        self.git_module_name = reponame


        self.setVarsToFunctionSelf()

        if not os.path.isdir(self.repository_workspace):
            os.makedirs(self.repository_workspace)
        else:
            self.mainExecCMD('cmdRmFolder',self.repository_workspace)


        filename = os.path.expanduser('~/.ssh/known_hosts')
        if os.path.isfile(filename):
            pass
        else:
            self.mainExecCMD('cmdTochFile',filename)


        cmdCheckSsh = self.mainExecCMD('cmdCheckSshAgent')
        if cmdCheckSsh == '':
            self.mainExecCMD('cmdEnableSshAgent')

        cmdCheckSshFinger = self.mainExecCMD('cmdCheckSshFingerprint',filename)
        if cmdCheckSshFinger == '':
            self.mainExecCMD('cmdAddSshFingerprint',filename)

        
        perm = oct(os.stat(self.git_key_path).st_mode)[-3:]
        if perm != 400:
            cmdChengeKeyPermissio = self.mainExecCMD('cmdChangeKeyPermission')


        if self.mainExecCMD('cmdRepoBranchCheck'):
            self.mainExecCMD('cmdGitClone',)
            clone_info =  ('Git: Copy repository %s from %s branch' % (self.git_link,self.git_branch))
            self.rmGitDir()
            return ('%s') % (clone_info.strip())
        else:
            msg = 'Branch not exist or you dont have  correct access rights'
            self.logging.writeLogWarning(msg)
            return msg



    def updateTerraformMainModuleListConfig(self):
        file = '%s/terraformModuleList.tf' %(self.repository_workspace)

        stdCmdCopyConf = self.mainExecCMD('cmdCopyConf',file)
        stdoutfiltered = 'Git: Update modules list:'
        for line in stdCmdCopyConf.split('\n'):
            if "terraformModuleList.tf" in line:
                stdoutfiltered = '%s %s' % (stdoutfiltered, line)

        return stdoutfiltered



    def mainExecCMD(self, command, var1=None):
        cmdRmFolder = 'rm -fr %s' % (var1)
        cmdTochFile = """touch %s""" % (var1)
        cmdCheckSshAgent = """ps aux | grep ssh-agent | grep -v 'grep'"""
        cmdEnableSshAgent = """eval `ssh-agent -s`"""
        cmdChangeKeyPermission = """ chmod 400 %s""" % (self.git_key_path)
        cmdCheckSshFingerprint = """cat %s | grep 'github.com' """ %(var1)
        cmdAddSshFingerprint = """ssh-keyscan github.com >> %s""" %(var1)
        cmdRepoBranchCheck = """ssh-agent bash -c 'ssh-add %s &>/dev/null;  git ls-remote --heads   %s %s'""" % (self.git_key_path, self.git_link, self.git_branch)
        cmdGitClone = """ssh-agent bash -c 'ssh-add %s &>/dev/null;  git clone --quiet --branch %s %s %s'""" % (self.git_key_path, self.git_branch , self.git_link, self.repository_workspace)
        cmdCopyConf = 'rsync -c -arvh -i --info=COPY --info=REMOVE --delete --no-times --no-perms --no-owner --no-group %s %s/' % (var1, self.terraform_dir)




        options = {'cmdChangeKeyPermission': cmdChangeKeyPermission,'cmdRmFolder': cmdRmFolder, 'cmdTochFile': cmdTochFile, 'cmdCheckSshAgent': cmdCheckSshAgent , 'cmdEnableSshAgent': cmdEnableSshAgent , 'cmdCheckSshFingerprint': cmdCheckSshFingerprint ,'cmdAddSshFingerprint': cmdAddSshFingerprint ,'cmdRepoBranchCheck': cmdRepoBranchCheck ,'cmdGitClone': cmdGitClone ,'cmdCopyConf': cmdCopyConf}

        if command in options:

            cmd = options[command]
            stdout = self.cmdCommunicateOS(cmd)
            return stdout
        else:
            return ("no command defined")


    def rmGitDir(self):
        git_dir = '%s/.git' % (self.repository_workspace)
        if os.path.isdir(git_dir):
            smdRemoveGit = 'rm -fr %s' % (git_dir)
            self.cmdCommunicateOS(smdRemoveGit)
            return 'Git directory removed for project %s/.git' %(self.repository_workspace)



    def cmdCommunicateOS(self, command):
        try:
            proc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,stdin=subprocess.PIPE)
            STDOUT, STDERR = proc.communicate()
        except subprocess.CalledProcessError as e:
            self.logging.writeLogWarning(e.output)
        if STDERR.decode('utf-8') != '':
            self.logging.writeLogWarning('%scommand %s error %s %s' % ('\n' ,command, STDERR.decode('utf-8') ,'\n'))
        return STDOUT.decode('utf-8')




