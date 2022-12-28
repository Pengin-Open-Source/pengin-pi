from sqlalchemy import func

from app.db import db
from app.util.uuid import id


class Event(db.Model):
    __tablename__ = 'events'
    id = db.Column(db.String(), default=id, primary_key=True)
    user_id = db.Column(db.String(), db.ForeignKey('user.id',
                                                    ondelete='CASCADE'))
    organizer = db.Column(db.String(), db.ForeignKey('user.id',
                                                      ondelete='CASCADE'))
    role = db.Column(db.String(), db.ForeignKey('roles.id',
                                                 ondelete='CASCADE'))
    role_info = db.relationship("Role", back_populates="event_info", lazy=True)
    date_created = db.Column(db.DateTime(timezone=True),
                             nullable=False, server_default=func.now())
    start_datetime = db.Column(db.DateTime(timezone=True), nullable=False)
    end_datetime = db.Column(db.DateTime(timezone=True), nullable=False)
    title = db.Column(db.String())
    description = db.Column(db.String())
    location = db.Column(db.String())

    def __repr__(self):  # for debug purpose
        return f"(id: {self.id}, organizer_id: {self.organizer_id}, title: {self.title}, desc: {self.description}, location: {self.location}, start_datetime: {self.start_datetime}, end_datetime: {self.end_datetime}, created_at: {self.created_at})\t"

    # Add/extract "time" properties on the fly when needed.
    def add_time(self):
        self.start_time = self.start_datetime.time().strftime("%H:%M")
        self.end_time = self.end_datetime.time().strftime("%H:%M")

    # Add/extract "date" properties on the fly when needed.
    def add_date(self):
        self.start_date = self.start_datetime.date()
        self.end_date = self.end_datetime.date()


'''
  how to do attendees?
'''
