from flask import Blueprint, redirect, render_template, request, url_for
from app.db.models.home import Home
from app.db import db
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
    sample_users = ['User 1', 'User 2', 'User 3', 'User 4', 'User 5', 'User 6', 'User 7', 'User 8', 'User 9', 'User 10', 'User 11', 'User 12', 'User 13', 'User 14', 'User 15']
    sample_message = {'sender': ['hi', 'how are you'], 'receiver': ['hello', "i'm good"]}
    return render_template('message/message.html', is_admin=is_admin, users = sample_users, messages = sample_message)