from flask import Blueprint, jsonify
from flask_login import login_required, current_user

from app.db import db
from app.db.models import Room, User


chat_blueprint = Blueprint("chat_blueprint", __name__, url_prefix="/chat")

DEFAULT_MESSAGES_TO_LOAD = 15


# Helper function to serialize a message
def serialize_message(message):
    return {
        "author_name": message.author.name,
        "content": message.content,
        "timestamp": message.timestamp,
    }


@chat_blueprint.route("/get_past_messages/<room_id>/")
@login_required
def get_past_messages(room_id):
    room = Room.query.get_or_404(room_id)

    past_messages = room.messages[-DEFAULT_MESSAGES_TO_LOAD:]
    past_messages = tuple(map(serialize_message, past_messages))

    return jsonify(past_messages)


@chat_blueprint.route("/get_more_messages/<room_id>/<int:messages_loaded>/")
@login_required
def get_more_messages(room_id, messages_loaded):
    room = Room.query.get_or_404(room_id)
    message_loaded = int(messages_loaded)

    # Get messages before the messages already loaded
    filtered_messages = room.messages[
        -(DEFAULT_MESSAGES_TO_LOAD + message_loaded) : -messages_loaded
    ]
    # Change order of messages to prepend them in the page
    sorted_messages = sorted(
        filtered_messages, key=lambda msg: msg.timestamp, reverse=True
    )

    past_messages = tuple(map(serialize_message, sorted_messages))

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

    def room_serializer(room_to_serialize):
        serialized_name = room_to_serialize.name
        if serialized_name is None:
            members_names = [
                member.name
                for member in room_to_serialize.members
                if member != current_user
            ]
            members_names.sort()
            serialized_name = ", ".join(members_names)

        return {
            "id": room_to_serialize.id,
            "name": serialized_name,
        }

    return jsonify(
        {
            "rooms": tuple(map(room_serializer, current_user.rooms)),
            "new_room_id": room.id,
        }
    )
