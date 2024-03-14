from app.db import db
from app.db.models.ticket import TicketForum
from app.util.uuid import id as ID
from datetime import datetime, timezone
from sqlalchemy.event import listen

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
    
class OrderChangeRequest(db.Model):
    __tablename__ = 'order_change_request'
    id = db.Column(db.String(36), default=ID, primary_key=True)
    data = db.Column(db.String(255))
    order_id = db.Column(db.String(36), db.ForeignKey('orders.id', ondelete='CASCADE'), nullable=False)
    order_date = db.Column(db.DateTime(timezone=True))
    customer_id = db.Column(db.String(36), nullable=False)
    timestamp = db.Column(db.DateTime(timezone=True))
    user_id = db.Column(db.String(36), db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)

class OrdersList(db.Model):
    __tablename__ = 'orders_list'
    id = db.Column(db.String(36), default=ID, primary_key=True)
    quantity = db.Column(db.Integer)

class OrderHistory(db.Model):
    __tablename__ = 'order_history'
    id = db.Column(db.String(36), default=ID, primary_key=True)
    data = db.Column(db.String(255))
    order_id = db.Column(db.String(36), db.ForeignKey('orders.id', ondelete='CASCADE'), nullable=False)
    timestamp = db.Column(db.DateTime(timezone=True))
    user_id = db.Column(db.String(36), db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)


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

def after_update_listener(mapper, connection, target):
    print('after_update_listener')
    old_data = {column.name: getattr(target, column.name) for column in mapper.columns}
    order_history = OrderHistory(order_id=target.id, timestamp=datetime.now(timezone.utc), old_data=str(old_data))

    ticket_summary = f"Order Change Request - Order ID: {target.id}"
    ticket_content = f"Changes to Order ID {target.id} pending approval. Please review and approve or reject the changes."

    ticket = TicketForum(
        summary=ticket_summary,
        content=ticket_content,
        tags="order-change-request"
    )

    db.session.add_all([order_history, ticket])
    db.session.commit()

listen(Orders, 'after_update', after_update_listener)