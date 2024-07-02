document.addEventListener("DOMContentLoaded", () => {
  document.querySelectorAll(".danger-btn, .danger-btn-outline").forEach(btn => {
    btn.onclick = e => {
      dangerConfirm(e, btn.value);
    }
  });
  
})

function dangerConfirm(e, value='continue') {
  actionList = ["withdraw", "delete", "remove", "cancel", "revoke", "continue"];
  if (confirm(`Are you sure you want to ${actionList.includes(value.toLowerCase()) ? value : 'continue'}?`)) {
    return true;
  } else {
    e.preventDefault();
  }
}