function openModal(id) {
    document.getElementById(id).classList.add("show");
}

function closeModal(id) {
    document.getElementById(id).classList.remove("show");
}
document.addEventListener("DOMContentLoaded", function () {
    const input = document.getElementById("eventPhotoInput");
    const label = document.getElementById("eventPhotoName");

    if (input && label) {
        input.addEventListener("change", function () {
            if (this.files.length > 0) {
                label.innerHTML =
                    `<i class="fas fa-file-image"></i> ${this.files[0].name}`;
            } else {
                label.innerHTML =
                    `<i class="fas fa-cloud-upload-alt"></i> Click to upload image`;
            }
        });
    }
});

