from flask import Blueprint, render_template, request, redirect, url_for, session
from flask import jsonify
from flask_mysqldb import MySQL, MySQLdb
from flask_mail import Mail, Message
from app import mail

def travel(mysql):
    toStation = request.get_json()['to'].lower()
    fromStation = request.get_json()['from'].lower()
    mode = request.get_json()['mode'].lower()
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    
    query1 = 'select `methodID`,`type`,`routeNo`,`routeName`,`Departure Station`.name as `from`,`Destination Station`.name as `to`,`fee` from Route join TransportationMethod using (routeID) join `Departure Station` using (routeID) join `Destination Station` using (routeID) where (`Departure Station`.name = % s and `Destination Station`.name = % s and `type`= % s )'
    cur.execute(query1, (fromStation, toStation,mode ,))
    methods1 = cur.fetchall()

    query2 = 'select `methodID`,`type`,`routeNo`,`routeName`,`Departure Station`.name as `from`,`Stop Station`.name as `to`,`fee` from Route join TransportationMethod using (routeID) join `Departure Station` using (routeID) join `Stop Station` using (routeID) where (`Departure Station`.name = % s and `Stop Station`.name = % s and `type`= % s )'
    cur.execute(query2, (fromStation, toStation,mode ,))
    methods2 = cur.fetchall()

    methods = methods1 + methods2

    if len(methods) == 0:
        return jsonify(methods=methods, er=1)
    else:
        return jsonify(methods=methods, er=0)

def sendEmail(mysql):
    email = request.get_json()["email"]
    subject = request.get_json()["subject"]
    msg = request.get_json()['message']
    print(email)
    message = Message(subject, sender="xyronchatbot@gmail.com", recipients=[email])

    message.body = msg

    mail.send(message)

    return jsonify( res = "Email sent")