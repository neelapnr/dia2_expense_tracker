const fileInput = document.getElementById("fileInput");

const preview = document.getElementById("preview");


fileInput.addEventListener("change", () => {

    const file = fileInput.files[0];

    if (!file) return;

    const reader = new FileReader();

    reader.onload = (e) => {

        preview.src = e.target.result;
    };

    reader.readAsDataURL(file);
});


document.body.addEventListener(
    "htmx:responseError",
    () => {

        document.querySelector("#confirmation").innerHTML = `
            <div class="error">
                Une erreur est survenue
            </div>
        `;
    }
);
