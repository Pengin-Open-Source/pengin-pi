from flask import Blueprint, redirect, render_template, request, url_for
from app.db.models.home import Home
from app.db import db
from app.db.models.customer import User
from flask_login import login_required
from app.util.security import admin_permission
from app.util.s3 import conn
import logging
from werkzeug.utils import secure_filename
chat_blueprint = Blueprint(
    'chat_blueprint', __name__,  url_prefix="/chat")


@chat_blueprint.route("/")
@chat_blueprint.route("/index")
@chat_blueprint.route("/chat")
def message():
    is_admin = admin_permission.can()
    users = User.query.all()
    # sample_message = {'sender': ['hi', 'how are you'],'receiver': ['hello', "i'm good"]}
    return render_template('message/message.html', is_admin=is_admin, users=users)

# Should I add this to the blueprint?  IT's not a route/view, nobody
# "navigates to" a URL address  to hit this method.

#
# @socketio.on('connect')
# def on_connect(json):
#     print('received json: ' + str(json))
#     print("We have a new connection!") """ """


# @socketio.on('message sent')
# def process_message(json, methods=['GET', 'POST']):
#     print('received json: ' + str(json))
#     print("Message.py did something with a Message!")
#     chatSocket.emit('update chat', json)
