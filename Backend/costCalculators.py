import sqlite3


def getLicencePrice(userinput):
    try:
        conn = sqlite3.connect('./instance/db.sqlite3')
        cur = conn.cursor()
    except:
        return "connection failed"
    sql = 'select LOWESTSELLINGPRICE from licences WHERE ID ="'+ str(userinput) + '";'
    cur.execute(sql)
    licenceValue = cur.fetchone()
    return int(licenceValue[0])

def getLicencePrice(userinput):
    try:
        conn = sqlite3.connect('./instance/db.sqlite3')
        cur = conn.cursor()
    except:
        return "connection failed"
    sql = 'select SEEDPRICE from licences WHERE ID ="'+ str(userinput) + '";'
    cur.execute(sql)
    licencePrice = cur.fetchone()
    return int(licencePrice[0])

def calcMinValue(licenceName, quantity):
    minValue = quantity * getLicencePrice(licenceName)
    return minValue

def calcLicenceCost(licenceID, quantity):
    licencesCost = quantity * getLicencePrice(licenceID)
    return licencesCost
