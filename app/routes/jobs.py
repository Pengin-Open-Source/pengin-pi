from datetime import datetime
from flask import Blueprint, render_template, redirect, url_for, request
from flask_login import login_required
from app.util.security import admin_permission
from app.db import db
from app.db.models import Job
from app.util.s3 import conn
from app.db.util import paginate

job_blueprint = Blueprint('job_blueprint',
                          __name__, url_prefix='/jobs')


@job_blueprint.route('/', methods=['GET', 'POST'])
def jobs():
    is_admin = admin_permission.can()
    jobs_per_page = 9
    if request.method == 'POST':
        page = (request.form.get('page_number', 1)) 
    else:
        page =1
    
    jobs = paginate(Job, page=page, key='job_title', pages=jobs_per_page)
    
    return render_template('jobs/jobs.html', is_admin=is_admin,
                           jobs=jobs, page=page,
                           primary_title='Jobs')

@job_blueprint.route('/<job_id>')
def job(job_id):
    is_admin = admin_permission.can()
    job = Job.query.filter_by(id=job_id).first()

    applications = job.applications
    
    return render_template('jobs/job.html', is_admin=is_admin, job=job, applications=applications, page=1,
                           primary_title=job.job_title)

@job_blueprint.route('/create', methods=['GET','POST'])
@login_required
@admin_permission.require()
def create_job():
    if request.method == 'POST':
        job_title = request.form.get('job_title')
        short_description = request.form.get('short_description')
        long_description = request.form.get('long_description')
        department = request.form.get('department')
        salary = request.form.get('salary')
        location = request.form.get('location')
        hiring_manager = request.form.get('hiring_manager')
        date_posted = datetime.now()

        job = Job(job_title=job_title, short_description=short_description,
                  long_description=long_description, department=department,
                  salary=salary, location=location,hiring_manager=hiring_manager, date_posted=date_posted)

        db.session.add(job)
        db.session.commit()

        return redirect(url_for('job_blueprint.jobs'))

    return render_template('jobs/job_create.html', primary_title='Create Job')

@job_blueprint.route('/<job_id>/edit', methods=['GET', 'POST'])
@login_required
@admin_permission.require()
def edit_job(job_id):
    job = Job.query.filter_by(id=job_id).first()

    if request.method == 'POST':
        job.job_title = request.form.get('job_title')
        job.short_description = request.form.get('short_description')
        job.long_description = request.form.get('long_description')
        job.department = request.form.get('department')
        job.salary = request.form.get('salary')
        job.location = request.form.get('location')
        job.hiring_manager = request.form.get('hiring_manager')

        db.session.commit()

        return redirect(url_for('job_blueprint.job', job_id=job.id))
    
    return render_template('jobs/job_edit.html', job=job, primary_title='Edit Job')


@job_blueprint.route('/<job_id>/delete', methods=['POST'])
@login_required
@admin_permission.require()
def delete_job(job_id):
    job = Job.query.filter_by(id=job_id).first()
    
    db.session.delete(job)
    db.session.commit()

    return redirect(url_for('job_blueprint.jobs'))