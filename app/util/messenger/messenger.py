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
from flask import Flask, render_template, redirect, url_for, request, session
from flask_socketio import SocketIO, join_room, leave_room, send
import os
import datetime

# import config.object


class Messenger:
    def __init__(self, socketio, rooms, config=None):
        # create messenger properties
        self.socketio = socketio
        self.rooms = rooms
        # apply optional configs
        pass

    def connection_handler(self, auth):
        print("you're in socketio.on('connect')")
        room = session.get("room")
        username = session.get("username")
        if not room or not username:
            return
        if room not in self.rooms:
            leave_room(room)
            return

        join_room(room)
        content = {
            "name": session.get("username"),
            "message": "has entered the room",
            "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        }
        send(content, json=True, to=room)
        print(f"{username} joined room {room}")

    def message_json(self, data):
        room = session.get("room")
        if room not in self.rooms:
            print(f"room {room} not in rooms {self.rooms}")
            return
        content = {
            "name": session.get("username"),
            "message": data["message"],
            "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        }
        send(content, json=True, to=room)
        self.rooms[room]["messages"].append(content)

    def disconnect_handler(self):
        pass


def init_app(app, socketio):
    # TODO: the init app method for flask.

    # TODO: get rooms from the database
    rooms = {}
    messenger = Messenger(socketio, rooms)

    @app.route("/", methods=["GET", "POST"])
    def login():
        if request.method == "POST":
            # For now, the user_id is the username
            # TODO: Change the user_id to be the user's ID from the database
            user_id = request.form["username"].strip()
            username = request.form["username"].strip()
            session["greeting"] = ""
            if username == "" or username is None:
                return render_template("messenger/login.html")
            session["username"] = username
            # TODO: handle users from the database, not the session
            if "users" not in session:
                # If there is no users yet
                session["users"] = {}

            # Handle a user coming back (their username is already in the session["users"] dictionary)
            if user_id in session["users"]:
                session["greeting"] = f"Welcome back {username}"
            else:
                # Add the user to the session["users"] dictionary
                session["users"][user_id] = {"username": username}
                session["greeting"] = f"Welcome {username}"

            session["current_user_id"] = user_id
            return redirect(url_for("chat_list"))

        return render_template("messenger/login.html")

    @app.route("/chat/")
    def chat_list():
        users = session.get("users")
        greeting = session.get("greeting", "")
        return render_template(
            "messenger/chat_list.html", users=users, greeting=greeting
        )

    def create_room_id(user1, user2):
        attendees = [user1, user2]
        attendees.sort()
        return f"{attendees[0]}_{attendees[1]}"

    @app.route("/chat/<other_user>/")
    def chat(other_user):
        room = create_room_id(session["current_user_id"], other_user)
        if room not in rooms:
            rooms[room] = {"messages": []}
        session["room"] = room
        return render_template(
            "messenger/chat_pair.html",
            user=other_user,
            room=room,
            messages=rooms[room]["messages"],
        )

    socketio.on_event("connect", messenger.connection_handler)
    socketio.on_event("json", messenger.message_json)
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
