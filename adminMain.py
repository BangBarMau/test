import re
import mysql
from PyQt5.QtGui import QStandardItemModel

from connection import myDB
from changePassTeacher import *

from PyQt5.QtWidgets import QDialog, QMessageBox, QTableWidgetItem, QHeaderView
from PyQt5.uic import loadUi
from changePassAdmin import *



class createAdmin(QDialog):
    def __init__(self):
        super(createAdmin, self).__init__()
        loadUi('newadmin.ui', self)

        self.btnAdminLogout.clicked.connect(self.logout)
        self.btnAdminSettings.clicked.connect(self.gotoChange)

        self.btnTeacherNew.clicked.connect(self.newTeacher)
        self.btnTeacherCancel.clicked.connect(self.cancelTeacher)
        self.btnTeacherSave.clicked.connect(self.saveTeacher)
        self.btnActive2.clicked.connect(self.setActiveTeacher)
        self.btnInactive2.clicked.connect(self.setInactiveTeacher)
        self.cmbFilter2.activated.connect(self.filterTeacher)
        self.btnSearch2.clicked.connect(self.searchTeacher)
        self.cmbDepartment.activated.connect(self.on_currentIndexChanged)

        self.btnCourseNew.clicked.connect(self.newCourse)
        self.btnCourseCancel.clicked.connect(self.cancelCourse)
        self.btnCourseSave.clicked.connect(self.saveCourse)
        self.cmbFilter3.activated.connect(self.filterCourse)
        self.btnSearch3.clicked.connect(self.searchCourse)
        self.btnActive3.clicked.connect(self.setActiveCourse)
        self.btnInactive3.clicked.connect(self.setInactiveCourse)
        self.populateRecord()
        self.populateRecordTeacher()
        self.populateRecordStudent()

        self.btnSearch1.clicked.connect(self.searchUser)
        self.cmbFilter1.activated.connect(self.filterUser)
        self.btnActive1.clicked.connect(self.setActiveStudent)
        self.btnInactive1.clicked.connect(self.setInactiveStudent)


    #update record
    def populateRecord(self):
        try:
            myDB._open_connection()
            mycursor = myDB.cursor(dictionary=True)

            sql = 'SELECT * FROM course_table WHERE Status = 1 ORDER BY CourseCode ASC'

            mycursor.execute(sql)

            myresult = mycursor.fetchall()

            self.widgetAdmin3.setRowCount(len(myresult))  # set number of rows
            self.widgetAdmin3.setColumnCount(4)

            rowcount = 0
            for row in myresult:
                if row['Status'] == 1:
                    status = 'Active'
                else:
                    status = 'Inactive'
                self.widgetAdmin3.setItem(rowcount, 0, QTableWidgetItem(str(row['CID'])))
                self.widgetAdmin3.setItem(rowcount, 1, QTableWidgetItem(row['CourseCode']))
                self.widgetAdmin3.setItem(rowcount, 2, QTableWidgetItem(row['CourseDesc']))
                self.widgetAdmin3.setItem(rowcount, 3, QTableWidgetItem(status))
                rowcount = rowcount + 1

            self.widgetAdmin3.horizontalHeader().setStretchLastSection(True)
            self.widgetAdmin3.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        except mysql.connector.Error as err:
            print('Error:', err.msg)

        finally:
            mycursor.close()
            myDB.close()
            print('MySQL connection is closed')


    # update record
    def populateRecordTeacher(self):
        try:
            myDB._open_connection()
            mycursor = myDB.cursor(dictionary=True)

            sql = 'SELECT * FROM user_table WHERE Status = 1 AND Userlevel = 2 ORDER BY Lastname ASC'

            mycursor.execute(sql)

            myresult = mycursor.fetchall()

            self.widgetAdmin2.setRowCount(len(myresult))  # set number of rows
            self.widgetAdmin2.setColumnCount(5)

            rowcount = 0
            for row in myresult:
                if row['Status'] == 1:
                    status = 'Active'
                else:
                    status = 'Inactive'
                self.widgetAdmin2.setItem(rowcount, 0, QTableWidgetItem(str(row['Employee_ID'])))
                self.widgetAdmin2.setItem(rowcount, 1, QTableWidgetItem(row['Lastname']))
                self.widgetAdmin2.setItem(rowcount, 2, QTableWidgetItem(row['Email']))
                self.widgetAdmin2.setItem(rowcount, 3, QTableWidgetItem(row['Department']))
                self.widgetAdmin2.setItem(rowcount, 4, QTableWidgetItem(status))
                rowcount = rowcount + 1

            self.widgetAdmin2.horizontalHeader().setStretchLastSection(True)
            self.widgetAdmin2.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)


        except mysql.connector.Error as err:
            print('Error:', err.msg)

        finally:
            mycursor.close()
            myDB.close()
            print('MySQL connection is closed')


    def populateRecordStudent(self):
        try:
            myDB._open_connection()
            mycursor = myDB.cursor(dictionary=True)

            sql = 'SELECT * FROM user_table WHERE Status = 1 AND Userlevel = 3 ORDER BY Lastname ASC'

            mycursor.execute(sql)

            myresult = mycursor.fetchall()

            self.widgetAdmin1.setRowCount(len(myresult))  # set number of rows
            self.widgetAdmin1.setColumnCount(5)

            rowcount = 0
            for row in myresult:
                if row['Status'] == 1:
                    status = 'Active'
                else:
                    status = 'Inactive'
                self.widgetAdmin1.setItem(rowcount, 0, QTableWidgetItem(str(row['Student_ID'])))
                self.widgetAdmin1.setItem(rowcount, 1, QTableWidgetItem(row['Lastname']))
                self.widgetAdmin1.setItem(rowcount, 2, QTableWidgetItem(row['Firstname']))
                self.widgetAdmin1.setItem(rowcount, 3, QTableWidgetItem(row['Email']))
                self.widgetAdmin1.setItem(rowcount, 4, QTableWidgetItem(status))
                rowcount = rowcount + 1

            self.widgetAdmin1.horizontalHeader().setStretchLastSection(True)
            self.widgetAdmin1.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        except mysql.connector.Error as err:
            print('Error:', err.msg)

        finally:
            mycursor.close()
            myDB.close()
            print('MySQL connection is closed')


    def logout(self):
        createAdmin.hide(self)
        from main import Login
        loginForm = Login()
        loginForm.exec_()


    def gotoChange(self):
        createAdmin.hide(self)
        changeForm = changePassAdmin()
        changeForm.exec_()

    def setActiveCourse(self):
        global userStatus
        userStatus = 1
        self.setstatus()

    def setInactiveCourse(self):
        global userStatus
        userStatus = 0
        self.setstatusCourse()

    def setActiveTeacher(self):
        global userStatus
        userStatus = 1
        self.setstatusTeacher()

    def setInactiveTeacher(self):
        global userStatus
        userStatus = 0
        self.setstatusTeacher()

    def setActiveStudent(self):
        global userStatus
        userStatus = 1
        self.setstatusStudent()

    def setInactiveStudent(self):
        global userStatus
        userStatus = 0
        self.setstatusStudent()


# -------------Start of Course

    def createTableCourse(self):
        model = QStandardItemModel()
        model.setHorizaontalHeaderLabels(['CID', 'COURSE CODE', 'COURSE DESCRIPTION', 'STATUS'])
        table = self.widgetAdmin3
        table.setModel(model)


    def searchCourse(self):
        try:
            inputSearch = self.inputSearch3.text().strip()

            myDB._open_connection()
            mycursor = myDB.cursor(dictionary=True)

            if len(inputSearch) > 0:
                sql = "SELECT * FROM course_table WHERE CourseCode LIKE CONCAT('%', %s, '%') OR CID = %s ORDER BY CourseCode ASC"
                val = (inputSearch, inputSearch)
                mycursor.execute(sql, val)
            else:
                return

            myresult = mycursor.fetchall()
            self.widgetAdmin3.setRowCount(len(myresult))  # set number of rows
            self.widgetAdmin3.setColumnCount(4)

            rowcount = 0
            for row in myresult:
                if row['Status'] == 1:
                    status = 'Active'
                else:
                    status = 'Inactive'
                self.widgetAdmin3.setItem(rowcount, 0, QTableWidgetItem(str(row['CID'])))
                self.widgetAdmin3.setItem(rowcount, 1, QTableWidgetItem(row['CourseCode']))
                self.widgetAdmin3.setItem(rowcount, 2, QTableWidgetItem(row['CourseDesc']))
                self.widgetAdmin3.setItem(rowcount, 3, QTableWidgetItem(status))
                rowcount = rowcount + 1

            self.widgetAdmin3.horizontalHeader().setStretchLastSection(True)
            self.widgetAdmin3.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)


        except mysql.connector.Error as err:
            print("Error:", err.msg)
        finally:
            mycursor.close()
            myDB.close()


    def filterCourse(self, index):
        try:
            courseFilter = self.cmbFilter3.itemText(index)

            myDB._open_connection()
            mycursor = myDB.cursor(dictionary=True)

            if courseFilter == 'Active':
                sql = 'SELECT * from course_table WHERE Status = 1 ORDER BY CourseCode ASC'
            elif courseFilter == 'Inactive':
                sql = 'SELECT * FROM course_table WHERE Status = 0 ORDER BY CourseCode ASC'
            else:
                sql = 'SELECT * FROM course_table ORDER BY CourseCode ASC'

            mycursor.execute(sql)

            # self.course_table.addItem(row['CourseCode'], row['CID'])
            myresult = mycursor.fetchall()
            self.widgetAdmin3.setRowCount(len(myresult))  # set number of rows
            self.widgetAdmin3.setColumnCount(4)

            rowcount = 0

            for row in myresult:
                if row['Status'] == 1:
                    status = 'Active'
                else:
                    status = 'Inactive'
                self.widgetAdmin3.setItem(rowcount, 0, QTableWidgetItem(str(row['CID'])))
                self.widgetAdmin3.setItem(rowcount, 1, QTableWidgetItem(row['CourseCode']))
                self.widgetAdmin3.setItem(rowcount, 2, QTableWidgetItem(row['CourseDesc']))
                self.widgetAdmin3.setItem(rowcount, 3, QTableWidgetItem(status))
                rowcount = rowcount + 1

            self.widgetAdmin3.horizontalHeader().setStretchLastSection(True)
            self.widgetAdmin3.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        except mysql.connector.Error as err:
            print("Error:", err.msg)
        finally:
            mycursor.close()
            myDB.close()


    def newCourse(self):
        self.btnCourseNew.setEnabled(False)
        self.btnCourseSave.setEnabled(True)
        self.btnCourseCancel.setEnabled(True)
        self.groupCourse.setEnabled(True)
        self.inputCourseCode.setFocus()

    def cancelCourse(self):
        self.btnCourseNew.setEnabled(True)
        self.btnCourseSave.setEnabled(False)
        self.btnCourseCancel.setEnabled(False)
        self.groupCourse.setEnabled(False)

    def saveCourse(self):
        CourseCode = self.inputCourseCode.text().strip()
        CourseDescription = self.inputCourseDescription.toPlainText()

        if CourseCode == "":
            QMessageBox.critical(self, "Required Input", "Please input Course Code")
            self.inputCourseCode.setFocus()
            return

        if CourseDescription == "":
            QMessageBox.critical(self, "Required Input", "Please input Course Code")
            self.inputCourseDescription.setFocus()
            return

        try:
            myDB._open_connection()
            mycursor = myDB.cursor()

            sql = 'INSERT INTO course_table(CourseCode, CourseDesc) VALUES (%s, %s)'
            val = (CourseCode, CourseDescription)
            mycursor.execute(sql, val)

            myDB.commit()

            print(mycursor.rowcount, 'record inserted')
            self.populateRecord()
            QMessageBox.information(self, "System Information", "Course Successfully Created!")

        except mysql.connector.Error as err:
            QMessageBox.information(self, "System Information", "The course code already used!")
            print('Error:', err.msg)
        finally:
            mycursor.close()
            myDB.close()


    def setstatusCourse(self):
        try:
            selected = []  # triggers when a row is selected in widget
            for i in range(1):
                selected.append(self.widgetAdmin3.item(self.widgetAdmin3.currentRow(), i).text())

            print(selected)

            myDB._open_connection()
            mycursor = myDB.cursor()

            sql = 'UPDATE course_table SET Status = %s WHERE CID = %s'
            val = (userStatus, selected[0])
            mycursor.execute(sql, val)

            myDB.commit()

            self.populateRecord()
            print(mycursor.rowcount, 'record updated')

        except mysql.connector.Error as err:
            print('Error:', err.msg)
        finally:
            mycursor.close()
            myDB.close()


#-------------End of Manage Course


#-------------Start of Manage Teacher

    def createTableTeacher(self):
        model = QStandardItemModel()
        model.setHorizaontalHeaderLabels(['EID', 'NAME', 'EMAIL', 'DEPARTMENT', 'STATUS'])
        table = self.widgetAdmin2
        table.setModel(model)

    def searchTeacher(self):
        try:
            inputSearch = self.inputSearch2.text().strip()

            myDB._open_connection()
            mycursor = myDB.cursor(dictionary=True)

            if len(inputSearch) > 0:
                sql = "SELECT * FROM user_table WHERE Lastname LIKE CONCAT('%', %s, '%') OR Employee_ID = %s ORDER BY Lastname ASC"
                val = (inputSearch, inputSearch)
                mycursor.execute(sql, val)
            else:
                return

            myresult = mycursor.fetchall()
            self.widgetAdmin2.setRowCount(len(myresult))  # set number of rows
            self.widgetAdmin2.setColumnCount(5)

            rowcount = 0
            for row in myresult:
                if row['Status'] == 1:
                    status = 'Active'
                else:
                    status = 'Inactive'
                self.widgetAdmin2.setItem(rowcount, 0, QTableWidgetItem(str(row['Employee_ID'])))
                self.widgetAdmin2.setItem(rowcount, 1, QTableWidgetItem(row['Lastname']))
                self.widgetAdmin2.setItem(rowcount, 2, QTableWidgetItem(row['Email']))
                self.widgetAdmin2.setItem(rowcount, 3, QTableWidgetItem(row['Department']))
                self.widgetAdmin2.setItem(rowcount, 4, QTableWidgetItem(status))
                rowcount = rowcount + 1

            self.widgetAdmin2.horizontalHeader().setStretchLastSection(True)
            self.widgetAdmin2.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)


        except mysql.connector.Error as err:
            print("Error:", err.msg)
        finally:
            mycursor.close()
            myDB.close()


    def filterTeacher(self, index):
        try:
            teacherFilter = self.cmbFilter2.itemText(index)

            myDB._open_connection()
            mycursor = myDB.cursor(dictionary=True)

            if teacherFilter == 'Active':
                sql = 'SELECT * FROM user_table WHERE Status = 1 AND Userlevel = 2 ORDER BY Lastname ASC'
            elif teacherFilter == 'Inactive':
                sql = 'SELECT * FROM user_table WHERE Status = 0 AND Userlevel = 2 ORDER BY Lastname ASC'
            else:
                sql = 'SELECT * FROM user_table WHERE Userlevel = 2 ORDER BY Lastname ASC'

            mycursor.execute(sql)

            # self.course_table.addItem(row['CourseCode'], row['CID'])
            myresult = mycursor.fetchall()
            self.widgetAdmin2.setRowCount(len(myresult))  # set number of rows
            self.widgetAdmin2.setColumnCount(5)

            rowcount = 0

            for row in myresult:
                if row['Status'] == 1:
                        status = 'Active'
                else:
                    status = 'Inactive'
                self.widgetAdmin2.setItem(rowcount, 0, QTableWidgetItem(str(row['Employee_ID'])))
                self.widgetAdmin2.setItem(rowcount, 1, QTableWidgetItem(row['Lastname']))
                self.widgetAdmin2.setItem(rowcount, 2, QTableWidgetItem(row['Firstname']))
                self.widgetAdmin2.setItem(rowcount, 3, QTableWidgetItem(row['Email']))
                self.widgetAdmin2.setItem(rowcount, 4, QTableWidgetItem(row['Department']))
                self.widgetAdmin2.setItem(rowcount, 5, QTableWidgetItem(status))
                rowcount = rowcount + 1

            self.widgetAdmin2.horizontalHeader().setStretchLastSection(True)
            self.widgetAdmin2.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        except mysql.connector.Error as err:
            print('Error:', err.msg)
        finally:
            mycursor.close()
            myDB.close()


    def newTeacher(self):
        self.btnTeacherNew.setEnabled(False)
        self.btnTeacherSave.setEnabled(True)
        self.btnTeacherCancel.setEnabled(True)
        self.groupTeacher.setEnabled(True)
        self.inputEmployeeID.setFocus()

    def cancelTeacher(self):
        self.btnTeacherNew.setEnabled(True)
        self.btnTeacherSave.setEnabled(False)
        self.btnTeacherCancel.setEnabled(False)
        self.groupTeacher.setEnabled(False)

    def on_currentIndexChanged(self, index):
        print(self.cmbDepartment.itemText(index))
        print(self.cmbDepartment.itemData(index))
        global getCourseID
        getCourseID = self.cmbDepartment.itemData(index)


    def saveTeacher(self):
        userlevel = 2
        employeeID = self.inputEmployeeID.text().strip()
        department = self.cmbDepartment.currentText()
        teacherEmail = self.inputTeacherEmail.text().strip()
        teacherContact = self.inputTeacherContact.text().strip()
        teacherLast = self.inputTeacherLast.text().strip()
        teacherFirst = self.inputTeacherFirst.text().strip()
        teacherMI = self.inputTeacherMI.text().strip()
        teacherPre = self.cmbPrefix.currentText()

        if employeeID == "":
            QMessageBox.critical(self, "Required Input", "Please input Employee ID")
            self.inputEmployeeID.setFocus()
            return

        if teacherPre == '-Prefix-':
            QMessageBox.critical(self, "Required Selection", "Please select a Prefix")
            return

        if teacherEmail == "":
            QMessageBox.critical(self, "Required Input", "Please input Employee Email")
            self.inputTeacherEmail.setFocus()
            return

        if department == 0:
            QMessageBox.critical(self, "Required Selection", "Please select Department")
            self.cmbDepartment.setFocus()
            return

        if not re.match(r"[^@]+@[^@]+\.[^@]", teacherEmail):
            QMessageBox.critical(self, "Invalid Input", "Invalid Input Address")
            self.inputTeaacherEmail.setFocus()
            return

        if teacherContact == "":
            QMessageBox.critical(self, "Required Input", "Please input Employee's Contact")
            self.inputTeacherContact.setFocus()
            return

        if teacherLast == "":
            QMessageBox.critical(self, "Required Input", "Please input Employee's Surname")
            self.inputTeacherLast.setFocus()
            return

        if teacherFirst == "":
            QMessageBox.critical(self, "Required Input", "Please input Employee's First Name")
            self.inputTeacherFirst.setFocus()
            return

        try:
            myDB._open_connection()
            mycursor = myDB.cursor()

            sql = 'INSERT INTO user_table(Employee_ID, Department, Email, Contact, Prefix, Lastname, Firstname, MI, Userlevel) ' \
                  'VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)'
            val = (employeeID, department, teacherEmail, teacherContact, teacherPre, teacherLast, teacherFirst, teacherMI, userlevel)
            mycursor.execute(sql, val)

            myDB.commit()

            print(mycursor.rowcount, "record inserted")
            self.populateRecord()
            QMessageBox.information(self, "System Information", "Employee Account Successfully Created!")


        except mysql.connector.Error as err:
            QMessageBox.warning(self, "System Information", "Employee already existed!")
            print("Error:", err.msg)

        finally:
            mycursor.close()
            myDB.close()


    def setstatusTeacher(self):
        try:
            selected = []  # triggers when a row is selected in widget
            for i in range(1):
                selected.append(self.widgetAdmin2.item(self.widgetAdmin2.currentRow(), i).text())

            print(selected)

            myDB._open_connection()
            mycursor = myDB.cursor()

            sql = 'UPDATE user_table SET Status = %s WHERE Employee_ID = %s'
            val = (userStatus, selected[0])
            mycursor.execute(sql, val)

            myDB.commit()

            self.populateRecordTeacher()
            self.populateRecordTeacher()
            print(mycursor.rowcount, 'record updated')

        except mysql.connector.Error as err:
            print('Error:', err.msg)
        finally:
            mycursor.close()
            myDB.close()

#-------------End of Manage Teacher

#-------------Start of Manage User

    def createTableUser(self):
        model = QStandardItemModel()
        model.setHorizaontalHeaderLabels(['SID', 'LAST NAME', 'FIRST NAME', 'EMAIL', 'STATUS'])
        table = self.widgetAdmin1
        table.setModel(model)

    def searchUser(self):
        try:
            inputSearch = self.inputSearch1.text().strip()

            myDB._open_connection()
            mycursor = myDB.cursor(dictionary=True)

            if len(inputSearch) > 0:
                sql = "SELECT * FROM user_table WHERE Lastname LIKE CONCAT('%', %s, '%') OR Student_ID = %s ORDER BY Lastname ASC"
                val = (inputSearch, inputSearch)
                mycursor.execute(sql, val)
            else:
                return

            myresult = mycursor.fetchall()
            self.widgetAdmin1.setRowCount(len(myresult))  # set number of rows
            self.widgetAdmin1.setColumnCount(5)

            rowcount = 0
            for row in myresult:
                if row['Status'] == 1:
                    status = 'Active'
                else:
                    status = 'Inactive'
                self.widgetAdmin1.setItem(rowcount, 0, QTableWidgetItem(str(row['Student_ID'])))
                self.widgetAdmin1.setItem(rowcount, 1, QTableWidgetItem(row['Lastname']))
                self.widgetAdmin1.setItem(rowcount, 2, QTableWidgetItem(row['Firstname']))
                self.widgetAdmin1.setItem(rowcount, 3, QTableWidgetItem(row['Email']))
                self.widgetAdmin1.setItem(rowcount, 4, QTableWidgetItem(status))
                rowcount = rowcount + 1

            self.widgetAdmin1.horizontalHeader().setStretchLastSection(True)
            self.widgetAdmin1.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)


        except mysql.connector.Error as err:
            print("Error:", err.msg)
        finally:
            mycursor.close()
            myDB.close()


    def filterUser(self, index):
        try:
            userFilter = self.cmbFilter1.itemText(index)

            myDB._open_connection()
            mycursor = myDB.cursor(dictionary=True)

            if userFilter == 'Active':
                sql = 'SELECT * from user_table WHERE Status = 1 AND Userlevel = 3 ORDER BY Lastname ASC'
            elif userFilter == 'Inactive':
                sql = 'SELECT * FROM user_table WHERE Status = 0 AND Userlevel = 3 ORDER BY Lastname ASC'
            else:
                sql = 'SELECT * FROM user_table WHERE Userlevel = 3 ORDER BY Lastname ASC'

            mycursor.execute(sql)

            # self.course_table.addItem(row['CourseCode'], row['CID'])
            myresult = mycursor.fetchall()
            self.widgetAdmin1.setRowCount(len(myresult))  # set number of rows
            self.widgetAdmin1.setColumnCount(5)

            rowcount = 0

            for row in myresult:
                if row['Status'] == 1:
                    status = 'Active'
                else:
                    status = 'Inactive'
                self.widgetAdmin1.setItem(rowcount, 0, QTableWidgetItem(str(row['Student_ID'])))
                self.widgetAdmin1.setItem(rowcount, 1, QTableWidgetItem(row['Lastname']))
                self.widgetAdmin1.setItem(rowcount, 2, QTableWidgetItem(row['Firstname']))
                self.widgetAdmin1.setItem(rowcount, 3, QTableWidgetItem(row['Email']))
                self.widgetAdmin1.setItem(rowcount, 4, QTableWidgetItem(status))
                rowcount = rowcount + 1

            self.widgetAdmin1.horizontalHeader().setStretchLastSection(True)
            self.widgetAdmin1.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        except mysql.connector.Error as err:
            print("Error:", err.msg)
        finally:
            mycursor.close()
            myDB.close()


    def setstatusStudent(self):
        try:
            selected = []  # triggers when a row is selected in widget
            for i in range(1):
                selected.append(self.widgetAdmin1.item(self.widgetAdmin1.currentRow(), i).text())

            print(selected)

            myDB._open_connection()
            mycursor = myDB.cursor()

            sql = 'UPDATE user_table SET Status = %s WHERE Student_ID = %s'
            val = (userStatus, selected[0])
            mycursor.execute(sql, val)

            myDB.commit()

            self.populateRecordStudent()
            print(mycursor.rowcount, 'record updated')

        except mysql.connector.Error as err:
            print('Error:', err.msg)
        finally:
            mycursor.close()
            myDB.close()

#-------------End of Manage Student