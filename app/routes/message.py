from flask import Blueprint, jsonify
from flask_login import login_required, current_user

from app.db import db
from app.db.models import Room, User


chat_blueprint = Blueprint("chat_blueprint", __name__, url_prefix="/chat")

DEFAULT_MESSAGES_TO_LOAD = 15


@chat_blueprint.route("/get_past_messages/<room_id>/")
@login_required
def get_past_messages(room_id):
    room = Room.query.get_or_404(room_id)

    def serialize_message(message):
        return {
            "author_name": message.author.name,
            "content": message.content,
            "timestamp": message.timestamp,
        }

    past_messages = room.messages[-DEFAULT_MESSAGES_TO_LOAD:]
    past_messages = tuple(map(serialize_message, past_messages))

    return jsonify(past_messages)


@chat_blueprint.route("/get_room_id/<user_id>/")
@login_required
def get_room_id(user_id):
    other_user = User.query.get_or_404(user_id)

    # Get room from DB if it both users are members
    # For now, look for a room with both users
    # TODO: add attribute to Room model to indicate room is a default 2-user room or a room created by a user
    room = Room.query.filter(
        Room.members.any(User.id == current_user.id),
        Room.members.any(User.id == other_user.id),
    ).first()

    if room is None:
        room = Room(
            members=[current_user, other_user],
        )
        db.session.add(room)
        db.session.commit()
        print(f"room {room.id} did not exist, it is now created:")
        print(f"room name: {room.name}")

    def user_rooms_serialize(room_to_serialize):
        return {
            "id": room_to_serialize.id,
            "name": room_to_serialize.name,
        }

    return jsonify(
        {
            "rooms": tuple(map(user_rooms_serialize, current_user.rooms)),
            "new_room_id": room.id,
        }
    )
