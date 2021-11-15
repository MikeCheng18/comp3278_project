import mysql.connector
from datetime import datetime

def removeLeadingZero(s):
    while s[0] == "0":
        s = s[1:]
    return s


def transferProgressFromPy(amount, msg, myID, receipent_id):
    # Check is my account saving account
    tmpMyID = removeLeadingZero(myID)
    myconn = mysql.connector.connect(
        host="localhost", user="root", passwd="!@#$%^&*()qwertyuiopWinter2021", database="iKYC")
    cursor = myconn.cursor()
    sql = "SELECT type, username FROM Account WHERE account_id=%s"
    value = (tmpMyID, )
    cursor.execute(sql, value)
    result = cursor.fetchall()
    myconn.commit()

    if (len(result) == 1):
        if (result[0][0] == 's'):
            tmp_receipent_id = removeLeadingZero(receipent_id)
            myconn = mysql.connector.connect(
                host="localhost", user="root", passwd="!@#$%^&*()qwertyuiopWinter2021", database="iKYC")
            cursor = myconn.cursor()
            sql = "SELECT type FROM Account WHERE account_id=%s AND username=%s"
            value = (tmp_receipent_id, result[0][1])
            cursor.execute(sql, value)
            result = cursor.fetchall()
            myconn.commit()
            if (len(result) == 0):
                return "500"

        # add transaction record
        myconn = mysql.connector.connect(
            host="localhost", user="root", passwd="!@#$%^&*()qwertyuiopWinter2021", database="iKYC")
        cursor = myconn.cursor()
        sql = "INSERT INTO Transaction (to_Customer_id, from_Customer_id, msg, amount, trans_time, trans_date) VALUES (%s,%s,%s,%s,%s,%s)"
        date = datetime.utcnow()
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        value = (receipent_id, myID, msg, amount, current_time, date)
        cursor.execute(sql, value)
        result = cursor.fetchall()
        myconn.commit()

        myID = removeLeadingZero(myID)
        receipent_id = removeLeadingZero(receipent_id)

        # substract my money
        myconn = mysql.connector.connect(
            host="localhost", user="root", passwd="!@#$%^&*()qwertyuiopWinter2021", database="iKYC")
        cursor = myconn.cursor()
        sql = "UPDATE Account SET balance=balance-%s WHERE account_id=%s"
        value = (amount, myID)
        cursor.execute(sql, value)
        result = cursor.fetchall()
        myconn.commit()

        # add his money
        myconn = mysql.connector.connect(
            host="localhost", user="root", passwd="!@#$%^&*()qwertyuiopWinter2021", database="iKYC")
        cursor = myconn.cursor()
        sql = """
        SELECT C.exchange_rate
        FROM Currency AS C, Account AS A
        WHERE
            A.currency = C.currency_ID
            AND A.account_id=%s
        """
        value = (receipent_id,)
        cursor.execute(sql, value)
        result = cursor.fetchall()
        myconn.commit()
        receipentRate = result[0][0]

        myconn = mysql.connector.connect(
            host="localhost", user="root", passwd="!@#$%^&*()qwertyuiopWinter2021", database="iKYC")
        cursor = myconn.cursor()
        sql = """
        SELECT C.exchange_rate
        FROM Currency AS C, Account AS A
        WHERE
            A.currency = C.currency_ID
            AND A.account_id=%s
        """
        value = (myID,)
        cursor.execute(sql, value)
        result = cursor.fetchall()
        myconn.commit()
        myRate = result[0][0]

        myconn = mysql.connector.connect(
            host="localhost", user="root", passwd="!@#$%^&*()qwertyuiopWinter2021", database="iKYC")
        cursor = myconn.cursor()
        sql = """
        UPDATE Account as B
        SET B.balance = B.balance + 
        (%s * %s / %s)
        WHERE B.account_id=%s"""
        print(amount, myRate, receipentRate, receipent_id)
        value = (amount, myRate, receipentRate, receipent_id)
        cursor.execute(sql, value)
        result = cursor.fetchall()
        myconn.commit()

        return "OK"
    return "404"
