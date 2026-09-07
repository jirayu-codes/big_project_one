const form = document.getElementById("add-plant-form");

form.addEventListener("submit", () => {
    const button = form.querySelector("button");
    button.disabled = true;
    button.textContent = "Adding...";
});
