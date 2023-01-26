from app.db import db
from app.util.uuid import id


class Home(db.Model):
    __tablename__ = 'home'
    id = db.Column(db.String(36), default=id, primary_key=True)
    company_name = db.Column(db.String(100))
    article = db.Column(db.Text)
    image = db.Column(db.String(200))
    tags = db.Column(db.String(150))
