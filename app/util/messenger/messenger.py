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
    render_template
)
from flask_socketio import SocketIO, join_room, leave_room, emit
from flask_login import current_user, login_required
import os
import datetime
import json
from app.db import db
from app.util.uuid import id
from app.db.models import Message, User, Room,  UserRoom


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
        emit("saved_message", context, to=message.room_id)

    def disconnect_handler(self):
        pass

    def create_room_name(self, user1, user2):
        attendees = [user1, user2]
        attendees.sort()
        return f"{attendees[0]}_{attendees[1]}"

    def make_user_room_link(self, chat_room_id, user_id):
        user_room = UserRoom(room_id=chat_room_id, user_id=user_id)
        db.session.add(user_room)
        db.session.commit()

    def process_message(self, json, methods=['GET', 'POST']):
        print('received json: ' + str(json))
        print("Message.py did something with a Message!")
        emit('update chat', json,  broadcast=True)

    def chat(self, room):
        self.current_room = room.id
        join_room(self.current_room)

        user_rooms = UserRoom.query.filter_by(room_id=room.id)

        # worked with some Google Gemini suggestions for getting all the selected User Rooms' user ids and names
        user_ids = user_rooms.with_entities(UserRoom.user_id).all()

        # print(user_ids)
        # for user_id in user_ids:
        #     user = User.query.get(user_id)
        #     if user:
        #         context = {
        #             "user_name":  user.name,
        #             "room_name":  room.name,
        #         }
        #     emit('users in group', context, to=room.id)

        users_in_list = []
        for user_id in user_ids:
            user = User.query.get(user_id)
            if user:
                users_in_list.append({
                    "user_name":  user.name,
                    "room_name":  room.name,
                })

        jsonified_users = json.dumps(users_in_list)
        print(jsonified_users)
        # print(f"What's the context? {context}")
        emit('users in group', jsonified_users, to=room.id)

        msgs = []
        for message in room.messages:
            msgs.append({
                "author_name": message.author.name,
                "content": message.content,
                "timestamp": message.timestamp,
            })
        jsonified_messages = json.dumps(msgs)
        emit('load chat', jsonified_messages, to=room.id)

    def chat_group(self, json, methods=['GET', 'POST']):
        if self.current_room:
            leave_room(self.current_room)
        print(f"group name in overlay: {json}")
        room = Room.query.filter_by(name=json['room_name']).first()

        self.chat(room)

    def chat_with(self, json, methods=['GET', 'POST']):
        if self.current_room:
            leave_room(self.current_room)
        print(f"chat name in overlay: {json}")
        other_user = User.query.filter_by(name=json['other_user']).first()

        if other_user:
            other_user_name = other_user.name
            chat_room_name = self.create_room_name(
                current_user.name, other_user_name)
            room = Room.query.filter_by(name=chat_room_name).first()
            if room is None:
                room = Room(id=id(), name=self.create_room_name(current_user.name,
                                                                other_user_name))
                db.session.add(room)
                db.session.commit()
                print(f"room {room.id} did not exist, it is now created:")
                print(f"room name: {room.name}")

            chat_room_id = room.id
            user_room = UserRoom.query.filter_by(
                room_id=chat_room_id, user_id=current_user.id).first()
            other_user_room = UserRoom.query.filter_by(
                room_id=chat_room_id, user_id=other_user.id).first()

            if user_room is None:
                self.make_user_room_link(chat_room_id, current_user.id)
                print(
                    f"User-room link for room id: {chat_room_id} room name: {chat_room_name} and user {current_user.name} did not exist, it is now created:")

            if other_user_room is None:
                self.make_user_room_link(chat_room_id, other_user.id)
                print(
                    f"User-room link for room id: {chat_room_id} room name: {chat_room_name} and user {other_user.name} did not exist, it is now created:")

            self.chat(room)


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
                "name": user.name,
            }

        co_workers = list(map(user_data, co_workers))
        return render_template("messenger/chat_list.html", users=co_workers)

    socketio.on_event("connect", messenger.connection_handler)
    socketio.on_event("save_message", messenger.save_message)
    socketio.on_event("disconnect", messenger.disconnect_handler)
    socketio.on_event("message sent", messenger.process_message)
    socketio.on_event("user selected", messenger.chat_with)
    socketio.on_event("room selected", messenger.chat_group)


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
