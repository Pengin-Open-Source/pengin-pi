#398-application-route
from flask import Blueprint, render_template, redirect, url_for, request
from flask_login import current_user, login_required
from app.util.security import (admin_permission, edit_status_permission, contact_applicant_permission, reject_applicant_permission, delete_applicant_permission, user_permission)
from app.db import db
from app.db.models import Application, Job, User
from app.db.models.application import ApplicationStatus
from app.util.mail import send_application_mail, send_accept_mail, send_reject_mail
from app.util.s3 import conn
from app.db.util import paginate
from werkzeug.utils import secure_filename
from datetime import datetime
from sqlalchemy import not_

applications = Blueprint('applications', __name__, url_prefix='/applications')

@applications.route('/<job_id>/application', methods=['GET'])
@login_required
def application(job_id):
    is_admin = admin_permission.can()
    application = Application.query.filter_by(job_id=job_id).first()
  
    return render_template('applications/application.html', is_admin=is_admin, application=application, job_id=job_id, primary_title='Application')

@applications.route('/<job_id>/application/create', methods=['POST'])
@login_required
def create_application(job_id):
    ALLOWED_EXTENSIONS = {'pdf', 'doc', 'docx'}

    def allowed_extension(filename):
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

    if request.method == 'POST':
        resume = request.files['resume']
        cover_letter = request.files['cover_letter']
        message = request.form.get('message')
        location = request.form.get('location')

        if not resume:
            return 'Resume is required', 400
        
        if not allowed_extension(resume.filename):
            return 'Invalid file type. Allowed formats: .pdf, .doc, .docx', 400
        
        if not allowed_extension(cover_letter.filename):
            return 'Invalid file type. Allowed formats: .pdf, .doc, .docx', 400

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
            date_applied=datetime.now(),
            job_id=job_id,
            user_id=current_user.id,
            )

        new_application.set_status_code('pending')

        db.session.add(new_application)
        db.session.commit()

        try:
            job = Job.query.filter_by(id=job_id).first()
            send_application_mail(current_user.email, new_application.id, current_user.name, job.job_title)
        except Exception as e:
            print('Error: ', e)

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

    resume_url = conn.get_URL(application.resume_path)

    if application.cover_letter_path:
        cover_letter_url = conn.get_URL(application.cover_letter_path)
    else:
        cover_letter_url = None

    return render_template('applications/application_view.html', job=job, application=application, resume_url=resume_url, cover_letter_url=cover_letter_url, primary_title='Application')

@applications.route('/my-applications', methods=['GET'])
@login_required
@user_permission.require()
def my_applications():
    if user_permission.can():
        applications_per_page = 9
        page = 1
        applications = paginate(Application, page=page, key="date_applied", filters={"user_id": current_user.id}, pages=applications_per_page)

        return render_template('applications/my_applications.html', applications=applications, page=page, primary_title='My Applications')
    
@applications.route('/<job_id>/job-applications', methods=['GET'])
@login_required
@admin_permission.require()
def job_applications(job_id):
    job = Job.query.filter_by(id=job_id).first()
    status = request.args.get('status')

    if request.method == 'POST':
        page = int(request.form.get('page_number', 1))
    else:
        page = 1

    if status == 'all':
        applications = paginate(Application, page=page, pages=20, filters={"status_code": not_('DELETED')})

    else:
        applications = paginate(Application, page=page, pages=20, filters={"status_code": status})

    return render_template('applications/job_applications.html', job=job, applications=applications, primary_title='Job Applications')

@applications.route('/<job_id>/<application_id>/edit-status', methods=['GET', 'POST'])
@login_required
@admin_permission.require()
def edit_status(job_id, application_id):
    job = Job.query.filter_by(id=job_id).first()
    application = Application.query.filter_by(id=application_id).first()

    if request.method == 'POST':
        status_code = request.form.get('status_code')
        application.set_status_code(status_code)
        db.session.commit()

        return redirect(url_for('applications.application_view', job_id=job_id, application_id=application_id))

    return render_template('applications/edit_application.html', job=job, application=application, primary_title='Edit Application')

@applications.route('/<job_id>/<application_id>/accept', methods=['POST'])
@login_required
@admin_permission.require()
def contact_applicant(job_id, application_id):
    application = Application.query.filter_by(id=application_id).first()
    accept_subject = request.form.get('accept-subject')
    accept_body = request.form.get('accept-body')

    try:
        send_accept_mail(application.user.email, application.id, application.user.name, application.job.job_title, accept_subject, accept_body)
        application.set_status_code('accepted')
        db.session.commit()
    except Exception as e:
        print('Error: ', e)

    return redirect(url_for('applications.application_view', job_id=job_id, application_id=application_id))

@applications.route('/<job_id>/<application_id>/reject', methods=['POST'])
@login_required
@admin_permission.require()
def reject_applicant(job_id, application_id):
    application = Application.query.filter_by(id=application_id).first()
    reject_subject = request.form.get('reject-subject')
    reject_body = request.form.get('reject-body')

    try:
        send_reject_mail(application.user.email, application.id, application.user.name, application.job.job_title, reject_subject, reject_body)
        application.set_status_code('rejected')
        db.session.commit()
    except Exception as e:
        print('Error: ', e)

    return redirect(url_for('applications.application_view', job_id=job_id, application_id=application_id))

@applications.route('/<job_id>/<application_id>/delete', methods=['POST'])
@login_required
@admin_permission.require()
def delete_applicant(job_id, application_id):
    application = Application.query.filter_by(id=application_id).first()

    try:
        application.set_status_code('deleted')
        db.session.commit()
    except Exception as e:
        print('Error: ', e)

    return redirect(url_for('applications.job_applications', job_id=job_id))