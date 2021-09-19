#app.py /request-grab data
#pip install python-dotenv
#pip install flask-mysqldb
#pip install bcrypt
#pip install -U flask-cors

from flask import Flask
from flask_mysqldb import MySQL
from os import environ as env

app = Flask(__name__)
mysql = MySQL(app)
app.secret_key = env.get('SECRET_KEY')

from app import routes
from app import db
