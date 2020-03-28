from PyQt5.QtWidgets import *
from configFileJson import configFileIni


class modulsList(QWidget , configFileIni ):
    def __init__(self, parent=None):
        super(modulsList, self).__init__(parent)

        self.layoutForm1 = QFormLayout(self)

        self.module_name = QLineEdit(self)
        self.layoutForm1.addRow(QLabel('Module Mame:'),self.module_name)

        self.btn1 = QPushButton("AddClient")
        self.btn2 = QPushButton("Ok")

        self.layoutGorizontal = QHBoxLayout()
        self.layoutGorizontal.addWidget(self.btn1)
        self.layoutGorizontal.addStretch()
        self.layoutGorizontal.addWidget(self.btn2)

        self.layoutForm1.addRow(self.layoutGorizontal)

        self.btn1.clicked.connect(self.writeToConfig)
        self.btn2.clicked.connect(self.closeWindows)




    def closeWindows(self):
        self.close()


    def messege(self,message):
        QMessageBox.about(self, 'Information', message)


    def writeToConfig(self):
        if str(self.module_name.text()) != "" :
            if  str(self.module_name.text()) not in (self.get_secton_values('ModulsList')):
                para_list = []
                count_modules = 1
                for line in (self.get_secton_values('ModulsList')):
                    para_list.append(['ModulsList',str(count_modules),str(line)])
                    count_modules = count_modules + 1
                para_list.append(['ModulsList',str(count_modules),str(self.module_name.text())])

                self.write_to_conf_file(para_list)
                self.messege("Appended to config")

            else:
                self.messege("module already exist")

        else:
            self.messege("the module name to write is empty")

    def main(self):


            self.exml = modulsList()
            if not self.exml.isActiveWindow():
                self.exml.setWindowTitle("Git Settings Windows")
                self.exml.resize(600, 100)
                self.exml.show()