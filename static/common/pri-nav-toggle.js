

closePriNav = () => {
  if (window.matchMedia("(width < 850px)").matches) {
    document.querySelector('#pri-nav ul').style.left = '100%';
  }
}

openPriNav = () => {
  if (window.matchMedia("(width < 850px)").matches) {
    document.querySelector('#pri-nav ul').style.left = '0';
  }
}