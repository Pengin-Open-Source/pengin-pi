from app.db import db
from app.util.uuid import id as ID


class Contracts(db.Model):
    __tablename__ = 'contracts'
    id = db.Column(db.String(36), default=ID, primary_key=True)
    contract_type = db.Column(db.String(100))
    content = db.Column(db.Text)
    service_date = db.Column(db.DateTime(timezone=True), nullable=True)
    expiration_date = db.Column(db.DateTime(timezone=True), nullable=True)


class Orders(db.Model):
    __tablename__ = 'orders'
    id = db.Column(db.String(36), default=ID, primary_key=True)
    order_date = db.Column(db.DateTime(timezone=True), nullable=True)
    

class OrdersList(db.Model):
    __tablename__ = 'orders_list'
    id = db.Column(db.String(36), default=ID, primary_key=True)
    quantity = db.Column(db.Integer)


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
    __tablename__ = "customer"
    id = db.Column(db.String(36), default=ID, primary_key=True)
    date = db.Column(db.DateTime(timezone=True), nullable=True)