from flask_login import current_user


# Helper function to serialize a message
def message_serializer(message):
    return {
        "author_name": message.author.name,
        "content": message.content,
        "timestamp": message.timestamp,
    }


def room_serializer(room_to_serialize):
    members = [
        member.name for member in room_to_serialize.members if member != current_user
    ]
    members.sort()
    members = ", ".join(members)

    serialized_name = room_to_serialize.name
    if serialized_name is None:
        serialized_name = members

    if room_to_serialize.messages:
        last_updated = room_to_serialize.messages[-1].timestamp
    elif room_to_serialize.date_created is not None:
        last_updated = room_to_serialize.date_created.strftime("%Y-%m-%d %H:%M:%S")
    else:
        last_updated = ""

    return {
        "id": room_to_serialize.id,
        "name": serialized_name,
        "members": members,
        "last_updated": last_updated,
    }


# Function to order rooms by their latest update, with the newest updated rooms first
def room_order_by_last_update(rooms):
    return sorted(
        rooms,
        key=lambda room: room["last_updated"] or "",
        reverse=True,
    )
