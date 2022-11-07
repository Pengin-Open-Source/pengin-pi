from flask_login import UserMixin
from sqlalchemy import func
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(UserMixin, db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True) 
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))
    roles = db.relationship('Role', secondary='user_roles')


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50), unique=True)


class UserRoles(db.Model):
    __tablename__ = 'user_roles'
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id', ondelete='CASCADE'))
    role_id = db.Column(db.Integer(), db.ForeignKey('roles.id', ondelete='CASCADE'))


class BlogPost(db.Model):
    __tablename__ = "blogpost"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), unique=True)
    date = db.Column(db.DateTime(timezone=True), server_default=func.now())
    content = db.Column(db.String(10000))
    tags = db.Column(db.String(1000))
   

class Company(db.Model):
    __tablename__ = "company"
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50), unique=True)
    phone = db.Column(db.String())
    city = db.Column(db.String())
    state = db.Column(db.String())
    country = db.Column(db.String())
    zipcode = db.Column(db.String())
    email = db.Column(db.String(100), unique=True)
    address1 = db.Column(db.String())
    address2 = db.Column(db.String())
    members = db.relationship('User', secondary='company_members')
    
    
class CompanyMembers(db.Model):
    __tablename__ = "company_members"
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id', ondelete='CASCADE'))
    company_id = db.Column(db.Integer(), db.ForeignKey('company.id', ondelete='CASCADE'))
    role_id = db.Column(db.Integer(), db.ForeignKey('roles.id', ondelete='CASCADE'))


class ForumPost(db.Model):
    __tablename__ = "forum_post"
    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String())
    content = db.Column(db.String())
    thread = db.Column(db.String())
    author = db.Column(db.String())
    tags = db.Column(db.String())
    date = db.Column(db.Integer())
    comment = db.relationship('ForumComment')


class ForumComment(db.Model):
    __tablename__ = "forum_comment"
    id = db.Column(db.Integer(), primary_key=True)
    post_id = db.Column(db.Integer(), db.ForeignKey('forum_post.id', ondelete='CASCADE'))
    content = db.Column(db.String())
    author = db.Column(db.String())
    date = db.Column(db.Integer())