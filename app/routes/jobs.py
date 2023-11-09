from flask import Blueprint, redirect, render_template, request, url_for
from flask_login import current_user, login_required
from flask_principal import Permission, RoleNeed
from app.db import db
from app.util.uuid import id as ID
from app.db.models import Job, Application, User
from app.db.util import paginate
from app.util.security import admin_permission
from datetime import datetime


jobs_blueprint = Blueprint('jobs_blueprint', __name__,
                               url_prefix="/jobs")


@jobs_blueprint.route('/', methods=["GET", "POST"])
def jobs():
    is_admin = admin_permission.can()
    if request.method == "POST":
        page = int(request.form.get('page_number', 1))
    else:
        page = 1

    jobs = paginate(Job, page=page, key="title", pages=9)
    return render_template('jobs/jobs.html', is_admin=is_admin, jobs=jobs, page=page)

@jobs_blueprint.route('/<job_id>')
def job(job_id):
    is_admin = admin_permission.can()
    job = Job.query.filter_by(id=job_id).first()
    
    return render_template('jobs/job.html', is_admin=is_admin, job=job)

@jobs_blueprint.route('/create', methods=['GET', 'POST'])
@login_required
@admin_permission.require()
def create_job():
    if request.method == 'POST':
        title = request.form.get('title').strip()
        description = request.form.get('description').strip()
        tags = request.form.get('tags').strip()
        start_datetime = datetime.strptime(
            request.form.get('start_datetime'), '%Y-%m-%dT%H:%M')
        end_datetime = datetime.strptime(
            request.form.get('end_datetime'), '%Y-%m-%dT%H:%M')
        department = request.form.get('department').strip()
        
        new_job = Job(title=title, description=description, tags=tags,
                          start_datetime=start_datetime, end_datetime=end_datetime,
                          department=department)

        db.session.add(new_job)
        db.session.commit()

        return redirect(url_for('jobs_blueprint.jobs'))

    return render_template('jobs/job_create.html')


@jobs_blueprint.route('/edit/<id>', methods=['GET', 'POST'])
@login_required
@admin_permission.require()
def edit_job(id):
    job = Job.query.filter_by(id=id).first()

    if request.method == 'POST':
        title = request.form.get('title').strip()
        description = request.form.get('description').strip()
        tags = request.form.get('tags').strip()
        start_datetime = datetime.strptime(
            request.form.get('start_datetime'), '%Y-%m-%dT%H:%M')
        end_datetime = datetime.strptime(
            request.form.get('end_datetime'), '%Y-%m-%dT%H:%M')
        department = request.form.get('department').strip()
        
        job = job(title=title, description=description, tags=tags,
                          start_datetime=start_datetime, end_datetime=end_datetime,
                          department=department)

        db.session.commit()

        return redirect(url_for('jobs_blueprint.job', job_id=id))


    return render_template('jobs/job_edit.html', job=job)


@jobs_blueprint.route('/delete/<id>', methods=['POST'])
@login_required
@admin_permission.require()
def delete_jobs(id):
    job = Job.query.filter_by(id=id).first()
    db.session.delete(job)
    db.session.commit()

    return redirect(url_for('jobs_blueprint.jobs'))
