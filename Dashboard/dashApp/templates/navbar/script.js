// JavaScript
const darkModeToggle = document.getElementById("dark-mode-toggle");
const sunIcon = document.getElementById("sun-icon");
const moonIcon = document.getElementById("moon-icon");

darkModeToggle.addEventListener("click", () => {
  document.body.classList.toggle("dark");
  sunIcon.classList.toggle("hidden");
  moonIcon.classList.toggle("block");
});
