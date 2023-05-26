from app.db import db
from app.util.uuid import id
from job import Job
from datetime import datetime


class Application(db.Model): #399-application-crm
    __tablename__ = 'application'
    id = db.Column(db.String(36), default=id, primary_key=True)
    job_id = db.Column(db.String(36), db.ForeignKey(Job.id)) #matches the id of the job for which the applicant is applying
    job_name = db.Column(db.String(100), db.ForeignKey(Job.job_title))
    current_user =db.Column(db.String(),db.ForeignKey())
    message_to_hiring_manager = db.Column(db.Text)
    date_applied = db.Column(db.DateTime(timezone=True), default=datetime.utcnow())
    location_of_candidate = db.Column(db.String(100))
    resume_path = db.Column(db.String(500)) #look at our images file framework for ideas
    cover_letter_path = db.Column(db.String(500)) #look at our images file framework for ideas