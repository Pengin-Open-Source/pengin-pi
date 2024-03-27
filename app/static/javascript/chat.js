/// >>>>>>>>>>>>>>>>>>>>> CHAT DISPLAY FUNCTIONS <<<<<<<<<<<<<<<<<<<<<

// Define the modal
const messageModal = document.getElementById('message-display');
// Define the chat conversation section
const chatConversationSection = document.getElementById('chat-conversation-section');


// Open chat window
function openMessageModal() {
    messageModal.classList.add("show");
    addEventListenersToRoomButtons();
}

// Close chat window
function closeMessageModal() {
    messageModal.classList.remove("show")
}

function closeChatConversation() {
    chatConversationSection.classList.add("hide");
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
        // Call route to create room if needed and get room id
        fetch(`/chat/get_room_id/${user_id}/`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json'
            },
        })
            .then(response => response.json())
            .then(room_id => {
                selectRoom(room_id)
            })
            .catch(error => {
                console.error('Error:', error);
            })
    });
}

// Add event listener to the room buttons (to open a room already created)
function addEventListenersToRoomButtons() {
    const selectRoomButtons = $(".btn-select-chat");
    for (const button of selectRoomButtons) {
        button.addEventListener("click", function () {
            const room_id = this.dataset.roomId;
            selectRoom(room_id)
        });
    }
}

// Update room list in the page
function updateRoomList(rooms) {
    const roomList = $('#group-container')[0];
    roomList.innerHTML = "";
    for (const room of rooms) {
        const roomButton = document.createElement('div');
        roomButton.classList.add("message-grid-item", "btn-select-chat");
        roomButton.dataset.roomId = room.id;
        roomButton.innerText = room.name;
        roomList.appendChild(roomButton);
    }
    addEventListenersToRoomButtons();
}

// Join current user to room with selected room
function selectRoom(room_id) {
    $('div.message-holder').empty();
    $('div.message-load-button-container').empty();
    socketio.emit("join_room", {room_id: room_id});
}

// Scroll to last message
function scrollToLastMessage() {
    const messageHolder = $('.message-holder')[0];
    const lastMessage = messageHolder.lastElementChild;
    if (lastMessage) {
        lastMessage.scrollIntoView();
    }
}

// Fetch messages when opening the chat conversation window
function fetchMessage(room_id) {
    fetch(`/chat/get_past_messages/${room_id}/`, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json'
        },
    })
        .then(response => response.json())
        .then(data => {
            updateRoomList(data.rooms)
            if (data.past_messages && data.past_messages.length > 0) {
                addLoadMoreButton();
                for (const message of data.past_messages) {
                    // Trigger function to add message in page
                    createMessage({
                        author_name: message.author_name,
                        content: message.content,
                        timestamp: message.timestamp
                    });
                }
            } else {
                noMessages();
            }
        })
        .then(() => {
            scrollToLastMessage();
        })
        .catch(error => {
            console.error('Error:', error);
        });
}

// Fetch previous messages to load
function get_more_messages() {
    const messageHolder = $('.message-holder')[0];
    const messagesLoaded = messageHolder.childElementCount;
    fetch(`/chat/get_more_messages/${room_id}/${messagesLoaded}/`, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json'
        },
    })
        .then(response => response.json())
        .then(messages => {
            if (messages && messages.length > 0) {
                for (const message of messages) {
                    // Trigger function to add messages in page
                    createMessage({
                        author_name: message.author_name,
                        content: message.content,
                        timestamp: message.timestamp
                    }, true);
                }
            } else {
                noMoreMessages();
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });

}

// Add button to load more messages
function addLoadMoreButton() {
    const loadMoreButton = document.createElement('p');
    loadMoreButton.classList.add("message-load-text", "message-load-button", "load-more-messages");
    loadMoreButton.innerText = "Load more messages";
    loadMoreButton.addEventListener('click', function () {
        get_more_messages()
    });
    $('div.message-load-button-container').empty().append(loadMoreButton)
}

function noMessages() {
    const noMessages = document.createElement('p');
    noMessages.classList.add("message-load-text", "no-messages");
    noMessages.innerText = "No messages yet. \nSend a message to start the conversation.";
    $('div.message-load-button-container').empty().append(noMessages)

}
function noMoreMessages() {
    const noMoreMessages = document.createElement('p');
    noMoreMessages.classList.add("message-load-text", "no-more-messages");
    noMoreMessages.innerText = "You've loaded all the messages.";
    $('div.message-load-button-container').empty().append(noMoreMessages)
}

// Add new message in the page
function createMessage(message, before=false) {

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
    if (before) {
        $('div.message-holder')[0].prepend(msgSection)

    } else {
        $('div.message-holder')[0].append(msgSection)
    }
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
socketio.on('joined_message', room => {
    if (room.members) {
        $('.chat-list-members')[0].innerText = "Now chatting with " + room.members;
    }
    room_id = room.id;
    chatConversationSection.classList.remove("hide");
    fetchMessage(room.id)
});
