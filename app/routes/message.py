from flask import Blueprint, jsonify
from app.db.models.message import Room
from flask_login import login_required


chat_blueprint = Blueprint("chat_blueprint", __name__, url_prefix="/chat")


@chat_blueprint.route("/get_past_messages/<room_id>/")
@login_required
def get_past_messages(room_id):
    room = Room.query.get(room_id)

    # TODO paginate messages
    past_messages = []
    for message in room.messages:
        past_messages.append(
            {
                "author_name": message.author.name,
                "content": message.content,
                "timestamp": message.timestamp,
            }
        )
    return jsonify(past_messages)
