# import sqlite3

# def createUserTable():
#     conn = sqlite3.connect('./instance/db.sqlite3')

#     conn.execute('''CREATE TABLE IF NOT EXISTS user
#                  (USERNAME       TEXT    NOT NULL,
#                  PASSWORD       TEXT    NOT NULL,
#                  EMAIL          TEXT    NOT NULL,
#                  ACCOUNTTYPE    TEXT    NOT NULL);''')
#     print("Table Created successfully")

# def createLicencesTable():
#     conn = sqlite3.connect('./instance/db.sqlite3')

#     conn.execute('''CREATE TABLE IF NOT EXISTS licences
#                  (CROPNAME       TEXT    NOT NULL,
#                  SEEDPRICE       INT    NOT NULL,
#                  LOWESTSELLINGPRICE          INT    NOT NULL);''')
#     print("Table Created successfully")

# def createSalesTable():
#     conn = sqlite3.connect('./instance/db.sqlite3')

#     conn.execute('''CREATE TABLE IF NOT EXISTS sales
#                  (USERID         TEXT   NOT NULL,
#                  CROPNAME       TEXT    NOT NULL,
#                  SEASON         TEXT    NOT NULL,
#                  QUANTITYSOLD          TEXT    NOT NULL,
#                  PROFITMADE     INT     NOT NULL,
#                  FOREIGN KEY(USERID) REFERENCES user(ROWID));''')
#     print("Table Created successfully")

# createUserTable()
# createLicencesTable()
# createSalesTable()