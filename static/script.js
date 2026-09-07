function disableSubmit(form) {
    const button = form.querySelector("button");
    button.disabled = true;
    button.textContent = "Adding...";
}

const form = document.getElementById("add-plant-form");

form.addEventListener("submit", () => disableSubmit(form));

document.querySelectorAll(".water-form").forEach((waterForm) => {
    waterForm.addEventListener("submit", () => {
        const button = waterForm.querySelector("button");
        button.disabled = true;
        button.textContent = "Watering...";
    });
});
