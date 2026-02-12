document.addEventListener("DOMContentLoaded", () => {
    const canvas = document.getElementById("deptChart");
    if (!canvas) return;

    try {
        const labels = JSON.parse(document.getElementById("labels").textContent);
        const values = JSON.parse(document.getElementById("values").textContent);

        new Chart(canvas, {
            type: 'bar',
            data: {
                labels: labels,
                datasets: [{
                    label: 'Registrations',
                    data: values,
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
                    legend: {
                        display: false
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        grid: {
                            color: 'rgba(255, 255, 255, 0.05)'
                        },
                        ticks: {
                            color: '#94A3B8'
                        }
                    },
                    x: {
                        grid: {
                            display: false
                        },
                        ticks: {
                            color: '#94A3B8'
                        }
                    }
                }
            }
        });
    } catch (e) {
        console.error("Error initializing chart:", e);
    }
});
