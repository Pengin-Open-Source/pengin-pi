from app.db import db
from app.util.uuid import id


class Home(db.Model):
    __tablename__ = 'home'
    id = db.Column(db.String(), default=id, primary_key=True)
    company_name = db.Column(db.String())
    article = db.Column(db.String())
    image = db.Column(db.String())
