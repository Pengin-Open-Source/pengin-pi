from flask import Blueprint, redirect, render_template, request, url_for
from app.db.models.home import Home
from app.db import db
from app.db.models.customer import User
from flask_login import login_required
from app.util.security import admin_permission
from app.util.s3 import conn
import logging
from werkzeug.utils import secure_filename

message_blueprint = Blueprint('message_blueprint', __name__)


@message_blueprint.route("/")
@message_blueprint.route("/index")
@message_blueprint.route("/message")
def message():
    is_admin = admin_permission.can()
    users = User.query.all()
    sample_message = {'sender': ['hi', 'how are you'], 'receiver': ['hello', "i'm good"]}
    return render_template('message/message.html', is_admin=is_admin, users = users, messages = sample_message)