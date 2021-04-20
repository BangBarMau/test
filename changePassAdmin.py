from PyQt5.QtWidgets import QDialog
from PyQt5.uic import loadUi


class changePassAdmin(QDialog):
    def __init__(self):
        super(changePassAdmin, self).__init__()
        loadUi('newpassAdmin.ui', self)

        self.btnChangeBackAdmin.clicked.connect(self.backAdmin)


    def backAdmin(self):
        changePassAdmin.hide(self)
        from main import createAdmin
        adminForm = createAdmin()
        adminForm.exec_()