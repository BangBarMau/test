
from datetime import datetime
import mysql
from PyQt5.QtCore import QTimer,QTime
from PyQt5.QtWidgets import QDialog, QMessageBox, QTableWidgetItem, QHeaderView
from PyQt5.uic import loadUi

from changePassStudent import *
from connection import myDB


class createStudent(QDialog):
    def __init__(self):
        super(createStudent, self).__init__()
        loadUi('newstudent.ui', self)
        self.btnStudentLogout.clicked.connect(self.logout)
        self.btnStudentSettings.clicked.connect(self.gotoChange)
        self.btnSet.clicked.connect(self.setAppointment)
        self.cmbDepartment.activated.connect(self.SelectedDepartment)
        self.cmbInstructor.activated.connect(self.on_currentIndexChanged)
        global getEID
        getEID = self.cmbInstructor.setCurrentIndex(0)

    def logout(self):
        createStudent.hide(self)
        from main import Login
        loginForm = Login()
        loginForm.exec_()

    def gotoChange(self):
        createStudent.hide(self)
        changeForm = changePassStudent()
        changeForm.exec_()

    def populateRecord(self):
        try:
            SID = globals.getSID

            myDB._open_connection()
            mycursor = myDB.cursor(dictionary=True)

            sql = "SELECT CONCAT(U.Lastname, ', ', U.Firstname, ' ', U.MI) AS InstructorName, A.AID, A.Department, A.A_Date, A.Status FROM appointment_table AS A INNER JOIN user_table AS U ON(U.UID = A.EID) WHERE A.SID = %s ORDER BY A.A_Date AND A.Status=2 DESC"
            val = (SID,)
            mycursor.execute(sql, val)
            myresult = mycursor.fetchall()
            self.tblRecord.setRowCount(len(myresult))  ##set number of rows
            self.tblRecord.setColumnCount(5)


            rowcount = 0
            for row in myresult:
                status = ""
                if row["Status"] == 1:
                    status = "Accepted"
                if row["Status"] == 2:
                    status = "On-Going"
                if row["Status"] == 3:
                    status = "Declined"
                if row["Status"] == 4:
                    status = "Cancelled"

                self.tblRecord.setItem(rowcount, 0, QTableWidgetItem(str(row["AID"])))
                self.tblRecord.setColumnHidden(0, True) #-->> To Hide Column AID
                self.tblRecord.setItem(rowcount, 1, QTableWidgetItem(row["InstructorName"]))
                self.tblRecord.setItem(rowcount, 2, QTableWidgetItem(row["Department"]))
                self.tblRecord.setItem(rowcount, 3, QTableWidgetItem(str(row["A_Date"])))
                self.tblRecord.setItem(rowcount, 4, QTableWidgetItem(status))
                #self.tblRecord.setItem(rowcount, 3, QTableWidgetItem(QIcon("source-files/resources/images/cancel.png"),"", 1)) #THIS IS TO DISPLAY IMAGE TO TABLE WIDGET

                rowcount = rowcount + 1

            self.tblRecord.horizontalHeader().setStretchLastSection(True)
            self.tblRecord.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)


        except mysql.connector.Error as err:
                print("Error:", err.msg)
        finally:
            mycursor.close()
            myDB.close()
            print("MySQL connection is closed")

    def timeprogress(self):
        self.lblTimeAndDate.setText(datetime.today().strftime('%m-%d-%Y | %I:%M:%S %p'))

    def on_currentIndexChanged(self, index):
        global getEID
        getEID = self.cmbInstructor.itemData(index)

    def SelectedDepartment(self):
        try:
            selectedDept = str(self.cmbDepartment.currentText())
            #print(selectedDept)

            myDB._open_connection()
            mycursor = myDB.cursor(dictionary=True)

            sql = "SELECT CONCAT(Prefix, ' ', Lastname, ', ', Firstname) AS Fullname, UID FROM user_table WHERE Department = %s ORDER BY Lastname ASC"
            val = (selectedDept, )
            mycursor.execute(sql, val)

            myresult = mycursor.fetchall()

            self.cmbInstructor.clear()
            self.cmbInstructor.addItem("--Select Instructor--", 0)
            for row in myresult:
                self.cmbInstructor.addItem(row["Fullname"], row["UID"])
            print(myresult)#for testing the result
        except mysql.connector.Error as err:
            print("Error:", err.msg)
        finally:
            self.cmbInstructor.setCurrentIndex(0)
            mycursor.close()
            myDB.close()
            print("MySQL connection is closed")

    def setAppointment(self):
        global getEID
        getEID = 0
        global getSID
        getSID = 0
        EID = getEID
        SID = getSID
        Subject = self.inputAppointmentSubject.text().strip()
        DepartmentIndex = self.cmbDepartment.currentIndex()
        Instructor = str(self.cmbInstructor.currentIndex())
        DepartmentText = str(self.cmbDepartment.currentText())
        Details = self.txtDetails.toPlainText().strip()
        Date = datetime.today().strtime('%Y-%m-%d')
        Time = self.timeSet.time().toString()

        # -->>TIMER START
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.timeprogress)
        # -->>TIME IN MILLISECONDS
        self.timer.start(1000)  # set to 35 for fast load

        # -->>INITIAL TEXT
        self.lblTimeAndDate.setText(datetime.today().strftime('%m-%d-%Y | %I:%M:%S %p'))

        # -->>POPULATE DATA RECORD FROM DATABASE
        self.populateRecord()

        if len(Subject) == 0:
            QMessageBox.critical(self, 'Required Input', 'Please Enter Appointment Subject')
            self.txtAppointment.setFocus()
            return
        if DepartmentIndex == 0:
            QMessageBox.critical(self, 'Required Selection', 'Please Select a Department')
            self.cmbDepartment.setFocus()
            return
        if EID == 0 or EID == None or Instructor == "--Select Instructor--":
            QMessageBox.critical(self, 'Required Selection', 'Please Select an Instructor')
            self.cmbInstructor.setFocus()
            return
        try:
            myDB._open_connection()
            mycursor = myDB.cursor(dictionary = True)

            """---------------For trapping of once per day of appointment here--------------"""
            sql = "SELECT COUNT(AID) AS TotalCount, Department FROM appointment_table WHERE A_Date = %s AND Department = %s AND SID = %s AND Status = %s"
            val = (Date, DepartmentText, SID, 2)
            mycursor.execute(sql, val)

            myresult = mycursor.fetchall()

            print(myresult)  # testing result of limit per day

            for getResult in myresult:

                if getResult["TotalCount"] < 1:
                    print("pwede pa")
                else:
                    QMessageBox.information(self, 'System Info',
                                            "You have pending appointment for " + DepartmentText + " Department! Please come back later or cancel your pending appointment!",
                                            QMessageBox.Ok)
                    return

            """---------------End trapping of once per day of appointment--------------"""

            """---------------For trapping the priority number here--------------"""
            sql = "SELECT COUNT(AID) AS TotalCount, Department FROM appointment_table WHERE A_Date = %s AND Department = %s"
            val = (Date, DepartmentText)
            mycursor.execute(sql, val)

            myresult = mycursor.fetchall()

            print(myresult)  # testing result of limit per day

            getLastPriorityNumber = 1  # default for first Priority number
            for getResult in myresult:

                if getResult["TotalCount"] < 5:
                    print("pwede pa")
                else:
                    QMessageBox.information(self, 'System Info',
                                            "Maximum appointment for " + DepartmentText + " Department! Please come back tomorrow!",
                                            QMessageBox.Ok)
                    return
                getLastPriorityNumber = getResult["TotalCount"] + 1

            """---------------End of trapping the priority number--------------"""

            msgboxButton = QMessageBox.question(self, 'System', "Do you want to set this appointment schedule?",
                                                QMessageBox.Yes | QMessageBox.No,
                                                QMessageBox.No)
            if msgboxButton == QMessageBox.Yes:
                sql = "INSERT INTO appointment_table(SID, EID, Subject, Department, Details, A_Date, A_Time, PriorityNo) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
                val = (SID, EID, Subject, DepartmentText, Details, Date, Time, getLastPriorityNumber)
                mycursor.execute(sql, val)

                myDB.commit()

                print(mycursor.rowcount, "Record Inserted.")
                QMessageBox.warning(self, "System Info", "Successfully Saved Appointment!")
                self.populateRecord() #--> To refresh table record
            else:
                print("Nothing Inserted")

        except mysql.connector.Error as err:
            print("Error:", err.msg)
        finally:
            mycursor.close()
            myDB.close()