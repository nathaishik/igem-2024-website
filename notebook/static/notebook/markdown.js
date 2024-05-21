document.querySelector('.markdown-body').innerHTML = document.querySelector('.markdown-body').innerText;

document.addEventListener("DOMContentLoaded", () => {
  document.querySelectorAll(".markdown-body code").forEach((block) => {
    const array = block.innerHTML.split('\n')
    if (array.length > 1) {
      const parent = block.parentNode;
      parent.classList.add('code-block');
      const pre = document.createElement('pre');
      parent.replaceChild(pre, block);
      block.innerText = block.innerText.slice(1, block.innerText.length);
      pre.appendChild(block);
    }
  });
  document.querySelectorAll(".markdown-body blockquote p").forEach((block) => {
      const CODES = ["NOTE", "IMPORTANT", "TIP", "WARNING", "CAUTION"]
      const end = block.innerHTML.search(']\n');
      const type = block.innerHTML.slice(2, end);
      block.innerHTML = block.innerHTML.slice(end + 1, block.innerHTML.length);
      if (CODES.includes(type)) {
      block.classList.add(`alert-${type.toLowerCase()}`);
      }
})
});