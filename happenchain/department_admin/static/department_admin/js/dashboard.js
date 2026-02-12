document.addEventListener("DOMContentLoaded", () => {

    if (document.getElementById("eventsContainer")) {
        renderEvents();
    }

    if (document.getElementById("registrationTableBody")) {
        renderRegistrations();
    }

});


function formatTeamMembers(members) {
    if (!members || members.length === 0) {
        return "<div style='padding:12px;'>No team members found.</div>";
    }

    let html = "<div style='padding:12px 20px;'>";
    html += "<strong>Team Members</strong><ul style='margin-top:8px;'>";

    members.forEach(m => {
        html += `
            <li>
                ${m.name}
                <small style="color:#94A3B8;">
                    ${m.email} • ${m.role} • ${m.college}
                </small>
            </li>`;
    });

    html += "</ul></div>";
    return html;
}

$(document).ready(function () {
    const table = $('#registrationTable').DataTable({
        pagingType: 'simple_numbers',
        pageLength: 8,
        lengthChange: false,
        autoWidth: false,
        columnDefs: [
            { targets: -1, visible: false } // hide members column
        ],
        dom:
            "<'dt-top'f>" +
            "<'dt-table'tr>" +
            "<'dt-bottom'<'dt-info'i><'dt-pagination'p>>"
    });

    $('#registrationTable tbody').on('click', 'tr', function () {
        const row = table.row(this);
        const rowData = row.data();

        if (!rowData) return;

        // 👇 LAST COLUMN = members JSON
        const membersJson = rowData[rowData.length - 1];

        let members;
        try {
            members = JSON.parse(membersJson);
        } catch (e) {
            // Not a team row or empty
            return;
        }

        if (row.child.isShown()) {
            row.child.hide();
            $(this).removeClass('shown');
        } else {
            row.child(formatTeamMembers(members)).show();
            $(this).addClass('shown');
        }
    });
});


