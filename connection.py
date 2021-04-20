import mysql.connector

try:
    myDB = mysql.connector.connect(
        host = "localhost",
        user = "root",
        password = "",
        database = "db_queuing_system"
    )

    print("Database connected")
    myDB.close()

except mysql.connector.Error as err:
    print("Invalid Input: Wrong username/database or password")
    print("Error:", err.msg)