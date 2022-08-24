import mysql.connector

mydb = mysql.connector.connect(host="localhost", user="root", passwd="1234", database="challenge_me")

accounts = [("asd", "asd"),
            ("valaki01", "asdasd01"),
            ("valaki02", "asdasd02"),
            ("valaki03", "asdasd03")]
accounts_fighters = [("Adam", 50, 10, 4),
            ("Bela", 30, 4, 2),
            ("Lajos", 10, 5, 5),
            ("Laci", 25, 2, 12)]

mycursor = mydb.cursor()

# Q1 = "CREATE TABLE Accounts (id int PRIMARY KEY AUTO_INCREMENT, username VARCHAR(20), pswd VARCHAR(20))"
# Q2 = "CREATE TABLE Fighters (accountId int PRIMARY KEY, FOREIGN KEY(accountId) REFERENCES Accounts(id), name VARCHAR(15), hp int DEFAULT 20, power int DEFAULT 2, defense int DEFAULT 1)"
#
# mycursor.execute(Q1)
# mycursor.execute(Q2)
# mycursor.execute("SHOW TABLES")
#
# for x in mycursor:
#     print(x)

# mycursor.executemany("INSERT INTO Accounts (username, pswd) VALUES (%s, %s)", accounts)
Q3 = "INSERT INTO Accounts (username, pswd) VALUES (%s, %s)"
Q4 = "INSERT INTO Fighters (accountId, name, hp, power, defense) VALUES (%s, %s, %s, %s, %s)"

for x, account in enumerate(accounts):
    mycursor.execute(Q3, account)
    last_id = mycursor.lastrowid
    mycursor.execute(Q4, (last_id,) + accounts_fighters[x])
mydb.commit()
mycursor.execute("SELECT * FROM Fighters")
for x in mycursor:
    print(x)
mycursor.execute("SELECT * FROM Accounts")
for x in mycursor:
    print(x)

