document.addEventListener('DOMContentLoaded', function () {
    // optional initialization if needed
});

/* ===========================
   TOGGLE VISIBILITY
   =========================== */
function toggleSubEvents(eventId) {
    const section = document.getElementById(`subevents-${eventId}`);
    const icon = document.getElementById(`icon-${eventId}`);

    if (section.style.display === "none") {
        section.style.display = "block";
        icon.style.transform = "rotate(180deg)";
    } else {
        section.style.display = "none";
        icon.style.transform = "rotate(0deg)";
    }
}

/* ===========================
   VIEW DETAILS MODALS
   =========================== */
function handleShowEventDetails(btn) {
    // Read data attributes
    const title = btn.getAttribute('data-title');
    const desc = btn.getAttribute('data-desc');
    const venue = btn.getAttribute('data-venue');
    const start = btn.getAttribute('data-start');
    const end = btn.getAttribute('data-end');
    const type = btn.getAttribute('data-type');

    const content = `
        <p><strong>Type:</strong> ${type}</p>
        <p><strong>Venue:</strong> ${venue}</p>
        <p><strong>Date:</strong> ${start} to ${end}</p>
        <hr style="border-color: rgba(255,255,255,0.1); margin: 15px 0;">
        <p><strong>Description:</strong><br>${desc}</p>
    `;

    document.getElementById('infoTitle').textContent = title;
    document.getElementById('infoContent').innerHTML = content;
    document.getElementById('infoModal').style.display = 'flex';
}

function handleShowSubEventDetails(btn) {
    const title = btn.getAttribute('data-title');
    const desc = btn.getAttribute('data-desc');
    const cost = btn.getAttribute('data-cost');
    const venue = btn.getAttribute('data-venue');
    const start = btn.getAttribute('data-start');
    const end = btn.getAttribute('data-end');
    const isTeam = btn.getAttribute('data-is-team'); // string "True"/"False" or "true"/"false"
    const min = btn.getAttribute('data-min');
    const max = btn.getAttribute('data-max');

    let teamInfo = '';
    // Check various truthy values just in case
    if (isTeam === 'True' || isTeam === 'true' || isTeam === true) {
        teamInfo = `<p><strong>Team Size:</strong> ${min} - ${max} Members</p>`;
    } else {
        teamInfo = `<p><strong>Participation:</strong> Individual</p>`;
    }

    const content = `
        <p><strong>Venue:</strong> ${venue}</p>
        <p><strong>Time:</strong> ${start} - ${end}</p>
        <p><strong>Cost:</strong> ₹${cost || 'Free'}</p>
        ${teamInfo}
        <hr style="border-color: rgba(255,255,255,0.1); margin: 15px 0;">
        <p><strong>Description:</strong><br>${desc}</p>
    `;

    document.getElementById('infoTitle').textContent = title;
    document.getElementById('infoContent').innerHTML = content;
    document.getElementById('infoModal').style.display = 'flex';
}

/* ===========================
   EVENT: CREATE & EDIT
   =========================== */
function openCreateEventModal() {
    const form = document.getElementById('eventForm');
    form.reset();

    // We need the base URL for creation. 
    // Best practice: store this in a data attribute on the body or the button.
    // For now, we assume the action attribute is already set to 'create' in the HTML or we reset it.
    // BUT since editEvent changes it, we must ensure we set it back.
    // We'll read the 'data-create-url' from the Create button itself if passed, or rely on a global variable.
    // Let's rely on finding the Create button to get the URL, OR simply hardcode/inject it in HTML.
    // Better: let the view handling remain in HTML? No, user wants external JS.
    // We will pass the create URL to this function or store it in a generic element.

    // To solve this: we'll call this function with the URL from the button's data attribute.
}

function handleOpenCreateEvent(btn) {
    const url = btn.getAttribute('data-url');
    const form = document.getElementById('eventForm');
    form.reset();
    form.action = url;

    document.getElementById('eventModalTitle').textContent = "Create New Event";
    document.getElementById('eventSubmitBtn').textContent = "Create Event";
    document.getElementById('eventModal').style.display = 'flex';
}

function handleEditEvent(btn) {
    const id = btn.getAttribute('data-id');
    const title = btn.getAttribute('data-title');
    const typeId = btn.getAttribute('data-type-id');
    const venue = btn.getAttribute('data-venue');
    const start = btn.getAttribute('data-start'); // YYYY-MM-DD
    const end = btn.getAttribute('data-end');     // YYYY-MM-DD
    const desc = btn.getAttribute('data-desc');
    const editUrlBase = btn.getAttribute('data-edit-url-base'); // /department_admin/events/edit/

    document.getElementById('eventTitle').value = title;

    const typeSelect = document.getElementById('eventType');
    for (let i = 0; i < typeSelect.options.length; i++) {
        if (typeSelect.options[i].value === typeId) {
            typeSelect.selectedIndex = i;
            break;
        }
    }

    document.getElementById('eventVenue').value = venue;
    document.getElementById('eventStartDate').value = start;
    document.getElementById('eventEndDate').value = end;
    document.getElementById('eventDescription').value = desc;

    document.getElementById('eventModalTitle').textContent = "Edit Event";
    document.getElementById('eventSubmitBtn').textContent = "Update Event";

    // Set Action URL
    // Remove trailing slash if needed, append ID
    let finalUrl = editUrlBase;
    if (!finalUrl.endsWith('/')) finalUrl += '/';
    finalUrl += id + '/';

    document.getElementById('eventForm').action = finalUrl;
    document.getElementById('eventModal').style.display = 'flex';
}


/* ===========================
   SUB-EVENT: CREATE & EDIT
   =========================== */

function handlePrepareCreateSubEvent(btn) {
    const eventId = btn.getAttribute('data-event-id');
    const eventTitle = btn.getAttribute('data-event-title');
    const createUrl = btn.getAttribute('data-url');

    const form = document.getElementById('subEventForm');
    form.reset();
    form.action = createUrl;

    document.getElementById('parentEventId').value = eventId;
    document.getElementById('parentEventName').textContent = eventTitle;

    document.getElementById('subEventModalTitle').textContent = "Add Sub-Event";
    document.getElementById('subEventSubmitBtn').textContent = "Create Sub-Event";

    document.getElementById('minTeamSize').disabled = true;
    document.getElementById('maxTeamSize').disabled = true;

    document.getElementById('subEventModal').style.display = 'flex';
}

function handleEditSubEvent(btn) {
    const id = btn.getAttribute('data-id');
    const title = btn.getAttribute('data-title');
    const desc = btn.getAttribute('data-desc');
    const cost = btn.getAttribute('data-cost');
    const venue = btn.getAttribute('data-venue');
    const start = btn.getAttribute('data-start'); // YYYY-MM-DDTHH:mm
    const end = btn.getAttribute('data-end');
    const isTeam = btn.getAttribute('data-is-team');
    const min = btn.getAttribute('data-min');
    const max = btn.getAttribute('data-max');
    const eventTitle = btn.getAttribute('data-event-title');
    const editUrlBase = btn.getAttribute('data-edit-url-base'); // /sub-events/edit/

    const form = document.getElementById('subEventForm');

    document.getElementById('subEventTitle').value = title;
    document.getElementById('subEventDesc').value = desc;
    document.getElementById('subEventCost').value = (cost && cost !== 'None') ? cost : '';
    document.getElementById('subEventVenue').value = venue;
    document.getElementById('subEventStart').value = start;
    document.getElementById('subEventEnd').value = end;

    // Team Select Logic
    const teamSelect = document.getElementById('isTeamSelect');
    const minInput = document.getElementById('minTeamSize');
    const maxInput = document.getElementById('maxTeamSize');

    const isTeamBool = (isTeam === 'True' || isTeam === 'true' || isTeam === true);
    teamSelect.value = isTeamBool ? 'true' : 'false';

    if (isTeamBool) {
        minInput.disabled = false;
        maxInput.disabled = false;
        minInput.value = (min && min !== 'None') ? min : '';
        maxInput.value = (max && max !== 'None') ? max : '';
    } else {
        minInput.disabled = true;
        maxInput.disabled = true;
        minInput.value = '';
        maxInput.value = '';
    }

    document.getElementById('parentEventName').textContent = eventTitle;

    document.getElementById('subEventModalTitle').textContent = "Edit Sub-Event";
    document.getElementById('subEventSubmitBtn').textContent = "Update Sub-Event";

    let finalUrl = editUrlBase;
    if (!finalUrl.endsWith('/')) finalUrl += '/';
    finalUrl += id + '/';

    form.action = finalUrl;
    document.getElementById('subEventModal').style.display = 'flex';
}

/* ===========================
   TEAM SIZE LOGIC (Listener)
   =========================== */
// We need to attach this listener dynamically or checking if element exists
document.addEventListener('change', function (e) {
    if (e.target && e.target.id === 'isTeamSelect') {
        const teamSelect = e.target;
        const minInput = document.getElementById('minTeamSize');
        const maxInput = document.getElementById('maxTeamSize');

        if (teamSelect.value === 'true') {
            minInput.disabled = false;
            maxInput.disabled = false;
        } else {
            minInput.disabled = true;
            maxInput.disabled = true;
            minInput.value = '';
            maxInput.value = '';
        }
    }
});

/* ===========================
   CLOSE MODAL
   =========================== */
function closeModal(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) {
        modal.style.display = 'none';
    }
}
