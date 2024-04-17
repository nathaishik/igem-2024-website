document.querySelectorAll('nav a').forEach((a) => {
  if (a.href == window.location.href) {
    console.log(a.href, window.location.href)
    a.classList.add('active-btn');
  }
});