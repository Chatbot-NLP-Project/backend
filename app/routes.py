#from flask_mysqldb import MySQL,MySQLdb  

from flask import Blueprint, render_template, request, redirect, url_for, session
from flask_cors import CORS
from app import app
from app import mysql
#A Flask extension for handling Cross Origin Resource Sharing (CORS), making cross-origin AJAX possible.
#Axios doesnt work without this
from app.src.TransportationBot import chat3
from app.src.TransportationBot import travel

CORS(app)

#######################################################
##################''' Controllers '''##################
#######################################################
from app.src import User


#######################################################
##################''' User Routes '''##################
#######################################################
@app.route('/register', methods=["GET", "POST"]) 
def register():
    if request.method == 'GET':
        return request.get_json()['email']
    else:
        return User.register(mysql)


@app.route('/login',methods=["GET","POST"])
def login():
    if request.method == 'POST':
        return User.login(mysql)
    else:
        return "Done"

@app.route('/logout')
def logout():
    return User.logout()

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

@app.route("/travel",methods=["POST"])
def travel():
    print('here')
    if request.method == 'POST':
        re = travel(request.get_json()['to', 'from', 'method'])
        print(re)
        return {"members": re}
