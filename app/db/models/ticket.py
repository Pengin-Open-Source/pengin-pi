from app.db import db
from sqlalchemy import func
from app.util.uuid import id


class Ticket(db.Model):
    __tablename__ = 'ticket'
    id = db.Column(db.String(), default=id, primary_key=True)
    customer_id = db.Column(db.String(),db.ForeignKey('customer.id', ondelete='CASCADE'))
    forum_post_id = db.Column(db.String(),db.ForeignKey('forum_post.id',ondelete='CASCADE'))
    thread_id = db.Column(db.Integer())
    

class TicketForum(db.Model):
    __tablename__ = 'ticket_forum'
    id = db.Column(db.String(), default=id, primary_key=True)
    customer_id = db.Column(db.String(),db.ForeignKey('customer.id', ondelete='CASCADE'))
    summary = db.Column(db.String())
    content = db.Column(db.String())
    tags = db.Column(db.String())
    date = db.Column(db.String())
    resolution_id = db.Column(db.String(),db.ForeignKey('resolution.id', ondelete='CASCADE'))
    resolution_date = db.Column(db.String(),db.ForeignKey('resolution.date', ondelete='CASCADE'))


class Resolution(db.Model):
    __tablename__='resolution'
    id = db.Column(db.String(), default=id, primary_key=True)
    name = db.Column(db.String())
    date= db.Column(db.DateTime(timezone=True), server_default=func.now())


class TicketComment(db.Model):
    __tablename__='ticket_comment'
    id = db.Column(db.String(), default=id, primary_key=True)
    ticket_id = db.Column(db.String(), db.ForeignKey('ticket_forum.id', ondelete='CASCADE'))
    author_id = db.Column(db.String(), db.ForeignKey('user.id', ondelete='CASCADE'))
    date= db.Column(db.String)
    content = db.Column(db.String())