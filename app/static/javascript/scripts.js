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
function displayBtn() {
  const messageModal = document.getElementById('message-display')
  messageModal.classList.add("show")
}

function closeMessage() {
  const messageModal = document.getElementById('message-display')
  messageModal.classList.remove("show")
}

let display_user = false
let display_group = true

function displayUser() {
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

  if (display_group && !display_user) {
    userDiv.classList.add('hide')
    groupDiv.classList.remove('hide')
    // userDiv.style.maxHeight = '0px'
    // groupDiv.style.maxHeight = '200px'
  } else if (!display_group && display_user) {
    userDiv.classList.remove('hide')
    groupDiv.classList.add('hide')
    // groupDiv.style.maxHeight = '0px'
    // userDiv.style.maxHeight = '200px'
  } else if (!display_group && !display_user) {
    userDiv.classList.add('hide')
    groupDiv.classList.add('hide')
    // groupDiv.style.maxHeight = '0px'
    // userDiv.style.maxHeight = '0px'
  } else {
    userDiv.classList.remove('hide')
    groupDiv.classList.remove('hide')
    // groupDiv.style.maxHeight = '120px'
    // userDiv.style.maxHeight = '120px'
  }
}




///  >>>>>>>>>>>>>>>>>>>>>>>> END CHAT MESSAGE SECTION <<<<<<<<<<<<<<<<<<<<<