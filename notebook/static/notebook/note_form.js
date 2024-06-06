// getCookie function from django documentation
function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
      const cookies = document.cookie.split(';');
      for (let i = 0; i < cookies.length; i++) {
          const cookie = cookies[i].trim();
          // Does this cookie string begin with the name we want?
          if (cookie.substring(0, name.length + 1) === (name + '=')) {
              cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
              break;
          }
      }
  }
  return cookieValue;
}


// Cleaning the file file input layout.
const file_div = document.querySelector("div:has(>#id_file)");
const fileInput = file_div.querySelector("#id_file");
let link = "";
let clearFile = "";
if (file_div.querySelector("a") !== null) {
  file_div.querySelector("a").innerText = "View current file";
  link = file_div.querySelector("a");
}
if (file_div.querySelector("#file-clear_id") !== null) {
  clearFile = file_div.querySelector("#file-clear_id");
  clearFile.classList.add("clear_button");
};
file_div.innerHTML = '';
file_div.append(link, clearFile, fileInput);

fileInput.addEventListener('change', () => {
  if (fileInput.files.length > 0 && clearFile != null) {
    clearFile.checked = false;
}
});

if (clearFile != '') {
  clearFile.addEventListener('click', () => {
    fileInput.value = '';
  });
}

// Adding a seperator between department input and title

const dept_div = document.querySelector("#id_department");
dept_div.after("/");

// Uploading Image
const file_handler = document.querySelector("#id_image");
file_handler.addEventListener('change', () => {
  if (file_handler.files.length > 0) {
    document.querySelector("label[for='id_image']").innerText = file_handler.files[0].name;
  }
});

const img_form = document.querySelector("#image_upload");
img_form.addEventListener('submit', e => {
  e.preventDefault();
  
  if (file_handler.files.length > 0) {
    const form = new FormData();
    form.append("image", file_handler.files[0]);
    console.log(file_handler.files[0])
    fetch(img_form.dataset.url, {
      method: 'POST',
      body: form,
      headers: {
        'X-CSRFToken': getCookie('csrftoken'),
      },
    })
    .then(response => response.json())
    .then(data => {
      console.log(data)
      if (data["images"]) {
        file_handler.value = '';
        const img_list = document.querySelector("#image_selector");
        if (img_list.querySelector("#no-img") != null) {img_list.querySelector("#no-img").remove()};
        let li = document.createElement("li");
        image = data["images"];
        li.id = image.id;
        li.innerHTML = `
            <img src="${ image.url }" alt="${ image.url }" class="image">
            <p class="img-name">${ image.location }</p>
            <div class="img-actions">
                <button type="copy" class="btn task-btn" onclick="copyLink('${image.url}')"><span class="material-icons">content_copy</span></button>
                <button type="delete" class="btn danger-btn" onclick="deleteImage('${ image.id }')"><span class="material-icons">delete</span></button>
            </div>
        `;
        img_list.prepend(li);
      }})
    .catch(error => console.error(error));
    }

  });

// Copying Image Link
function copyLink(link) {
  navigator.clipboard.writeText(link);
}

function deleteImage(id) {
  if (!confirm("Are you sure you want to delete this image?")) {
    return;
  };
  console.log(id);
  fetch(img_form.dataset.url, {
    method: 'DELETE',
    body: JSON.stringify({"id": id}),
    headers: {
      'X-CSRFToken': getCookie('csrftoken'),
    },
  })
  .then(response => response.json())
  .then(data => {
    console.log(data, id);
    if (data["status"] == 200) {
      const li = document.querySelector(`#${id}`);
      console.log(li);
      li.style.animationPlayState = "running";
      li.addEventListener('animationend', () => {
        li.remove();
        if (document.querySelector("#image_selector").querySelector("li") == null) {
          document.querySelector("#image_selector").innerHTML = "<p id='no-img'>No images uploaded yet.</p>";
        }
      });
    }
  })
}

function preview(link) {
  window.open(link, '_blank');
}

// Codemirror
const lightTheme = 'duotone-light';
const darkTheme = 'duotone-dark';

var editor = CodeMirror.fromTextArea(document.querySelector("#id_content"), {
  lineNumbers: true,
  mode: 'text/x-markdown',
  matchBrackets: true,
  autoCloseBrackets: true,
  styleActiveLine: true,
  theme: window.matchMedia('(prefers-color-scheme: dark)').matches ? darkTheme : lightTheme,
});

window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', e => {
  editor.setOption('theme', e.matches ? darkTheme : lightTheme);
});


