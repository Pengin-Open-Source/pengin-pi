from app.db import db
from app.util.uuid import id


class Contracts(db.Model):
    __tablename__ = 'contracts'
    id = db.Column(db.String(36), default=id, primary_key=True)
    customer_id = db.Column(db.String(36), db.ForeignKey('customer.id',
                                                        ondelete='CASCADE'))
    contract_type = db.Column(db.String(100))
    expiration_date = db.Column(db.DateTime(255), nullable=True)
