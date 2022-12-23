from sqlalchemy import func

from app.db import db
from app.util.uuid import id


class BlogPost(db.Model):
    __tablename__ = "blogpost"
    id = db.Column(db.String(), default=id, primary_key=True)
    title = db.Column(db.String(100), unique=True)
    date = db.Column(db.DateTime(timezone=True), server_default=func.now())
    content = db.Column(db.String(10000))
    tags = db.Column(db.String(1000))
