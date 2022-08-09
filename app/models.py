from flask_login import UserMixin
from sqlalchemy import func
from . import db


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
    customer = db.relationship('User', secondary='customer')

    
class CompanyMembers(db.Model):
    __tablename__ = "company_members"
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id', ondelete='CASCADE'))
    company_id = db.Column(db.Integer(), db.ForeignKey('company.id', ondelete='CASCADE'))
    role_id = db.Column(db.Integer(), db.ForeignKey('roles.id', ondelete='CASCADE'))

class Customer(db.Model):
    __tablename__ = "customer"
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(),db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    company_id = db.Column(db.Integer(), db.ForeignKey('company.id', ondelete='CASCADE'), nullable=False)
    order_id= db.Column(db.Integer(),db.ForeignKey('order.id', ondelete='CASCADE'))
    ticket_id= db.Column(db.Integer(),db.ForeignKey('ticket.id', ondelete='CASCADE'))
    date = db.Column(db.DateTime(timezone=True),server_default=func.now())
    service_date = db.Column(db.DateTime(255), nullable=True) 
    expiration_date = db.Column(db.DateTime(255), nullable=True)


class Contracts(db.Model):
     __tablename__ = 'contracts'
     id = db.Column(db.Integer(), primary_key=True)
     customer_id = db.Column(db.Integer(),db.ForeignKey('customer.id', ondelete='CASCADE'))
     contract_type = db.Column(db.String())
     expiration_date = db.Column(db.DateTime(255), nullable=True)

class Ticket(db.Model):
     __tablename__ = 'ticket'
     id = db.Column(db.Integer(), primary_key=True)
     customer_id = db.Column(db.Integer(),db.ForeignKey('customer.id', ondelete='CASCADE'))
     forum_post_id = db.column(db.Integer(),db.ForeignKey('forum_post.id',ondelete='CASCADE'))
     thread_id = db.column(db.Integer())

class Order(db.Model):
     __tablename__ = 'order'
     id = db.Column(db.Integer(), primary_key=True)
     product_id = db.Column(db.Integer(),db.ForeignKey('product.id', ondelete='CASCADE')) 
     order_date = db.Column(db.DateTime(255), nullable=True) 
     service_date = db.Column(db.DateTime(255), nullable=True) 
     expiration_date = db.Column(db.DateTime(255), nullable=True)
     customer_id = db.Column(db.Integer(),db.ForeignKey('customer.id', ondelete='CASCADE'))
     shipping_address_id=db.Column(db.Integer(),db.ForeignKey('shipping_address.id', ondelete='CASCADE'))

class ShippingAddress(db.Model):
     __tablename__ = 'shipping_address'
     id = db.Column(db.Integer(), primary_key=True)
     address1 = db.Column(db.String())
     address2 = db.Column(db.String())
     city = db.Column(db.String())
     state = db.Column(db.String())
     country = db.Column(db.String())
     zipcode = db.Column(db.Integer())

class Product(db.Model):
     id = db.Column(db.Integer(), primary_key=True)
     description = db.Column(db.String())
     price = db.Column(db.Integer())

# #adding forum_post from #112
# class Forum_Post(db.Model):
#      __tablename__ = 'forum_post'
#      id = db.Column(db.Integer(), primary_key=True)
#      title = db.Column(db.String())
#      content = db.Column(db.String())
#      thread = db.Column(db.String())
#      author = db.Column(db.String())
#      tags = db.Column(db.String())
#      date = db.Column(db.DateTime(timezone=True), server_default=func.now())
#      comments = db.relationship('Forum_Comment', secondary='forum_comment')
