import sqlite3

from accountTypeMannager import authAdmin


def fetchSales(UID):
    try:
        conn = sqlite3.connect('./instance/db.sqlite3')
        cur = conn.cursor()
    except:
        return "connection failed"
    if authAdmin(UID) == True:
        try:
            sql = '''SELECT ROWID,* FROM sales'''
            cur.execute(sql)
            saleList = cur.fetchall()
            print(saleList)
            return saleList
        except:
            print("Fetch failed")
            return "Fetch failed"
    else:
        print("User not verified for this action")
        return "User not verified for this action"

def deleteSales(UID,saleID):
    try:
        conn = sqlite3.connect('./instance/db.sqlite3')
    except:
        return "connection failed"
    if authAdmin(UID) == True:
        try:
            sql = '''DELETE FROM sales WHERE ROWID = ''' + str(saleID) + ";"
            conn.execute(sql)
            conn.commit()
            print("Delete successful")
            return "Delete successful"
        except:
            print("Delete unsuccessful "+ str(sql))
            return "Delete unsuccessful"
    else:
        print("User not verified for this action")
        return "User not verified for this action"
