from sqlalchemy import func
from app.db import db
from app.util.uuid import id


class Job(db.Model):
    __tablename__ = 'job'
    id = db.Column(db.String(36), default=id, primary_key=True)
    date_created = db.Column(db.DateTime(timezone=True),
                             nullable=False, server_default=func.now())
    start_datetime = db.Column(db.DateTime(timezone=True), nullable=False)
    end_datetime = db.Column(db.DateTime(timezone=True), nullable=True)
    title = db.Column(db.String(255))
    description = db.Column(db.Text)
    department = db.Column(db.String(255))
    tags = db.Column(db.String(255))


class Application(db.Model):
    __tablename__ = 'application'
    id = db.Column(db.String(36), default=id, primary_key=True)
    job_id = db.Column(db.String(36), db.ForeignKey('job.id'), nullable=False)
    user_id = db.Column(db.String(36), db.ForeignKey('user.id'), nullable=False)
    resume_path = db.Column(db.String(255))
    cover_letter_path = db.Column(db.String(255))
    message_to_hiring_manager = db.Column(db.Text)
    date_applied = db.Column(db.DateTime(timezone=True),
                             nullable=False, server_default=func.now())


class Status(db.Model):
    __tablename__ = 'status'
    id = db.Column(db.String(36), default=id, primary_key=True)
    name = db.Column(db.String(255))