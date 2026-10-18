// Minimal client-side filtering for the event tables. No dependencies.
(function () {
  "use strict";

  function norm(value) {
    return (value || "").toLowerCase().normalize("NFD").replace(/[\u0300-\u036f]/g, "");
  }

  function setup(tools) {
    var tableId = tools.getAttribute("data-table");
    var table = document.getElementById(tableId);
    if (!table) return;
    var input = tools.querySelector('input[type="search"]');
    var select = tools.querySelector("select");
    var result = tools.querySelector(".result");
    var rows = Array.prototype.slice.call(table.querySelectorAll("tbody tr"));
    var counter = table.querySelector("[data-row-count]");

    function apply() {
      var q = norm(input ? input.value.trim() : "");
      var choice = select ? norm(select.value) : "";
      var shown = 0;
      rows.forEach(function (row) {
        var hay = norm(row.getAttribute("data-search") || row.textContent);
        var bucket = norm(row.getAttribute("data-bucket") || "");
        var ok = (!q || hay.indexOf(q) !== -1) &&
                 (!choice || choice === "all" || bucket.indexOf(choice) !== -1);
        row.hidden = !ok;
        if (ok) shown += 1;
      });
      if (result) {
        result.textContent = shown + " of " + rows.length + " rows";
      }
      if (counter) counter.textContent = String(shown);
    }

    if (input) input.addEventListener("input", apply);
    if (select) select.addEventListener("change", apply);
    apply();
  }

  document.querySelectorAll(".table-tools[data-table]").forEach(setup);

  // Highlight the row targeted by a #row-... hash on flagged/cross-reference links.
  if (window.location.hash) {
    var target = document.getElementById(window.location.hash.slice(1));
    if (target && target.tagName === "TR") {
      target.style.background = "#fff8e6";
    }
  }
})();
