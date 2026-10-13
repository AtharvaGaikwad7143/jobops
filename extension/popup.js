const button = document.getElementById("detect-job");
const status = document.getElementById("status");

button.addEventListener("click", () => {
    status.textContent = "Detecting job...";
});