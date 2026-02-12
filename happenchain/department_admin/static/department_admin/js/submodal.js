
function openSubEventModal(eventId, eventTitle) {
    const eventIdInput = document.getElementById("parentEventId");
    const eventNameSpan = document.getElementById("parentEventName");

    if (eventIdInput && eventNameSpan) {
        eventIdInput.value = eventId;
        eventNameSpan.innerText = eventTitle;
    }

    openModal("subEventModal");
}
document.addEventListener("DOMContentLoaded", function () {
    const select = document.getElementById("isTeamSelect");

    if (select) {
        select.addEventListener("change", function () {
            const enabled = this.value === "true";
            document.getElementById("minTeamSize").disabled = !enabled;
            document.getElementById("maxTeamSize").disabled = !enabled;
        });
    }
});
