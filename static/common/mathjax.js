window.MathJax = {
  tex: {
    inlineMath: [['$', '$'], ['\\(', '\\)']],
    displayMath: [['$$', '$$'], ['\\[', '\\]']],
  },
  svg: {
    fontCache: 'global'
  }
};

// The below tex-svg.js has been provided by MathJax.org and is owned by them under the Apache 2.0 License.

(function () {
  var script = document.createElement('script');
  script.src = `${window.location.pathname.split('/')[0]}/static/common/tex-svg.js`;
  script.async = true;
  document.head.appendChild(script);
})();
