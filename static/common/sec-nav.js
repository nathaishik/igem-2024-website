document.addEventListener("DOMContentLoaded", () => {
  const url = window.location.pathname;
  let url_array = url.split('/');
  url_array = url_array.filter((item) => item !== '');
  const len = url_array.length;
  document.querySelectorAll('nav a').forEach((a) => {
    let url_str = window.location.protocol + '//' + window.location.hostname + ':' + window.location.port + '/';
    for (let i = 0; i < len; i++) {
    console.log(url_str, len, url_array);
    if (a.href === url_str + url_array[i] + '/') {
      a.classList.add('active');
      break;
    } else {
      url_str += url_array[i] + '/';
    }; 
  }
});
});