import mysql.connector
from datetime import datetime

def removeLeadingZero(s):
    while s[0] == "0":
        s = s[1:]
    return s

def homePage(username):
    myconn = mysql.connector.connect(
    host="localhost", user="root", passwd="!@#$%^&*()qwertyuiopWinter2021", database="iKYC")
    cursor = myconn.cursor() 
    sql = "SELECT currency_id, exchange_rate, interest_rate FROM Currency ORDER BY currency_id"
    value = ()
    cursor.execute(sql, value)
    result = cursor.fetchall()
    myconn.commit()
    exchangeTable = result

    # current account table
    myconn = mysql.connector.connect(
    host="localhost", user="root", passwd="!@#$%^&*()qwertyuiopWinter2021", database="iKYC")
    cursor = myconn.cursor() 
    sql = "SELECT A.account_id, A.currency, A.balance FROM Account AS A, Currency AS C WHERE A.username=%s AND A.type='c' AND A.currency=C.currency_id ORDER BY (A.balance*C.exchange_rate) DESC, A.account_id DESC"
    value = (username, )
    cursor.execute(sql, value)
    result = cursor.fetchall()
    myconn.commit()
    currentTable = []
    for i in result:
        from interestRateCal import interestRateCal
        tmp = interestRateCal(i[0])
        currentTable += [[str(i[0]).zfill(6), i[1], "%.2f" % round(tmp,2), "%.2f" % round(tmp - i[2],2)]]

    myconn = mysql.connector.connect(
    host="localhost", user="root", passwd="!@#$%^&*()qwertyuiopWinter2021", database="iKYC")
    cursor = myconn.cursor() 
    sql = "SELECT A.account_id, A.currency, A.balance FROM Account AS A, Currency AS C WHERE A.username=%s AND A.type='s' AND A.currency=C.currency_id ORDER BY (A.balance*C.exchange_rate) DESC, A.account_id DESC"
    value = (username, )
    cursor.execute(sql, value)
    result = cursor.fetchall()
    myconn.commit()
    savingTable = []
    for i in result:
        from interestRateCal import interestRateCal
        tmp = interestRateCal(i[0])
        savingTable += [[str(i[0]).zfill(6), i[1], "%.2f" % round(tmp,2), "%.2f" % round(tmp - i[2],2)]]

    myconn = mysql.connector.connect(
    host="localhost", user="root", passwd="!@#$%^&*()qwertyuiopWinter2021", database="iKYC")
    cursor = myconn.cursor() 
    sql = '''
    SELECT C.currency_id FROM Currency C WHERE C.currency_id NOT IN (SELECT currency FROM Account WHERE username=%s AND type='s')
    '''
    value = (username, )
    cursor.execute(sql, value)
    result = cursor.fetchall()
    myconn.commit()
    savingDiff = result
    
    myconn = mysql.connector.connect(
    host="localhost", user="root", passwd="!@#$%^&*()qwertyuiopWinter2021", database="iKYC")
    cursor = myconn.cursor() 
    sql = '''
    SELECT C.currency_id FROM Currency C WHERE C.currency_id NOT IN (SELECT currency FROM Account WHERE username=%s AND type='c')
    '''
    value = (username, )
    cursor.execute(sql, value)
    result = cursor.fetchall()
    myconn.commit()
    currentDiff = result

    return exchangeTable, currentTable, savingTable, savingDiff, currentDiff

homePage("AMY")