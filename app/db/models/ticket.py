from sqlalchemy import func
from app.db import db
from app.util.uuid import id


class TicketForum(db.Model):
    __tablename__ = 'ticket_forum'
    id = db.Column(db.String(36), default=id, primary_key=True)
    summary = db.Column(db.String(100))
    content = db.Column(db.Text)
    tags = db.Column(db.String(150))
    date = db.Column(db.String(100))
    resolution_status = db.Column(db.String(100))
    resolution_date = db.Column(db.String(100))


class Resolution(db.Model):
    __tablename__ = 'resolution'
    id = db.Column(db.String(36), default=id, primary_key=True)
    name = db.Column(db.String(100))
    date = db.Column(db.DateTime(timezone=True), server_default=func.now())


class TicketComment(db.Model):
    __tablename__ = 'ticket_comment'
    id = db.Column(db.String(36), default=id, primary_key=True)
    date = db.Column(db.String(100))
    content = db.Column(db.Text)
