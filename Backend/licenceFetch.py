# import sqlite3


# def fetchLicences(UID):
#     try:
#         conn = sqlite3.connect('./instance/db.sqlite3')
#         cur = conn.cursor()
#     except:
#         return "connection failed"
#     try:
#         sql = '''SELECT ROWID, CROPNAME, LICENCEPRICE, LOWESTSELLINGPRICE FROM licences'''
#         cur.execute(sql)
#         licencesList = cur.fetchall()
#         print(licencesList)
#         return licencesList
#     except:
#         print("Fetch failed")
#         return "Fetch failed"