from PyQt5.QtWidgets import (QWidget,QFormLayout,QLineEdit,QLabel,QPushButton,QHBoxLayout,QMessageBox)
from configFileJson import configFileIni
from PyQt5.QtCore import Qt
#import sys


class awsSettings(QWidget , configFileIni ):
    def __init__(self, parent=None):
        super(awsSettings, self).__init__(parent)


        self.layoutForm1 = QFormLayout(self)

        self.region = QLineEdit(self)
        self.region.setText(self.read_conf_file("AWS", "region"))
        self.layoutForm1.addRow(QLabel('AWS Region:'), self.region)

        self.access_key = QLineEdit(self)
        self.access_key.setText(self.read_conf_file("AWS","accesskey"))
        self.layoutForm1.addRow(QLabel('AWS Access Key:'), self.access_key)

        self.secret_key = QLineEdit(self)
        self.secret_key.setText(self.read_conf_file("AWS","secretkey"))
        self.layoutForm1.addRow(QLabel('AWS Secret Key:'), self.secret_key)


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

    def writeToConfig(self):
        if  str(self.region.text()) != "" and str(self.secret_key.text()) != "" and str(self.access_key.text()) != "":
            if not (self.read_conf_file('AWS', 'region')) == (self.region.text()) or \
               not (self.read_conf_file('AWS','accesskey')) == (self.access_key.text()) or \
               not (self.read_conf_file('AWS','secretkey')) == (self.secret_key.text()):

                para_list = []
                para_list.append(['AWS', 'region',  str(self.region.text())])
                para_list.append(['AWS','accesskey',str(self.access_key.text())])
                para_list.append(['AWS','secretkey',str(self.secret_key.text())])
                self.write_to_conf_file(para_list)
                self.messege("Wrote to config")

            self.closeWindows()

        else:
            self.messege("one or more of fields is empty")

    def main(self):


            self.exaws = awsSettings()
            if not self.exaws.isActiveWindow():
                self.exaws.setWindowTitle("AWS Settings Windows")
                self.exaws.resize(600, 150)
                self.exaws.show()
