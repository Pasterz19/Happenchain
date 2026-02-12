function fetchSubEvents(eventId) {
    const url = FETCH_SUB_EVENTS_URL.replace("0", eventId);

    fetch(url)
        .then(res => res.json())
        .then(data => openSubEventModal(data))
        .catch(err => console.error(err));
}

document.addEventListener("DOMContentLoaded", () => {
    document.querySelectorAll("[data-event-id]").forEach(btn => {
        btn.addEventListener("click", () => {
            fetchSubEvents(btn.dataset.eventId);
        });
    });
});

function openSubEventModal(data) {
    document.getElementById("parentEventTitle").innerText = data.event;

    const list = document.querySelector(".sub-event-list");
    list.innerHTML = "";

    data.sub_events.forEach(se => {
        const div = document.createElement("div");
        div.className = "event-card";

        div.innerHTML = `
            <h4>${se.title}</h4>
            <p>${se.description}</p>
            <p>${se.is_team_event ? "👥 Team Event" : "👤 Individual Event"}</p>
            <p>${se.is_team_event ? `Reg Fee : Rs.${se.cost}/team`:`Reg Fee : Rs.${se.cost}/head`}</p>
            <button class="btn btn-primary"
                    onclick="openRegisterModal(${se.id}, ${se.is_team_event})">
                Register
            </button>
        `;

        list.appendChild(div);
    });

    document.getElementById("subEventModal").style.display = "flex";
}
function closeSubEventModal() {
    const modal = document.getElementById("subEventModal");
    if (modal) {
        modal.style.display = "none";
    }
}

