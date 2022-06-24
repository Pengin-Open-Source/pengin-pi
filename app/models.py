from flask_login import UserMixin
from sqlalchemy import func
from . import db
from datetime import datetime

class User(UserMixin, db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))

# copy/paste job from tobuwebflask per issue #39
class BlogPost(db.Model):
    __tablename__ = "blogpost"
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    title = db.Column(db.String(100), unique=True)
    date = db.Column(datetime(timezone=True), server_default=func.utcnow())
    content = db.Column(db.String(10000))
    tags = db.Column(db.String(1000))
    user = db.Column(db.Integer)
