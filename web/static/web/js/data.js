document.addEventListener("DOMContentLoaded", () => {
    $("table").first()
        .addClass("table table-striped table-bordered")
        .removeClass("dataframe")
        .attr("border", "0")
        .attr("cellspacing", "0")
        .attr("width", "100%");
    $("tr").first().css("text-align", "center");
    $("th").each(function(i, v) {
        $(this).addClass("th-sm");
    });
    $("tbody").each(function(i, v) {
        $(this).find("td").first().attr("scope", "row");
    });
    $("table.table").DataTable();
    $(".dataTables_length").addClass("bs-select");
});
