from app.db import db
from app.util.uuid import id as ID


class Message(db.Model):
    __tablename__ = "message"
    id = db.Column(db.String(36), default=ID, primary_key=True)
    content = db.Column(db.Text)
    date = db.Column(db.String(100))
    # author must be linked in __init__.py
    # room must be linked in __init__.py


class Room(db.Model):
    # a room contains a name and members interacting in the thread
    __tablename__ = "room"
    id = db.Column(db.String(36), default=ID, primary_key=True)
    name = db.Column(db.String(100))
    # members must be linked in __init__.py


class UserRoom(db.Model):
    __tablename__ = "user_room"
    id = db.Column(db.String(36), default=ID, primary_key=True)
