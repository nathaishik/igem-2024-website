document.addEventListener("DOMContentLoaded", () => {
  actionList = ["withdraw", "delete", "remove", "cancel", "revoke"];
  document.querySelectorAll(".danger-btn, .danger-btn-outline").forEach(btn => {
    btn.onclick = e => {
      console.log(btn.value in actionList, actionList);
      if (confirm(`Are you sure you want to ${actionList.includes(btn.value) ? btn.value : "continue"}?`)) {
        return true;
      } else {
        e.preventDefault();
      }
    }
  });

})