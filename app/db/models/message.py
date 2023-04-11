from app.db import db
from app.util.uuid import id
from datetime import datetime


class Message(db.Model):
    id = db.Column(db.String(36), default=id, primary_key=True)
    content = db.Column(db.Text)
    date = db.Column(db.DateTime(timezone=True), default=datetime.utcnow())