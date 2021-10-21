#from flask_mysqldb import MySQL,MySQLdb  

from flask import Blueprint, render_template, request, redirect, url_for, session
from flask.json import jsonify
from flask.wrappers import Response

from app import app
from app import mysql
from flask_login import login_user, login_required, logout_user

from flask_cors import CORS
#A Flask extension for handling Cross Origin Resource Sharing (CORS), making cross-origin AJAX possible.
#Axios doesnt work without this
from app.src.TransportationBot import chat3

CORS(app)

#######################################################
##################''' Controllers '''##################
#######################################################
from app.src import User, Controllers

@app.route('/register', methods=["GET", "POST"]) 
def register():
    if request.method == 'GET':
        return request.get_json()['email']
    else:
        return User.register(mysql)


@app.route('/login', methods=["GET", "POST"]) 
def login():
    if request.method == 'POST':
        return User.login(mysql) 
    else:
        return ""
        
@app.route('/logout')
@login_required
def logout():
    return User.logout()

@app.route('/checkLogin', methods=["GET", "POST"]) 
def check():
    if request.method == 'GET':
        return User.checkLogin(mysql) 
    else:
        return ""

@app.route('/profile', methods=['GET','POST'])
def viewprofile():
    if request.method == 'GET':
        return User.viewprofile(mysql)
    if request.method == 'POST':
        return User.updateprofile(mysql)

@app.route('/password', methods=['POST'])
def password():
    return User.updatepassword(mysql)
     
#######################################################
################''' Tranport Routes '''#################
#######################################################

@app.route("/chat")
def chat():
    re = chat3("Hi")
    return {"members":["Member",re]}

@app.route("/reply",methods=["GET","POST"])
def reply():
    if request.method == 'POST':
        # if request.get_json()['msg'] == "Hi":
        re = chat3(request.get_json()['msg'])
        print(re)
        return {"members": re}

@app.route("/travel",methods=["GET","POST"])
def travel():
    return Controllers.travel(mysql)

@app.route('/sendEmail', methods=["GET", "POST"]) 
def sendEmail():
    if request.method == 'POST':
        return Controllers.sendEmail(mysql)


