from flask_login import UserMixin
from . import db

class User(UserMixin, db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    admin = db.Column(db.Boolean)

class Schedule(db.Model):
    __tablename__ = "schedule"
    id = db.Column(db.Integer, primary_key=True)
    weekday = db.Column(db.Integer)
    hour = db.Column(db.Integer)
    minute = db.Column(db.Integer)
    mode = db.Column(db.Integer)

class Mode(db.Model):
    __tablename__ = "mode"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    red = db.Column(db.Integer)
    green = db.Column(db.Boolean)
    blue = db.Column(db.Boolean)

