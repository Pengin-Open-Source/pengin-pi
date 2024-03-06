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
    status_code = db.Column(db.String(20), default='pending')
    status_code_date_change = db.Column(db.DateTime(timezone=True), nullable=True)
    
    def set_status_code(self, code):
        if code in ApplicationStatus.status_codes.values(): # check for valid code
            self.status_code = ApplicationStatus.status_codes[code] # set the status_code attribute to the corresponding value
            self.status_code_date_change = datetime.now()
    
    def pending_application(self):
        self.set_status_code('pending')
    
    def reject_application(self):
        self.set_status_code('rejected')
    
    def accept_application(self):
        self.set_status_code('accepted')
    
    def delete_application(self):
        self.set_status_code('deleted')
class ApplicationStatus(db.Model):
    __tablename__ = 'application_status'
    id = db.Column(db.String(36), default=id, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)

    status_codes = {
        'pending': 'pending',
        'accepted': 'accepted',
        'rejected': 'rejected',
        'deleted': 'deleted'
    }
