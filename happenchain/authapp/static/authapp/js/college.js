// js/college.js

let currentCollegeStep = 1;
const totalCollegeSteps = 3;

function showCollegeStep(step) {
    document.querySelectorAll('.form-step').forEach(el => el.classList.remove('active'));
    document.getElementById(`collegeStep${step}`).classList.add('active');

    document.getElementById('collegeProgressBar').style.width = `${(step / totalCollegeSteps) * 100}%`;

    document.getElementById('collegePrevBtn').style.visibility = step === 1 ? 'hidden' : 'visible';
    document.getElementById('collegeNextBtn').style.display = step === totalCollegeSteps ? 'none' : 'block';
    document.getElementById('collegeSubmitBtn').style.display = step === totalCollegeSteps ? 'block' : 'none';
}

function changeCollegeStep(n) {
    currentCollegeStep += n;
    showCollegeStep(currentCollegeStep);
}

function updateFileName(input, displayId) {
    document.getElementById(displayId).innerText = input.files[0].name;
}

// function handleCollegeFormSubmit(e) {
//     alert("College Registration Submitted!");
//     window.location.href = "home.html";
// }

showCollegeStep(1);
