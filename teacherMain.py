from PyQt5.QtWidgets import QDialog, QApplication, QMessageBox, QTableWidgetItem
from PyQt5.uic import loadUi
from connection import myDB

from changePassTeacher import *


class createTeacher(QDialog):
    def __init__(self):
        super(createTeacher, self).__init__()
        loadUi('newteacher.ui', self)
        self.btnTeacherLogout.clicked.connect(self.logout)
        self.btnTeacherSettings.clicked.connect(self.gotoChange)


    def logout(self):
        createTeacher.hide(self)
        from main import Login
        loginForm = Login()
        loginForm.exec_()

    def gotoChange(self):
        createTeacher.hide(self)
        changeForm = changePassTeacher()
        changeForm.exec_()

