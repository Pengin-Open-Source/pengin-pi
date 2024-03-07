const socket = io();
const sent_messages = document.querySelector(".message-display-sender");
const received_messages = document.querySelector(".message-display-receiver");
const user_section = document.querySelector("#user-section");
const group_section = document.querySelector("#group-section");
const inChatUserHeader = document.getElementById("users-per-chat-head")
const inChatUsers = document.getElementById("users-in-chat")

socket.on('connect', function () {
    console.log("We have a new connection!")

    const chatForm = $('#chat-form').on('submit', function (e) {
        e.preventDefault()
        let display_name = "{{current_user.name}}"
        let message_text = $('textarea.message_text').val()

        socket.emit('message sent', {
            chat_name: display_name,
            content: message_text
        })
        $('textarea.message_text').val('').focus()
    })


    const userPick = $('#chat-with-user').on("click", ".other-chat-user", function (e) {
        e.preventDefault()
        const user_picked = $(this).val();
        sent_messages.content = document.querySelector(".message-display-sender");
        received_messages.content = document.querySelector(".message-display-receiver");

        socket.emit('user selected', {
            other_user: user_picked
        })

    })


    const groupPick = $('#chat-with-group').on("click", ".chat-group", function (e) {
        e.preventDefault()
        const group_picked = $(this).val();
        sent_messages.content = document.querySelector(".message-display-sender");
        received_messages.content = document.querySelector(".message-display-receiver");
        socket.emit('room selected', {
            room_name: group_picked
        })

    })

})

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


