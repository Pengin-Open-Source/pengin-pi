from app.db import db
from app.util.uuid import id
from datetime import datetime

class Job(db.Model):
    __tablename__ = 'job'
    id = db.Column(db.String(36), default=id, primary_key=True)
    job_title = db.Column(db.String(100))
    short_description = db.Column(db.String(280))
    long_description = db.Column(db.Text)
    salary = db.Column(db.String(100))
    date_posted = db.Column(db.DateTime(timezone=True), default=datetime.utcnow())
    
    #Children (See relationships in models/__init__.py)
    #department = db.Column(db.String(100))
    #hiring_manager = db.Column(db.String(100))
    #location = db.Column(db.String(100))