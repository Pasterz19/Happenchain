$(document).ready(function () {
    const tableSelector = '#studentTable';

    // Check if table exists and is not already a DataTable
    if ($(tableSelector).length && !$.fn.DataTable.isDataTable(tableSelector)) {
        $(tableSelector).DataTable({
            pagingType: 'simple_numbers',
            pageLength: 8,
            lengthChange: false,
            autoWidth: false,
            // Custom DOM layout to match theme structure
            dom:
                "<'dt-top'f>" +
                "<'dt-table'tr>" +
                "<'dt-bottom'<'dt-info'i><'dt-pagination'p>>",
            language: {
                search: "_INPUT_",
                searchPlaceholder: "Search students...",
                emptyTable: "No student registrations found",
                zeroRecords: "No matching students found"
            },
            columnDefs: [
                { orderable: false, targets: [5, 7] } // Disable sorting for Photo and Action columns
            ]
        });
    }
});
