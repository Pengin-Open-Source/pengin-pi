const hamburgerToggle= () => {
  const nav = document.querySelector('#nav-id');

  if (nav.className === 'header-navigation') {
    nav.className = 'responsive-nav'
  } else {
    nav.className = 'header-navigation'
  }
  console.log('test')
}

const addOrderRow = () => {
  const order = document.querySelector('.order');
  const newOrder = order.cloneNode(true);

  order.after(newOrder);
}

const removeOrderRow = (event) => {
  const orders = document.querySelectorAll('.order');
  console.log(orders.length)
  if (orders.length > 1) {
    event.parentElement.parentElement.remove();
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