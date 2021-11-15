import mysql.connector

def interestRateCal(account_id):
    myconn = mysql.connector.connect(
        host="localhost", user="root", passwd="!@#$%^&*()qwertyuiopWinter2021", database="iKYC")
    cursor = myconn.cursor()
    sql = """
    UPDATE Account INNER JOIN
    (SELECT a.balance * POW(1+ir.interest_rate, d.day) newBalance
    FROM (SELECT DISTINCT DATEDIFF(now(), LH.login_date) day
    FROM LoginHistory LH WHERE LH.login_date = (
        SELECT lh.login_date FROM(
        SELECT LH.login_date FROM LoginHistory LH, Account A
        WHERE LH.username = A.username AND A.account_id = %s
        ORDER BY LH.login_date DESC LIMIT 2
        )lh ORDER BY lh.login_date ASC LIMIT 1)) d, 
    (SELECT A.balance balance FROM Account A WHERE A.account_id = %s) a,
    
    (SELECT (Cur.interest_rate / 365) interest_rate FROM Currency Cur, Account A
        WHERE A.currency = Cur.currency_ID AND A.account_id = %s) ir) temp
    
    SET balance = temp.newBalance WHERE account_id = %s
    """
    value = (account_id, account_id, account_id, account_id)
    cursor.execute(sql, value)
    result = cursor.fetchall()
    myconn.commit()

    myconn = mysql.connector.connect(
        host="localhost", user="root", passwd="!@#$%^&*()qwertyuiopWinter2021", database="iKYC")
    cursor = myconn.cursor()
    sql = """
    SELECT balance FROM Account WHERE account_id=%s
    """
    value = (account_id,)
    cursor.execute(sql, value)
    result = cursor.fetchall()
    myconn.commit()
    return result[0][0]

interestRateCal(1)