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
from flask import Flask, Blueprint, render_template, redirect, url_for, request, session
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
        pass

    def connection_handler(self, auth):
        if self.current_room is None:
            print("no room")
            return

        join_room(self.current_room)
        context = {
            "author_name": current_user.name,
            "content": "has entered the room",
            "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        }
        emit("saved_message", context, to=self.current_room)
        print(f"{current_user.name} joined room {self.current_room}")

    def save_message(self, data):
        if self.current_room is None:
            print("in save_message, room does not exist")
            return
        with db.session.no_autoflush:
            message = Message(
                author_id=data["author_id"],
                timestamp=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                room_id=data["room_id"],
                content=data["content"]
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
        emit("saved_message", context, to=message.room.id)
        # emit("saved_message", context, to=self.current_room)

    def disconnect_handler(self):
        pass

    def process_message(self, json, methods=['GET', 'POST']):
        print('received json: ' + str(json))
        print("Message.py did something with a Message!")
        emit('update chat', json)


messenger_blueprint = Blueprint('messenger_blueprint', __name__,
                                url_prefix="/messenger")


def init_app(app, socketio):
    messenger = Messenger(socketio)

    @messenger_blueprint.route("/")
    @login_required
    def chat_list():
        # TODO get user's company members
        # For now, get all users except current user
        co_workers = User.query.filter(User.id != current_user.id)

        def user_data(user):
            return {
                "id": user.id,
                "name": user.name,
            }

        co_workers = list(map(user_data, co_workers))
        return render_template("messenger/chat_list.html", users=co_workers)

    def create_room_id(user1, user2):
        attendees = [user1, user2]
        attendees.sort()
        return f"{attendees[0]}_{attendees[1]}"

    @messenger_blueprint.route("/<other_user>", methods=["GET", "POST"])
    @login_required
    def chat(other_user):
        other_user_name = User.query.get(other_user).name
        room_id = create_room_id(current_user.name, other_user_name)
        room = Room.query.get(room_id)
        if room is None:
            room = Room(id=room_id, name=create_room_id(current_user.name,
                                                        other_user_name))
            db.session.add(room)
            db.session.commit()
            print(f"room {room_id} did not exist, it is now created:")
            print(f"room name: {room.name}")

        messenger.current_room = room_id

        # Return only the 100 last messages
        return render_template(
            "messenger/chat_pair.html",
            user=other_user_name,
            room_id=room_id,
            room_name=room.name,
            messages=room.messages
        )

    socketio.on_event("connect", messenger.connection_handler)
    socketio.on_event("save_message", messenger.save_message)
    socketio.on_event("disconnect", messenger.disconnect_handler)


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
