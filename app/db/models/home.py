from app.db import db
from app.util.uuid import id


class Home(db.Model):
    __tablename__ = 'home'
    id = db.Column(db.String(36), default=id, primary_key=True)
    company_name = db.Column(db.String(200))
    article = db.Column(db.String(10000))
    image = db.Column(db.String(200))
