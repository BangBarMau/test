from PyQt5.QtWidgets import QDialog
from PyQt5.uic import loadUi


class changePassTeacher(QDialog):
    def __init__(self):
        super(changePassTeacher, self).__init__()
        loadUi('newpassTeacher.ui', self)

        self.btnChangeBack.clicked.connect(self.backTeacher)


    def backTeacher(self):
        changePassTeacher.hide(self)
        from main import createTeacher
        teacherForm = createTeacher()
        teacherForm.exec_()

