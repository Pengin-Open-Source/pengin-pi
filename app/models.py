from email import contentmanager
from flask_login import UserMixin
from . import db
from sqlalchemy import func

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    title = db.Column(db.String(100), unique=True)
    date_posted = db.Column(db.DateTime(timezone=True), server_default=func.utcnow())
    content = db.Column(db.String(10000))
    author = db.Column(db.String(100))