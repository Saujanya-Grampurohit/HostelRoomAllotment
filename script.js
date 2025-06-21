document.getElementById("studentForm")?.addEventListener("submit", function (e) {
    e.preventDefault();
    alert("Registration successful! (data can be stored via backend)");
    this.reset();
  });
  