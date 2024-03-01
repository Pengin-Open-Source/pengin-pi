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
from flask import (
    Flask,
    Blueprint,
    jsonify,
)
from flask_socketio import SocketIO, join_room, leave_room, emit
from flask_login import current_user, login_required
import os
import datetime
from app.db import db
from app.db.models import Message, User, Room


# import config.object


class Messenger:
    def __init__(self, socketio, config=None):
        # create messenger properties
        self.socketio = socketio
        self.current_room = None
        # apply optional configs

    def on_join(self, data):
        other_user = data["other_user"]
        room_id = self.create_room_id(current_user.name, other_user)
        room = Room.query.get(room_id)
        if room is None:
            room = Room(
                id=room_id,
                name=self.create_room_id(current_user.name, other_user),
            )
            db.session.add(room)
            db.session.commit()
            print(f"room {room_id} did not exist, it is now created:")
            print(f"room name: {room.name}")
        join_room(room.id)

        print(f"{current_user.name} joined room {room.id}")
        emit(
            "joined_message",
            {"room_id": room.id},
        )

    def save_message(self, data):
        with db.session.no_autoflush:
            message = Message(
                author_id=data["author_id"],
                timestamp=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                room_id=data["room_id"],
                content=data["content"],
            )
            db.session.add(message)
            db.session.commit()
        self.send_message(message)

    def send_message(self, message):
        context = {
            "author_name": message.author.name,
            "content": message.content,
            "timestamp": message.timestamp,
        }
        print(f"rooms id = {message.room_id}")
        emit("saved_message", context, to=message.room_id)
        # emit("saved_message", context, to=self.current_room)

    def disconnect_handler(self):
        pass

    def create_room_id(self, user1, user2):
        attendees = [user1, user2]
        attendees.sort()
        return f"{attendees[0]}_{attendees[1]}"


messenger_blueprint = Blueprint(
    "messenger_blueprint", __name__, url_prefix="/messenger"
)


def init_app(app, socketio):
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

    init_app(app, socketio)

    socketio.run(app, port=3000)
