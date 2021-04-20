import re #for validation password (Regular Expression)
import sys
from PyQt5.QtWidgets import QDialog, QApplication, QMessageBox
from PyQt5.uic import loadUi

from studentMain import *
from teacherMain import *
from adminMain import *

from connection import myDB
import base64
import mysql

class Login(QDialog):
    def __init__(self):
        super(Login, self).__init__()
        loadUi('newlogin.ui', self)
        self.btnRegister1.clicked.connect(self.gotoRegister)
        self.btnGuest.clicked.connect(self.gotoGuest)
        self.btnLogin.clicked.connect(self.LoginFunction)
        self.inputPassword1.setEchoMode(self.inputPassword1.Password)

    def gotoRegister(self):
        Login.hide(self)
        registrationForm = createAccount()
        registrationForm.exec_()

    def gotoGuest(self):
        Login.hide(self)
        guestForm = guestAppointmentForm()
        guestForm.exec_()


    def LoginFunction(self):
        Email = self.inputEmail1.text().strip()
        Pass = self.inputPassword1.text().strip()

        try:
            myDB._open_connection()
            mycursor = myDB.cursor(dictionary = True) #use dictionary if there is a need to get
                                                      #data in the database

            sql = 'SELECT * FROM user_table WHERE Email = %s AND  Password = %s'
            val = (Email, base64.b64encode(Pass.encode()))
            mycursor.execute(sql,val)

            myresult = mycursor.fetchone()

            admin = 1
            teacher = 2
            student = 3

            if not myresult == None:
                if myresult['Userlevel'] == admin:
                    print(myresult['Email'], 'admin found')
                    Login.hide(self)
                    adminform = createAdmin()
                    adminform.exec_()

                elif myresult['Userlevel'] == teacher:
                    print(myresult['Email'], 'teacher found')
                    Login.hide(self)
                    teacherform = createTeacher()
                    teacherform.exec_()

                elif myresult['Userlevel'] == student:
                    print(myresult['Email'], 'student found')
                    Login.hide(self)
                    studentform = createStudent()
                    studentform.exec_()

            else:
                QMessageBox.warning(self, "Invalid Input", "Invalid username/password")
        except mysql.connector.Error as err:
            print('Error:', err.msg)
        finally:
            mycursor.close()
            myDB.close()

class guestAppointmentForm(QDialog):
    def __init__(self):
        super(guestAppointmentForm, self).__init__()
        loadUi('newguest.ui', self)

        self.btnGuestExit.clicked.connect(self.guestExit)
        self.btnGuestSet.clicked.connect(self.guestSet)


    def guestSet(self): #to be continued...
        userlevel = 4
        FName = self.inputGuestFirstName.text().strip()
        LName = self.inputGuestLastName.text().strip()
        Contact = self.inputGuestContact.text().strip()
        #Subject = self.inputGuestAppointmentSubject.text().strip()
        #details
        #department

        if FName == "":
            QMessageBox.critical(self, 'Required Input', 'Please input your name')
            self.inputGuestFirstName.setFocus()
            return

        if LName == "":
            QMessageBox.critical(self, 'Required Input', 'Please input your name')
            self.inputGuestLastName.setFocus()
            return

        try:
            myDB._open_connection()
            mycursor = myDB.cursor()

            sql = 'INSERT INTO user_table (Firstname, Lastname, Contact, Userlevel) VALUES (%s, %s, %s, %s)'
            #form = 'INSERT INTO appointment_table (Subject) VALUES (%s)'
            val = (FName, LName, Contact, userlevel)
            #valTwo = (Subject)
            mycursor.execute(sql, val)
            myDB.commit()

            print(mycursor.rowcount, 'record inserted')
            QMessageBox.information(self, 'System Informataion', 'Appointment Successfully Submitted!')

        except mysql.connector.Error as err:
            QMessageBox.information(self, 'System Information', 'Appointment Form Failed')
            print('Error:', err.msg)
        finally:
            mycursor.close()
            myDB.commit()


    def guestExit(self):
        guestAppointmentForm.hide(self)
        loginForm = Login()
        loginForm.exec_()


class createAccount(QDialog):
    def __init__(self):
        super(createAccount, self).__init__()
        loadUi('newregistration.ui', self)
        self.btnRegister2.clicked.connect(self.createRegisterFunction)
        self.btnReturnToLogin.clicked.connect(self.returnToLogin)
        self.inputPassword2.setEchoMode(self.inputPassword2.Password)
        self.inputConfirmation.setEchoMode(self.inputConfirmation.Password)
        self.cmbCourse.clear()
        self.cmbCourse.activated.connect(self.on_currentIndexChanged)

        try:
            myDB._open_connection()
            mycursor = myDB.cursor(dictionary=True)

            sql = 'SELECT CID, CourseCode FROM course_table WHERE Status = 1 ORDER BY CourseCode ASC'

            mycursor.execute(sql)

            myresult = mycursor.fetchall()

            self.cmbCourse.addItem('--Course--', 0)

            for row in myresult:
                global getCourseID
                getCourseID = 0 #reset index to 0
                self.cmbCourse.addItem(row["CourseCode"], row["CID"])

        except mysql.connector.Error as err:
            print('Error:', err.msg)
        finally:
            self.cmbCourse.setCurrentIndex(0)
            mycursor.close()
            myDB.close()
            print('MySQL connection is close')



    def on_currentIndexChanged(self, index):
        print(self.cmbCourse.itemText(index))
        print(self.cmbCourse.itemData(index))
        global getCourseID
        getCourseID = self.cmbCourse.itemData(index)


    def returnToLogin(self):
        createAccount.hide(self)
        loginForm = Login()
        loginForm.exec_()


    def createRegisterFunction(self):
        userlevel = 3
        IDNumber = self.inputID.text().strip()
        Course = getCourseID
        FName = self.inputFirst.text().strip()
        LName = self.inputLast.text().strip()
        MI = self.inputMI.text().strip()
        Email = self.inputEmail2.text().strip()
        Contact = self.inputContact.text().strip()
        Password = self.inputPassword2.text().strip()
        Confirmation = self.inputConfirmation.text().strip()

        base64_encryption = base64.b64encode(Password.encode()) #encoding encryption

        if IDNumber == '':
            QMessageBox.critical(self, "Required Input", "Please input ID Number")
            self.inputID.setFocus()
            return

        if Course == 0:
            QMessageBox.critical(self, "Required Selection", "Please select Course")
            self.cmbCourse.setFocus()
            return

        if FName == '':
            QMessageBox.critical(self, "Required Input", "Please input Name")
            self.inputFirst.setFocus()
            return

        if LName == '':
            QMessageBox.critical(self, "Required Input", "Please input Name")
            self.inputLast.setFocus()
            return

        #EMAIL_REGEX = re.compile(r"[^@]+@[^@]+\.[^@]+")

        if not re.match(r"[^@]+@[^@]+\.[^@]+", Email):
            QMessageBox.critical(self, "Required Input", "Please input XU Email")
            self.inputEmail2.setFocus()
            return

        SpecialSymbols = ['!', '@', '#', '$', '%', '^', '&', '*', '(', ')',
                          '_', '-', '+', '=', '~', '`', '[', '{', ']', '}',
                          ';', ':', '', '"', '<', ',','.', '>', '/', '?',
                          '|']
        if Password == '':
            QMessageBox.critical(self, "Required Input", "Please input Password")
            self.inputPassword2.setFocus()
            return

        if len(Password) < 6:
            QMessageBox.critical(self, "Invalid Input", "Please input at least 6 Password length")
            self.inputPassword2.setFocus()
            return

        if len(Password) > 15:
            QMessageBox.critical(self, "Invalid Input", "Please input not more than 15 Password length")
            self.inputPassword2.setFocus()
            return

        if not any(char.isdigit() for char in Password):
            QMessageBox.critical(self, "Invalid Input", "Please input at least one numeral")
            self.inputPassword2.setFocus()
            return

        if not any(char.isupper() for char in Password):
            QMessageBox.critical(self, "Invalid Input", "Please input at least one uppercase")
            self.inputPassword2.setFocus()
            return

        if not any(char.islower() for char in Password):
            QMessageBox.critical(self, "Invalid Input", "Please input at least one lowercase")
            self.inputPassword2.setFocus()
            return

        if not any(char in SpecialSymbols for char in Password):
            QMessageBox.critical(self, "Invalid Input", "Please input at least one special symbol")
            self.inputPassword2.setFocus()
            return

        if not Password == Confirmation:
            QMessageBox.critical(self, "Invalid Input", "The password does not match!")
            self.inputPassword2.setFocus()
            return

        try:
            myDB._open_connection()
            mycursor = myDB.cursor() #mycursor executes myDB in connection.py

            sql = 'INSERT INTO user_table (Student_ID, Firstname, Lastname, MI, Email, Password, Contact, Course, Userlevel) ' \
                  'VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)' #VALUES converts variable
            val = (IDNumber, FName, LName, MI, Email, base64_encryption, Contact, Course, userlevel)
            mycursor.execute(sql, val)

            myDB.commit() #need to have changes in the database (except SELECT)

            print(mycursor.rowcount, 'record inserted')
            QMessageBox.information(self, "System Information", "Account Successfully Created!")

        except mysql.connector.Error as err:
            QMessageBox.information(self, "System Information", "Email already used")
            print('Error:', err.msg)
        finally:
            mycursor.close()
            myDB.close()



if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainwindow = Login()
    mainwindow.setFixedSize(1940, 1050)
    mainwindow.show()
    app.exec_()