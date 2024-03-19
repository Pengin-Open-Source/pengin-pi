from flask import Blueprint, jsonify
from app.db.models.message import Room
from flask_login import login_required


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
