#Necessary libraries
from flask import Flask, render_template, url_for, session, request,redirect
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
#from sendemail import sendmail,sendgridmail
import smtplib

app = Flask(__name__)

#Secret key to grab data from sessions
app.secret_key = 'a'

#Setting up configurations of app
app.config['MYSQL_HOST'] = "Localhost"
app.config['MYSQL_USER'] = "root"
app.config['MYSQL_PASSWORD'] = ""
app.config['MYSQL_DB'] = "registration_portal"

#Configuration given to flask
mysql = MySQL(app)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/register', methods =['GET', 'POST'])
def register():
    msg = ''
    if request.method == 'POST' :
        name = request.form['name']
        username = request.form['username']
        email = request.form['email']
        address = request.form['address']
        password = request.form['password']
        designation = request.form['designation']
        mobile = request.form['mobile']
        
        #Establishing connection using cursor
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM user_details WHERE username = % s', (username, ))
        account = cursor.fetchone()
        print(account)
        if account:
            msg = 'Account already exists !'
        elif not re.match(r'^[A-Za-z ]+$', name):
            msg = 'Please Enter a Valid Name !'
        elif not re.match(r'^[A-Za-z0-9._%+-@#!~`&*]{7,30}$', username):
            msg = 'Please Choose an Appropriate Username !'
        elif not re.match(r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+[\.\w{2,3}]+$', email):
            msg = 'Please Enter a Valid Email Address !'
        elif not re.match(r'^[A-Za-z ,]+$', address):
            msg = 'Please Enter Valid Address'
        elif not re.match(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{6,20}$', password):
            msg = 'Please Enter Valid Password'
        elif not re.match(r'^[A-Za-z]+$', designation):
            msg = 'Please Enter Valid Designation'
        elif not re.match(r'^[0-9+]+$', mobile):
            msg = 'Please Enter Valid Mobile Number'
        else:
            cursor.execute('INSERT INTO user_details VALUES (NULL, % s, % s, % s, % s, % s, % s, % s)', (name, username, email, address, password, designation, mobile))
            
            #Commiting the connection/insertion or declaring the values
            mysql.connection.commit()
            msg = 'You have successfully registered !'
            TEXT = "Hello "+username + ",\n\n"+ """Thanks for registering """ 
            message  = 'Subject: {}\n\n{}'.format("smartinterns Carrers", TEXT)
            #sendmail(TEXT,email)
            #sendgridmail(email,TEXT)
    elif request.method == 'POST':
        msg = 'Please fill out the form !'
    return render_template('register.html', msg = msg)

@app.route('/login',methods =['GET', 'POST'])
def login():
    global userid
    msg = ''
  
    if request.method == 'POST' :
        username = request.form['username']
        password = request.form['password']
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM user_details WHERE username = % s AND password = % s', (username, password ))
        account = cursor.fetchone()
        print (account)
        if account:
            session['loggedin'] = True
            session['id'] = account[0]
            userid =  account[0]
            session['username'] = account[1]
            msg = 'Logged in successfully !'
            return render_template('dashboard.html', msg = msg)
        else:
            msg = 'Incorrect username / password !'
    return render_template('login.html', msg = msg)

@app.route('/buy',methods =['GET', 'POST'])
def buy():
     msg = ''
     if request.method == 'POST' :
         name = request.form['name']
         stock = request.form['stock']
         cursor = mysql.connection.cursor()
         #cursor.execute('SELECT * FROM cart WHERE userid = % s', (session['id'], ))
         #account = cursor.fetchone()
         #print(account)
         cursor = mysql.connection.cursor()
         cursor.execute('INSERT INTO cart VALUES (NULL, % s, % s)', (name, stock))
         mysql.connection.commit()
         msg = 'You have successfully purchased !'
         session['loggedin'] = True
         #TEXT = "Hello sandeep,a new appliaction for job position" +jobs+"is requested"
         
         #sendmail(TEXT,"sandeep@thesmartbridge.com")
         #sendgridmail("sandeep@thesmartbridge.com",TEXT)
         
     elif request.method == 'POST':
         msg = 'Please specify the items you want to purchase !'
     return render_template('buy.html', msg = msg)

@app.route('/dashboard')
def dash():
    return render_template('dashboard.html')
""" 
@app.route('/display')
def display():
    print(session["username"],session['id'])
    
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM item_details WHERE userid = % s', (str(session['id'])))
    account = cursor.fetchone()
    print("accountdisplay",account)
    return render_template('display.html',account = account)
"""
@app.route('/logout')
def logout():
   session.pop('loggedin', None)
   session.pop('id', None)
   session.pop('username', None)
   return render_template('home.html')

if __name__ == ('__main__'):
    app.run(host = '0.0.0.0', debug = True, port = 9000)