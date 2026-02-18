import sqlite3

from costCalculators import calcLicenceCost


def createSaleReport(userId,licenceId, subscription, quantity, revenue):
    try:
        conn = sqlite3.connect('./instance/db.sqlite3')
    except:
        return "connection failed"
    profit = revenue - calcLicenceCost(licenceId, quantity)
    sql = '''INSERT INTO sales (userid,licenceid,subscription,quantitysold,profitmade) VALUES(?,?,?,?,?)'''
    params = (userId, licenceId, subscription, quantity, profit)
    try:
        conn.execute(sql, params)
        conn.commit()
        print("Insert successful")
        return("insert successful")
    except:
        print("insert failed - "+ sql + " " + str(params))
        return "insert successful"
    
createSaleReport(1, 8, "Spring", 100, 15000) 
createSaleReport(1, 1, "Spring", 10, 800) 
createSaleReport(1, 5, "Spring", 100, 9000) 
createSaleReport(2, 8, "Spring", 50, 8000) 
createSaleReport(2, 1, "Spring", 100, 8000) 
createSaleReport(2, 5, "Spring", 50, 4500) 
createSaleReport(3, 8, "Spring", 1000, 150000) 
createSaleReport(3, 1, "Spring", 20, 1600) 
createSaleReport(3, 5, "Spring", 25, 2700) 