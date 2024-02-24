#398-application-route
from flask import Blueprint, render_template, redirect, url_for, request
from flask_login import login_required
from app.util.security import admin_permission
from app.db import db
from app.db.models import Application
from app.db.models import Job
from app.util.s3 import conn
from app.db.util import paginate
from werkzeug.utils import secure_filename
from datetime import datetime

applications = Blueprint('applications', __name__, url_prefix='/applications')

'''
The actual job needs to have an apply button that uses this route.
The page needs to load our application view for that job.
The GET method will need to render the application form.
NOTE: We must require someone to be authenticated.
The authenticated user decorator must be applied to the application route.
Secondly, we need another route that handles the POST method
that will take the information provided by the application form and store it in the application table.
Application GET
Application POST'''

@applications.route('/<job_id>/application')
@login_required
def application(job_id):
    is_admin = admin_permission.can()
    application = Application.query.filter_by(job_id=job_id).first()

    return render_template('applications/application.html', is_admin=is_admin, application=application, job_id=job_id,primary_title='Application')

@applications.route('/<job_id>/application/create', methods=['POST'])
@login_required
def create_application(job_id):
    if request.method == 'POST':
        resume = request.files['resume']
        cover_letter = request.files['cover_letter']
        message = request.form.get('message')
        location = request.form.get('location')

        if not resume:
            return 'Resume is required', 400

        resume.filename = secure_filename(resume.filename)
        resume_path = conn.create(resume)

        if cover_letter:
            cover_letter.filename = secure_filename(cover_letter.filename)
            cover_letter_path = conn.create(cover_letter)
        else:
            cover_letter_path = None

        new_application = Application(
            resume_path=resume_path, 
            cover_letter_path=cover_letter_path, 
            message=message, 
            location=location, 
            date_applied=datetime.now()
            )
        
        print('NEW APPLICATION: ', new_application)
        db.session.add(new_application)
        db.session.commit()

        return redirect(url_for(
            'applications.application_success', 
            job_id=job_id,
            application_id=new_application.id
            ))
    
    return render_template('applications/create_application.html', job_id=job_id, primary_title='Create Application')        

@applications.route('/<job_id>/application/<application_id>/success', methods=['GET'])
@login_required
def application_success(job_id, application_id):
    return render_template(
        'applications/application_success.html', 
        primary_title='Application Success',
        job_id=job_id,
        application_id=application_id
        )

@applications.route('/<job_id>/application/<application_id>', methods=['GET'])
@login_required
def application_view(job_id, application_id):
    application = Application.query.filter_by(id=application_id).first()
    job = Job.query.filter_by(id=job_id).first()

    print('JOB.TITLE: ', job.job_title)
    return render_template('applications/application_view.html', job=job, application=application, primary_title='Application')