from app.db import db
from app.util.uuid import id
from app.db.models.job import Job
from datetime import datetime

class Application(db.Model):
    __tablename__ = 'application'
    id = db.Column(db.String(36), default=id, primary_key=True)
    resume_path = db.Column(db.String(100))
    cover_letter_path = db.Column(db.String(100))
    message = db.Column(db.Text)
    location = db.Column(db.String(100))
    date_applied = db.Column(db.DateTime(timezone=True), nullable=True)
    status_code = db.Column(db.String(36), db.ForeignKey('status_code.id'))
    status_code_date_change = db.Column(db.DateTime(timezone=True), nullable=True)

class StatusCode(db.Model):
    __tablename__ = 'status_code'
    id = db.Column(db.String(36), default=id, primary_key=True)
    code = db.Column(db.String(20), unique=True, nullable=False)
