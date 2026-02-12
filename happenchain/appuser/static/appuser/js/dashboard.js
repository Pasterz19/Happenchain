function filterEvents(query) {
    query = query.toLowerCase();

    document.querySelectorAll(".event-card").forEach(card => {
        card.style.display = card.innerText.toLowerCase().includes(query)
            ? "block"
            : "none";
    });
}
