import sqlite3


def updateAccountType(targetUID, newAccountType):
    try:
        conn = sqlite3.connect('./instance/db.sqlite3')
        cur = conn.cursor()
    except:
        return "connection failed"
    #if authAdmin(UID) == True:
    try:
        sql = '''UPDATE users SET accounttype = "''' + newAccountType + '" WHERE ROWID = ' + str(targetUID) + ';'
        conn.execute(sql)
        conn.commit()
        print ("User " + str(targetUID) + " updated to account type " + newAccountType)
        return ("User " + str(targetUID) + " updated to account type " + newAccountType)
    except:
        print("Update failed")
        return "Update failed"
    #else:
        print("User not verified for this action")
        return "User not verified for this action"

conn = sqlite3.connect('./instance/db.sqlite3')
cur = conn.cursor

def mockCrops():
    try:
        conn.execute(
        '''INSERT INTO crops (CROPNAME,SEEDPRICE,LOWESTSELLINGPRICE)
        VALUES
            ("Blue Jazz",30,50),
            ("Cauliflower",80,175),
            ("Garlic",40,60),
            ("Green Bean",60,40),
            ("Kale",70,110),
            ("Parsnip",70,110),
            ("Potato",50,80),
            ("Strawberry",100,120),
            ("Tulip",20,30),
            ("Unmilled Rice",40,30);'''
        )
        conn.commit()
        print("Insert success")
    except: print("insert failed")

def mockSales():
    try:
        conn.execute(
        '''INSERT INTO sales (CROPID,SEASON,QUANTITYSOLD,PROFITMADE,USERID)
        VALUES
            (1,"Spring",10,1000,1),
            (2,"Spring",5,500,1),
            (3,"Summer",15,1500,2),
            (4,"Fall",20,2000,3),
            (5,"Winter",25,2500,4),
            (6,"Spring",30,3000,5);'''
        )
        conn.commit()
        print("Insert success")
    except: print("insert failed")

        
