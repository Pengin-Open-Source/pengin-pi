"""
TODO
DONE -- Import flask-socketIO
Import config, if any
DONE -- Create the Messenger class that contains the methods to create the socket IO websocket
apply any config to messenger
DONE -- create the handler methods to establish and close connections

DONE -- create the init app function

DONE -- create the if name == main function and create a basic flask app to run a basic messenger outside of a project
"""

# import flask-socketIO
from flask import Flask, Blueprint, render_template
from flask_socketio import SocketIO, join_room, leave_room, emit, send
from flask_login import current_user, login_required
import os
import datetime
from app.db import db
from app.db.models import Message, User, Room
from .serializer import message_serializer, room_serializer, room_order_by_last_update


# import config.object


class Messenger:
    def __init__(self, socketio, config=None):
        # create messenger properties
        self.socketio = socketio
        # apply optional configs

    @login_required
    def on_join(self, data):
        if "room_id" in data:
            room_id = data["room_id"]
            room = Room.query.get_or_404(room_id)
        else:
            print("No room_id or user_id in data")
            return
        join_room(room.id)

        emit(
            "joined_message",
            room_serializer(room),
        )

    @login_required
    def save_message(self, data):
        with db.session.no_autoflush:
            message = Message(
                author_id=current_user.id,
                timestamp=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                room_id=data["room_id"],
                content=data["content"],
            )
            db.session.add(message)
            db.session.commit()
        self.send_message(message)

    @login_required
    def send_message(self, message):
        emit("saved_message", message_serializer(message), to=message.room_id)

    @login_required
    def disconnect_handler(self):
        pass


messenger_blueprint = Blueprint(
    "messenger_blueprint", __name__, url_prefix="/messenger"
)


def init_app(socketio):
    messenger = Messenger(socketio)

    socketio.on_event("save_message", messenger.save_message)
    socketio.on_event("disconnect", messenger.disconnect_handler)
    socketio.on_event("join_room", messenger.on_join)


if __name__ == "__main__":
    # if running messenger as an app
    # TODO: create the mini flask app and load messenger here

    # Get the path to the current directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # Create a Flask application instance and specify the templates folder
    template_path = os.path.join(current_dir, "../../templates")
    app = Flask("messenger_app", template_folder=template_path)

    app.config["SECRET_KEY"] = "blagdefwukfhkaewubfkcwq41234fhkaewub645tfdwee!@$1.2"
    app.config["DEBUG"] = True

    socketio = SocketIO(app, debug=True)

    init_app(socketio)

    socketio.run(app, port=3000)
