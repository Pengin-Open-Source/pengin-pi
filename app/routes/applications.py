from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required
from app.util.security import admin_permission
from app.db import db
from app.db.models import Application
from app.util.s3 import conn
from app.db.util import paginate

application_blueprint = Blueprint('application_blueprint',
                                  __name__, url_prefix='/applications')
#398-application-route
g
@application_blueprint.route('/create/<job_id>', methods=['GET','POST']) #CREATE (applicant submits their application)
@login_required
def create_application(job_id):
    if request.method == 'POST':
        message_to_hiring_manager = request.form.get('message_to_hiring_manager') #wait... do I need "get" here????
        location_of_candidate = request.form.get('location_of_candidate')
        resume_path = x #look at our images file framework for ideas
        cover_letter_path = y #look at our images file framework for ideas
        
        application = Application(message_to_hiring_manager=message_to_hiring_manager,
                                  location_of_candidate=location_of_candidate
                                  resume_path=resume_path
                                  cover_letter_path=cover_letter_path)
        
        db.session.add(application)
        db.session.commit()
        #flash('Your application has been submitted.')
        return redirect(url_for(application_blueprint.application))
    return render_template('applications/application_create.html', primary_title='Create Application')



@application_blueprint.route('/<job_id>') #READ (displays the form to apply for the job)
@login_required
def application(job_id):
    is_admin = admin_permission.can()
    application = Application.b.query.filter_by(job_id=job_id).first()
    
    return render_template('applications/application.html',is_admin=is_admin,application=application,
                           page=1, primary_title=application.job_title + " Application") #hope this works



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

