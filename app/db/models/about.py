from app.db import db
from app.util.uuid import id

# Is there a way to put a constraint on table to only allow single row
# as all we need is one entry per organization?


class About(db.Model):
    __tablename__ = "about"
    id = db.Column(db.String(36), default=id, primary_key=True)
    name = db.Column(db.String(100))
    image = db.Column(db.String(100))
    twitter = db.Column(db.String(100))
    facebook = db.Column(db.String(100))
    instagram = db.Column(db.String(100))
    whatsapp = db.Column(db.String(100))
    linkedin = db.Column(db.String(100))
    line = db.Column(db.String(100))
    youtube = db.Column(db.String(100))
    phone = db.Column(db.String(100))
    address1 = db.Column(db.String(100))
    address2 = db.Column(db.String(100))
    city = db.Column(db.String(100))
    state = db.Column(db.String(100))
    country = db.Column(db.String(100))
    article = db.Column(db.Text)
    tags = db.Column(db.String(150))
    # vip = db.relationship('Vip')


# class Vip(db.Model):
    # __tablename__ = "vip"
    # id = db.Column(db.String(), default=id, primary_key=True)
    # name = db.Column(db.String(100))
    # content = db.Column(db.String(10000))
    # image = db.Column(db.String(100))
