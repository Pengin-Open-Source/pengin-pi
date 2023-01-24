from app.db import db
from app.util.uuid import id as ID
from sqlalchemy import schema  # , ForeignKey
from datetime import datetime


class Contracts(db.Model):
    __tablename__ = 'contracts'
    id = db.Column(db.String(36), default=ID, primary_key=True)
    customer_id = db.Column(db.String(36), db.ForeignKey('customer.id',
                                                        ondelete='CASCADE'))
    contract_type = db.Column(db.String(100))
    content = db.Column(db.Text)
    service_date = db.Column(db.DateTime(timezone=True), nullable=True)
    expiration_date = db.Column(db.DateTime(timezone=True), nullable=True)


class Order(db.Model):
    __tablename__ = 'order'
    id = db.Column(db.String(36), default=ID, primary_key=True)
    order_date = db.Column(db.DateTime(timezone=True), nullable=True)
    order_list = db.relationship('Product', secondary='order_list')
    customer_id = db.Column(db.String(36), db.ForeignKey('customer.id',
                                                       ondelete='CASCADE'))
    

class OrderList(db.Model):
    __tablename__ = 'order_list'
    id = db.Column(db.String(36), default=ID, primary_key=True)
    product_id = db.Column(db.String(36), db.ForeignKey('product.id',
                                                      ondelete='CASCADE'))
    order_id = db.Column(db.String(36), db.ForeignKey('order.id',
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
    customer = db.Column(db.String(36),
                        db.ForeignKey('customer.id', ondelete='CASCADE'),
                        nullable=False)
    

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
    orders = db.relationship('Order')
    contracts = db.relationship('Contracts')
    shipping_address = db.relationship('ShippingAddress')
    # ticket_id= db.Column(db.Integer(),
    #                       db.ForeignKey('ticket.id', ondelete='CASCADE'))
    date = db.Column(db.DateTime(timezone=True), nullable=True)