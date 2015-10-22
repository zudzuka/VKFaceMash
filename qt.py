#!/usr/bin/python
import sys
import pickle
import random
import math
import sys

from PyQt4 import QtGui, QtCore
import functions

class Person():
    elo = 0                     # Elo rating
    group = 0                   # Matchmaking group
    k = 40                      # Initial coefficient
    battles = 0                 # Batlles was played

class LoginWindow(QtGui.QDialog):
    def __init__(self):
        QtGui.QDialog().__init__(self)



class MainWindow(QtGui.QMainWindow):     
    def __init__(self, parent=None):#параметры по умолчанию класса MainWindow
        QtGui.QMainWindow.__init__(self, parent)

        #self — описание окна, определение переменных виджетов 
        self.setGeometry(300, 300, 1500, 800)
        mainWidget = QtGui.QWidget()
        self.setCentralWidget(mainWidget)

        #Настройка меню
        menu = self.menuBar()
        list1 = menu.addMenu('File')
        list1.addAction('exit')
        list1.addAction('save')
        list1.addAction('save as')

        #Настройка панелей инструментов
        toolbar = self.addToolBar('Exit')
        toolbar.addAction('exit')
        toolbar.addAction('save')
        toolbar.addAction('save as')

        #определение переменных кнопок, редакторов, сеток.
        self.rButton = QtGui.QPushButton("Right")
        self.lButton = QtGui.QPushButton("Left")
        self.dButton = QtGui.QPushButton("Download")

        self.label1 = QtGui.QLabel()
        self.label2 = QtGui.QLabel()

        self.textEdit = QtGui.QTextBrowser(readOnly=1)
        self.textEdit.setOpenExternalLinks(True)

        grid = QtGui.QGridLayout(mainWidget)
        #положение на сетке
        #grid.setSpacing(100)
        grid.setColumnMinimumWidth(0, 400)
        grid.setColumnMinimumWidth(1, 400)
        grid.setColumnMinimumWidth(2, 200)
        grid.addWidget(self.label1, 0, 0)
        grid.addWidget(self.label2, 0, 1)
        grid.addWidget(self.lButton, 1, 0)
        grid.addWidget(self.rButton, 1, 1)
        grid.addWidget(self.dButton, 1, 2)
        grid.addWidget(self.textEdit, 0, 2)


        self.person=functions.unpickle()
        #self.person=self.person[:10]
        self.rButton.clicked.connect(self.rbutton)
        self.lButton.clicked.connect(self.lbutton)
        self.dButton.clicked.connect(self.dbutton)
        #self.person[13].elo=200
        self.update(2)
        self.setGeometry(300, 300, 250, 150)
        #self.connect(self.rButton, QtCore.SIGNAL('clicked(int)'), self.update(1))

    def rbutton(self):
        self.update(0)

    def lbutton(self):
        self.update(1)  

    def dbutton(self):
        functions.download()
        self.person=functions.unpickle()
        self.update(2)

    def update(self, a):
        #Новый рейтинг предыдущих
        if a == 1: 
            functions.buttle(self.left, self.right)
            self.person[self.nleft]=self.left
            self.person[self.nright]=self.right
        if a == 0: 
            functions.buttle(self.right, self.left)
            self.person[self.nleft]=self.left
            self.person[self.nright]=self.right
        #сортируем`
        self.person=sorted(self.person, key=lambda person: person.elo)

        #матчмэйкинг
        self.left=random.choice(self.person)
        self.nleft=self.person.index(self.left)
        d=1

        if self.nleft<d:
            self.right=[i for i in self.person[:d*2] if i != self.left]
        elif self.nleft>(len(self.person)-d):    
            self.right=[i for i in self.person[self.nleft-d*2:] if i != self.left]
        else: 
            self.right=[i for i in self.person[self.nleft-d:self.nleft+d] if i != self.left]

        self.right=random.choice(self.right)
        self.nright=self.person.index(self.right)

        #Установка картинок
        self.label1.setPixmap(QtGui.QPixmap(self.left.jpg).scaledToHeight(400))
        self.label2.setPixmap(QtGui.QPixmap(self.right.jpg).scaledToHeight(400))
        #self.label2.setGeometry(160, 40, 80, 30)

        self.textEdit.clear()
        #Текст
        for i in range(len(self.person)):
             text="<a href='http://www.vk.com/id"+str(self.person[i].id)+"'>"
             text=text+self.person[i].sname.ljust(2)+' '+self.person[i].name+'</a>'
             text=str(self.person[i].elo)[:4]+'\t'+text
             self.textEdit.append(text)

        self.textEdit.toHtml()

    def closeEvent(self, event):
        reply = QtGui.QMessageBox.question(self, 'Message',
            "Are you sure to quit?", QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)
        if reply == QtGui.QMessageBox.Yes:
            functions.save(self.person)
            event.accept()
        else:
            event.ignore()


    def showEvent(self, event):
        reply = QtGui.QDialog()
        Login_Dialog.setObjectName("Login_Dialog")
        Login_Dialog.resize(285, 134)
        reply.show()


app = QtGui.QApplication(sys.argv)
main = MainWindow()
main.show()
sys.exit(app.exec_())