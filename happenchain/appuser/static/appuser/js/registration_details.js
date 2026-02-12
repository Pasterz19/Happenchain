document.addEventListener('DOMContentLoaded', function () {
    const modal = document.getElementById("regDetailsModal");
    const closeBtn = document.querySelector(".close-modal");

    if (!modal) return;

    // Open Modal
    document.querySelectorAll('.details-btn').forEach(btn => {
        btn.addEventListener('click', function () {
            document.getElementById('modalEvent').textContent = this.dataset.event;
            document.getElementById('modalSubEvent').textContent = this.dataset.subevent;
            document.getElementById('modalVenue').textContent = this.dataset.venue;
            document.getElementById('modalDate').textContent = this.dataset.date;
            document.getElementById('modalTeam').textContent = this.dataset.team;
            document.getElementById('modalAmount').textContent = '₹' + this.dataset.amount;
            document.getElementById('modalStatus').textContent = this.dataset.status;
            document.getElementById('modalTxnId').textContent = this.dataset.txnid;

            modal.style.display = "block";
        });
    });

    // Close Modal
    if (closeBtn) {
        closeBtn.onclick = function () {
            modal.style.display = "none";
        }
    }

    // Outside Click
    window.onclick = function (event) {
        if (event.target == modal) {
            modal.style.display = "none";
        }
    }
});
