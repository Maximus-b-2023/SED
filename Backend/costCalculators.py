import sqlite3


def getCropPrice(userinput):
    try:
        conn = sqlite3.connect('./instance/db.sqlite3')
        cur = conn.cursor()
    except:
        return "connection failed"
    sql = 'select LOWESTSELLINGPRICE from crops WHERE ID ="'+ str(userinput) + '";'
    cur.execute(sql)
    cropValue = cur.fetchone()
    return int(cropValue[0])

def getSeedPrice(userinput):
    try:
        conn = sqlite3.connect('./instance/db.sqlite3')
        cur = conn.cursor()
    except:
        return "connection failed"
    sql = 'select SEEDPRICE from crops WHERE ID ="'+ str(userinput) + '";'
    cur.execute(sql)
    seedPrice = cur.fetchone()
    return int(seedPrice[0])

def calcMinValue(cropName, quantity):
    minValue = quantity * getCropPrice(cropName)
    return minValue

def calcSeedCost(cropID, quantity):
    seedsCost = quantity * getSeedPrice(cropID)
    return seedsCost
