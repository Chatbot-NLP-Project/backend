from flask import Blueprint, render_template, request, redirect, url_for, session
from flask.helpers import make_response
import bcrypt
from flask import jsonify
from flask_mysqldb import MySQL,MySQLdb
import re
import datetime
from datetime import (timedelta, timezone)
from flask_jwt_extended import (JWTManager, jwt_required, get_jwt_identity, create_access_token, set_access_cookies, unset_jwt_cookies, get_jwt)
from app import app
from flask_login import LoginManager, login_user, login_required, logout_user, UserMixin,login_manager, current_user

from app import mysql
login_manager = LoginManager()
login_manager.init_app(app)

class User(UserMixin):
    pass

@login_manager.user_loader
def user_loader(email):
    curl = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    curl.execute("SELECT * FROM user WHERE email=%s",(email,))
    users = curl.fetchone()
    curl.close()
    if not users:
        return

    user = User()
    user.id = email
    return user


@login_manager.request_loader
def request_loader(request):
    email = request.form.get('email')
    curl = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    curl.execute("SELECT * FROM user WHERE email=%s",(email,))
    users = curl.fetchone()
    curl.close()
    if not users:
        return

    user = User()
    user.id = email
    return user
#######################################################
###################''' Register '''####################
####################################################### 
def register(mysql):
        email = request.get_json()['email']
        password = request.get_json()['password'].encode('utf-8')
        phone_number = request.get_json()['phoneNumber']
        first_name = request.get_json()['firstName']
        last_name = request.get_json()['lastName']
        sim_type = request.get_json()['simType']
        pn = phone_number[0:3]
        
        if (pn == "071" or pn == "070"):
            sim_type = "Mobitel"
        elif(pn == "077" or pn == "076"):
            sim_type = "Dialog"
        elif(pn == "075"):
            sim_type = "Airtel"
        elif(pn == "072" or pn == "078"):
            sim_type = "Hutch"
        print(sim_type)
        current_balance = float(500.00)
        hash_password = bcrypt.hashpw(password, bcrypt.gensalt())
        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor) #Object that is going to go through our database
        reg_date = datetime.datetime.now()
        try:
            cur.execute('SELECT * FROM User WHERE email = % s', (email, ))
            account = cur.fetchone()
            if account:
                msg = 'Account already exists !'
                registered = False
            elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
                msg = 'Invalid email address !'
                registered = False
            else:
                cur.execute("INSERT INTO User (email, password, phone_number, first_name, last_name, reg_date, current_balance, sim_type, anytime_data, night_time_data, 4g_data) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",(email,hash_password, phone_number, first_name, last_name, reg_date, current_balance, sim_type, 0, 0, 0))
                mysql.connection.commit()
                msg = 'Account created successfully'
                session['email'] = request.get_json()['email']
                registered = True
        except Exception as e:
            msg = str(e)
            registered = False
        
        return jsonify(
        error=msg,
        registered = registered
    )

#######################################################
###################''' Login '''####################
#######################################################
def login(mysql):
        # print(request.get_json(force=True)['email'])
        email = request.get_json(force=True)['email']
        password = request.get_json(force=True)['password'].encode('utf-8')

        curl = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        curl.execute("SELECT * FROM User WHERE email=%s",(email,))
        user = curl.fetchone()
        curl.close()
        if user:
            if bcrypt.hashpw(password, user["password"].encode('utf-8')) == user["password"].encode('utf-8'):
                session['user_id'] = user["user_id"]
                session['email'] = user['email']
                user.pop("password")
                session['user'] = user
                session.permanent = True
                app.permanent_session_lifetime = timedelta(minutes=45)
                u = User()
                u.id = email
                login_user(u)
                print(session.get('user_id'))
                access_token = create_access_token(identity = {
                    "user_id" : user["user_id"],
                    "email" : user["email"]
                })
                msg = "login successful"
                # res = make_response("msg")
                # res.set_cookie("ssss", access_token)
                # response = jsonify({"msg": "login successful"})
                # set_access_cookies(response, access_token)
                auth = True
                
            else:
                msg = "Password is incorrect"
                access_token = ""
                auth = False
        else:
            msg =  "Error user not found"
            access_token = ""
            auth = False
        print(msg)
        return jsonify(
        auth=auth,
        msg=msg,
        access_token=access_token,
        user = user
    )
#######################################################
###################''' CheckLogin '''####################
#######################################################
def checkLogin(mysql):
        # print(session['user_id'])
        if(not session.get("user_id") is None):
            LoggedIn = True
            user = session['user']
        else:
            LoggedIn = False
            user = ""
        
        return jsonify(
            LoggedIn = LoggedIn,
            user = user
        )

#######################################################
###################''' Logout '''####################
#######################################################
def logout():
    session.clear()
    logout_user()
    return "Done"

def refresh(response):
    try:
        exp_timestamp = get_jwt()["exp"]
        now = datetime.now(timezone.utc)
        target_timestamp = datetime.timestamp(now + timedelta(minutes=30))
        if target_timestamp > exp_timestamp:
            access_token = create_access_token(identity=get_jwt_identity())
            set_access_cookies(response, access_token)
        return response
    except (RuntimeError, KeyError):
        # Case where there is not a valid JWT. Just return the original respone
        return response

def get(id):
    curl = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    curl.execute("SELECT * FROM user WHERE user_id=%s",(id,))
    user = curl.fetchone()
    return user


#######################################################
###################''' View Profile '''####################
#######################################################

def viewprofile(mysql):
    # user_id = request.get_json()['user_id']   // for postmon use this
    user_id = request.args.get('user_id', '')  #// for axios use this
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor) #Object that is going to go through our database

    try:
        cur.execute('SELECT * FROM user WHERE user_id = % s', (user_id ,))
        user = cur.fetchone()
        cur.close()
        if user:
            print(user)
            return jsonify(user)
        else:
            print('Error here')
            return "Error no user found"
    except:
        print('Error h')
        return "Error cannot connect to database"

#######################################################
###################''' Update Profile '''####################
#######################################################

def updateprofile(mysql):

    # for postman
    user_id = request.get_json()['user_id']
    first_name = request.get_json()['first_name']
    last_name = request.get_json()['last_name']
    phone_number = request.get_json()['phone_number'] 
    email = request.get_json()['email']

    # for axios
    # user_id = request.args.get('user_id', '')
    # first_name = request.args.get('first_name', '')
    # last_name = request.args.get('last_name', '')
    # phone_number = request.args.get('phone_number', '')
    # email = request.args.get('email', '')
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor) #Object that is going to go through our database

    try:
        print( first_name, last_name, phone_number, email)
        # update query is not working somehow
        cur.execute('UPDATE user SET email = % s, first_name = % s, last_name = % s, phone_number = % s WHERE user_id = % s', (email ,first_name ,last_name ,phone_number ,user_id ,))
        mysql.connection.commit()
        print('Added successfully')
        return 'Added successfully'
        # user = cur.fetchone()
        # cur.close()
        # if user:
        #     return jsonify(user)
        # else:
        #     return "Error no user found"
    except:
        print('Can\'t connect to database')
        return "Error cannot connect to database"

# #######################################################
# ###################''' Update Password '''####################
# #######################################################
    
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