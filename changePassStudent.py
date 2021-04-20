from PyQt5.QtWidgets import QDialog
from PyQt5.uic import loadUi


class changePassStudent(QDialog):
    def __init__(self):
        super(changePassStudent, self).__init__()
        loadUi('newpassStudent.ui', self)

        self.btnChangeBackStudent.clicked.connect(self.backStudent)


    def backStudent(self):
        changePassStudent.hide(self)
        from main import createStudent
        studentForm = createStudent()
        studentForm.exec_()


    #def ch
