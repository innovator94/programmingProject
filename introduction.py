##Unused file, implemented into main.py without calling

import sys
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QWidget, QLabel, QLineEdit, QMessageBox
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtCore import QSize
from main import Game

class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)

        self.setMinimumSize(QSize(320, 140))    
        self.setWindowTitle("Aim Game") 

        self.nameLabel = QLabel(self)
        self.nameLabel.setText('Name:')
        self.line = QLineEdit(self)

        self.line.move(80, 20)
        self.line.resize(200, 32)
        self.nameLabel.move(20, 20)

        self.pybutton = QPushButton('Submit', self)
        self.pybutton.clicked.connect(self.clickMethod)
        self.pybutton.resize(200,32)
        self.pybutton.move(80, 60)

    def clickMethod(self):
        textboxValue = self.line.text()
        self.line.setText("")
        self.setMinimumSize(QSize(500, 200))
        self.line.move(-200, -200)
        self.pybutton.move(-200, -200)
        
        self.nameLabel.setText(f"Welcome, {textboxValue} to Aim Game!\nThe rules of the game are simple, kill the enemies.\nThe controls are WASD for movements and Left Click for shooting.\nHave Fun!")
        self.nameLabel.resize(500, 150)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    mainWin = MainWindow()
    mainWin.show()
    sys.exit( app.exec_() )
