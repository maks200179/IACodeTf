from PyQt5.QtWidgets import *
from configFileJson import configFileIni
from PyQt5.QtCore import Qt



class gitSettings(QWidget , configFileIni ):
    def __init__(self, parent=None):
        super(gitSettings, self).__init__(parent)


        self.layoutForm1 = QFormLayout(self)

        self.ssh_link = QLineEdit(self)
        self.ssh_link.setText(self.read_conf_file("Git", "ssh_link"))
        self.ssh_link.setEnabled(False)
        self.layoutForm1.addRow(QLabel('SSH Link:'), self.ssh_link)


        self.git_url = QLineEdit(self)
        self.git_url.setText(self.read_conf_file("Git","url"))
        self.layoutForm1.addRow(QLabel('Git URL:'), self.git_url)

        self.git_username = QLineEdit(self)
        self.git_username.setText(self.read_conf_file("Git","Username"))
        self.layoutForm1.addRow(QLabel('Git Username:'), self.git_username)

        self.git_repository_name = QLineEdit(self)
        self.git_repository_name.setText(self.read_conf_file("Git","Repository_Name"))
        self.layoutForm1.addRow(QLabel('Git Repository Name:'), self.git_repository_name)

        self.git_branch = QLineEdit(self)
        self.git_branch.setText(self.read_conf_file("Git","Branch"))
        self.layoutForm1.addRow(QLabel('Git Repository Branch:'), self.git_branch)

        self.btn = QPushButton("Git SSH Key")
        self.btn.clicked.connect(self.getSrcFile)

        self.git_ssh_key_path = QLineEdit(self)
        self.git_ssh_key_path.setText(self.read_conf_file("Git","SSH_Key_Path"))
        self.layoutForm1.addRow(self.btn, self.git_ssh_key_path)


        self.btn1 = QPushButton("Ok")
        self.layoutGorizontal = QHBoxLayout()
        self.layoutGorizontal.addWidget(self.btn1,1,Qt.AlignRight)
        self.layoutGorizontal.addStretch()
        self.layoutForm1.addRow(self.layoutGorizontal)

        self.btn1.clicked.connect(self.writeToConfig)

    def closeWindows(self):
        self.close()


    def messege(self,message):
        QMessageBox.about(self, 'Information', message)


    def getSrcFile(self):
        srcDir = (QFileDialog.getOpenFileName(self, "Select Private SSH Key","")[0])
        self.git_ssh_key_path.setText(srcDir)
        return  srcDir

    def writeToConfig(self):
        # make sure not empty
        if str(self.git_url.text()) != "" and str(self.git_username.text()) != "" and str(self.git_repository_name.text()) != "" and str(self.git_ssh_key_path.text()) != "":
            #make sure de value is same or not if not vrite to conf
            if  not (self.read_conf_file('Git','Url')) == (self.git_url.text()) or  \
                not (self.read_conf_file('Git','Username')) == (self.git_username.text()) or  \
                not (self.read_conf_file('Git','Repository_Name')) == (self.git_repository_name.text()) or  \
                not (self.read_conf_file('Git','Branch')) == (self.git_branch.text()) or  \
                not (self.read_conf_file('Git','SSH_Key_Path')) == (self.git_ssh_key_path.text()):

                #add data and save
                construct_url = 'git@' + str(self.git_url.text() + ':%s' % str(self.git_username.text()) + '/%s.git' % str(self.git_repository_name.text()))
                para_list = []
                para_list.append(['Git','SSH_link',construct_url])
                para_list.append(['Git','Url',str(self.git_url.text())])
                para_list.append(['Git','Username',str(self.git_username.text())])
                para_list.append(['Git','Repository_Name',str(self.git_repository_name.text())])
                para_list.append(['Git','Branch',str(self.git_branch.text())])
                para_list.append(['Git','SSH_Key_Path', str(self.git_ssh_key_path.text())])

                self.write_to_conf_file(para_list)
                self.messege("Wrote to config")
            self.closeWindows()

        else:
            print("the value to write is empty")

    def main(self):


            self.exgit = gitSettings()
            if not self.exgit.isActiveWindow():
                self.exgit.setWindowTitle("Git Settings Windows")
                self.exgit.resize(600, 150)
                self.exgit.show()
