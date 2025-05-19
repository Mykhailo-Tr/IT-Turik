document.addEventListener("DOMContentLoaded", function () {
    const input = document.getElementById("id_profile_picture");
    const preview = document.getElementById("preview");

    if (input && preview) {
        input.addEventListener("change", function (event) {
            const [file] = event.target.files;
            if (file) {
                preview.src = URL.createObjectURL(file);
            }
        });
    }
});