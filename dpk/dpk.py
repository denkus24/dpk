from PyQt5.QtWidgets import (QMainWindow, QApplication, QListWidgetItem,
                             QMessageBox, QFileDialog, QWidget)
from PyQt5.QtGui import QIcon
from customKeyWidget import customKeyWidget
from sys import argv
from os import getcwd
from database import (openDatabase, entriesByGroup, addNewEntry,
                      removeEntry, changeParams, groupByName, addNewGroup, createNewFile)
from pykeepass.exceptions import CredentialsError
import pyautogui as typer
import design, about
import webbrowser


class Main(QMainWindow, design.Ui_MainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)

        ## MAIN PAGE
        self.addButton.clicked.connect(self.addButtonMethod)
        self.webButton_2.clicked.connect(self.webOpen)
        self.removeButton_2.clicked.connect(self.removeKey)
        self.lockButton.clicked.connect(self.lock)
        self.saveButton_2.clicked.connect(self.saveEntry)
        self.saveNewEntryButton_2.clicked.connect(self.saveNewEntry)
        self.openButton.clicked.connect(self.openDatabase)
        self.autotypeButton.clicked.connect(self.autotype)
        self.aboutButton.clicked.connect(self.about)
        self.showPasswordButton_2.clicked.connect(self.showPassword)
        self.newButton.clicked.connect(self.createNewDatabase)
        self.addGroupButton.clicked.connect(self.addNewGroup)
        self.saveGroupButton.clicked.connect(self.addNewGroupMethod)

        self.groupWidget.setCurrentRow(0)

        self.keysWidget.itemClicked.connect(self.infoPrint)
        self.groupWidget.itemClicked.connect(self.fillKeys)

        self.searchEdit.textChanged.connect(self.searching)

        self.errorMessage = QMessageBox()
        self.errorMessage.setWindowTitle('Error')
        self.errorMessage.setIcon(QMessageBox.Critical)

        ## OPEN DATABASE PAGE

        self.openDBButton.clicked.connect(self.openDatabasePageOpen)
        self.cancelButton.clicked.connect(self.openDatabasePageCancelMethod)
        self.okButton.clicked.connect(self.openDatabasePageOkMethod)
        self.browseButton.clicked.connect(self.openDatabasePageBrowseKeyFile)
        self.showPasswordButton_3.clicked.connect(self.openDatabasePageShowPassword)

        ## NEW DATABASE PAGE

        self.createDBButton.clicked.connect(self.newDatabasePageOpen)
        self.cancelButton_2.clicked.connect(self.newDatabasePageCancelMethod)
        self.okButton_2.clicked.connect(self.newDatabasePageOkMethod)
        self.browseButton_2.clicked.connect(self.newDatabasePageBrowseKeyFile)
        self.showPasswordButton_4.clicked.connect(self.newDatabasePageShowPassword)

        self.passwordEdit_4.textChanged.connect(self.checkPasswordEdits)
        self.repeatPasswordEdit.textChanged.connect(self.checkPasswordRepeatEdits)

        ## OTHER
        self.openedDatabase = ''

        self.lock()

    def removeKey(self):
        selected_item = self.keysWidget.currentRow()
        selected_widget = self.keysWidget.itemWidget(self.keysWidget.selectedItems()[0])

        removeEntry(self.openedDatabase, selected_widget.keepassExample)

        self.keysWidget.takeItem(selected_item)
        self.keysWidget.clearSelection()
        self.setInfoFrameMode(4)

    def webOpen(self):
        selected_widget = self.keysWidget.itemWidget(self.keysWidget.selectedItems()[0])
        print(selected_widget.textDownQLabel.text())
        webbrowser.open(selected_widget.textDownQLabel.text())

    def addNewEntry(self, title, link, username, password, notes, group, keepassExam):
        myQCustomQWidget = customKeyWidget()

        myQCustomQWidget.username = username
        myQCustomQWidget.password = password
        myQCustomQWidget.notes = notes
        myQCustomQWidget.group = group
        myQCustomQWidget.keepassExample = keepassExam

        myQCustomQWidget.setTextUp(title)
        myQCustomQWidget.setTextDown(link)
        myQListWidgetItem = QListWidgetItem(self.keysWidget)

        myQListWidgetItem.setSizeHint(myQCustomQWidget.sizeHint())
        self.keysWidget.addItem(myQListWidgetItem)
        self.keysWidget.setItemWidget(myQListWidgetItem, myQCustomQWidget)

    def infoPrint(self, item):
        self.setInfoFrameMode(1)
        link = self.keysWidget.itemWidget(item).textDownQLabel.text()
        title = self.keysWidget.itemWidget(item).textUpQLabel.text()
        username = self.keysWidget.itemWidget(item).username
        password = self.keysWidget.itemWidget(item).password
        notes = self.keysWidget.itemWidget(item).notes

        for edit in [self.linkEdit_2, self.titleEdit_2, self.passwordEdit_2, self.usernameEdit_2, self.noteEdit_2]:
            edit.clear()

        self.titleEdit_2.setText(title)
        self.linkEdit_2.setText(link)
        self.usernameEdit_2.setText(username)
        self.passwordEdit_2.setText(password)
        self.noteEdit_2.setPlainText(notes)

    def addAllItems(self, itemList):
        for x in itemList:
            listWidgetItem = QListWidgetItem(self.keysWidget)
            listWidgetItem.setSizeHint(x.sizeHint())
            self.keysWidget.addItem(listWidgetItem)
            self.keysWidget.setItemWidget(listWidgetItem, x)

    def searching(self):
        text = self.searchEdit.text()

        self.keysWidget.clear()
        currentlyGroup = self.groupWidget.selectedItems()[0]
        self.fillKeys(currentlyGroup)

        add_elements = list()

        for entry in range(self.keysWidget.count()):
            widget = self.keysWidget.itemWidget(self.keysWidget.item(entry))
            if text.lower() in widget.textUpQLabel.text().lower():
                add_elements.append(
                    [widget.textUpQLabel.text(), widget.textDownQLabel.text(), widget.username, widget.password,
                     widget.notes, currentlyGroup, widget.keepassExample])
        self.keysWidget.clear()
        for x in add_elements:
            self.addNewEntry(x[0], x[1], x[2], x[3], x[4], x[5], x[6])

    def lock(self):
        self.setWindowTitle('DPK')

        self.stackedInfoWidget.setCurrentIndex(0)

        self.keysWidget.clear()
        self.keysWidget.setEnabled(False)

        self.groupWidget.clear()
        self.groupWidget.setEnabled(False)

        self.nothingLabel.show()

        self.addButton.setEnabled(False)
        self.lockButton.setEnabled(False)
        self.searchEdit.setEnabled(False)
        self.addGroupButton.setEnabled(False)
        self.autotypeButton.setEnabled(False)

        self.update()

        self.openedDatabase = ''

        self.mainStackedWidget.setCurrentIndex(0)

    def unlock(self):
        self.setWindowTitle('DPK - ' + self.openedDatabase.filename)

        self.keysWidget.setEnabled(True)
        self.groupWidget.setEnabled(True)
        self.addButton.setEnabled(True)
        self.lockButton.setEnabled(True)
        self.searchEdit.setEnabled(True)
        self.addGroupButton.setEnabled(True)
        self.autotypeButton.setEnabled(True)

    def saveEntry(self):
        changeWidget = self.keysWidget.itemWidget(self.keysWidget.selectedItems()[0])

        newTitle = self.titleEdit_2.text()

        if newTitle == '':
            self.errorMessage.setText("Title can't be empty!")
            self.errorMessage.exec_()
            return

        newUsername = self.usernameEdit_2.text()
        newPassword = self.passwordEdit_2.text()
        newLink = self.linkEdit_2.text()
        newNotes = self.noteEdit_2.toPlainText()

        changeWidget.textUpQLabel.setText(newTitle)
        changeWidget.textDownQLabel.setText(newLink)
        changeWidget.username = newUsername
        changeWidget.password = newPassword
        changeWidget.notes = newNotes

        changeParams(keepassExam=self.openedDatabase,
                     entry=changeWidget.keepassExample,
                     title=newTitle,
                     link=newLink,
                     username=newUsername,
                     password=newPassword,
                     notes=newNotes)

    def setInfoFrameMode(self, mode):
        if mode == 1:  # Show entry info
            self.stackedInfoWidget.setCurrentIndex(2)
            self.saveNewEntryButton_2.hide()
            self.saveNewEntryButton_2.setEnabled(False)
            self.saveButton_2.show()
            self.saveButton_2.setEnabled(True)
            self.webButton_2.show()
            self.removeButton_2.show()

            self.nothingLabel.hide()
        elif mode == 2:  # Add new entry
            self.stackedInfoWidget.setCurrentIndex(2)
            self.keysWidget.clearSelection()
            self.saveButton_2.hide()
            self.saveButton_2.setEnabled(False)
            self.saveNewEntryButton_2.show()
            self.saveNewEntryButton_2.setEnabled(True)
            for edit in [self.linkEdit_2, self.noteEdit_2, self.passwordEdit_2, self.usernameEdit_2, self.titleEdit_2]:
                edit.clear()
            for button in [self.webButton_2, self.removeButton_2]:
                button.hide()

            self.nothingLabel.hide()
        elif mode == 4:  # Hide all
            self.stackedInfoWidget.setCurrentIndex(0)
            self.nothingLabel.show()

    def addButtonMethod(self):
        selectedGroup = self.groupWidget.selectedItems()
        if len(selectedGroup) == 0:  # If group is not selected
            self.errorMessage.setText('Group is not selected')
            self.errorMessage.exec_()
            return

        self.setInfoFrameMode(2)

    def saveNewEntry(self):
        newTitle = self.titleEdit_2.text()
        newUsername = self.usernameEdit_2.text()
        newPassword = self.passwordEdit_2.text()
        newLink = self.linkEdit_2.text()
        newNotes = self.noteEdit_2.toPlainText()
        group = groupByName(self.openedDatabase, self.groupWidget.selectedItems()[0].text())

        entry = addNewEntry(self.openedDatabase,
                            title=newTitle,
                            link=newLink,
                            username=newUsername,
                            password=newPassword,
                            notes=newNotes,
                            group=group)
        self.addNewEntry(newTitle, newLink, newUsername, newPassword, newNotes, group, entry)

    def openDatabase(self):
        self.openDatabasePageOpen()

    def createNewDatabase(self):
        self.mainStackedWidget.setCurrentIndex(2)

    def autotype(self):
        typeWidget = self.keysWidget.itemWidget(self.keysWidget.selectedItems()[0])

        typeUsername = typeWidget.username
        typePassword = typeWidget.password

        typer.hotkey('Alt', 'Tab')
        typer.write(typeUsername)
        typer.press('tab')
        typer.write(typePassword)
        typer.press('enter')

    def about(self):
        about_win.show()

    def showPassword(self):
        if self.passwordEdit_2.echoMode() == 2:
            self.passwordEdit_2.setEchoMode(0)
            self.showPasswordButton_2.setIcon(QIcon('../icons/show.png'))
        elif self.passwordEdit_2.echoMode() == 0:
            self.passwordEdit_2.setEchoMode(2)
            self.showPasswordButton_2.setIcon(QIcon('../icons/hidden.png'))

    def fillGroups(self):
        all_groups = self.openedDatabase.groups

        self.groupWidget.clear()

        for x in all_groups:
            self.groupWidget.addItem(QListWidgetItem(x.name))

    def fillKeys(self, group_item):
        group_name = group_item.text()
        all_entries = entriesByGroup(self.openedDatabase, group_name=group_name)

        self.keysWidget.clear()
        for x in all_entries:
            self.addNewEntry(x.title, x.url, x.username, x.password, x.notes, group_name, x)

    def randomPasswordGen(self):
        pass

    def addNewGroup(self):
        self.stackedInfoWidget.setCurrentIndex(1)

    def addNewGroupMethod(self):
        groupTitle = self.titleGroupEdit.text()
        groupNotes = self.notesGroupEdit.toPlainText()
        addNewGroup(self.openedDatabase, groupTitle, groupNotes)
        self.groupWidget.clear()
        self.fillGroups()

        self.stackedInfoWidget.setCurrentIndex(0)
        self.nothingLabel.show()

    ##----------------OPEN DATABASE PAGE---------------
    def openDatabasePageOpen(self):

        self.databaseOpenName, _ = QFileDialog.getOpenFileName(
            parent=self,
            caption="Select database file",
            directory=getcwd(),
            filter='KDBX file (*.kdbx;);;All files (*)',
            initialFilter='KDBX file (*.kdbx;)')

        if self.databaseOpenName:
            self.passwordEdit_3.clear()
            self.pathEdit.clear()
            self.mainStackedWidget.setCurrentIndex(1)
            self.setWindowTitle('Opening new file')

    def openDatabasePageOkMethod(self):
        if self.databaseOpenName:
            try:
                password = self.passwordEdit_3.text()
                if password == '':
                    password = None
                path = self.pathEdit.text()

                if path == '':
                    path = None

                db = openDatabase(self.databaseOpenName, password, path)
                self.openedDatabase = db

                self.fillGroups()
                self.unlock()

                self.mainStackedWidget.setCurrentIndex(3)
            except CredentialsError:
                self.errorMessage.setText('Password is not correct!')
                self.errorMessage.exec_()
                return

    def openDatabasePageBrowseKeyFile(self):
        fileName, _ = QFileDialog.getOpenFileName(
            parent=self,
            caption="Select key file",
            directory=getcwd(),
            filter='Key file (*.key; *.keyx);;All files (*)',
            initialFilter='Key file (*.key; *.keyx)')

        if fileName:
            self.pathEdit.setText(fileName)

    def openDatabasePageCancelMethod(self):
        self.mainStackedWidget.setCurrentIndex(0)
        self.setWindowTitle('DPK')

    def openDatabasePageShowPassword(self):
        if self.passwordEdit_3.echoMode() == 2:
            self.passwordEdit_3.setEchoMode(0)
            self.showPasswordButton_3.setIcon(QIcon('../icons/show.png'))
        elif self.passwordEdit_3.echoMode() == 0:
            self.passwordEdit_3.setEchoMode(2)
            self.showPasswordButton_3.setIcon(QIcon('../icons/hidden.png'))

    # ----------------NEW  DATABASE PAGE---------------
    def newDatabasePageOpen(self):
        self.titleEdit_3.clear()
        self.passwordEdit_4.clear()
        self.repeatPasswordEdit.clear()
        self.pathEdit_2.clear()
        self.mainStackedWidget.setCurrentIndex(2)
        self.setWindowTitle('Creating new database')

    def newDatabasePageCancelMethod(self):
        self.mainStackedWidget.setCurrentIndex(0)
        self.setWindowTitle('DPK')

    def newDatabasePageBrowseKeyFile(self):
        fileName, _ = QFileDialog.getOpenFileName(
            parent=self,
            caption="Select key file",
            directory=getcwd(),
            filter='Key file (*.key; *.keyx);;All files (*)',
            initialFilter='Key file (*.key; *.keyx)')

        if fileName:
            self.pathEdit_2.setText(fileName)

    def openNewDatabase(self):
        db = openDatabase(self.databaseNewName, self.passwordEdit_4.text(), self.pathEdit_2.text())
        self.openedDatabase = db

        self.fillGroups()
        self.unlock()

        self.mainStackedWidget.setCurrentIndex(3)

    def newDatabasePageOkMethod(self):
        if self.titleEdit_3.text() == '':
            self.errorMessage.setText("Title can't be empty!")
            self.errorMessage.exec_()
            return
        if self.repeatPasswordEdit.text() != self.passwordEdit_4.text():
            self.errorMessage.setText('Passwords do not match')
            self.errorMessage.exec_()
            return
        if self.passwordEdit_4.text() == '' and self.pathEdit_2.text() == '':
            self.errorMessage.setText('Install at least one protection method')
            self.errorMessage.exec_()
            return

        self.databaseNewName, _ = QFileDialog.getSaveFileName(
            parent=self,
            caption="Create new KeePass database",
            directory=self.titleEdit_3.text() + '.kdbx',
            filter='KeePass database (*.kdbx);;All files (*)',
            initialFilter='KeePass database (*.kdbx)')

        if self.databaseNewName:
            createNewFile(self.databaseNewName, self.titleEdit_3.text(), self.passwordEdit_4.text(),
                          self.pathEdit_2.text())
            self.openNewDatabase()

    def newDatabasePageShowPassword(self):
        if self.passwordEdit_4.echoMode() == 2:
            self.passwordEdit_4.setEchoMode(0)
            self.repeatPasswordEdit.setEchoMode(0)
            self.showPasswordButton_4.setIcon(QIcon('../icons/show.png'))
        elif self.passwordEdit_4.echoMode() == 0:
            self.passwordEdit_4.setEchoMode(2)
            self.repeatPasswordEdit.setEchoMode(2)
            self.showPasswordButton_3.setIcon(QIcon('../icons/hidden.png'))

    def checkPasswordEdits(self, passwordText):
        if passwordText != self.repeatPasswordEdit.text():
            self.repeatPasswordEdit.setStyleSheet('background-color:rgb(255, 105, 107);')
        else:
            self.repeatPasswordEdit.setStyleSheet('')

    def checkPasswordRepeatEdits(self, passwordRepeatText):
        if passwordRepeatText != self.passwordEdit_4.text():
            self.repeatPasswordEdit.setStyleSheet('background-color:rgb(255, 105, 107);')
        else:
            self.repeatPasswordEdit.setStyleSheet('')


class About(QWidget, about.Ui_Form):
    # About window
    def __init__(self):
        super(About, self).__init__()
        self.setupUi(self)


if __name__ == '__main__':
    app = QApplication(argv)
    main_win = Main()
    about_win = About()

    main_win.show()

    app.exec_()
