from flask_login import UserMixin
from sqlalchemy import func, schema  # , ForeignKey
from datetime import datetime
from app.db import db
from app.util.uuid import id as ID

# from sqlalchemy.orm import with_polymorphic


class User(UserMixin, db.Model):
    __tablename__ = "user"
    id = db.Column(db.String(36), default=ID, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(100))
    validated = db.Column(db.Boolean, default=False, nullable=False)
    validation_date = db.Column(db.DateTime(timezone=True), default=datetime.utcnow())
    validation_id = db.Column(db.String(36), default=ID, unique=True)
    roles = db.relationship('Role', secondary='user_roles')
    posts = db.relationship('ForumPost')
    comments = db.relationship('ForumComment')
    companies = db.relationship('Company', secondary='company_members')
    customer = db.relationship('Customer')
    tickets = db.relationship('TicketForum')
    ticket_comments = db.relationship('TicketComment')
    
    # def __repr__(self): # for debug purpose
    #   return f"----- name: {self.name} || roles: {self.roles} "


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.String(36), default=ID, primary_key=True)
    name = db.Column(db.String(50), unique=True)
    # used for populating "name" about role when showing dropdown of roles
    event_info = db.relationship('Event', back_populates="role_info", lazy=True)

    # def __repr__(self): # for debug purpose
    #    return f"----- id: {self.id} || name: {self.name} "


class UserRoles(db.Model):
    __tablename__ = 'user_roles'
    id = db.Column(db.String(36), default=ID, primary_key=True)
    user_id = db.Column(db.String(36), db.ForeignKey('user.id',
                                                   ondelete='CASCADE'))
    role_id = db.Column(db.String(36), db.ForeignKey('roles.id',
                                                   ondelete='CASCADE'))


class Order(db.Model):
    __tablename__ = 'order'
    id = db.Column(db.String(36), default=ID, primary_key=True)
    order_date = db.Column(db.DateTime(255), nullable=True)
    product_id = db.Column(db.String(36), db.ForeignKey('product.id',
                                                      ondelete='CASCADE'))
    # service_date = db.Column(db.DateTime(255), nullable=True)
    # expiration_date = db.Column(db.DateTime(255), nullable=True)
    customer_id = db.Column(db.String(36), db.ForeignKey('customer.id',
                                                       ondelete='CASCADE'))


class ShippingAddress(db.Model):
    __tablename__ = 'shipping_address'
    id = db.Column(db.String(36), default=ID, primary_key=True)
    address1 = db.Column(db.String(50))
    address2 = db.Column(db.String(50))
    city = db.Column(db.String(50))
    state = db.Column(db.String(50))
    country = db.Column(db.String(50))
    phone = db.Column(db.String(50), unique=True)
    email = db.Column(db.String(50), unique=True)


class Customer(db.Model):
    # Customer can be a user or a company, it can also be both
    __tablename__ = "customer"
    __table_args__ = (
        schema.CheckConstraint('NOT(user_id IS NULL AND company_id IS NULL)'),
    )
    id = db.Column(db.String(36), default=ID, primary_key=True)
    user_id = db.Column(db.String(36),
                        db.ForeignKey('user.id', ondelete='CASCADE'),
                        nullable=False)
    company_id = db.Column(db.String(36),
                           db.ForeignKey('company.id', ondelete='CASCADE'),
                           nullable=False)
    orders = db.ForeignKey('order.id', ondelete='CASCADE')
    # ticket_id= db.Column(db.Integer(),
    #                       db.ForeignKey('ticket.id', ondelete='CASCADE'))
    date = db.Column(db.DateTime(timezone=True), server_default=func.now())
    service_date = db.Column(db.DateTime(255), nullable=True)
    expiration_date = db.Column(db.DateTime(255), nullable=True)


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
    customer = db.relationship('Customer')


class CompanyMembers(db.Model):
    __tablename__ = "company_members"
    id = db.Column(db.String(36), default=ID, primary_key=True)
    company_id = db.Column(db.String(36), db.ForeignKey('company.id',
                           ondelete='CASCADE'))
    user_id = db.Column(db.String(36), db.ForeignKey('user.id',
                        ondelete='CASCADE'))
    role_id = db.Column(db.String(36), db.ForeignKey('roles.id',
                        ondelete='CASCADE'))
