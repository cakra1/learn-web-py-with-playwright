// toggle show / hide password
document.addEventListener("DOMContentLoaded", function () {
  document.querySelectorAll(".toggle-password").forEach(icon => {
    icon.addEventListener("click", function () {
      const input = document.getElementById(this.dataset.target);

      if (!input) return;

      if (input.type === "password") {
        input.type = "text";
        this.classList.remove("fa-eye");
        this.classList.add("fa-eye-slash");
      } else {
        input.type = "password";
        this.classList.remove("fa-eye-slash");
        this.classList.add("fa-eye");
      }
    });
  });
});


document.querySelector("form").addEventListener("submit", function(e) {
  const name = document.getElementById("name").value.trim();
  const email = document.getElementById("email").value.trim();
  const password = document.getElementById("password").value;
  const confirm = document.getElementById("confirm_password").value;

  const formError = document.getElementById("form-error");
  const passwordError = document.getElementById("password-error");

  // reset error
  formError.style.display = "none";
  passwordError.style.display = "none";

  // cek kosong
  if (!name || !email || !password || !confirm) {
    e.preventDefault();
    formError.style.display = "block";
    return;
  }

  // cek password sama
  if (password !== confirm) {
    e.preventDefault();
    passwordError.style.display = "block";
    return;
  }
});
