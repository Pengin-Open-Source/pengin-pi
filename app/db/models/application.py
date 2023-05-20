#399-application-crm
from app.db import db
from app.util.uuid import id
from job import Job

class Application(db.Model):
    __tablename__ = 'application'
    id = db.Column(db.String(36), default=id, primary_key=True)
    job_id = db.Column(db.String(36), db.ForeignKey(Job.id)) #matches the id of the job for which the applicant is applying
    message_to_hiring_manager = db.Column(db.Text)
    date_applied = db.Column(db.String(100))
    location_of_candidate = db.Column(db.String(100))
    resume_path = x #look at our images file framework for ideas
    cover_letter_path = y #look at our images file framework for ideas