from app.db import db
from app.util.uuid import id

class Event(db.Model):
    __tablename__ = 'events'
    id = db.Column(db.String(), default=id, primary_key=True)
    user_id = db.Column(db.Integer(),db.ForeignKey('user.id', ondelete='CASCADE'))
    organizer = db.Column(db.Integer(),db.ForeignKey('user.id', ondelete='CASCADE'))
    company_id = db.Column(db.Integer(),db.ForeignKey('company.id', ondelete='CASCADE'))
    date_created = db.Column(db.String())
    start_date = db.Column(db.String())
    end_date = db.Column(db.String())
    start_time = db.Column(db.String())
    end_time = db.Column(db.String())
    title = db.Column(db.String())
    description = db.Column(db.String())
    #attendees = db.relationship('User')
    location =  db.Column(db.String())


''' 
  how to do attendees?
'''
