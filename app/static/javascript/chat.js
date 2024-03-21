/// >>>>>>>>>>>>>>>>>>>>> CHAT DISPLAY FUNCTIONS <<<<<<<<<<<<<<<<<<<<<

// Open chat window
function displayBtn() {
    const messageModal = document.getElementById('message-display')
    messageModal.classList.add("show")
}

// Close chat window
function closeMessage() {
    const messageModal = document.getElementById('message-display')
    messageModal.classList.remove("show")
}

const collapseButtons = $('.collapsible');
for (const button of collapseButtons) {
    button.addEventListener('click', function () {
        this.classList.toggle('active');
        const content = this.nextElementSibling;
        content.classList.toggle('hide');
    });
}

/// >>>>>>>>>>>>>>>>>>>>> SOCKET IO CHAT FUNCTIONS AND EVENT LISTENERS <<<<<<<<<<<<<<<<<<<<<
const socketio = io();
let room_id = "";

// Add event listener to the user buttons (to open chat with another user)
const selectUserButtons = $(".btn-select-user");
for (const button of selectUserButtons) {
    button.addEventListener("click", function () {
        const user_id = this.dataset.userId;
        selectRoom("user_id", user_id)
        fetch(`/chat/get_room_id/${user_id}/`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json'
            },
        })
            .then(response => response.json())
            .then(data => {
                updateRoomList(data.rooms)
                selectRoom(data.new_room_id)
            })
            .catch(error => {
                console.error('Error:', error);
            })
    });
}

// Add event listener to the room buttons (to open a room already created)
const selectRoomButtons = $(".btn-select-room");
for (const button of selectRoomButtons) {
    button.addEventListener("click", function () {
        const room_id = this.dataset.roomId;
        selectRoom(room_id)
    });
}

// Join current user to room with selected room
function selectRoom(room_id) {
    $('div.message-display').empty();
    socketio.emit("join_room", {room_id: room_id});
}

// Scroll to last message
function scrollToLastMessage() {
    const messageHolder = $('.message-display')[0];
    const lastMessage = messageHolder.lastElementChild;
    lastMessage.scrollIntoView();
}

// Fetch all messages from the server DB
function fetchMessage(room_id) {
    console.log("fetching messages for " + room_id)
    // Send AJAX request to server
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
                createMessage({
                    author_name: message.author_name,
                    content: message.content,
                    timestamp: message.timestamp
                });
            }
        })
        .then(() => {
            scrollToLastMessage();
        })
        .catch(error => {
            console.error('Error:', error);
        });
}

// Add new message in the page
function createMessage(message) {

    const currentUserName = document.getElementById('current-user').dataset.name;
    const isSender = message.author_name === currentUserName;

    const msgSection = document.createElement('div');
    msgSection.classList.add("text-section");
    msgSection.classList.add(isSender ? "sender" : "receiver");

    const metadata = document.createElement('div');
    metadata.classList.add("message-metadata");

    const author = document.createElement('span');
    author.classList.add("message-author");
    author.innerText = message.author_name;
    const timestamp = document.createElement('span');
    timestamp.classList.add("message-timestamp");
    timestamp.innerText = message.timestamp;

    metadata.appendChild(author);
    metadata.appendChild(timestamp);

    const content = document.createElement('p');
    content.classList.add("message-content");
    content.innerText = message.content;

    msgSection.appendChild(metadata);
    msgSection.appendChild(content);
    $('div.message-display')[0].appendChild(msgSection)
}

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
    scrollToLastMessage();
});

// Adding room_id to the client
socketio.on('joined_message', data => {
    room_id = data.room_id;
    fetchMessage(data.room_id)
});
