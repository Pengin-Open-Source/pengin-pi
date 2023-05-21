#398-application-route
from flask import Blueprint, render_template, redirect, url_for, request
from flask_login import login_required
from app.util.security import admin_permission
from app.db import db
from app.db.models import application
from app.util.s3 import conn
from app.db.util import paginate

application_blueprint = Blueprint('application_blueprint', __name__, url_prefix='/applications')
#don't forget to add it to routes>__init__.py

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

