function openModal(id) {
    document.getElementById(id).style.display = 'block';
}

function closeModal(id) {
    document.getElementById(id).style.display = 'none';
}

function openEditModal(id, name) {
    document.getElementById('editName').value = name;
    let form = document.getElementById('editDeptForm');

    // Construct the edit URL
    const currentPath = window.location.pathname;
    let basePath = currentPath.endsWith('/') ? currentPath.slice(0, -1) : currentPath;

    // This logic assumes we are on the manage_departments page
    form.action = `${basePath}/edit/${id}/`;

    openModal('editDeptModal');
}

function confirmDelete(url) {
    if (confirm("Are you sure? Deleting a department may cascade to its courses and other data.")) {
        window.location.href = url;
    }
}

window.onclick = function (event) {
    if (event.target.classList.contains('modal')) {
        event.target.style.display = "none";
    }
}
