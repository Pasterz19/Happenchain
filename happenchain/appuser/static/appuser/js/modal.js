function openRegisterModal(subEventId, isTeam) {
    document.getElementById("subEventInput").value = subEventId;

    const teamSection = document.getElementById("teamSection");
    const teamNameInput = document.getElementById("teamNameInput");

    if (isTeam) {
        teamSection.style.display = "block";
        teamNameInput.required = true;   // ✅ REQUIRED ONLY FOR TEAM
    } else {
        teamSection.style.display = "none";
        teamNameInput.required = false;  // ✅ NOT REQUIRED FOR INDIVIDUAL
        teamNameInput.value = "";        // optional cleanup
    }

    document.getElementById("registerModal").style.display = "flex";
}


function closeRegisterModal() {
    document.getElementById("registerModal").style.display = "none";
}
