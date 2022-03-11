from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLabel,QVBoxLayout


class customKeyWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.username = str
        self.password = str
        self.notes = str
        self.group = str
        self.keepassExample = str

        self.textQVBoxLayout = QVBoxLayout()

        self.textUpQLabel = QLabel()
        self.textUpQLabel.setStyleSheet('font:75 12pt "Arial";'
                                        'background-color:none;')
        self.textDownQLabel = QLabel()
        self.textDownQLabel.setContentsMargins(2,0,0,0)
        self.textDownQLabel.setStyleSheet('font: 10pt "Arial";'
                                          'background-color:none;')
        self.textQVBoxLayout.addWidget(self.textUpQLabel)
        self.textQVBoxLayout.addWidget(self.textDownQLabel)
        self.allQHBoxLayout = QHBoxLayout()

        self.allQHBoxLayout.addLayout(self.textQVBoxLayout, 1)

        self.setLayout(self.allQHBoxLayout)

    def setTextUp(self, text):
        self.textUpQLabel.setText(text)

    def setTextDown(self, text):
        self.textDownQLabel.setText(text)
