from email import contentmanager
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
    roles = db.relationship('Role', secondary='user_roles')


# Define the Role data-model
class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50), unique=True)

# Define the UserRoles association table
class UserRoles(db.Model):
    __tablename__ = 'user_roles'
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id', ondelete='CASCADE'))
    role_id = db.Column(db.Integer(), db.ForeignKey('roles.id', ondelete='CASCADE'))

# copy/paste job from tobuwebflask per issue #39
class BlogPost(db.Model):
    __tablename__ = "blogpost"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), unique=True)
    date = db.Column(db.DateTime(timezone=True), server_default=func.now())
    content = db.Column(db.String(10000))
    tags = db.Column(db.String(1000))
    # Logan Kiser: hold off on user/group field - something will be added when
    #              we incorporate flask-principal
    # user = db.Column(db.Integer)
    # TODO
    # Logan Kiser: might be nice to include a convenient __init__ method or two
