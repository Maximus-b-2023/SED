import sqlite3
from werkzeug.security import generate_password_hash

from accountTypeMannager import authAdmin


def updatePasswordAdmin(UID,targetUID, newPassword):
    try:
        conn = sqlite3.connect('./instance/db.sqlite3')
    except:
        return "connection failed"
    if authAdmin(UID) == True:
        try:
            sql = '''UPDATE users SET PASSWORD = "''' + generate_password_hash(newPassword) + '" WHERE ROWID = ' + str(targetUID) + ';'
            conn.execute(sql)
            conn.commit()
            print ("User " + str(UID) + " updated password for user " + str(targetUID))
            return ("User " + str(UID) + " updated passwordfor user " + str(targetUID))
        except:
            print("Update failed")
            return "Update failed"
    else:
        print("User not verified for this action")
        return "User not verified for this action"
    
def updatePassword(UID, newPassword):
    try:
        conn = sqlite3.connect('./instance/db.sqlite3')
    except:
        return "connection failed"
    try:
        sql = '''UPDATE users SET PASSWORD = "''' + generate_password_hash(newPassword) + '" WHERE ROWID = ' + str(UID) + ';'
        conn.execute(sql)
        conn.commit()
        print ("User " + str(UID) + " updated password")
        return ("User " + str(UID) + " updated password")
    except:
        print("Update failed")
        return "Update failed"