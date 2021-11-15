import mysql.connector


def removeLeadingZero(s):
    while s[0] == "0":
        s = s[1:]
    return s


def printTransactionRecords(account_id):
    account_id = int(removeLeadingZero(account_id))

    # get my exchange rate
    myconn = mysql.connector.connect(
        host="localhost", user="root", passwd="!@#$%^&*()qwertyuiopWinter2021", database="iKYC")
    cursor = myconn.cursor()
    sql = """
    SELECT C.exchange_rate
    FROM Account A, Currency C
    WHERE
        A.account_id=%s
        AND A.currency=C.currency_ID
    """
    value = (account_id, )
    cursor.execute(sql, value)
    result = cursor.fetchall()
    myconn.commit()
    myExchange_rate = result[0][0]

    lose = []
    myconn = mysql.connector.connect(
        host="localhost", user="root", passwd="!@#$%^&*()qwertyuiopWinter2021", database="iKYC")
    cursor = myconn.cursor()
    sql = "SELECT to_Customer_id, msg, amount, trans_time, trans_date FROM Transaction WHERE from_Customer_id=%s"
    value = (account_id, )
    cursor.execute(sql, value)
    result = cursor.fetchall()
    myconn.commit()
    for i in result:
        lose += [[i[0],i[1],-i[2],str(i[3]),str(i[4])]]

    gain = []
    myconn = mysql.connector.connect(
        host="localhost", user="root", passwd="!@#$%^&*()qwertyuiopWinter2021", database="iKYC")
    cursor = myconn.cursor()
    sql = """
    SELECT T.from_Customer_id, T.msg, (T.amount * C.exchange_rate / %s)
    ,T.trans_time, T.trans_date
    FROM Transaction T, Account A, Currency C
    WHERE
        T.to_Customer_id=%s
        AND T.from_Customer_id=A.account_id
        AND A.currency=C.currency_ID
    """
    value = (myExchange_rate, account_id, )
    cursor.execute(sql, value)
    result = cursor.fetchall()
    myconn.commit()
    for i in result:
        gain += [[i[0],i[1],i[2],str(i[3]),str(i[4])]]
    

    all = gain + lose
    for i in range(len(all) - 1):
        for j in range(len(all) - i - 1):
            if ((all[j][4]<all[j+1][4]) or ((all[j][4]==all[j+1][4]) and (all[j][3]<all[j+1][3]))):
                tmp = all[j]
                all[j] = all[j+1]
                all[j+1] = tmp
    
    for i in range(len(all)):
        if (float(all[i][2])>0):
            all[i] += ['earn']
        else:
            all[i] += ['lose']
        all[i][2] = "%.2f" % round(all[i][2],2)
    
    return all

answer = printTransactionRecords("00000001")
for i in answer:
    print(i)