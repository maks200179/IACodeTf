
from awsCreateModuleTerraform import awsCreateModuleTerraform
from postBuildServer import  postBuildServer
from argparse import ArgumentParser

class buildModuleNoGui():
    
        
    
    def setVarsToFunctionSelf(self):
        self.triggered_module_name     = [self.args.triggered_module]
        self.stage_name                = self.args.stage
        self.command_name              = self.args.command
        

        self.awscreatemoduleterraform = awsCreateModuleTerraform()
        self.postbuildserver = postBuildServer()
        






    def buildDestroySelect(self):
        #QApplication.processEvents()
        if self.command_name == 'build':
            self.build()
        if self.command_name == 'destroy':
            self.destroyModule()
        if self.command_name == 'showDockers':
            for module in self.triggered_module_name:
                self.postCommandShowDockers(module)



    def build(self):

        stdUpdateRepo = self.postbuildserver.copyRepoToServer()
        print(stdUpdateRepo.strip())
        stdUpdateMainTf = self.postbuildserver.copyTfMainModule()
        print (stdUpdateMainTf)
        print ('----------------------------------------------------------------------------')
        

        for module in self.triggered_module_name:
            if not 'network_terraform_conf' in module:
                # check if server online
                stdCheckServer = self.postbuildserver.mainBuildRemoveModule('checkNetModuleIsCreated', module)
                if stdCheckServer is not True:
                    print (stdCheckServer)
                    continue

            
            
           
            
            
            #use aws creds and pass them to env vars 
            stdAwsCreds = self.postbuildserver.exportEnvAwsCredentials()
            if stdAwsCreds is not True:
                    print(stdAwsCreds)
            



            print(('Apply: module %s') % module)
            stdterraform = self.awscreatemoduleterraform.brockerExecCommandTerraform('applyTfConf',module)
            
            print(('Terraform: %s') %(stdterraform))
           


            if not 'network_terraform_conf' in module:

                collectDataFromServerJsonConf = self.postbuildserver.mainBuildRemoveModule('collectModuleDataFromJsonAndCheckIfExist', module)
                if collectDataFromServerJsonConf is not True:
                    print(collectDataFromServerJsonConf)
                    continue

                stdCheckServer = self.postbuildserver.mainBuildRemoveModule('cmdCheckServerOnline', module)
                if stdCheckServer is not True:
                    print (stdCheckServer)
                    continue



                stdCheckServerHasGitDeploy = self.postbuildserver.mainBuildRemoveModule('cmdCheckGitModulesToDeployAndCollectData', module)
                if stdCheckServerHasGitDeploy is True:
                    stdCloneToLocalAndToServer = self.postbuildserver.mainBuildRemoveModule('cmdGitCloneModules', module)

                    print (stdCloneToLocalAndToServer)













                stdCopyModule = self.postbuildserver.mainBuildRemoveModule('cmdRsync',module)
                print (stdCopyModule)

                stdCheckSwarm = self.postbuildserver.mainBuildRemoveModule('checkIfSwarm',module)
                if stdCheckSwarm is True:
                    stdInstallEnv = self.postbuildserver.mainBuildRemoveModule('cmdExecInstallEnv', module)
                    print (stdInstallEnv)
                    stdCheckIfManger = self.postbuildserver.mainBuildRemoveModule('checkIfManger',module)





                    if stdCheckIfManger is True:
                        stdInitSwarmManager = self.postbuildserver.mainBuildRemoveModule('initSwarmManager',module)
                        print (stdInitSwarmManager)
                        rebuildSwarmManager = self.postbuildserver.mainBuildRemoveModule('rebuildSwarmManager',module)
                        print (rebuildSwarmManager)
                        #self.postCommandShowDockers(module)

                    # if not manager then worker
                    if stdCheckIfManger is False:
                        stdConnectWorkerToManager = self.postbuildserver.mainBuildRemoveModule('connectWorkerToManager',module)
                        print (stdConnectWorkerToManager)
                        self.postCommandShowDockers(module)



                else:
                    stdInstallEnv = self.postbuildserver.mainBuildRemoveModule('cmdExecInstallEnv', module)
                    print ('Docker-compose: up info')
                    print (stdInstallEnv)
                    self.postCommandShowDockers(module)
                    

                print ('App: Install server and docker env  done')
                print ('----------------------------------------------------------------------------')
            else:
                print ('App: Install network module done')
                print ('----------------------------------------------------------------------------')




    def postCommandShowDockers(self,module):
        collectDataFromServerJsonConf = self.postbuildserver.mainBuildRemoveModule('collectModuleDataFromJsonAndCheckIfExist',module)
        if collectDataFromServerJsonConf is not True:
            self.textBrowserStd.append(('App: The module %s not installed or not contains dockers') %module)
            return
        stdDockerPs = self.postbuildserver.mainBuildRemoveModule('cmdExecDockerPs',module)
        print ('Docker: dockers on host')
        print (stdDockerPs)



    def destroyModule(self):
        for module in self.triggered_module_name:
            #use aws creds and pass them to env vars 
            stdAwsCreds = self.postbuildserver.exportEnvAwsCredentials()
            if stdAwsCreds is not True:
                print (stdAwsCreds)
            
            print (("Destroying module %s") % module)
            stdterraform = self.awscreatemoduleterraform.brockerExecCommandTerraform('destroyTfModule',module)
            print (('Terraform: %s') %(stdterraform))
            print ('----------------------------------------------------------------------------')



    def getVarsCommandLine(self):
        

        parser = ArgumentParser()
        
        parser.add_argument("--module_to_build", action='store', dest="triggered_module",help="Store triggered module name ", 
                                default=None)
        parser.add_argument("--stage", action='store', dest='stage', help='Store stage name',
                                default=None)
        parser.add_argument("--command", action='store', dest='command', help='Store command value',
                                default=None)
        #parser.add_argument("--infrastracture_repo", action='store', dest='infrastracture_repo_name', help='Store  infrastracture_repo_name value',
                            #default=None)
            #parser.add_argument("--ip", action='store', dest='server_ip_addr', help='Store server ip address ',
            #                    default=None)                    
            #parser.add_argument("--token", action='store', dest='server_token_key', help='Store server token',
            #                    default=None)                    

        self.args = parser.parse_args()

            # for x, y in vars(self.args).items():
            #     print(x, y)
            #
            # for x in vars(self.args):
            #     if x == ('build_all'):
            #         print (vars(self.args)[x])


        return vars(self.args)








def main():
    main = buildModuleNoGui()
    args = main.getVarsCommandLine()



    if  ((args)['triggered_module']) != '':
        main.setVarsToFunctionSelf()
        print ('App: Start %s %s process' % ((args)['triggered_module'],(args)['command']))
        
        
        
        main.buildDestroySelect()
        #main.setEnvVars()
        #main.saveTockenToFile()
        #main.buildSaveAll()

    else:
        print('args --build_all not defined')




if __name__ == "__main__":
    main()



