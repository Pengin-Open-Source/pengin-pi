const hamburgerToggle = () => {
  const nav = document.querySelector('#nav-id');

  if (nav.className === 'header-navigation') {
    nav.className = 'responsive-nav'
  } else {
    nav.className = 'header-navigation'
  }
}

const addOrderRow = () => {
  const order = document.querySelector('.order');
  const newOrder = order.cloneNode(true);

  order.after(newOrder);
}

const removeOrderRow = (event) => {
  const orders = document.querySelectorAll('.order');
  if (orders.length > 1) {
    event.parentElement.parentElement.remove();
  }

}

const adminHamburgerToggle = () => {
  // TODO this is all wrong it needs sorting for mobile admin toggle
  const admin_nav = document.querySelector('#nav-id');

  if (admin_nav.className === 'header-navigation') {
    admin_nav.className = 'responsive-nav'
  } else {
    admin_nav.className = 'header-navigation'
  }
}

/// >>>>>>>>>>>>>>>>>>>>> CHAT MESSAGE SECTION <<<<<<<<<<<<<<<<<<<<<
let display_user = true
let display_group = true
let display_chosen_group = false
let display_group_users = false
let in_room_now = false



function displayBtn() {
  messageBtn = document.getElementById("message-btn")
  // let messageDisplay = false;
  const messageModal = document.getElementById('message-display')
  messageModal.style.display = "block"
}

function closeMessage() {
  const messageModal = document.getElementById('message-display')
  messageModal.style.display = "none";
}


function displayUser() {
  // const userBtn = document.getElementById('user-btn')
  // const groupBtn = document.getElementById('group-btn')
  display_user = !display_user
  displayGroupsAndUsers()

}


function displayGroup() {
  display_group = !display_group
  displayGroupsAndUsers()

}

function displayGroupsAndUsers() {
  const userDiv = document.getElementById('user-container')
  const groupDiv = document.getElementById('group-container')

  // In case you want a different message when lists are collapsed
  //const userHeader = document.getElementById('user-list-head')
  //const groupHeader = document.getElementById('group-list-head')

  if ((display_group === true) && (display_user === false)) {
    userDiv.style.maxHeight = '0px'
    groupDiv.style.maxHeight = '200px'
    groupDiv.style.margin = '8px 0px'
  }
  else if ((display_group === false) && (display_user === true)) {
    groupDiv.style.maxHeight = '0px'
    userDiv.style.maxHeight = '200px'
    userDiv.style.margin = '8px 0px'

  } else if ((display_group === false) && (display_user === false)) {
    groupDiv.style.maxHeight = '0px'
    userDiv.style.maxHeight = '0px'
  }

  else {
    groupDiv.style.maxHeight = '120px'
    userDiv.style.maxHeight = '120px'
  }
}

function closeLists() {
  display_group = false
  display_user = false
  displayGroupsAndUsers()
}

// In case this is needed...
function openLists() {
  display_group = true
  display_user = true
  displayGroupsAndUsers()

}

function roomSelected() {
  in_room_now = true
  closeLists()
}

//In case this is needed later... Leave chat without opening a new one
//Reverse of displayRoomSelected.  Just in case you want a Leave Chat button at some point
function leaveChatRoom() {
  in_room_now = false
  openLists()
}


///  >>>>>>>>>>>>>>>>>>>>>>>> END CHAT MESSAGE SECTION <<<<<<<<<<<<<<<<<<<<<