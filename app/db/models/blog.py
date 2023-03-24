from datetime import datetime
from app.db import db
from app.util.uuid import id


class BlogPost(db.Model):
    __tablename__ = "blogpost"
    id = db.Column(db.String(36), default=id, primary_key=True)
    title = db.Column(db.String(100), unique=True)
    date = db.Column(db.DateTime(timezone=True), default=datetime.utcnow())
    content = db.Column(db.Text)
    tags = db.Column(db.String(150))
