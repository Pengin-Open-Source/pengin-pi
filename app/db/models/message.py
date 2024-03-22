from app.db import db
from app.util.uuid import id as ID

import datetime

import json


class Message(db.Model):
    __tablename__ = "message"
    id = db.Column(db.String(36), default=ID, primary_key=True)
    content = db.Column(db.Text)
    timestamp = db.Column(db.String(100))
    # author must be linked in __init__.py
    # room must be linked in __init__.py


class Room(db.Model):
    # a room contains a name and members interacting in the thread
    __tablename__ = "room"
    id = db.Column(db.String(36), default=ID, primary_key=True)
    name = db.Column(db.String(100))
    date_created = db.Column(
        db.DateTime, default=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    )


class UserRoom(db.Model):
    __tablename__ = "user_room"
    id = db.Column(db.String(36), default=ID, primary_key=True)
