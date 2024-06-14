document.addEventListener("DOMContentLoaded", () => {
  const url = window.location.pathname;
  let url_array = url.split('/');
  url_array = url_array.filter((item) => item !== '');
  const len = url_array.length;
  let links = document.querySelectorAll('#pri-nav a, #sec-nav a');
  let url_str = window.location.protocol + '//' + window.location.hostname + (window.location.port ? ':' + window.location.port : '') + '/';
  console.log("port", window.location.port);
  for (let i = 0; i < len; i++) {
    for (let a of links) {
      if (a.href === url_str + url_array[i] + '/' || a.href === url_str + url_array[i]) {
        if (a.parentElement.parentElement.parentElement.tagName.toLowerCase() === 'details') {
          a.parentElement.parentElement.parentElement.open = true;
        }
        a.classList.add('active');
      }
    }; 
    url_str += url_array[i] + '/';
}
document.querySelectorAll('.tabs a').forEach((tab) => {
  if (tab.href === window.location.href) {
    tab.classList.add('active');
  }
})
});