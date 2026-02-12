document.addEventListener("DOMContentLoaded", () => {
    const canvas = document.getElementById("registrationChart");
    if (!canvas) return;

    const labels = JSON.parse(
        document.getElementById("labels").textContent
    );

    const values = JSON.parse(
        document.getElementById("values").textContent
    );

    new Chart(canvas, {
        type: "bar",
        data: {
            labels: labels,
            datasets: [{
                data: values,
                backgroundColor: "rgba(0, 229, 255, 0.6)",
                borderRadius: 6
            }]
        },
        options: {
            plugins: {
                legend: { display: false }
            },
            scales: {
                y: { beginAtZero: true }
            }
        }
    });
});
