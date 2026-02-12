document.addEventListener("DOMContentLoaded", () => {

    // --- Chart 1: Top Events (Bar) ---
    const eventCanvas = document.getElementById("topEventsChart");
    if (eventCanvas) {
        const labels = JSON.parse(document.getElementById("eventLabels").textContent);
        const data = JSON.parse(document.getElementById("eventData").textContent);

        new Chart(eventCanvas, {
            type: 'bar',
            data: {
                labels: labels,
                datasets: [{
                    label: 'Registrations',
                    data: data,
                    backgroundColor: 'rgba(0, 229, 255, 0.6)',
                    borderColor: '#00E5FF',
                    borderWidth: 1,
                    borderRadius: 6
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: { display: false }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        grid: { color: 'rgba(255, 255, 255, 0.05)' },
                        ticks: { color: '#94A3B8' }
                    },
                    x: {
                        grid: { display: false },
                        ticks: { color: '#94A3B8' }
                    }
                }
            }
        });
    }

    // --- Chart 2: Department Share (Doughnut) ---
    const deptCanvas = document.getElementById("deptShareChart");
    if (deptCanvas) {
        const labels = JSON.parse(document.getElementById("deptLabels").textContent);
        const data = JSON.parse(document.getElementById("deptData").textContent);

        new Chart(deptCanvas, {
            type: 'doughnut',
            data: {
                labels: labels,
                datasets: [{
                    data: data,
                    backgroundColor: [
                        'rgba(0, 229, 255, 0.7)',
                        'rgba(123, 44, 191, 0.7)',
                        'rgba(255, 107, 107, 0.7)',
                        'rgba(255, 159, 67, 0.7)',
                        'rgba(0, 210, 211, 0.7)'
                    ],
                    borderColor: 'transparent',
                    borderWidth: 0
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'bottom',
                        labels: { color: '#94A3B8' }
                    }
                }
            }
        });
    }
});
