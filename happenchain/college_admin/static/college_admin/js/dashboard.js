

// 2. Render Events List
function renderEvents() {
    const listContainer = document.getElementById('eventsListContainer');
    if (!listContainer) return;
    listContainer.innerHTML = '';

    eventsRegistry.forEach(event => {
        // Determine badge class
        const badgeClass = event.status === 'Upcoming' ? 'status-upcoming' : 'status-pending';
        
        const item = document.createElement('div');
        item.className = 'event-item';
        item.innerHTML = `
            <div class="event-date">
                <span>${event.day}</span>
                <small>${event.month}</small>
            </div>
            <div class="event-details">
                <h5>${event.title}</h5>
                <p><i class="fas fa-layer-group"></i> ${event.dept}</p>
            </div>
            <span class="status-badge ${badgeClass}">${event.status}</span>
        `;
        listContainer.appendChild(item);
    });
}


// Initialize
document.addEventListener('DOMContentLoaded', () => {
    renderEvents();
});

function toggleSubEvents(id) {
    const el = document.getElementById(id);
    if (!el) return;

    el.style.display = el.style.display === "none" ? "block" : "none";
}
