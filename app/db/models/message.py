from app.db import db
from app.util.uuid import id as ID

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

    def __init__(self, name=None, members=None):
        self.name = name or self.generate_default_name(members)
        if members:
            self.members.extend(members)

    @staticmethod
    def generate_default_name(members):
        if members:
            members_dict = {member.id: member.name for member in members}
            return json.dumps(members_dict)
        else:
            return None  # No members, so no default name


class UserRoom(db.Model):
    __tablename__ = "user_room"
    id = db.Column(db.String(36), default=ID, primary_key=True)
