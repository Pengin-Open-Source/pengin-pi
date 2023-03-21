const hamburgerToggle= () => {
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

const adminHamburgerToggle= () => {
  // TODO this is all wrong it needs sorting for mobile admin toggle
  const admin_nav = document.querySelector('#nav-id');

  if (admin_nav.className === 'header-navigation') {
    admin_nav.className = 'responsive-nav'
  } else {
    admin_nav.className = 'header-navigation'
  }
}

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

let display_user = false
let display_group = false
function displayUser() {
  // const userBtn = document.getElementById('user-btn')
  // const groupBtn = document.getElementById('group-btn')
  display_user = !display_user
  const userDiv = document.getElementById('user-container')
  const groupDiv = document.getElementById('group-container')
  if (display_group === true) display_group = !display_group
  if ((display_user === true) && (display_group === false)) {
    groupDiv.style.maxHeight = '0px'
    userDiv.style.maxHeight = '200px'
    userDiv.style.margin = '8px 0px'
  } else {
    groupDiv.style.maxHeight = '120px'
    userDiv.style.maxHeight = '120px'
  }
  // const groupDiv = document.getElementById('group-container')
  
}

function displayGroup() {
  display_group = !display_group
  const userDiv = document.getElementById('user-container')
  const groupDiv = document.getElementById('group-container')
  if (display_user === true) display_user = !display_user
  if ((display_group === true) && (display_user === false)) {
    userDiv.style.maxHeight = '0px'
    groupDiv.style.maxHeight = '200px'
    groupDiv.style.margin = '8px 0px'
  } else {
    groupDiv.style.maxHeight = '120px'
    userDiv.style.maxHeight = '120px'
  }
}