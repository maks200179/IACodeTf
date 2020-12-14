#-*- coding:utf-8 -*-

import os,subprocess
from loggingGlobal import loggingGlobal
from configFileJson import configFileIni

class awsCreateModuleTerraform(configFileIni):
    def __init__(self):
        super(awsCreateModuleTerraform, self).__init__()
        self.logging = loggingGlobal()

        #self.moduleName = module


    def setVarsToFunctionSelf(self,moduleName):
        self.git_repo_name = self.read_conf_file('Git', 'repository_name')

        self.module_workspace = '%s/moduls/%s/%s' % (self.detectFileDir(),self.git_repo_name,moduleName)
        self.terraform_workspace = '%s/terraform/' %(self.detectFileDir())


    def detectFileDir(self):
        dirname = os.path.dirname(os.path.abspath(__file__))
        return dirname

    def checkTerraformConfigModuleExist(self,moduleName):
        config_name = '%s/%s.tf' %(self.module_workspace,moduleName)
        if os.path.isfile(config_name):
            pass
        else:
           return "\nTerraformConfigFile Not Exist %s" %config_name




    def brockerExecCommandTerraform(self,command,module):
        self.setVarsToFunctionSelf(module)
        self.checkTerraformConfigModuleExist(module)


        if command == 'applyTfConf':
            std_in = self.mainTerraformCommand('cmdTerraFormInit',module)
            if std_in == '':
                return 'Terraform init error check log'

            terraformPlanStatus = self.mainTerraformCommand('cmdTerraformPlan',module)
            if 'No changes. Infrastructure is up-to-date' in terraformPlanStatus:
                return terraformPlanStatus
            else:
                stdout = self.mainTerraformCommand('cmdTerraformApply',module)
                if stdout == '':
                    return "Terraform : An error acured during install module"
                else:
                    return stdout


        elif command == 'destroyTfModule':
            stdout = self.mainTerraformCommand('cmdTerraformDestroy',module)
            if stdout == '':
                return "Terraform : An error acured during destroy module"
            return stdout







    def mainTerraformCommand(self, command, module=None):
        cmdTerraformPlan = """cd %s && terraform plan -no-color -target=module.%s | grep 'No changes. Infrastructure is up-to-date'""" % (self.terraform_workspace, module)
        cmdTerraFormInit = """cd %s  && terraform init -no-color -input=false  | grep 'Terraform has been successfully initialized' """ % (self.terraform_workspace)
        cmdTerraformApply = """cd %s  && terraform apply -no-color -input=false -auto-approve  -backup=./bck_tf_state/%s_bck.tf -target=module.%s | grep 'Apply complete! Resources:' """ % (self.terraform_workspace, module, module)
        cmdTerraformDestroy = """cd %s  && terraform destroy -no-color -input=false -auto-approve -target=module.%s | grep 'Destroy complete! Resources:'""" % (self.terraform_workspace, module)



        options = {'cmdTerraformPlan': cmdTerraformPlan, 'cmdTerraFormInit': cmdTerraFormInit, 'cmdTerraformApply': cmdTerraformApply , 'cmdTerraformDestroy': cmdTerraformDestroy}

        if command in options:
            cmd1 = options[command]
            stdout = self.cmdCommunicateOS(cmd1)
            self.logging.writeLogWarning(stdout)
            return stdout.strip()
        else:
            return ("no command defined")









    def cmdCommunicateOS(self, command):
        try:
            proc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                    stdin=subprocess.PIPE)
            STDOUT, STDERR = proc.communicate()


        except subprocess.CalledProcessError as e:
            self.logging.writeLogWarning(e.output)

        if STDERR.decode('utf-8') != '':
            self.logging.writeLogWarning('%scommand %s error %s %s' % ('\n' ,command, STDERR.decode('utf-8') ,'\n'))

        return STDOUT.strip().decode('utf-8')



