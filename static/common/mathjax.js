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
  let script = document.createElement('script');
  script.src = STATIC_URL + 'common/tex-svg.js';
  script.async = true;
  document.head.appendChild(script);
})();
