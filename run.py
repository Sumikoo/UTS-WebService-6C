# M Satria Jalasena - 19090090 - 6C
# Satya Faqikhatul Maroh - 19090030 - 6C
# Nur khafidah - 19090075 - 6C
# Arsyad Abdillah - 19090134 - 6C

from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
import datetime, random, string


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
    id = db.Column(db.Integer, primary_key=True)
    event_creator = db.Column(db.String(20), nullable=False)
    event_name = db.Column(db.String(20), nullable=False)
    event_start_time = db.Column(db.DateTime, nullable=False)
    event_end_time = db.Column(db.DateTime, nullable=False)
    event_start_lat = db.Column(db.String(20), nullable=False)
    event_finish_lat = db.Column(db.String(20), nullable=False)
    event_start_lng = db.Column(db.String(20), nullable=False)
    event_finish_lng = db.Column(db.String(20), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)

class Logs(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False)
    event_name = db.Column(db.String(20), nullable=False)
    log_lat = db.Column(db.String(20), nullable=False)
    log_lng = db.Column(db.String(20), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)

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
            token = ''.join(random.choices(string.ascii_lowercase + string.digits, k=25))
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

    est = datetime.datetime.strptime(event_start_time, '%Y-%m-%d %H:%M') 
    eet = datetime.datetime.strptime(event_end_time, '%Y-%m-%d %H:%M') 
    user = Users.query.filter_by(token=token).first()
    if user:
        time = datetime.datetime.utcnow()
        event = Events(event_creator=user.username, event_name=event_name, event_start_time=est, event_end_time=eet, event_start_lat=event_start_lat, event_finish_lat=event_finish_lat, event_start_lng=event_start_lng, event_finish_lng=event_finish_lng,created_at=time)
        db.session.add(event)
        db.session.commit()
        return make_response(jsonify({"msg": "Membuat event sukses"}))
    return make_response(jsonify({"msg":"Token invalid"}))


# Create log event
# http://127.0.0.1:5000/api/v1/events/log
@app.route("/api/v1/events/log", methods=["POST"])
def log_event():
    token = request.json['token']
    event_name = request.json['event_name']
    log_lat = request.json['log_lat']
    log_lng = request.json['log_lng']
    time = datetime.datetime.utcnow()
    
    user = Users.query.filter_by(token=token).first()
    if user:
        logging = Logs(username=user.username, event_name=event_name, log_lat=log_lat, log_lng=log_lng, created_at=time)
        db.session.add(logging)
        db.session.commit()
        return make_response(jsonify({"msg":"Sukses mencatat posisi baru"}))
    return make_response(jsonify({"msg":"Token invalid"}))

# Create log event
# http://127.0.0.1:5000/api/v1/events/logs
@app.route("/api/v1/events/logs", methods=["GET"])
def log():
    token = request.json['token']
    event_name = request.json['event_name']

    user = Users.query.filter_by(token=token).first()
    if user:
        array_logs = []
        logs = Logs.query.all()
        for log in logs:
            if log.event_name == event_name:
                dict_logs = {}
                dict_logs.update({"username": log.username, "log_lat": log.log_lat, "log_lng": log.log_lng, "created_at":log.created_at})
                array_logs.append(dict_logs)
        return make_response(jsonify(array_logs), 200, {'content-type':'application/json'})
    return make_response(jsonify({"msg":"Token invalid"}))

if __name__ == '__main__':
   app.run(debug = True, port=5000)