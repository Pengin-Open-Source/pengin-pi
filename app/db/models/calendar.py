from sqlalchemy import func

from app.db import db
from app.util.uuid import id


class Event(db.Model):
    __tablename__ = 'events'
    id = db.Column(db.String(36), default=id, primary_key=True)
    date_created = db.Column(db.DateTime(timezone=True),
                             nullable=False, server_default=func.now())
    start_datetime = db.Column(db.DateTime(timezone=True), nullable=False)
    end_datetime = db.Column(db.DateTime(timezone=True), nullable=False)
    title = db.Column(db.String(50))
    description = db.Column(db.String(5000))
    location = db.Column(db.String(50))

    def __repr__(self):  # for debug purpose
        return f"(id: {self.id}, organizer_id: {self.organizer}, title: {self.title}, desc: {self.description}, location: {self.location}, start_datetime: {self.start_datetime}, end_datetime: {self.end_datetime}, created_at: {self.date_created})\t"

    # Add/extract "time" properties on the fly when needed.
    def add_time(self):
        self.start_time = self.start_datetime.time().strftime("%H:%M")
        self.end_time = self.end_datetime.time().strftime("%H:%M")

    # Add/extract "date" properties on the fly when needed.
    def add_date(self):
        self.start_date = self.start_datetime.date()
        self.end_date = self.end_datetime.date()

