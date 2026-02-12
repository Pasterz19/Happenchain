// js/main.js

// Header Scroll Effect
window.addEventListener('scroll', () => {
    const header = document.getElementById('mainHeader');
    if (!header) return;

    if (window.scrollY > 50) {
        header.classList.add('scrolled');
    } else {
        header.classList.remove('scrolled');
    }
});

// Navigation Highlight
window.addEventListener('scroll', () => {
    const sections = document.querySelectorAll('section');
    const navLinks = document.querySelectorAll('.nav-links a');
    let current = '';

    sections.forEach(section => {
        const sectionTop = section.offsetTop;
        if (pageYOffset >= sectionTop - 150) {
            current = section.getAttribute('id');
        }
    });

    navLinks.forEach(link => {
        link.classList.remove('active');
        if (link.getAttribute('href').slice(1) === current) {
            link.classList.add('active');
        }
    });
});

// Navigation Logic
function goToGetStarted() {
    document.getElementById('mainContent').style.display = 'none';
    document.getElementById('mainHeader').style.display = 'none';
    document.getElementById('getStartedSection').classList.add('show');
    window.scrollTo(0, 0);
}

function backToHome() {
    document.getElementById('mainContent').style.display = 'block';
    document.getElementById('mainHeader').style.display = 'flex';
    document.getElementById('getStartedSection').classList.remove('show');
}

// Modal Logic
function openModal(id) {
    document.getElementById(id).classList.add('show');
    document.body.style.overflow = 'hidden';
}

function closeModal(id) {
    document.getElementById(id).classList.remove('show');
    document.body.style.overflow = 'auto';
}

function switchModal(closeId, openId) {
    closeModal(closeId);
    openModal(openId);
}

// Close modal on outside click
window.onclick = function(event) {
    if (event.target.classList.contains('modal-overlay')) {
        event.target.classList.remove('show');
        document.body.style.overflow = 'auto';
    }
};
