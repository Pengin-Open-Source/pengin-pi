from .. import db


class Product(db.Model):
    __tablename__ = 'product'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String())
    description = db.Column(db.String())
    price = db.Column(db.String())