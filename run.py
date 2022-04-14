# 
# 
# Nur khafidah - 19090075 - 6C
# 

from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os, random, string


database_file = 'sqlite:///database/uts-tour.db'
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = database_file

db = SQLAlchemy(app)

# DATABASE SCHEMA
class Users(db.Model):
    username = db.Column(db.String(20), unique=True, nullable=False, primary_key=True)
    password = db.Column(db.String(20), unique=False, nullable=False)
    token = db.Column(db.String(100), unique=False)

class Events(db.Model):
    event_creator = db.Column(db.String(20))
    event_name = db.Column(db.String(20), unique=True, nullable=False, primary_key=True)
    event_start_time = db.Column(db.Date)
    event_end_time = db.Column(db.DateTime)
    event_start_lat = db.Column(db.String(20))
    event_finish_lat = db.Column(db.String(20))
    event_finish_lng = db.Column(db.String(20))
    created_at = db.Column(db.Date)

class Log(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20))
    event_name = db.Column(db.String(20))
    log_lat = db.Column(db.String(20))
    log_lng = db.Column(db.String(20))
    created_at = db.Column(db.DateTime)

db.create_all()


# Create User
# http://127.0.0.1:5000/api/v1/users/create
@app.route("/api/v1/users/create", methods=["POST"])
def createUser():
    username = request.json['username']
    password = request.json['password']
    user = Users(username=username, password=password)
    db.session.add(user)
    db.session.commit()
    return make_response(jsonify({"msg": "registrasi sukses"}))


# Login
# http://127.0.0.1:5000/api/v1/users/login
@app.route("/api/v1/users/login", methods=["POST"])
def login():
    username = request.json['username']
    password = request.json['password']

    if username and password:
        user = Users.query.filter_by(username=username, password=password).first()
        if user:
            token = ''.join(random.choices(string.ascii_uppercase + string.digits, k=20))
            Users.query.filter_by(username=username, password=password).update({'token':token})
            db.session.commit()
            return make_response(jsonify({"msg": "Login sukses", "token":token}))
        return make_response(jsonify({"msg": "username atau password salah"}))
    return make_response(jsonify({"msg": "Username atau password tidak boleh kosong"}))


# Create event
# http://127.0.0.1:5000/api/v1/events/create
@app.route("/api/v1/events/create", methods=["POST"])
def event():
    token = request.json['token']
    event_name = request.json['event_name']
    event_start_time = request.json['event_start_time']
    event_end_time = request.json['event_end_time']
    event_start_lat = request.json['event_start_lat']
    event_start_lng = request.json['event_start_lng']
    event_finish_lat = request.json['event_finish_lat']
    event_finish_lng = request.json['event_finish_lng']

    est = datetime.strptime(event_start_time, '%Y-%m-%d %H:%M')
    eet = datetime.strptime(event_end_time, '%Y-%m-%d %H:%M')
    user = Users.query.filter_by(token=token).first()
    if user:
        time = datetime.datetime.utcnow()
        event = Events(event_creator=user.username, event_name=event_name, event_start_time=est, event_end_time=eet, event_start_lat=event_start_lat, event_finish_lat=event_finish_lat, event_finish_lng=event_finish_lng,created_at=time)
        db.session.add(event)
        db.session.commit()
        return make_response(jsonify({"msg": "Success", "username":user.username, "time":time}))
    return make_response(jsonify({"msg":"Failed"}))


# Create event
# http://127.0.0.1:5000/api/v1/events/log
# @app.route("/api/v1/events/log", methods=["POST"])
# def log():


if __name__ == '__main__':
   app.run(debug = True, port=5000)