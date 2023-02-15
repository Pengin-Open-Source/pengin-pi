from flask_login import UserMixin
from datetime import datetime
from app.db import db
from app.util.uuid import id as ID


class User(UserMixin, db.Model):
    __tablename__ = "user"
    id = db.Column(db.String(36), default=ID, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(100))
    validated = db.Column(db.Boolean, default=False, nullable=False)
    validation_date = db.Column(db.DateTime(timezone=True), default=datetime.utcnow())
    validation_id = db.Column(db.String(36), default=ID, unique=True)


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.String(36), default=ID, primary_key=True)
    name = db.Column(db.String(50), unique=True)


class UserRoles(db.Model):
    __tablename__ = 'user_roles'
    id = db.Column(db.String(36), default=ID, primary_key=True) 


class Company(db.Model):
    __tablename__ = "company"
    id = db.Column(db.String(36), default=ID, primary_key=True)
    name = db.Column(db.String(50), unique=True)
    phone = db.Column(db.String(50))
    city = db.Column(db.String(50))
    state = db.Column(db.String(50))
    country = db.Column(db.String(50))
    zipcode = db.Column(db.String(50))
    email = db.Column(db.String(100), unique=True)
    address1 = db.Column(db.String(50))
    address2 = db.Column(db.String(50))


class CompanyMembers(db.Model):
    __tablename__ = "company_members"
    id = db.Column(db.String(36), default=ID, primary_key=True)
