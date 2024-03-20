const socketio = io();
const sent_messages = document.querySelector(".message-display-sender");
const received_messages = document.querySelector(".message-display-receiver");
let room_id = "";

// Add event listener to the user buttons (to open chat with another user)
const selectUserButtons = $(".btn-select-user");
for (const button of selectUserButtons) {
    button.addEventListener("click", function () {
        const user_id = this.dataset.userId;
        selectRoom("user", user_id)
    });
}

// Add event listener to the room buttons (to open a room already created)
const selectRoomButtons = $(".btn-select-room");
for (const button of selectRoomButtons) {
    button.addEventListener("click", function () {
        const room_id = this.dataset.roomId;
        selectRoom("room", room_id)
    });
}

// Join current user to room with selected room
function selectRoom(type_of_id, id) {
    $('div.message-display').empty();

    if (type_of_id === "user") {
        data = { user_id: id }
    } else if (type_of_id === "room") {
        data = { room_id: id }
    }
    socketio.emit("join_room", data);
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
    newMessage.innerHTML = `
    <p>
        <strong>${message.author_name}</strong>:
    </p>
    <p> ${message.content} </p>
    <p>
       <i> ${message.timestamp} </i>
    </p>`;

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

socket.on('load chat', function (messages) {

    sent_messages.innerHTML = "";
    received_messages.innerHTML = "";
    const msgList = JSON.parse(messages);

    msgList.forEach(message => {
        createMessage(message)
    });

});

socket.on('users in group', function (data) {
    const chatting = JSON.parse(data);
    inChatUserHeader.innerHTML = "In Chat Room:  " + chatting[0].room_name
    inChatUsers.innerHTML = ""
    roomSelected()
    chatting.forEach(item => {
        const userName = item.user_name;
        const chatUser = document.createElement('div');
        chatUser.className = "message-grid-item";
        chatUser.innerHTML = item.user_name
        inChatUsers.appendChild(chatUser)
    });

});

socket.on('update chat', function (data) {
    createMessage(data)
});


// Send message to the server
function sendMessage() {
    const message = $("#chat_message")[0];
    if (message.value === "") return;
    socketio.emit("save_message", {content: message.value, room_id: room_id});
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
