# import sqlite3


# def fetchCrops(UID):
#     try:
#         conn = sqlite3.connect('./instance/db.sqlite3')
#         cur = conn.cursor()
#     except:
#         return "connection failed"
#     try:
#         sql = '''SELECT ROWID, CROPNAME, SEEDPRICE, LOWESTSELLINGPRICE FROM crops'''
#         cur.execute(sql)
#         cropsList = cur.fetchall()
#         print(cropsList)
#         return cropsList
#     except:
#         print("Fetch failed")
#         return "Fetch failed"