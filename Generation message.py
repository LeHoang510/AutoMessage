from PyQt5.QtWidgets import QApplication
import sys
from PyQt5.QtWidgets import QMainWindow, QTextEdit, QVBoxLayout, QHBoxLayout, QComboBox, QTabWidget, QPushButton
from PyQt5.QtWidgets import QMenu, QAction, QToolBar, QFileDialog, QMessageBox
from PyQt5.QtWidgets import QLabel, QWidget, QGridLayout
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
import pyperclip
import json
import keyboard


# ============================================================================= #
# Class text
class Text(QTextEdit):

    # Constructor
    def __init__(self):
        QTextEdit.__init__(self)
        self.show()

    # Display text
    def display(self, t):
        cursor = self.textCursor()
        cursor.insertText(t)

    # Delete text
    def delete(self):
        self.setPlainText("")

# Class App
class Window(QMainWindow):
    def __init__(self,saving="save.json",output=""):

        # Input-output management
        if output == "":
            self.out = self
        else:
            self.out = output
        # Read json file
        self.jsonReader(saving)
        # Show widget
        QMainWindow.__init__(self)
        self.init_ui()
        self.show()
        self.updateForm()

    def jsonReader(self,saving):
        # Read json saving file
        try:
            f = open(saving, 'r')
        except IOError:
            print("The json file is not found - " + saving)
        else:
            try:
                # Load json file
                self.infor = json.load(f)
            except:
                print("Failed to load json file - " + saving)
            f.close()
            # Save json file name
            self.savingFile = saving

        if self.infor["json"]!="":
            # Read json permalien file
            self.jsonOpen(self.infor["json"])

    def jsonOpen(self, f):
        try:  # ERROR
            g = open(f[0], 'r')
        except IOError:
            print("The json file is not found - " + f[0])
        else:
            try:
                # Load json file
                self.perma = json.load(g)
            except:
                print("Failed to load json file - " + f[0])
            g.close()

    #==================================================================MENU======================================================================#
    # Add options to the menu
    def addChoiceMenu(self, text, menu, function, image=""):
        action = QAction(text, self)
        if image != "": action.setIcon(QIcon(image))
        menu.addAction(action)
        action.triggered.connect(function)
        return action
    # Adding the Files menu
    def addMenuFiles(self):
        # Menu Files
        self.menuFile = QMenu("&Menu")
        self.menubar.addMenu(self.menuFile)
        # Button
        self.actionOpen = self.addChoiceMenu("&Ouvrir le fichier permalien", self.menuFile, self.openClicked, "./Icons/Open.png")                               # Open
        self.actionCopy = self.addChoiceMenu("&Copier", self.menuFile, self.copyClicked, "./Icons/Copy.png")                               # Copy
        self.actionDelete= self.addChoiceMenu("&Effacer", self.menuFile, self.deleteTextClicked,"./Icons/Eraser.png")                # Delete
        # self.actionExecute = self.addChoiceMenu("&Ex??cuter", self.menuFile, self.generateClicked,"./Icons/Execute.png")                   # Execute
        self.actionInformations = self.addChoiceMenu("&Information", self.menuFile, self.informationsClicked,"./Icons/Information.png") # Information
        self.actionQuit = self.addChoiceMenu("&Quit", self.menuFile, self.close, "./Icons/Quit.png")                                     # Quit
    def addMenu(self):
        self.menubar = self.menuBar()
        self.addMenuFiles()
    # ==================================================================MENU======================================================================#

    # =================================================================TOOLBAR====================================================================#
    # Toolbar
    def addTool(self):
        self.toolBar = self.addToolBar("Shortcuts")
        # Add Button
        self.toolBar.addAction(self.actionOpen)
        self.toolBar.addAction(self.actionDelete)
        self.toolBar.addAction(self.actionCopy)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.actionInformations)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.actionQuit)
    # =================================================================TOOLBAR====================================================================#


    # ==================================================================FORM======================================================================#
    def tabPersonne(self):
        # Create tab personne
        self.personneWidget = QWidget()
        # Create layout
        self.gridP = QGridLayout()

        self.label={}
        self.edit={}
        list=["Nom","Pr??nom","Pr??nom P??re","Nom et Pr??nom M??re","R??giment","Page","Indice","Registre","Permalien"]
        for i in list:
            self.label[i]=QLabel(i)
            self.edit[i]=QLineEdit()

        self.label["GD"] = QLabel("GD")
        self.edit["GD"] = QComboBox()
        self.edit["GD"].addItem("gauche")
        self.edit["GD"].addItem("droite")

        # Put widgets in layout
        lig=0; col=0
        for i in list[:4]:
            self.gridP.addWidget(self.label[i], lig, col)
            col += 1;self.gridP.addWidget(self.edit[i], lig, col)
            col += 1

        lig+=1; col=0
        for i in list[4:8]:
            self.gridP.addWidget(self.label[i], lig, col)
            col += 1;self.gridP.addWidget(self.edit[i], lig, col)
            col += 1

        lig += 1; col = 0
        self.gridP.addWidget(self.label["GD"], lig, col)
        col += 1;self.gridP.addWidget(self.edit["GD"], lig, col)
        col += 1;self.gridP.addWidget(self.label["Permalien"], lig, col)
        col += 1;self.gridP.addWidget(self.edit["Permalien"], lig, col, 2, 5)

        # Update
        #self.edit["Nom"].textChanged.connect(self.changeInfo("Nom"))

        self.edit["Nom"].textChanged.connect(self.changeNom)
        self.edit["Pr??nom"].textChanged.connect(self.changePrenom)
        self.edit["Pr??nom P??re"].textChanged.connect(self.changeNomPere)
        self.edit["Nom et Pr??nom M??re"].textChanged.connect(self.changeNomMere)
        self.edit["R??giment"].textChanged.connect(self.changeRegiment)
        self.edit["Indice"].textChanged.connect(self.changeIndice)
        self.edit["Page"].textChanged.connect(self.changePage)
        self.edit["GD"].currentTextChanged.connect(self.changeGD)
        self.edit["Registre"].textChanged.connect(self.changeRegistre)
        self.edit["Permalien"].textChanged.connect(self.changeLien)

        self.edit["Permalien"].setDisabled(True)
        # Add tab
        self.personneWidget.setLayout(self.gridP)
        self.tabWidget.addTab(self.personneWidget, "&Personne")

    # Add form
    def addForm(self):

        # Create layout for window
        self.boxVPrinc = QVBoxLayout()
        self.window.setLayout(self.boxVPrinc)

        # Text zone
        self.text = Text()
        self.text.textChanged.connect(self.changeText)

        # Create layout for form
        self.gridL = QGridLayout()

        # Ligne et Soldat et Cousin ou Sosa
        self.labelNomcol = QLabel("Noms des colonnes")
        self.editNomcol = QLineEdit()
        self.labelSoldat = QLabel("Soldat")
        self.editSoldat = QLineEdit()
        self.buttonReset = QPushButton("Reset")
        self.buttonDelete = QPushButton("X")
        self.labelType = QLabel("Type")
        self.editType = QComboBox()
        self.editType.addItems(["","cousin", "sosa"])
        self.editType.currentIndexChanged.connect(self.changeType)
        self.editNomcol.textChanged.connect(self.changeNomCol)
        self.editSoldat.textChanged.connect(self.changeSoldat)
        # self.editNomcol.textChanged.connect(self.run)
        # self.editSoldat.textChanged.connect(self.run)
        self.buttonReset.clicked.connect(self.reset)
        self.buttonDelete.clicked.connect(self.deleteSoldat)

        # Place field
        col = 0; lig = 0
        self.gridL.addWidget(self.labelNomcol, lig, col)
        col += 1;self.gridL.addWidget(self.editNomcol, lig, col)
        col += 1;self.gridL.addWidget(self.labelSoldat, lig, col)
        col += 1;self.gridL.addWidget(self.editSoldat, lig, col)
        col += 1;self.gridL.addWidget(self.buttonDelete, lig, col)
        col += 1;self.gridL.addWidget(self.labelType, lig, col)
        col += 1;self.gridL.addWidget(self.editType, lig, col)
        col += 1;self.gridL.addWidget(self.buttonReset, lig, col)
        lig += 1; col=0

        # Add tab personne
        self.tabWidget = QTabWidget()
        self.tabPersonne()
        self.gridL.addWidget(self.tabWidget, lig, col, 2, 8)

        # Add Form and Text
        self.boxVPrinc.addLayout(self.gridL)
        self.boxVPrinc.addWidget(self.text)
    # ==================================================================FORM======================================================================#

    # ===========================================================If something change==============================================================#
    def changeText(self):
        self.infor["Text"]=self.text.toPlainText()
        self.updateJSON()
    def changeNomCol(self):
        self.infor["Noms des Colonnes"] = self.editNomcol.text()
        self.updateJSON()
    def changeSoldat(self):
        self.infor["Soldat"] = self.editSoldat.text()
        self.updateJSON()
        self.run()
        if self.generateCheck():
            self.generateClicked()
    def changeType(self):
        self.infor["Type"] = self.editType.currentText()
        self.updateJSON()
        if self.generateCheck():
            self.generateClicked()
    def changeInfo(self,str):
        self.infor[str] = self.edit[str].text()
        self.updateJSON()
        self.run()
        if self.generateCheck():
            self.generateClicked()
    def changeNom(self):
        self.infor["Nom"]=self.edit["Nom"].text()
        self.updateJSON()
        if self.generateCheck():
            self.generateClicked()
    def changePrenom(self):
        self.infor["Pr??nom"] = self.edit["Pr??nom"].text()
        self.updateJSON()
        if self.generateCheck():
            self.generateClicked()
    def changeNomPere(self):
        self.infor["Pr??nom P??re"] = self.edit["Pr??nom P??re"].text()
        self.updateJSON()
        if self.generateCheck():
            self.generateClicked()
    def changeNomMere(self):
        self.infor["Nom et Pr??nom M??re"] = self.edit["Nom et Pr??nom M??re"].text()
        self.updateJSON()
        if self.generateCheck():
            self.generateClicked()
    def changeIndice(self):
        self.infor["Indice"] = self.edit["Indice"].text()
        self.updateJSON()
        if self.generateCheck():
            self.generateClicked()
    def changePage(self):
        self.infor["Page"] = self.edit["Page"].text()
        self.updateJSON()
        if self.generateCheck():
            self.generateClicked()
    def changeRegiment(self):
        self.infor["R??giment"] = self.edit["R??giment"].text()
        self.updateJSON()
        if self.generateCheck():
            self.generateClicked()
    def changeGD(self):
        self.infor["GD"]=self.edit["GD"].currentText()
        self.updateJSON()
        if self.generateCheck():
            self.generateClicked()
    def changeRegistre(self):
        self.infor["Registre"] = self.edit["Registre"].text()
        self.updateJSON()
        if self.generateCheck():
            self.generateClicked()
    def changeLien(self):
        self.infor["Permalien"]=self.edit["Permalien"].text()
        self.updateJSON()
        if self.generateCheck():
            self.generateClicked()
    # ===========================================================If something change==============================================================#


    # Interface initialization
    def init_ui(self):
        # Application name
        self.setWindowTitle("G??neration message")
        self.setWindowIcon(QIcon("./Icons/GMIcon.png"))
        # Main widget
        self.window = QWidget()

        # Add menu and toolbar and form
        self.addMenu()
        self.addTool()
        self.addForm()

        # Set center zone
        self.setCentralWidget(self.window)

    def updateForm(self):
        self.editType.setCurrentText(self.infor["Type"])
        self.edit["R??giment"].setText(self.infor["R??giment"])
        self.edit["Nom"].setText(self.infor["Nom"])
        self.edit["Pr??nom"].setText(self.infor["Pr??nom"])
        self.edit["Pr??nom P??re"].setText(self.infor["Pr??nom P??re"])
        self.edit["Nom et Pr??nom M??re"].setText(self.infor["Nom et Pr??nom M??re"])
        self.edit["GD"].setCurrentText(self.infor["GD"])
        self.edit["Indice"].setText(self.infor["Indice"])
        self.edit["Page"].setText(self.infor["Page"])
        self.edit["Permalien"].setText(self.infor["Permalien"])
        self.editNomcol.setText(self.infor["Noms des Colonnes"])
        self.editSoldat.setText(self.infor["Soldat"])
        self.edit["Registre"].setText(self.infor["Registre"])
        self.text.setText(self.infor["Text"])

    def updateJSON(self):
        # Write json saving file
        try:
            f = open(self.savingFile, 'w')
        except IOError:
            print("The json file is not found - " + self.savingFile)
        else:
            json.dump(self.infor, f, sort_keys=False, indent=2, ensure_ascii=False)
            f.close()

    # =========================================================BUTTON-ACTION======================================================================#
    def run(self):
        self.nomColonne=self.editNomcol.text()
        tableCol=self.nomColonne.split("\t")
        self.soldat=self.editSoldat.text()
        tableSoldat=self.soldat.split("\t")
        tableRes={}
        length=min(len(tableSoldat),len(tableCol))
        for i in range(length):
            tableRes[tableCol[i]]=tableSoldat[i]
        self.edit["R??giment"].setText(tableRes['R??giment'])
        self.edit["Nom"].setText(tableRes['Nom'])
        self.edit["Pr??nom"].setText(tableRes['Pr??nom'])
        self.edit["Pr??nom P??re"].setText(tableRes['Pr??nom p??re'])
        self.edit["Nom et Pr??nom M??re"].setText(tableRes['Nom m??re']+' '+tableRes['Pr??nom m??re'])
        self.edit["GD"].setCurrentText(tableRes['Page (gauche/droite)'])
        # Other name
        if tableRes['Autre nom']!="":
            self.nom=tableRes['Autre nom']
        else:
            self.nom=tableRes['Nom']
        if tableRes['Autre pr??nom m??re']!="":
            self.prenomMere=tableRes['Autre pr??nom m??re']
        else:
            self.prenomMere=tableRes['Pr??nom m??re']
        if tableRes['Autre nom m??re']!="":
            self.nomMere=tableRes['Autre nom m??re']
        else:
            self.nomMere=tableRes['Nom m??re']
        self.mere=self.nomMere+" "+self.prenomMere


        # Get Indice
        indice=tableRes['Indice'].strip("\n")
        self.edit["Indice"].setText(self.indice_to_string(indice))
        # Get permalien
        num=tableRes["Cl??"][0:4]
        # Get page
        page = num.lstrip("0")
        self.edit["Page"].setText(str(int(page) + 1))

        prefixe=self.perma["prefixe"]
        self.edit["Permalien"].setText(prefixe+self.perma[num])
        # Get registre
        registre=self.perma["registre"].replace("_"," ")
        self.edit["Registre"].setText(registre)


    def indice_to_string(self,indice):
        switcher = {
            "1": "premier",
            "2": "deuxi??me",
            "3": "troisi??me",
            "4": "quatri??me",
            "5": "cinqui??me",
            "6": "sixi??me",
            "7": "septi??me",
            "8": "huiti??me",
            "9": "neuvi??me"
        }
        return switcher.get(indice, "Error")

    def deleteSoldat(self):
        self.delete()

    def reset(self):
        self.editNomcol.setText("")
        self.editType.setCurrentText("")
        self.delete()

    def delete(self):
        self.editSoldat.setText("")
        self.edit["R??giment"].setText("")
        self.edit["Nom"].setText("")
        self.edit["Pr??nom"].setText("")
        self.edit["Pr??nom P??re"].setText("")
        self.edit["Nom et Pr??nom M??re"].setText("")
        self.edit["GD"].setCurrentText("gauche")
        self.edit["Page"].setText("")
        self.edit["Indice"].setText("")
        self.edit["Registre"].setText("")
        self.edit["Permalien"].setText("")
        self.text.delete()
    # ==========================================================BUTTON-ACTION=====================================================================#

    # ===========================================================MENU-ACTION======================================================================#
    def openClicked(self):
        self.infor["json"] = QFileDialog.getOpenFileName(self, "Select file")
        self.updateJSON()
        self.jsonOpen(self.infor["json"])
        self.run()
        self.updateForm()
    def copyClicked(self):
        pyperclip.copy(self.text.toPlainText())
    def deleteTextClicked(self):
        self.text.delete()
    def generateCheck(self):
        if self.infor["Nom"]!='' and self.infor["Pr??nom"]!='' and self.infor["R??giment"]!='' and self.infor["Nom et Pr??nom M??re"]!='' and self.infor["Pr??nom P??re"]!='':
            if self.infor["Indice"]!='' and self.infor["Page"]!='' and self.infor["GD"]!='' and self.infor["Registre"]!='' and self.infor["Permalien"]:
                return True
            else:
                return False
        else:
            return False

    def generateClicked(self):
        self.text.delete()
        #    self.text.display("Titre du message: \"{} {}, fils {} et {}\"\n\n".format(self.infor["Nom"],self.infor["Prenom"],self.infor["Nom Pere"],self.infor["Nom Mere"]) +
        #        "Corps du message :\n")
        type = ""
        if self.infor["Type"] != "":
            type = ", votre "+self.infor["Type"]+" semble-t-il"

        titre="{} {}, fils {} et {}".format(self.nom,self.infor["Pr??nom"],self.infor["Pr??nom P??re"],self.mere)
        self.text.display(
            "Bonjour,\n\n" + titre +"{},".format(type)+
            " est soldat au r??giment du {}, registre {} du site M??moire des Hommes, ".format(self.infor["R??giment"],self.infor["Registre"]) +
                      "page {}, page de {}, {} soldat...\n\n".format(self.infor["Page"],self.infor["GD"],self.infor["Indice"]) +
                      "Je vous donne le permalien allant ?? la page {} ".format(self.infor["Page"]) +
                      ":\n\n" +
                      "{}\n\n".format(self.infor["Permalien"]) +
                      "Bonne journ??e.\n\n" +
                      "Ivan Leplumey - Rennes")
        pyperclip.copy(self.text.toPlainText())
        '''
        while True:
            if keyboard.is_pressed('ctrl+c'):
                pyperclip.copy(self.infor["Text"])
                break
        '''

        '''
        if self.generateCheck():
            def press_on(key):
                pyperclip.copy(self.infor["Text"])
            def press_off(key):
                return False
            with Listener(on_press = press_on, on_release=press_off) as listener:
                listener.join()
        '''

    def informationsClicked(self):
        nom=self.infor["json"][0].split("/")
        QMessageBox.information(self,"Information", "Voici les informations du fichier json: \n\nNom du fichier: "+nom[-1]+"\n\nPosition: "+self.infor["json"][0])

    # ===========================================================MENU-ACTION======================================================================#

# ===================================================================
#                         Programme principal
# ===================================================================
if __name__ == "__main__":
    # V??rification de la syntaxe d'appel
    syntaxe = "Syntaxe: " + sys.argv[0]
    if (len(sys.argv) != 1):
        print(syntaxe)
        exit()

    app = QApplication([])
    mf = Window()
    app.exec_()

