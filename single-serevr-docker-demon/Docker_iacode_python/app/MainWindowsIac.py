 #!/usr/bin/env python
#-*- coding:utf-8 -*-



from PyQt5.QtCore import (Qt,QEvent,QObject)
from PyQt5.QtGui import (QKeySequence,QMouseEvent)
from PyQt5.QtWidgets import (QAction, QActionGroup, QApplication, QFrame,
                             QLabel, QMainWindow, QMenu, QMessageBox,
                             QSizePolicy, QVBoxLayout,QListWidget,
                             QAbstractItemView,QWidget)
from gitSettings import gitSettings
from awsSettings import awsSettings
from modulsList import modulsList
#from gitHubCopyRepository import gitHubCopyRepo
from configFileJson import configFileIni
from buildModule import buildModule
import time
import re
import os





class MainWindow(QMainWindow , configFileIni):
    def __init__(self):
        super(MainWindow, self).__init__()





        #pass to class mymodules
        self.gitsettings = gitSettings()
        self.awssettings = awsSettings()
        self.modulslist =  modulsList()
        #self.githubcopyrepo = gitHubCopyRepo()
        self.buildmodule = buildModule(moduls=None,command=None)
        #self.configFile = configFileIni()



        widget = QWidget()
        self.setCentralWidget(widget)

        topFiller = QWidget()
        topFiller.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)




        self.listWidget = QListWidget(self)
        self.listWidget.setContextMenuPolicy(Qt.ActionsContextMenu)
        self.listWidget.setAlternatingRowColors(True)
        self.listWidget.setSelectionMode(QAbstractItemView.MultiSelection)
        self.listWidget.setWordWrap(True)
        self.listWidget.setObjectName("listWidget")
        self.getAllModules()







        vbox = QVBoxLayout()
        vbox.setContentsMargins(5, 5, 5, 5)
        vbox.addWidget(topFiller)
        vbox.addWidget(self.listWidget,stretch=1)


        #vbox.addWidget(bottomFiller)
        widget.setLayout(vbox)


        self.createActions()
        self.createMenus()

        message = "A context menu is available by right-clicking"
        self.statusBar().showMessage(message)

        self.setWindowTitle("Menus")
        self.setMinimumSize(160, 160)
        self.resize(480, 320)
        #(os.setenv("CLICOLOR", "0"))
        os.environ["CLICOLOR"] = "0"
        #self.messege (os.getenv("CLICOLOR", "1"))
        #self.messege (os.environ.get('CLICOLOR'))




    def eventFilter(self, obj, event):

        if event.type() == QEvent.MouseButtonPress and event.button() == Qt.RightButton:
            return False
        elif event.type() == QEvent.MouseButtonRelease and event.button() == Qt.RightButton:
            return True
        else:
             return False


    def contextMenuEvent(self, event):

        menu = QMenu(self)
        menu.installEventFilter(self)
        #menu.addAction(self.cutAct)
        #menu.addAction(self.copyAct)
        #menu.addAction(self.pasteAct)
        menu.addAction(self.buildModule)
        menu.addAction(self.destroyModule)
        menu.addAction(self.refreshModuls)
        menu.addAction(self.getDockersList)
        #menu.exec_(self.mapToGlobal(QPoint(0, 0)))
        #menu.exec_(event.screenPos())
        #menu.exec_(QCursor.pos())
        #menu.exec_(QCursor.pos())
        menu.exec_(self.mapToGlobal(event.pos()))






    def gitSettingsWindows(self):
        self.gitsettings.main()

    def addNewModuleWindows(self):
        self.modulslist.main()

    def awsSettingsWindows(self):
        self.awssettings.main()

    def buildModuleAWS(self):
        moduls = self.getSelectedModules()
        #print (moduls)
        command = 'build'
        self.buildmodule.main(moduls,command)
        #self.buildmodule.main(moduls,command)
        #time.sleep(5)

        #self.buildmodule.buildModule()
        #sdtin = (self.githubcopyrepo.main())
        #self.messege(sdtin)
        #for module in moduls:
            #for line in module:
               # self.messege(line)



    def destroyModuleAWS(self):
        moduls = self.getSelectedModulesNetworkAtEnd()
        #print (moduls)
        command='destroy'
        self.buildmodule.main(moduls,command)


        #self.buildmodule.destroyModule()
        #sdtin = (self.githubcopyrepo.main())
        #self.messege(sdtin)
        #for module in moduls:
            #for line in module:
               # self.messege(line)


    def newFile(self):
        self.listWidget.addItem("Invoked <b>File|New</b>")

    def open(self):
        self.listWidget.addItem("Invoked <b>File|Open</b>")

    def save(self):
        self.listWidget.addItem("Invoked <b>File|Save</b>")

    def print_(self):
        self.listWidget.addItem("Invoked <b>File|Print</b>")

    def undo(self):
        self.listWidget.addItem("Invoked <b>Edit|Undo</b>")

    def redo(self):
        self.listWidget.addItem("Invoked <b>Edit|Redo</b>")

    def cut(self):
        self.listWidget.addItem("Invoked <b>Edit|Cut</b>")

    def copy(self):
        self.listWidget.addItem("Invoked <b>Edit|Copy</b>")

    def paste(self):
        self.listWidget.addItem("Invoked <b>Edit|Paste</b>")

    def bold(self):
        self.listWidget.addItem("Invoked <b>Edit|Format|Bold</b>")

    def italic(self):
        self.listWidget.addItem("Invoked <b>Edit|Format|Italic</b>")

    def leftAlign(self):
        self.listWidget.addItem("Invoked <b>Edit|Format|Left Align</b>")

    def rightAlign(self):
        self.listWidget.addItem("Invoked <b>Edit|Format|Right Align</b>")

    def justify(self):
        self.listWidget.addItem("Invoked <b>Edit|Format|Justify</b>")

    def center(self):
        self.listWidget.addItem("Invoked <b>Edit|Format|Center</b>")

    def setLineSpacing(self):
        self.listWidget.addItem("Invoked <b>Edit|Format|Set Line Spacing</b>")

    def setParagraphSpacing(self):
        self.listWidget.addItem("Invoked <b>Edit|Format|Set Paragraph Spacing</b>")

    def about(self):
        self.listWidget.addItem("Invoked <b>Help|About</b>")
        QMessageBox.about(self, "About Menu",
                          "The <b>Menu</b> example shows how to create menu-bar menus "
                          "and context menus.")

    def aboutQt(self):
        self.listWidget.addItem("Invoked <b>Help|About Qt</b>")


    def getAllModules(self):
        self.listWidget.clear()
        for item in (self.get_secton_values('ModulsList')):
            self.listWidget.addItem('\n'.join(item.split()))



    def getSelectedModules(self):
        items = self.listWidget.selectedItems()
        listClSelected = []
        for element in (items):
            pattern = 'network_terraform'
            if re.search(pattern,(element.text())):
                listClSelected.insert(0,element.text())
                continue
            listClSelected.append(element.text())
        return (listClSelected)

    def getSelectedModulesNetworkAtEnd(self):
        items = self.listWidget.selectedItems()
        listClSelected = []
        for element in (items):
            pattern = 'docker_compose_env'
            if re.search(pattern, (element.text())):
                listClSelected.insert(0, element.text())
                continue
            listClSelected.append(element.text())
        return (listClSelected)


    def refreshModuleList(self):
        self.getAllModules()

    def getDockersTable(self):
        moduls = self.getSelectedModules()
        command = 'showDockers'
        self.buildmodule.main(moduls,command)


    def messege(self,message):
        QMessageBox.about(self, 'Information', message)



    def createActions(self):

        self.gitSettingss = QAction("&Git Settings", self,shortcut="Ctrl+G",
                              statusTip="Git settings", triggered=self.gitSettingsWindows)

        self.modulsListss = QAction("&Add Module Name", self, shortcut="Alt+M",
                                    statusTip="Add module", triggered=self.addNewModuleWindows)

        self.awsSettingss = QAction("&AWS Settings", self,shortcut="Ctrl+A",
                              statusTip="AWS settings", triggered=self.awsSettingsWindows)

        self.buildModule = QAction("&Build Module", self, shortcut="Alt+B",
                                statusTip="Build Selected Module and Env ", triggered=self.buildModuleAWS)

        self.destroyModule = QAction("&Destroy Module", self, shortcut="Alt+B",
                                statusTip="Destroy Selected Module and Env ", triggered=self.destroyModuleAWS)

        self.refreshModuls = QAction("&Refresh", self, shortcut="Alt+R",
                                   statusTip="Refresh Module List", triggered=self.refreshModuleList)

        self.getDockersList = QAction("&Get Dockers", self, shortcut="Alt+G",
                                   statusTip="Get Dockers List Installed", triggered=self.getDockersTable)





        self.newAct = QAction("&New", self, shortcut=QKeySequence.New,
                              statusTip="Create a new file", triggered=self.newFile)

        self.openAct = QAction("&Open...", self, shortcut=QKeySequence.Open,
                               statusTip="Open an existing file", triggered=self.open)

        self.saveAct = QAction("&Save", self, shortcut=QKeySequence.Save,
                               statusTip="Save the document to disk", triggered=self.save)

        self.printAct = QAction("&Print...", self, shortcut=QKeySequence.Print,
                                statusTip="Print the document", triggered=self.print_)

        self.exitAct = QAction("E&xit", self, shortcut="Ctrl+Q",
                               statusTip="Exit the application", triggered=self.close)

        self.undoAct = QAction("&Undo", self, shortcut=QKeySequence.Undo,
                               statusTip="Undo the last operation", triggered=self.undo)

        self.redoAct = QAction("&Redo", self, shortcut=QKeySequence.Redo,
                               statusTip="Redo the last operation", triggered=self.redo)

        self.cutAct = QAction("Cu&t", self, shortcut=QKeySequence.Cut,
                              statusTip="Cut the current selection's contents to the clipboard",
                              triggered=self.cut)

        self.copyAct = QAction("&Copy", self, shortcut=QKeySequence.Copy,
                               statusTip="Copy the current selection's contents to the clipboard",
                               triggered=self.copy)

        self.pasteAct = QAction("&Paste", self, shortcut=QKeySequence.Paste,
                                statusTip="Paste the clipboard's contents into the current selection",
                                triggered=self.paste)

        self.boldAct = QAction("&Bold", self, checkable=True,
                               shortcut="Ctrl+B", statusTip="Make the text bold",
                               triggered=self.bold)

        boldFont = self.boldAct.font()
        boldFont.setBold(True)
        self.boldAct.setFont(boldFont)

        self.italicAct = QAction("&Italic", self, checkable=True,
                                 shortcut="Ctrl+I", statusTip="Make the text italic",
                                 triggered=self.italic)

        italicFont = self.italicAct.font()
        italicFont.setItalic(True)
        self.italicAct.setFont(italicFont)

        self.setLineSpacingAct = QAction("Set &Line Spacing...", self,
                                         statusTip="Change the gap between the lines of a paragraph",
                                         triggered=self.setLineSpacing)

        self.setParagraphSpacingAct = QAction("Set &Paragraph Spacing...",
                                              self, statusTip="Change the gap between paragraphs",
                                              triggered=self.setParagraphSpacing)

        self.aboutAct = QAction("&About", self,
                                statusTip="Show the application's About box",
                                triggered=self.about)

        self.aboutQtAct = QAction("About &Qt", self,
                                  statusTip="Show the Qt library's About box",
                                  triggered=self.aboutQt)
        self.aboutQtAct.triggered.connect(QApplication.instance().aboutQt)

        self.leftAlignAct = QAction("&Left Align", self, checkable=True,
                                    shortcut="Ctrl+L", statusTip="Left align the selected text",
                                    triggered=self.leftAlign)

        self.rightAlignAct = QAction("&Right Align", self, checkable=True,
                                     shortcut="Ctrl+R", statusTip="Right align the selected text",
                                     triggered=self.rightAlign)

        self.justifyAct = QAction("&Justify", self, checkable=True,
                                  shortcut="Ctrl+J", statusTip="Justify the selected text",
                                  triggered=self.justify)

        self.centerAct = QAction("&Center", self, checkable=True,
                                 shortcut="Ctrl+C", statusTip="Center the selected text",
                                 triggered=self.center)

        self.alignmentGroup = QActionGroup(self)
        self.alignmentGroup.addAction(self.leftAlignAct)
        self.alignmentGroup.addAction(self.rightAlignAct)
        self.alignmentGroup.addAction(self.justifyAct)
        self.alignmentGroup.addAction(self.centerAct)
        self.leftAlignAct.setChecked(True)

    def createMenus(self):
        self.fileMenu = self.menuBar().addMenu("&File")

        self.settings = self.fileMenu.addMenu("Settings")
        self.settings.addAction(self.gitSettingss)
        self.settings.addAction(self.modulsListss)
        self.settings.addAction(self.awsSettingss)

        self.fileMenu.addAction(self.newAct)
        self.fileMenu.addAction(self.openAct)
        self.fileMenu.addAction(self.saveAct)
        self.fileMenu.addAction(self.printAct)
        self.fileMenu.addSeparator()
        self.fileMenu.addAction(self.exitAct)


        self.editMenu = self.menuBar().addMenu("&Edit")
        self.editMenu.addAction(self.undoAct)
        self.editMenu.addAction(self.redoAct)
        self.editMenu.addSeparator()
        self.editMenu.addAction(self.cutAct)
        self.editMenu.addAction(self.copyAct)
        self.editMenu.addAction(self.pasteAct)
        self.editMenu.addSeparator()


        self.helpMenu = self.menuBar().addMenu("&Help")
        self.helpMenu.addAction(self.aboutAct)
        self.helpMenu.addAction(self.aboutQtAct)

        self.formatMenu = self.editMenu.addMenu("&Format")
        self.formatMenu.addAction(self.boldAct)
        self.formatMenu.addAction(self.italicAct)
        self.formatMenu.addSeparator().setText("Alignment")
        self.formatMenu.addAction(self.leftAlignAct)
        self.formatMenu.addAction(self.rightAlignAct)
        self.formatMenu.addAction(self.justifyAct)
        self.formatMenu.addAction(self.centerAct)
        self.formatMenu.addSeparator()
        self.formatMenu.addAction(self.setLineSpacingAct)
        self.formatMenu.addAction(self.setParagraphSpacingAct)


if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())