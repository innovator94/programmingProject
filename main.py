import pygame, sys
import PyQt5
from settings import *
from level import *

import sys, os
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QWidget, QLabel, QLineEdit, QMessageBox
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtCore import QSize

#Class to run the whole game
class Game:
    #All pygame programs need the following, it's protocol
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((720, 480))
        self.clock = pygame.time.Clock()
        pygame.display.set_caption("Aim Game")
        self.status = "Game"
        self.level = Level(self.state_change)
        
    def game_over(self):
        self.screen.fill('black')
        font = pygame.font.Font("programming project 2/assets/Monocraft.ttf",30)
        text = font.render("Game Over",True,'White')
        self.screen.blit(text, (275, 150))
        
    def state_change(self, input):
        if input == "Game":
            self.status = input
        elif input == "Dead":
            self.status = input
        
    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                    
            self.screen.fill('white')
            if self.status == "Game":
                self.level.run()
            elif self.status == "Dead":
                self.game_over()
            pygame.display.update()
            self.clock.tick(60)

#PyQt5 boiler template for user input window
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
        self.pybutton.clicked.connect(self.entry)
        self.pybutton.resize(200,32)
        self.pybutton.move(80, 60)
    
    def entry(self):
        textboxValue = self.line.text()
        self.line.setText("")
        
        invalid = ["\\", ".", ",", ";", ":", " ",]
        flag = False
        
        if textboxValue == "":
            flag = True
        for count in range(len(textboxValue)):
            if textboxValue[count] in invalid:
                flag = True
        if len(textboxValue) < 3 or len(textboxValue) > 15:
            flag = True
        
        if flag == True:
            QMessageBox.question(self, 'Error', f"You typed: {textboxValue}. This is invalid", QMessageBox.Ok, QMessageBox.Ok)
        else:
            file = open("programming project 2/assets/users.txt", "a")
            file.close()
            file = open("programming project 2/assets/users.txt", "r+")
            users = file.read()
            
            if os.stat("programming project 2/assets/users.txt").st_size == 0:
                users_list = []
                users_list.append(textboxValue)
            else:
                users_list = eval(users)
                users_list.append(textboxValue)
            
            file.close()
            file = open("programming project 2/assets/users.txt", "w")
            file.write(str(users_list))
            file.close()
            self.instruction_screen(textboxValue)

    #Changes screen to display user input and instructions
    def instruction_screen(self, textboxValue):
        self.setMinimumSize(QSize(500, 200))
        self.line.move(-200, -200)
        self.pybutton.move(-200, -200)
        
        self.nameLabel.setText(f"Welcome, {textboxValue} to Aim Game!\nThe rules of the game are simple, kill the enemies.\nThe controls are WASD for movements and Left Click for shooting.\nHave Fun!")
        self.nameLabel.resize(500, 150)


if __name__ == '__main__':
    
        app = QtWidgets.QApplication(sys.argv)
        mainWin = MainWindow()
        mainWin.show()
        game = Game()
        game.run()
        sys.exit( app.exec_())