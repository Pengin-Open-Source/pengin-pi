from app.db import db
from app.util.uuid import id


class Product(db.Model):
    __tablename__ = 'product'
    id = db.Column(db.String(), default=id, primary_key=True)
    name = db.Column(db.String())
    description = db.Column(db.String())
    price = db.Column(db.String())
