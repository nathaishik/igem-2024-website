let markdown = document.querySelector('.markdown-body');

markdown.innerHTML = markdown.innerText;

document.addEventListener("DOMContentLoaded", () => {
  markdown.querySelectorAll("blockquote p").forEach((block) => {
      const CODES = ["NOTE", "IMPORTANT", "TIP", "WARNING", "CAUTION"]
      const end = block.innerHTML.search(']\n');
      const type = block.innerHTML.slice(2, end);
      block.innerHTML = block.innerHTML.slice(end + 1, block.innerHTML.length);
      if (CODES.includes(type)) {
      block.classList.add(`alert-${type.toLowerCase()}`);
      }
  })

  let linkButton = document.createElement("button");
  linkButton.classList.add("btn");
  linkButton.classList.add("section-link-btn");
  linkButton.innerHTML = "<span class=material-icons>link</span>";
  markdown.querySelectorAll("h1, h2, h3, h4, h5, h6").forEach((h) => {
    const btn = linkButton.cloneNode(true);
    btn.onclick = () => copyLink(window.location.href.split('#')[0] + "#" + h.id);
      h.appendChild(btn);
  });

  markdown.querySelectorAll("table").forEach((table) => {
    const p = document.createElement("p");
    p.classList.add("table");
    p.appendChild(table.cloneNode(true));
    table.before(p);
    table.remove();
  });
});

function copyLink(link) {
  navigator.clipboard.writeText(link);
}
