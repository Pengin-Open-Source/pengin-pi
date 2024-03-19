from app.db import db
from app.util.uuid import id
from app.db.models.job import Job
from enum import Enum
from datetime import datetime
class ApplicationStatusCode(Enum):
    PENDING = 'pending' # default status when application is created
    ACCEPTED = 'accepted'
    REJECTED = 'rejected'
    DELETED = 'deleted' # deletes from view but keeps in database
class Application(db.Model):
    __tablename__ = 'application'
    id = db.Column(db.String(36), default=id, primary_key=True)
    resume_path = db.Column(db.String(100))
    cover_letter_path = db.Column(db.String(100))
    message = db.Column(db.Text)
    location = db.Column(db.String(100))
    date_applied = db.Column(db.DateTime(timezone=True), nullable=True)
    status_code = db.Column(db.Enum(ApplicationStatusCode), default=ApplicationStatusCode.PENDING)
    status_code_date_change = db.Column(db.DateTime(timezone=True), nullable=True)

    # Methods to handle application status code changes
    def pending_application(self):
        self.status_code = ApplicationStatusCode.PENDING
        self.status_code_date_change = datetime.now()

    def reject_application(self):
        self.status_code = ApplicationStatusCode.REJECTED
        self.status_code_date_change = datetime.now()

    def accept_application(self):
        self.status_code = ApplicationStatusCode.ACCEPTED
        self.status_code_date_change = datetime.now()
    
    def delete_application(self):
        self.status_code = ApplicationStatusCode.DELETED
        self.status_code_date_change = datetime.now()