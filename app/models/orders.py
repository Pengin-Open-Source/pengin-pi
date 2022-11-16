from .config import db
from sqlalchemy import func, schema #, ForeignKey
#from sqlalchemy.orm import with_polymorphic
from .company import Company


class Order(db.Model):
    __tablename__ = 'order'
    id = db.Column(db.Integer(), primary_key=True)
    product_id = db.Column(db.Integer(),db.ForeignKey('product.id', ondelete='CASCADE')) 
    order_date = db.Column(db.DateTime(255), nullable=True) 
    #service_date = db.Column(db.DateTime(255), nullable=True) 
    #expiration_date = db.Column(db.DateTime(255), nullable=True)
    customer_id = db.Column(db.Integer(),db.ForeignKey('customer.id', ondelete='CASCADE'))

class ShippingAddress(db.Model):
    __tablename__ = 'shipping_address'
    id = db.Column(db.Integer(), primary_key=True)
    address1 = db.Column(db.String())
    address2 = db.Column(db.String())
    city = db.Column(db.String())
    state = db.Column(db.String())
    country = db.Column(db.String())
    phone = db.Column(db.String(50), unique=True)
    email = db.Column(db.String(50), unique=True)


class Customer(db.Model):
    #Customer can be a user or a company, it can also be both
    __tablename__ = "customer"
    __table_args__ = (
        schema.CheckConstraint('NOT(user_id IS NULL AND company_id IS NULL)'),
    )
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(),db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    company_id = db.Column(db.Integer(), db.ForeignKey('company.id', ondelete='CASCADE'), nullable=False)
    orders = db.ForeignKey('order.id', ondelete='CASCADE')
    #ticket_id= db.Column(db.Integer(),db.ForeignKey('ticket.id', ondelete='CASCADE'))
    date = db.Column(db.DateTime(timezone=True),server_default=func.now())
    service_date = db.Column(db.DateTime(255), nullable=True) 
    expiration_date = db.Column(db.DateTime(255), nullable=True)
    
