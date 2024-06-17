

closeSecNav = () => {
  if (window.matchMedia("(width < 850px)").matches) {
    document.querySelector('#left-panel').style.left = '-100%';
  }
}

openSecNav = () => {
  if (window.matchMedia("(width < 850px)").matches) {
    document.querySelector('#left-panel').style.left = '0';
  }
}