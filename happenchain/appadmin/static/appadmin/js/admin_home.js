function showSection(id) {
    document.querySelectorAll('.section').forEach(sec => {
        sec.classList.remove('active');
    });

    document.querySelectorAll('.sidebar nav a').forEach(link => {
        link.classList.remove('active');
    });

    document.getElementById(id).classList.add('active');
    event.target.classList.add('active');
}
