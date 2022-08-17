import mysql.connector

mydb = mysql.connector.connect(host="localhost", user="root", passwd="1234", database="challenge_me")
mycursor = mydb.cursor()
mycursor.execute("select * from player")

for i in mycursor:
    print(i)
