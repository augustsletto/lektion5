import mysql.connector

db = mysql.connector.connect(
    host = "localhost", 
    port = 3336,
    user = "root",
    password = "password",
    database = "northwind",
    

)


cursor = db.cursor()

query = "SELECT EmployeeID, LastName, FirstName, Title FROM northwind.Employees;"

cursor.execute(query)

for (EmployeeID, LastName, FirstName, Title) in cursor:
    print(f"{EmployeeID}, {LastName}, {FirstName}, {Title}")