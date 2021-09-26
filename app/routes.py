#from flask_mysqldb import MySQL,MySQLdb  

from flask import Blueprint, render_template, request, redirect, url_for, session
from flask_cors import CORS
from app import app
from app import mysql
#A Flask extension for handling Cross Origin Resource Sharing (CORS), making cross-origin AJAX possible.
#Axios doesnt work without this
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
     
#######################################################
################''' Telecom Routes '''#################
#######################################################

