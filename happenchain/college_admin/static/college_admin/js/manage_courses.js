function openModal(id) {
    document.getElementById(id).style.display = 'block';
}

function closeModal(id) {
    document.getElementById(id).style.display = 'none';
}

function openEditModal(id, name, degree, duration, deptId) {
    document.getElementById('editName').value = name;
    document.getElementById('editDegree').value = degree;
    document.getElementById('editDuration').value = duration;

    let form = document.getElementById('editCourseForm');
    // Base URL must be handled carefully. Ideally passed or inferred.
    // Assuming the script is loaded where the context is roughly known, 
    // but the best way is to set the action dynamically based on a data attribute or similar.
    // However, recreating the exact logic from inline:

    // We can't rely on template tags in external JS.
    // Strategy: The form action should be set initially to a dummy, and we replace the ID.
    // OR simpler: just update the Action if we know the base structure.
    // Previous logic: form.action = baseUrl.replace(/\/$/, "") + "/edit/" + id + "/";
    // We need the baseUrl.

    // Better Approach: Store the base URL in a data attribute on the body or the table
    // For now, we'll assume the URL structure is consistent

    // Changing approach slightly to be robust:
    // We will assume the edit form has a data-pending-action attribute or we construct it relative to current location if possible,
    // but current location might be /manage_courses/.

    const currentPath = window.location.pathname; // /college_admin/courses/ hopefully
    // If we are at /college_admin/courses/, then edit url is /college_admin/courses/edit/<id>/

    // Let's use a regex or string manipulation.
    // If path ends with /, string it.
    let basePath = currentPath.endsWith('/') ? currentPath.slice(0, -1) : currentPath;

    form.action = `${basePath}/edit/${id}/`;

    openModal('editCourseModal');
}

function confirmDelete(url) {
    if (confirm("Are you sure you want to delete this course? This action cannot be undone.")) {
        window.location.href = url;
    }
}

window.onclick = function (event) {
    if (event.target.classList.contains('modal')) {
        event.target.style.display = "none";
    }
}
