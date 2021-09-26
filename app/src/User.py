from flask import Blueprint, render_template, request, redirect, url_for, session
import bcrypt
from flask import jsonify
from flask_mysqldb import MySQL,MySQLdb
import re
import datetime
#######################################################
###################''' Register '''####################
#######################################################
def register(mysql):
        email = request.get_json()['email']
        password = request.get_json()['password'].encode('utf-8')
        hash_password = bcrypt.hashpw(password, bcrypt.gensalt())
        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor) #Object that is going to go through our database
        registered_on = datetime.datetime.now()
        try:
            cur.execute('SELECT * FROM user WHERE email = % s', (email, ))
            account = cur.fetchone()
            if account:
                msg = 'Account already exists !'
            elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
                msg = 'Invalid email address !'
            else:
                cur.execute("INSERT INTO user (email, password) VALUES (%s,%s)",(email,hash_password))
                mysql.connection.commit()
                msg = 'Account created successfully'
                session['email'] = request.get_json()['email']
        except Exception as e:
            return jsonify(
            error = str(e),
            registered = False
            )
        
        return jsonify(
        error=msg,
        registered = True,
        status = 200
    )

#######################################################
###################''' Login '''####################
#######################################################
def login(mysql):
        email = request.form['email']
        password = request.form['password'].encode('utf-8')
        curl = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        curl.execute("SELECT * FROM users WHERE email=%s",(email,))
        user = curl.fetchone()
        curl.close()
        if len(user) > 0:
            if bcrypt.hashpw(password, user["password"].encode('utf-8')) == user["password"].encode('utf-8'):
                session['name'] = user['name']
                session['email'] = user['email']
            else:
                msg = "Error password and email not match"
        else:
            msg =  "Error user not found"
        return jsonify(
        error=msg
    )
#######################################################
###################''' Logout '''####################
#######################################################
def logout():
    session.clear()
    return "Done"

#######################################################
###################''' View Profile '''####################
#######################################################
def viewprofile(mysql):
    user_id = request.get_json()['user_id']
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor) #Object that is going to go through our database

    try:
        cur.execute('SELECT * FROM user WHERE user_id = % s', (user_id ,))
        user = cur.fetchone()
        cur.close()
        if user:
            return jsonify(user)
        else:
            return "Error no user found"
    except:
        return "Error cannot connect to database"

#######################################################
###################''' Update Profile '''####################
#######################################################
def updateprofile(mysql):
    user_id = request.get_json()['user_id']
    first_name = request.get_json()['first_name']
    last_name = request.get_json()['last_name']
    phone_number = request.get_json()['phone_number'] 
    email = request.get_json()['email']
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor) #Object that is going to go through our database

    try:
        print(id, first_name, last_name, phone_number, email)
        print(1)
        # update query is not working somehow
        cur.execute('UPDATE user SET email = % s, first_name = % s, last_name = % s, phone_number = % s WHERE user_id = % s', (email ,first_name ,last_name ,phone_number ,user_id ,))
        print(2)
        user = cur.fetchone()
        cur.close()
        if user:
            return jsonify(user)
        else:
            return "Error no user found"
    except:
        return "Error cannot connect to database"

#######################################################
###################''' Update Password '''####################
####################################################### 
def updatepassword(mysql):

    id = request.get_json()['user_id']
    current = request.get_json()['currentPassword'].encode('utf-8')
    new = request.get_json()['newPassword'].encode('utf-8')
    confirm = request.get_json()['confirmPassword'].encode('utf-8')

    hashed_current = bcrypt.hashpw(current, bcrypt.gensalt())
    hashed_new = bcrypt.hashpw(new, bcrypt.gensalt())
    hashed_confirm = bcrypt.hashpw(confirm, bcrypt.gensalt())

    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    try:
        cur.execute("SELECT * FROM user WHERE user_id=%s",(id,))
        user = cur.fetchone()
        if (user):
            print(user["password"].encode('utf-8'))
            print(hashed_current)
            if (user["password"].encode('utf-8') == hashed_current):
                cur.execute('UPDATE user SET password = % s WHERE user_id = % s', (hashed_new ,id ,))
                mysql.connection.commit()
                cur.close()
                print('password changed')
                return('Password Updataed Successfully!')
            else:
                cur.close()
                print('incorrect current password')
                return('Current Password did not match')
    except:
        print('database connection error')
        return('Can\'t connect to database')