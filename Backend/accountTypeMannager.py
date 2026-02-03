import sqlite3


def authAdmin(UID):
    try:
        conn = sqlite3.connect('./instance/db.sqlite3')
        cur = conn.cursor()
    except:
        return "connection failed"
    try:
        sql = '''SELECT ACCOUNTTYPE FROM users WHERE ROWID = ''' + str(UID) + ';'
        cur.execute(sql)
        accountType = cur.fetchone()
    except:
        print("retrieval failed")
        return "retrival failed"
    if str(accountType[0]) == "Admin":
        print("True")
        return True
    else:
        print("False")
        return False


def fetchUsers(UID):
    try:
        conn = sqlite3.connect('./instance/db.sqlite3')
        cur = conn.cursor()
    except:
        return "connection failed"
    if authAdmin(UID) == True:
        try:
            sql = '''SELECT ROWID, USERNAME, ACCOUNTTYPE FROM users'''
            cur.execute(sql)
            userList = cur.fetchall()
            print(userList)
            return userList
        except:
            print("Fetch failed")
            return "Fetch failed"
    else:
        print("User not verified for this action")
        return "User not verified for this action"
    

def updateAccountType(UID,targetUID, newAccountType):
    try:
        conn = sqlite3.connect('./instance/db.sqlite3')
        cur = conn.cursor()
    except:
        return "connection failed"
    if authAdmin(UID) == True:
        try:
            sql = '''UPDATE users SET accounttype = "''' + newAccountType + '" WHERE ROWID = ' + str(targetUID) + ';'
            conn.execute(sql)
            conn.commit()
            print ("User " + str(targetUID) + " updated to account type " + newAccountType)
            return ("User " + str(targetUID) + " updated to account type " + newAccountType)
        except:
            print("Update failed")
            return "Update failed"
    else:
        print("User not verified for this action")
        return "User not verified for this action"

