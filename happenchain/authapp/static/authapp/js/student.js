let currentStudentStep = 1;
const totalStudentSteps = 3;

function showStudentStep(step) {
    document.querySelectorAll('.form-step')
        .forEach(el => el.classList.remove('active'));

    const stepEl = document.getElementById(`step${step}`);
    if (!stepEl) return;

    stepEl.classList.add('active');

    document.getElementById('progressBar').style.width =
        `${(step / totalStudentSteps) * 100}%`;

    document.getElementById('prevBtn').style.visibility =
        step === 1 ? 'hidden' : 'visible';

    document.getElementById('nextBtn').style.display =
        step === totalStudentSteps ? 'none' : 'block';

    document.getElementById('submitBtn').style.display =
        step === totalStudentSteps ? 'block' : 'none';
}

function changeStudentStep(n) {
    currentStudentStep += n;

    if (currentStudentStep < 1) currentStudentStep = 1;
    if (currentStudentStep > totalStudentSteps)
        currentStudentStep = totalStudentSteps;

    showStudentStep(currentStudentStep);
}

function updateFileName(input, displayId) {
    if (input.files.length > 0) {
        document.getElementById(displayId).innerText = input.files[0].name;
    }
}

function handleStudentFormSubmit(e) {
    e.preventDefault();
    alert("Student Registration Successful!");
}

showStudentStep(1);

document.addEventListener('DOMContentLoaded', function () {
    const collegeSelect = document.getElementById('collegeSelect');
    const departmentSelect = document.getElementById('departmentSelect');
    const degreeSelect = document.getElementById('degreeSelect');
    const courseSelect = document.getElementById('courseSelect');

    if (collegeSelect) {
        collegeSelect.addEventListener('change', function () {
            const collegeId = this.value;
            const url = this.getAttribute('data-departments-url');

            // Clear downstream
            departmentSelect.innerHTML = '<option value="" disabled selected>Select Dept</option>';
            degreeSelect.innerHTML = '<option value="" disabled selected>Select Degree</option>';
            courseSelect.innerHTML = '<option value="" disabled selected>Select Course</option>';

            if (collegeId) {
                fetch(`${url}?college_id=${collegeId}`)
                    .then(response => response.json())
                    .then(data => {
                        data.forEach(item => {
                            const option = document.createElement('option');
                            option.value = item.id;
                            option.textContent = item.name;
                            departmentSelect.appendChild(option);
                        });
                    })
                    .catch(error => console.error('Error loading departments:', error));
            }
        });
    }

    if (departmentSelect) {
        departmentSelect.addEventListener('change', function () {
            const departmentId = this.value;
            const url = this.getAttribute('data-degrees-url');

            degreeSelect.innerHTML = '<option value="" disabled selected>Select Degree</option>';
            courseSelect.innerHTML = '<option value="" disabled selected>Select Course</option>';

            if (departmentId) {
                fetch(`${url}?department_id=${departmentId}`)
                    .then(response => response.json())
                    .then(data => {
                        data.forEach(item => {
                            const option = document.createElement('option');
                            option.value = item.id;
                            option.textContent = item.name;
                            degreeSelect.appendChild(option);
                        });
                    })
                    .catch(error => console.error('Error loading degrees:', error));
            }
        });
    }

    if (degreeSelect) {
        degreeSelect.addEventListener('change', function () {
            const degreeId = this.value;
            const departmentId = departmentSelect.value;
            const url = this.getAttribute('data-courses-url');

            courseSelect.innerHTML = '<option value="" disabled selected>Select Course</option>';

            if (degreeId && departmentId) {
                fetch(`${url}?department_id=${departmentId}&degree_id=${degreeId}`)
                    .then(response => response.json())
                    .then(data => {
                        data.forEach(item => {
                            const option = document.createElement('option');
                            option.value = item.id;
                            option.textContent = item.name;
                            courseSelect.appendChild(option);
                        });
                    })
                    .catch(error => console.error('Error loading courses:', error));
            }
        });
    }
});