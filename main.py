from flask import Flask, render_template, Response, request, send_file
import mysql.connector
from datetime import datetime
import os

'''
export FLASK_APP=main
export FLASK_ENV=development
flask run
'''


def updateLogintime(username):
    myconn = mysql.connector.connect(
        host="localhost", user="root", passwd="!@#$%^&*()qwertyuiopWinter2021", database="iKYC")
    date = datetime.utcnow()
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    cursor = myconn.cursor()
    sql = "INSERT INTO `LoginHistory` (`login_time`, `login_date`, `username`) VALUE (%s, %s, %s)"
    value = (current_time, date, username)
    cursor.execute(sql, value)
    myconn.commit()


def removeLeadingZero(s):
    while s[0] == "0":
        s = s[1:]
    return s

# instatiate flask app
app = Flask(__name__, template_folder='./html')
if __name__ == '__main__':
    app.run()

# Create database connection
'''
myconn = mysql.connector.connect(
    host="localhost", user="root", passwd="!@#$%^&*()qwertyuiopWinter2021", database="iKYC")
cursor = myconn.cursor()
sql = "SELECT * FROM Customer"
value = (request.args.get('username'),request.args.get('password'))
cursor.execute(sql, value)
result = cursor.fetchall()
myconn.commit()
'''


@app.route('/')
def index():
    print("GET usernamePasswordLogin.html")
    return render_template('usernamePasswordLogin.html')


@app.route('/usernamePasswordLogin', methods=['POST', 'GET'])
def usernamePasswordLogin():
    print("POST usernamePasswordLogin")
    myconn = mysql.connector.connect(
        host="localhost", user="root", passwd="!@#$%^&*()qwertyuiopWinter2021", database="iKYC")
    cursor = myconn.cursor()
    sql = "SELECT username FROM Customer WHERE username=%s AND password=%s"
    value = (request.args.get('username'), request.args.get('password'))
    cursor.execute(sql, value)
    result = cursor.fetchall()
    myconn.commit()
    if (result == []):
        # username or password wrong
        return "404"
    else:
        updateLogintime(request.args.get('username'))
        return "OK"


@app.route('/faceIDLogin.html')
def faceIDLogin():
    print("GET faceIDLogin.html")
    return render_template('faceIDLogin.html')

@app.route('/faceIDLoginProgress', methods=['POST', 'GET'])
def faceIDLoginProgress():
    print("POST faceIDLoginProgress")
    from faceIDLoginProcessCode import faceIDLoginProcessCode
    name = faceIDLoginProcessCode()
    if (name == "404"):
        return "404"
    else:
        updateLogintime(name)
        return name

@app.route('/usernameRegister.html')
def usernameRegister():
    print("GET usernameRegister.html")
    return render_template('usernameRegister.html')

@app.route('/usernameRegisterProgress', methods=['POST', 'GET'])
def usernameRegisterProgress():
    name = request.args.get('username')
    print("GET usernameRegisterProgress with username="+name)
    
    myconn = mysql.connector.connect(
    host="localhost", user="root", passwd="!@#$%^&*()qwertyuiopWinter2021", database="iKYC")
    cursor = myconn.cursor()
    sql = "SELECT username FROM Customer WHERE username=%s"
    value = (name, )
    cursor.execute(sql, value)
    result = cursor.fetchall()
    myconn.commit()
    if (result == []):
        return "OK"
    else:
        return "404"

@app.route('/passwordRegister/<username>')
def passwordRegister(username):
    print("GET /passwordRegister/<userName>")
    return render_template('passwordRegister.html')

@app.route('/passwordRegisterProgress')
def passwordRegisterProgress():
    username = request.args.get('username')
    password = request.args.get('password')
    print("GET passwordRegisterProgress with username="+username)
    from faceCapture import faceCapture
    faceCapture(username)
    
    myconn = mysql.connector.connect(
    host="localhost", user="root", passwd="!@#$%^&*()qwertyuiopWinter2021", database="iKYC")
    cursor = myconn.cursor()
    sql = "INSERT INTO `Customer` (`username`, `password`) VALUE (%s, %s)"
    value = (username, password)
    cursor.execute(sql, value)
    result = cursor.fetchall()
    myconn.commit()
    if (result == []):
        updateLogintime(username)
        return "OK"
    else:
        return "404"

@app.route('/home/<username>')
def loginUserAccount(username):
    print("GET /home/"+username)
    from homePage import homePage
    exchangeTable, currentTable, savingTable, savingDiff, currentDiff = homePage(username)
    return render_template('home.html', username=username.capitalize(), exchangeTable=exchangeTable, currentTable=currentTable, savingTable=savingTable, savingDiff=savingDiff, currentDiff=currentDiff)

@app.route('/image/<username>')
def image(username):
    path = os.path.abspath(os.getcwd()) + '/data/' + username.upper() + '/' + username.upper()+ '005.jpg'
    return send_file(path, as_attachment=True)

@app.route('/lastLoginHistory/<username>')
def lastLoginHistory(username):
    print("GET lastLoginHistory with username="+username)
    myconn = mysql.connector.connect(
    host="localhost", user="root", passwd="!@#$%^&*()qwertyuiopWinter2021", database="iKYC")
    cursor = myconn.cursor()
    sql = "SELECT login_time, login_date FROM LoginHistory WHERE username=%s ORDER BY login_date DESC, login_time DESC LIMIT 1 OFFSET 1"
    value = (username, )
    cursor.execute(sql, value)
    result = cursor.fetchall()
    myconn.commit()
    if (len(result) == 1):
        return str(result[0][1]) + '<br>' + str(result[0][0])
    else:
        return "404"

@app.route('/transfer/<username>/<accountID>')
def transfer(username, accountID):
    accountID = removeLeadingZero(accountID)
    myconn = mysql.connector.connect(
    host="localhost", user="root", passwd="!@#$%^&*()qwertyuiopWinter2021", database="iKYC")
    cursor = myconn.cursor()
    sql = "SELECT balance, currency, type FROM Account WHERE account_id=%s"
    value = (accountID, )
    cursor.execute(sql, value)
    result = cursor.fetchall()
    myconn.commit()
    answer = str(result[0][1]) + " " +str(result[0][0])
    accoutType = result[0][2]
    if (accoutType == 's'):
        accoutType = "Saving Account"
    else:
        accoutType = "Current Account"
    return render_template('transfer.html', username=username, accountID=accountID.zfill(6), answer=answer, max=result[0][0], accoutType=accoutType)

@app.route('/transferProgress', methods=['POST', 'GET'])
def transferProgress():
    amount = request.args.get('amount')
    msg = request.args.get('msg')
    myID = request.args.get('myID')
    receipent_id = request.args.get('receipent_id')
    from transferProgressFromPy import transferProgressFromPy
    return transferProgressFromPy(amount, msg, myID, receipent_id)

@app.route('/transactionRecords/<accountID>')
def transactionRecords(accountID):
    accountID = removeLeadingZero(accountID)
    myconn = mysql.connector.connect(
    host="localhost", user="root", passwd="!@#$%^&*()qwertyuiopWinter2021", database="iKYC")
    cursor = myconn.cursor()
    sql = "SELECT balance, currency, type FROM Account WHERE account_id=%s"
    value = (accountID, )
    cursor.execute(sql, value)
    result = cursor.fetchall()
    myconn.commit()
    answer = str(result[0][1]) + " " +str(result[0][0])
    accoutType = result[0][2]
    if (accoutType == 's'):
        accoutType = "Saving Account"
    else:
        accoutType = "Current Account"
    currency_ID = result[0][1]
    from printTransactionRecords import printTransactionRecords
    tableData = printTransactionRecords(accountID)
    print(tableData)
    return render_template('transactionRecords.html', tableData=tableData, accountID=accountID.zfill(6), answer=answer, currency_ID=currency_ID, accoutType=accoutType)

@app.route('/addAccount/<username>/<currency>/<acc_type>')
def addAccount(username,currency,acc_type):
    myconn = mysql.connector.connect(
    host="localhost", user="root", passwd="!@#$%^&*()qwertyuiopWinter2021", database="iKYC")
    cursor = myconn.cursor()
    sql = "INSERT INTO `Account` (`username`,`currency`,`balance`, `type`) VALUE (%s, %s, %s, %s)"
    value = (username,currency,0,acc_type)
    cursor.execute(sql, value)
    result = cursor.fetchall()
    myconn.commit()
    return "OK"

@app.route('/loginHistory/<username>')
def loginHistory(username):
    myconn = mysql.connector.connect(
    host="localhost", user="root", passwd="!@#$%^&*()qwertyuiopWinter2021", database="iKYC")
    cursor = myconn.cursor()
    sql = "SELECT login_time, login_date FROM LoginHistory WHERE username=%s ORDER BY login_date DESC, login_time DESC"
    value = (username, )
    cursor.execute(sql, value)
    result = cursor.fetchall()
    myconn.commit()
    return render_template('loginHistory.html', tableData=result)

@app.route('/resetPassowrd/<username>')
def resetPassowrd(username):
    return render_template('resetPassword.html', username=username)

@app.route('/resetPassowrdProcess/<username>/<password>')
def resetPassowrdProcess(username,password):
    myconn = mysql.connector.connect(
    host="localhost", user="root", passwd="!@#$%^&*()qwertyuiopWinter2021", database="iKYC")
    cursor = myconn.cursor()
    sql = "UPDATE Customer SET password=%s WHERE username=%s"
    value = (password, username)
    cursor.execute(sql, value)
    result = cursor.fetchall()
    myconn.commit()
    return "OK"