// Filters the sources table. The table is complete without this script;
// it only hides rows. The URL carries the state: ?tag=DL,WB&act=2&q=tritium
(function () {
  "use strict";
  var form = document.querySelector(".filters");
  if (!form) return;
  var rows = Array.prototype.slice.call(document.querySelectorAll("table.sources tbody tr"));
  var boxes = Array.prototype.slice.call(form.querySelectorAll('input[name="tag"]'));
  var act = form.querySelector("#act");
  var q = form.querySelector("#q");
  var count = document.getElementById("count");
  var text = rows.map(function (r) { return r.textContent.toLowerCase(); });

  function read() {
    var p = new URLSearchParams(location.search);
    if (p.has("tag")) {
      var want = p.get("tag").split(",");
      boxes.forEach(function (b) { b.checked = want.indexOf(b.value) >= 0; });
    }
    act.value = p.get("act") || "";
    q.value = p.get("q") || "";
  }

  function apply(push) {
    var tags = boxes.filter(function (b) { return b.checked; }).map(function (b) { return b.value; });
    var words = q.value.toLowerCase().split(/\s+/).filter(Boolean);
    var shown = 0;
    rows.forEach(function (r, i) {
      var ok = tags.indexOf(r.dataset.tag) >= 0 &&
        (!act.value || r.dataset.act === act.value) &&
        words.every(function (w) { return text[i].indexOf(w) >= 0; });
      r.hidden = !ok;
      if (ok) shown++;
    });
    count.textContent = shown === rows.length ? rows.length + " sources"
      : shown + " of " + rows.length + " sources";
    if (push) {
      var p = new URLSearchParams();
      if (tags.length < boxes.length) p.set("tag", tags.join(","));
      if (act.value) p.set("act", act.value);
      if (q.value) p.set("q", q.value);
      var s = p.toString();
      history.replaceState(null, "", s ? "?" + s : location.pathname);
    }
  }

  read();
  apply(false);
  form.addEventListener("input", function () { apply(true); });
  form.addEventListener("change", function () { apply(true); });
})();
