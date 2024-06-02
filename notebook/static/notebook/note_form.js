const submitButton = document.querySelector('#form_submit');
const publish_div = document.querySelector('div:has(>#id_published)');
publish_div.append(submitButton);

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
file_div.append("File: ", link, clearFile, fileInput);

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


