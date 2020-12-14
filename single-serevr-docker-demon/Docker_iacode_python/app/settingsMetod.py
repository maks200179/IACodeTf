from PyQt5.QtWidgets import *
from configFileJson import configFileIni


class settingsMetod(QWidget,configFileIni):
    def __init__(self, parent=None):
        super(settingsMetod, self).__init__(parent)

        self.b1 = QCheckBox("ssh")
        self.b2 = QCheckBox("socket")
        #print (self.read_conf_file("communicationSettings","protocol","ssh"))
        self.b1.setChecked(self.read_conf_file("communicationSettings","protocol","ssh"))
        self.b2.setChecked(self.read_conf_file("communicationSettings","protocol","socket"))

        self.b1.toggled.connect(lambda: self.btnstate(self.b1))
        self.b2.toggled.connect(lambda: self.btnstate(self.b2))

        if self.b1.isChecked() == True:
            self.b2.setEnabled(False)

        if self.b2.isChecked() == True:
            self.b1.setEnabled(False)

        self.layoutForm = QFormLayout(self)
        self.l2 = QLabel("Please Set Transfer Protocol:")
        self.hbox = QHBoxLayout()

        self.hbox.addWidget(self.b1)
        self.hbox.addWidget(self.b2)
        self.hbox.addStretch()

        self.layoutForm.addRow(self.l2 , self.hbox)

    def btnstate(self, b):
        para_list = []
        if b.text() == "ssh":
            if b.isChecked() == True:
                self.b2.setEnabled(False)
                para_list.append(["communicationSettings","protocol",str(b.text())])
                self.write_to_conf_file(para_list)
            else:
                self.b2.setEnabled(True)

        if b.text() == "socket":
            if b.isChecked() == True:
                self.b1.setEnabled(False)
                para_list.append(["communicationSettings", "protocol", str(b.text())])
                self.write_to_conf_file(para_list)
            else:
                self.b1.setEnabled(True)

    def main(self):
            self.exmetod = settingsMetod()
            self.exmetod.setWindowTitle("Settings Windows")
            self.exmetod.resize(350,50)
            self.exmetod.show()

if __name__ != "__main__":
    pass

else:
    print ('only executable if not main')