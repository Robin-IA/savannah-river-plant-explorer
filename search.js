// Search on the home page: matching passages in the three chapters,
// matching timeline events, and a count of matching sources. Without this script
// the form goes to the sources page, which filters on the same words.
// Nothing here writes markup: results are built from text nodes.
(function () {
  "use strict";
  var form = document.querySelector("form.search");
  var input = document.getElementById("site-q");
  var panel = document.getElementById("results");
  if (!form || !input || !panel) return;
  var countEl = document.getElementById("results-count");
  var storyEl = document.getElementById("results-story");
  var timeEl = document.getElementById("results-time");
  var passages = null, sources = null, events = null;

  function load(url) {
    return fetch(url).then(function (r) { return r.ok ? r.json() : []; }).catch(function () { return []; });
  }
  var ready = Promise.all([load("data/passages.json"), load("data/sources.json"), load("data/timeline.json")]).then(function (d) {
    passages = d[0]; sources = d[1]; events = d[2];
  });

  function el(tag, text, cls) {
    var e = document.createElement(tag);
    if (text != null) e.textContent = text;
    if (cls) e.className = cls;
    return e;
  }

  // Append text to node with each word in <mark>.
  function marked(node, text, words) {
    var lower = text.toLowerCase(), i = 0;
    while (i < text.length) {
      var best = -1, len = 0;
      words.forEach(function (w) {
        var at = lower.indexOf(w, i);
        if (at >= 0 && (best < 0 || at < best)) { best = at; len = w.length; }
      });
      if (best < 0) { node.appendChild(document.createTextNode(text.slice(i))); break; }
      node.appendChild(document.createTextNode(text.slice(i, best)));
      node.appendChild(el("mark", text.slice(best, best + len)));
      i = best + len;
    }
  }

  function snippet(text, words) {
    var lower = text.toLowerCase(), at = lower.indexOf(words[0]);
    var start = Math.max(0, at - 90), end = Math.min(text.length, at + 160);
    return (start > 0 ? "…" : "") + text.slice(start, end).trim() + (end < text.length ? "…" : "");
  }

  function run(q) {
    var words = q.toLowerCase().split(/\s+/).filter(Boolean);
    storyEl.textContent = ""; timeEl.textContent = "";
    if (!words.length) { panel.hidden = true; return; }
    var hits = (passages || []).filter(function (p) {
      var t = p.t.toLowerCase();
      return words.every(function (w) { return t.indexOf(w) >= 0; });
    });
    hits.slice(0, 12).forEach(function (p) {
      var li = el("li"), a = el("a");
      a.href = p.p + "#" + p.id;
      a.appendChild(el("span", "Chapter " + p.c + " · " + p.s, "res-section"));
      var s = el("span", null, "res-text");
      marked(s, snippet(p.t, words), words);
      a.appendChild(s);
      li.appendChild(a);
      storyEl.appendChild(li);
    });
    if (hits.length > 12) storyEl.appendChild(el("li", "and " + (hits.length - 12) + " more passages", "res-more"));
    if (!hits.length) storyEl.appendChild(el("li", "No passages match.", "res-more"));

    var evs = (events || []).filter(function (e) {
      var t = (e.date + " " + e.text).toLowerCase();
      return words.every(function (w) { return t.indexOf(w) >= 0; });
    });
    evs.forEach(function (e) {
      var li = el("li"), a = el("a");
      a.href = "timeline.html#ev-" + e.i;
      a.appendChild(el("span", e.date, "res-section"));
      var s = el("span", null, "res-text");
      marked(s, e.text, words);
      a.appendChild(s);
      li.appendChild(a);
      timeEl.appendChild(li);
    });
    if (!evs.length) timeEl.appendChild(el("li", "No events match.", "res-more"));

    var nsrc = (sources || []).filter(function (s) {
      return words.every(function (w) { return s.search.indexOf(w) >= 0; });
    }).length;
    countEl.textContent = "";
    countEl.appendChild(document.createTextNode(
      hits.length + (hits.length === 1 ? " passage" : " passages") + " in the story, " +
      evs.length + (evs.length === 1 ? " event" : " events") + " on the timeline, and "));
    var a = el("a", nsrc + (nsrc === 1 ? " source" : " sources"));
    a.href = "sources.html?q=" + encodeURIComponent(q);
    countEl.appendChild(a);
    countEl.appendChild(document.createTextNode("."));
    panel.hidden = false;
  }

  function go(push) {
    var q = input.value.trim();
    ready.then(function () { run(q); });
    if (push) history.replaceState(null, "", q ? "?q=" + encodeURIComponent(q) : location.pathname + location.hash);
  }

  var timer;
  form.addEventListener("submit", function (e) {
    e.preventDefault();
    go(true);
    panel.scrollIntoView({ block: "start" });
  });
  input.addEventListener("input", function () {
    clearTimeout(timer);
    timer = setTimeout(function () { go(true); }, 200);
  });
  document.getElementById("results-close").addEventListener("click", function () {
    input.value = "";
    go(true);
    input.focus();
  });
  var start = new URLSearchParams(location.search).get("q");
  if (start) { input.value = start; go(false); }
})();
