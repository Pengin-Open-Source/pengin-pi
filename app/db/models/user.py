from flask_login import UserMixin
from app.util.uuid import id
from app.db import db
#from sqlalchemy.orm import with_polymorphic


class User(UserMixin, db.Model):
    __tablename__ = "user"
    id = db.Column(db.String(), default=id, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))
    roles = db.relationship('Role', secondary='user_roles')
    posts = db.relationship('ForumPosts')
    #companies = db.relationship('Company', secondary='company_members')


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.String(), default=id, primary_key=True)
    name = db.Column(db.String(50), unique=True)


class UserRoles(db.Model):
    __tablename__ = 'user_roles'
    id = db.Column(db.String(), default=id, primary_key=True)
    user_id = db.Column(db.String(), db.ForeignKey('user.id', ondelete='CASCADE'))
    role_id = db.Column(db.String(), db.ForeignKey('roles.id', ondelete='CASCADE'))