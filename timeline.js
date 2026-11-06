// Timeline: a tooltip on hover or focus, and filters by where the source
// is held. The chart and the list are complete without this script.
(function () {
  "use strict";
  var tip = document.getElementById("tl-tip");
  var fig = document.querySelector(".tl-figure");
  var marks = Array.prototype.slice.call(document.querySelectorAll("svg.timeline a.ev"));
  var items = Array.prototype.slice.call(document.querySelectorAll(".tl-list li"));
  var buttons = Array.prototype.slice.call(document.querySelectorAll(".tl-filter"));
  if (!tip || !fig) return;

  function show(a) {
    var label = a.getAttribute("aria-label") || "";
    var cut = label.indexOf(": ");
    tip.textContent = "";
    var d = document.createElement("strong");
    d.textContent = label.slice(0, cut);
    var t = document.createElement("span");
    t.textContent = label.slice(cut + 2);
    tip.appendChild(d);
    tip.appendChild(t);
    tip.hidden = false;
    var r = a.getBoundingClientRect(), f = fig.getBoundingClientRect();
    var x = r.left - f.left + r.width / 2, y = r.top - f.top;
    var w = tip.offsetWidth;
    tip.style.setProperty("left", Math.max(4, Math.min(f.width - w - 4, x - w / 2)) + "px");
    tip.style.setProperty("top", Math.max(0, y - tip.offsetHeight - 10) + "px");
  }
  function hide() { tip.hidden = true; }
  marks.forEach(function (a) {
    a.addEventListener("mouseenter", function () { show(a); });
    a.addEventListener("focus", function () { show(a); });
    a.addEventListener("mouseleave", hide);
    a.addEventListener("blur", hide);
  });
  document.addEventListener("keydown", function (e) { if (e.key === "Escape") hide(); });

  function apply() {
    var on = buttons.filter(function (b) { return b.getAttribute("aria-pressed") === "true"; })
      .map(function (b) { return b.dataset.tag; });
    marks.forEach(function (a) {
      var off = on.indexOf(a.dataset.tag) < 0;
      a.classList.toggle("off", off);
      if (off) a.setAttribute("tabindex", "-1"); else a.removeAttribute("tabindex");
    });
    items.forEach(function (li) { li.hidden = on.indexOf(li.dataset.tag) < 0; });
  }
  buttons.forEach(function (b) {
    b.addEventListener("click", function () {
      b.setAttribute("aria-pressed", b.getAttribute("aria-pressed") === "true" ? "false" : "true");
      apply();
    });
  });
})();
