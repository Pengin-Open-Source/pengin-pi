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
