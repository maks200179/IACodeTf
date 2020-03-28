#-*- coding:utf-8 -*-


from PyQt5.QtWidgets import (QWidget,QTextBrowser,QGridLayout,QVBoxLayout,QPushButton,QApplication,QHBoxLayout)
from PyQt5.QtCore import (Qt,pyqtSlot)
from PyQt5.QtGui import QTextCursor
from configFileJson import configFileIni
#from gitHubCopyRepository import gitHubCopyRepo
from awsCreateModuleTerraform import awsCreateModuleTerraform
from postBuildServer import  postBuildServer
from loggingGlobal import loggingGlobal
#import sys
#import time
import re



class buildModule(QWidget , configFileIni ):
    def __init__(self,moduls,command, parent=None):
        super(buildModule, self).__init__(parent)

        self.modulsName = moduls

        self.awscreatemoduleterraform = awsCreateModuleTerraform()
        self.postbuildserver = postBuildServer()
        self.logging = loggingGlobal()
        # init jenkins
        
        





        layout = QGridLayout()
        layout.setSpacing(10)


        self.textBrowserStd =QTextBrowser()
        self.textBrowserStd.setObjectName("Process Text")
        self.textBrowserStd.setStyleSheet("QFrame {background-color: rgb(66,244,217);}")
        self.textBrowserStd.resize(100,100)
        #self.textBrowserStd.AutoFormattingFlag()

        self.cursor = QTextCursor()
        self.cursor = self.textBrowserStd.textCursor()

        self.cursor1 = QTextCursor()
        self.cursor1 = self.textBrowserStd.textCursor()

        self.cursor2 = QTextCursor()
        self.cursor2 = self.textBrowserStd.textCursor()



        self.layoutVertical = QVBoxLayout()
        self.layoutVertical.addWidget(self.textBrowserStd, stretch=1)

        layout.addItem(self.layoutVertical,2,0)

        self.btn1 = QPushButton("Ok")
        self.btn1.setEnabled(False)

        self.layoutGorizontal = QHBoxLayout()
        self.layoutGorizontal.addWidget(self.btn1, 1, Qt.AlignRight)
        self.layoutGorizontal.addStretch()
        layout.addItem(self.layoutGorizontal)

        self.btn1.clicked.connect(self.closeWindows)

        self.setLayout(layout)




    def closeWindows(self):
        self.close()




        #QApplication.processEvents()


    def buildDestroySelect(self,command):
        QApplication.processEvents()
        if command == 'build':
            self.buildModule()
        if command == 'destroy':
            self.destroyModule()
        if command == 'showDockers':
            for module in self.modulsName:
                self.postCommandShowDockers(module)












    def buildModule(self):

        stdUpdateRepo = self.postbuildserver.copyRepoToServer()
        self.textBrowserStd.append(stdUpdateRepo.strip())
        stdUpdateMainTf = self.postbuildserver.copyTfMainModule()
        self.textBrowserStd.append(stdUpdateMainTf)
        self.textBrowserStd.append('----------------------------------------------------------------------------')


        for module in self.modulsName:
            if not 'network_terraform_conf' in module:
                # check if server online
                stdCheckServer = self.postbuildserver.mainBuildRemoveModule('checkNetModuleIsCreated', module)
                if stdCheckServer is not True:
                    self.textBrowserStd.append(stdCheckServer)
                    continue

            
            
           
            
            
            #use aws creds and pass them to env vars 
            stdAwsCreds = self.postbuildserver.exportEnvAwsCredentials()
            if stdAwsCreds is not True:
                self.textBrowserStd.append(stdAwsCreds)
            



            self.textBrowserStd.append(('Apply: module %s') % module)
            QApplication.processEvents()
            stdterraform = self.awscreatemoduleterraform.brockerExecCommandTerraform('applyTfConf',module)
            self.textBrowserStd.append(('Terraform: %s') %(stdterraform))
            QApplication.processEvents()



            if not 'network_terraform_conf' in module:

                collectDataFromServerJsonConf = self.postbuildserver.mainBuildRemoveModule('collectModuleDataFromJsonAndCheckIfExist', module)
                if collectDataFromServerJsonConf is not True:
                    self.textBrowserStd.append(collectDataFromServerJsonConf)
                    continue

                stdCheckServer = self.postbuildserver.mainBuildRemoveModule('cmdCheckServerOnline', module)
                if stdCheckServer is not True:
                    self.textBrowserStd.append(stdCheckServer)
                    continue



                stdCheckServerHasGitDeploy = self.postbuildserver.mainBuildRemoveModule('cmdCheckGitModulesToDeployAndCollectData', module)
                if stdCheckServerHasGitDeploy is True:
                    stdCloneToLocalAndToServer = self.postbuildserver.mainBuildRemoveModule('cmdGitCloneModules', module)

                    self.textBrowserStd.append(stdCloneToLocalAndToServer)













                QApplication.processEvents()
                stdCopyModule = self.postbuildserver.mainBuildRemoveModule('cmdRsync',module)
                self.textBrowserStd.append(stdCopyModule)

                stdCheckSwarm = self.postbuildserver.mainBuildRemoveModule('checkIfSwarm',module)
                if stdCheckSwarm is True:
                    stdInstallEnv = self.postbuildserver.mainBuildRemoveModule('cmdExecInstallEnv', module)
                    self.textBrowserStd.append(stdInstallEnv)
                    stdCheckIfManger = self.postbuildserver.mainBuildRemoveModule('checkIfManger',module)





                    if stdCheckIfManger is True:
                        stdInitSwarmManager = self.postbuildserver.mainBuildRemoveModule('initSwarmManager',module)
                        self.textBrowserStd.append(stdInitSwarmManager)
                        rebuildSwarmManager = self.postbuildserver.mainBuildRemoveModule('rebuildSwarmManager',module)
                        self.textBrowserStd.append(rebuildSwarmManager)
                        QApplication.processEvents()
                        self.postCommandShowDockers(module)

                    # if not manager then worker
                    if stdCheckIfManger is False:
                        stdConnectWorkerToManager = self.postbuildserver.mainBuildRemoveModule('connectWorkerToManager',module)
                        self.textBrowserStd.append(stdConnectWorkerToManager)
                        QApplication.processEvents()
                        self.postCommandShowDockers(module)



                else:
                    QApplication.processEvents()
                    stdInstallEnv = self.postbuildserver.mainBuildRemoveModule('cmdExecInstallEnv', module)
                    self.textBrowserStd.append('Docker-compose: up info')
                    self.textBrowserStd.append(stdInstallEnv)
                    QApplication.processEvents()
                    self.postCommandShowDockers(module)
                    QApplication.processEvents()


                self.textBrowserStd.append('App: Install server and docker env  done')
                self.textBrowserStd.append('----------------------------------------------------------------------------')
            else:
                self.textBrowserStd.append('App: Install network module done')
                self.textBrowserStd.append('----------------------------------------------------------------------------')

    def postCommandShowDockers(self,module):
        collectDataFromServerJsonConf = self.postbuildserver.mainBuildRemoveModule('collectModuleDataFromJsonAndCheckIfExist',module)
        if collectDataFromServerJsonConf is not True:
            self.textBrowserStd.append(('App: The module %s not installed or not contains dockers') %module)
            return
        stdDockerPs = self.postbuildserver.mainBuildRemoveModule('cmdExecDockerPs',module)
        self.textBrowserStd.append('Docker: dockers status info table')
        self.insertTableToTextBrowser(stdDockerPs)



#Here i cant put data from bash ,for dinamik amount of fields HELP!

    def insertTableToTextBrowser(self,data):
        count = 0
        wordln = 1
        rownum = data.count('\n')
        for row1 in data.split('\n'):
            if count != 2:
                count = count + 1
                continue
            else:
                if row1 != '':
                    wordln = len(re.split(r"\s{2,}", row1))
                    count = count + 1



        self.cursor.insertTable(rownum, wordln)

        for row in data.split('\n'):
            for word in re.split(r"\s{2,}", row):
                self.cursor.insertText(word)
                self.cursor.movePosition(QTextCursor.NextCell)



    def destroyModule(self):
        for module in self.modulsName:
            QApplication.processEvents()
            #use aws creds and pass them to env vars 
            stdAwsCreds = self.postbuildserver.exportEnvAwsCredentials()
            if stdAwsCreds is not True:
                self.textBrowserStd.append(stdAwsCreds)
            
            self.textBrowserStd.append(("Destroying module %s") % module)
            stdterraform = self.awscreatemoduleterraform.brockerExecCommandTerraform('destroyTfModule',module)
            self.textBrowserStd.append(('Terraform: %s') %(stdterraform))
            self.textBrowserStd.append('----------------------------------------------------------------------------')



    def main(self,moduls,command):
        #self.bumd = threading.Thread(target=buildModule(moduls,command)).start()
        self.bumd = buildModule(moduls,command)
        if not self.bumd.isActiveWindow():
            self.bumd.setWindowTitle("Build A Module Windows")
            self.bumd.resize(800, 600)
            self.bumd.show()
            self.bumd.textBrowserStd.append('App: Start %s process' % (command))
            self.bumd.textBrowserStd.append('----------------------------------------------------------------------------')
            self.bumd.buildDestroySelect(command)
            self.bumd.btn1.setDisabled(False)
        else:
            self.logging.writeLogCritical('the buildwindows run more then once')







