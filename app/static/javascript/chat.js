const socketio = io();
const sent_messages = document.querySelector(".message-display-sender");
const received_messages = document.querySelector(".message-display-receiver");
let room_id = "";

// Add event listener to the room buttons (to open chat with other users)
const selectRoomButtons = $(".btn-select-room");
for (const button of selectRoomButtons) {
    button.addEventListener("click", function () {
        const room = this.dataset.room;
        selectRoom(room)
    });
}

// Join current user to room with selected room
function selectRoom(room) {
    $('div.message-display-sender').empty();
    $("div.message-display-receiver").empty();
    sent_messages.content = document.querySelector(".message-display-sender");
    received_messages.content = document.querySelector(".message-display-receiver");

    console.log("about to join room with " + room)
    socketio.emit("join_room", { other_user: room });
}

// Fetch all messages from the server DB
function fetchMessage(room_id) {
    console.log("fetching messages for " + room_id)
    // Send AJAX request to update instance status
    fetch(`/chat/get_past_messages/${room_id}/`, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json'
        },
    })
        .then(response => response.json())
        .then(data => {
            // Update the status on the page
            for (const message of data) {
                // Trigger function to add message in page
                createMessage({author_name: message.author_name, content: message.content, timestamp: message.timestamp});
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
}

// Create new message in the page
function createMessage(message) {

    const currentUserName = document.getElementById('current-user').dataset.name;
    const isSender = message.author_name === currentUserName;

    const msgSection = document.createElement('div');
    const newMessage = document.createElement('div');
    const msgSpace = document.createElement('div');
    msgSection.className = "text-section";
    newMessage.innerHTML = message.content;
    if (isSender) {
        newMessage.className = "text-section-s"
        msgSpace.className = "text-section-s";

        msgSection.appendChild(newMessage)
        msgSection.appendChild(msgSpace)
        sent_messages.appendChild(msgSection)
    } else {
        newMessage.className = "text-section-r"
        msgSpace.className = "text-section-r";

        msgSection.appendChild(msgSpace)
        msgSection.appendChild(newMessage)
        received_messages.appendChild(msgSection)
    }
}

// Send message to the server
function sendMessage() {
    const message = $("#message")[0];
    if (message.value === "") return;
    const currentUserId = document.getElementById('current-user').dataset.id;
    socketio.emit("save_message", { author_id: currentUserId, content: message.value, room_id: room_id});
    message.value = "";
}

// Listening for new saved data from the server
socketio.on('saved_message', (message) => {
    // Trigger function to add message in page
    createMessage({author_name: message.author_name, content: message.content, timestamp: message.timestamp});
});

// Adding room_id to the client
// TODO find alternative to avoid having the room id saved in the javascript
socketio.on('joined_message', data => {
    room_id = data.room_id;
    fetchMessage(data.room_id)
});
