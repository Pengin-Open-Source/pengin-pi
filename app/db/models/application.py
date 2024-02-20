from app.db import db
from app.util.uuid import id
from app.db.models.job import Job

class Application(db.Model):
    __tablename__ = 'application'
    id = db.Column(db.String(36), default=id, primary_key=True)
    message_to_hiring_manager = db.Column(db.Text)
    date_applied = db.Column(db.String(100))
    location_of_candidate = db.Column(db.String(100))
    # resume_path = x #look at our images file framework for ideas
    # cover_letter_path = y #look at our images file framework for ideas