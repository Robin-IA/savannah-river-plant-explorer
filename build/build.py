#!/usr/bin/env python3
"""Build the explorer's pages from the Markdown in content/.

    python3 build/build.py

Reads content/story.md and content/sources-act{1,2,3}.md and writes
index.html (the story), sources.html (every source, filterable) and
data/sources.json. about.html is written by hand and not touched.

Needs the `markdown` package (pip install markdown).
"""

import html
import json
import pathlib
import re

import markdown

ROOT = pathlib.Path(__file__).resolve().parent.parent
CONTENT = ROOT / "content"

TITLE = "Bomb Making: A History of the Savannah River Plant"
DESCRIPTION = ("The Savannah River Plant in South Carolina made plutonium and "
               "tritium for American nuclear weapons from 1953 until 1988. This "
               "is its history, from the towns moved off the land to the "
               "clean-up, told from records held in Democracy's Library, the "
               "wider Internet Archive, the Wayback Machine and elsewhere.")
CHECKED = "6 November 2026"
FEEDBACK = ("mailto:robin.fay@archive.org?subject=Feedback%20about%20Explorers"
            "%3A%20Bomb%20Making%3A%20A%20History%20of%20the%20Savannah%20River"
            "%20Plant")

TAGS = {
    "DL": "Democracy's Library",
    "IA": "Internet Archive",
    "WB": "Wayback Machine",
    "AIT": "Archive-It",
    "EXT": "Held elsewhere",
}
ACTS = {
    1: "Act 1. Building the bomb plant, 1950–1969",
    2: "Act 2. The reactors under scrutiny, 1970–1992",
    3: "Act 3. After the bombs, 1992 to now",
}
TAG_RE = re.compile(r"^(DL|IA|WB|AIT|EXT)\b\s*:?\s*(.*)$", re.S)


def md_inline(text):
    """Render one line of Markdown without the wrapping <p>."""
    out = markdown.markdown(text.strip())
    return re.sub(r"^<p>(.*)</p>$", r"\1", out, flags=re.S)


def split_label(raw):
    """'IA (lending)' -> ('IA', '(lending)'); 'EXT:OSTI' -> ('EXT', 'OSTI')."""
    m = TAG_RE.match(raw.strip().rstrip(":").strip())
    if not m:
        return None, None
    return m.group(1), m.group(2).strip().strip("()").strip()


def first_link(text):
    """The source's own address: a URL, else the first archive.org id."""
    url = re.search(r"https?://[^\s)`|>\]]+", text)
    ident = re.search(r"`([A-Za-z0-9][\w.\-]+)`", text)
    if ident and (not url or text.find("`") < text.find(url.group(0))):
        return "https://archive.org/details/" + ident.group(1), ident.group(1)
    ol = re.search(r"\b(OL\d+[WM])\b", text)
    if not url and ol:
        kind = "works" if ol.group(1).endswith("W") else "books"
        return "https://openlibrary.org/%s/%s" % (kind, ol.group(1)), "Open Library " + ol.group(1)
    if url:
        u = url.group(0).rstrip(".,;")
        return u, u
    return None, None


# --------------------------------------------------------------------------
# The three source files use three layouts: a table (act 1), one bullet per
# source (act 2), and a numbered item with sub-bullets (act 3).

def sources(path, act):
    out, section = [], None
    lines = path.read_text(encoding="utf-8").splitlines()
    i = 0
    while i < len(lines):
        line = lines[i]
        h = re.match(r"^## (\d+)\.\s+(.*)", line)
        if h:
            section = h.group(2).strip()
        elif line.startswith("## "):
            section = None
        if section is None:
            i += 1
            continue

        entry = None
        if line.startswith("|") and not re.match(r"^\|\s*(Label|-)", line):
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            tag, qual = split_label(cells[0])
            if tag and len(cells) >= 6:
                href, ident = first_link(cells[1])
                body = "<strong>%s</strong>" % md_inline(cells[2])
                if cells[3]:
                    body += " · " + html.escape(cells[3])
                if cells[4]:
                    body += " · " + md_inline(cells[4])
                body += "<br>" + md_inline(cells[5])
                entry = dict(tag=tag, qual=qual, href=href, ident=ident,
                             body=body, text=" ".join(cells[1:]))
        else:
            b = re.match(r"^- \*\*([^*]+)\*\*:?\s*(.*)", line)
            n = re.match(r"^\d+\.\s+\*\*([^*]+)\*\*:?\s*(.*)", line)
            m = b or n
            if m:
                tag, qual = split_label(m.group(1))
                if tag:
                    head = m.group(2)
                    subs = []
                    while i + 1 < len(lines) and re.match(r"^\s+\S", lines[i + 1]):
                        i += 1
                        s = lines[i].strip()
                        if s.startswith("- "):
                            subs.append(s[2:])
                        elif subs:
                            subs[-1] += " " + s
                        else:
                            head += " " + s
                    href, ident = first_link(head + " " + " ".join(subs))
                    bare = re.fullmatch(r"\s*(https?://\S+|`[^`]+`)\s*", head)
                    body = md_inline(head) if head and not bare else ""
                    if subs:
                        body += "<ul>%s</ul>" % "".join(
                            "<li>%s</li>" % md_inline(s) for s in subs)
                    entry = dict(tag=tag, qual=qual, href=href, ident=ident,
                                 body=body, text=head + " " + " ".join(subs))
        if entry:
            entry["act"] = act
            entry["section"] = section
            text = re.sub(r"[`*_\[\]]", "", entry.pop("text"))
            entry["search"] = re.sub(r"\s+", " ", text).lower()
            out.append(entry)
        i += 1
    return out


# --------------------------------------------------------------------------
# Page furniture shared by all three pages.

def head(title, here):
    nav = []
    for href, label in (("index.html", "Story"), ("sources.html", "Sources"),
                        ("about.html", "About")):
        cur = ' aria-current="page"' if href == here else ""
        nav.append('<a href="%s"%s>%s</a>' % (href, cur, label))
    return """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>%s</title>
<meta name="description" content="%s">
<link rel="stylesheet" href="style.css">
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<header class="bar">
  <div class="wrap">
    <a class="logo" href="https://archive.org/"><img src="img/internet-archive.png" alt="Internet Archive" width="36" height="36"></a>
    <a class="logo dl" href="https://archive.org/details/democracys-library"><img src="img/democracys-library.png" alt="Democracy's Library" width="36" height="36"></a>
    <nav aria-label="Pages">%s</nav>
  </div>
</header>
""" % (html.escape(title), html.escape(DESCRIPTION, quote=True), "".join(nav))


def foot():
    return """<footer class="foot">
  <div class="wrap">
    <p>Sources checked live on %s. Code and source notes on
      <a href="https://github.com/Robin-IA/savannah-river-plant-explorer">GitHub</a>.</p>
    <p>Feedback? <a href="%s">Email us</a></p>
  </div>
</footer>
</body>
</html>
""" % (CHECKED, FEEDBACK)


def legend():
    rows = "".join('<li><span class="tag tag-%s">%s</span> %s</li>'
                   % (t.lower(), t, html.escape(n)) for t, n in TAGS.items())
    return '<ul class="legend" aria-label="Where each source is held">%s</ul>' % rows


# --------------------------------------------------------------------------

def tag_links(body):
    """Give every story citation a visible holder tag."""
    def repl(m):
        attrs, tag, rest = m.group(1), m.group(2), m.group(3)
        return ('<a%s class="cite"><span class="tag tag-%s">%s</span>%s</a>'
                % (attrs, tag.lower(), tag, rest))
    return re.sub(r"<a([^>]*)>(DL|IA|WB|AIT|EXT)\b(.*?)</a>", repl, body, flags=re.S)


def build_story():
    text = (CONTENT / "story.md").read_text(encoding="utf-8")
    # The title and the "how to read" section become the page's own header.
    text = re.sub(r"\A# .*?\n", "", text)
    text = re.sub(r"## How to read the sources.*?\n---\n", "", text, flags=re.S)
    text = re.sub(r"\[(sources-act\d\.md)\]\(\1\)", "[the source lists](sources.html)", text)
    md = markdown.Markdown(extensions=["tables", "toc"],
                           extension_configs={"toc": {"toc_depth": "2-2"}})
    body = tag_links(md.convert(text))
    body = body.replace("<table>", '<div class="scroll"><table>').replace("</table>", "</table></div>")
    toc = md.toc  # <div class="toc"><ul>…</ul></div>
    toc = toc.replace('<div class="toc">', '<nav class="toc" aria-label="Contents"><h2>Contents</h2>').replace("</div>", "</nav>")
    page = head(TITLE, "index.html") + """<main id="main" class="wrap story">
<div class="intro">
  <h1>%s</h1>
  <p class="lede">%s</p>
  <p>Every claim carries a tag saying where its source is held. Click a tag to open the source.</p>
  %s
</div>
<div class="cols">
%s
<article>
%s
</article>
</div>
</main>
""" % (html.escape(TITLE), html.escape(DESCRIPTION), legend(), toc, body) + foot()
    (ROOT / "index.html").write_text(page, encoding="utf-8")


def build_sources(items):
    counts = {t: sum(1 for s in items if s["tag"] == t) for t in TAGS}
    rows = []
    for s in items:
        link = ('<a href="%s">%s</a>' % (html.escape(s["href"], quote=True),
                                         html.escape(s["ident"]))
                if s["href"] else "")
        qual = ('<span class="qual">%s</span>' % md_inline(s["qual"])) if s["qual"] else ""
        rows.append(
            '<tr data-tag="%s" data-act="%d"><td><span class="tag tag-%s">%s</span>%s</td>'
            '<td><div class="src">%s</div><div class="note">%s</div></td>'
            '<td class="where">Act %d<br><span>%s</span></td></tr>'
            % (s["tag"], s["act"], s["tag"].lower(), s["tag"], qual, link, s["body"], s["act"],
               html.escape(s["section"])))
    tagbtns = "".join(
        '<label><input type="checkbox" name="tag" value="%s" checked> '
        '<span class="tag tag-%s">%s</span> %s <span class="n">(%d)</span></label>'
        % (t, t.lower(), t, html.escape(TAGS[t]), counts[t]) for t in TAGS)
    actopts = "".join('<option value="%d">%s</option>' % (a, html.escape(l))
                      for a, l in ACTS.items())
    page = head("Sources · " + TITLE, "sources.html") + """<main id="main" class="wrap">
<div class="intro">
  <h1>Sources</h1>
  <p class="lede">All %d sources behind <a href="index.html">the story</a>, with where each is held and what it contributes. Checked live on %s, except where a note says otherwise.</p>
</div>
<form class="filters" role="search" aria-label="Filter sources" onsubmit="return false">
  <fieldset><legend>Held in</legend>%s</fieldset>
  <div class="row">
    <label for="act">Act</label>
    <select id="act" name="act"><option value="">All acts</option>%s</select>
    <label for="q">Search</label>
    <input id="q" name="q" type="search" placeholder="Ellenton, tritium, DWPF…">
  </div>
</form>
<p id="count" class="count" role="status" aria-live="polite">%d sources</p>
<div class="scroll">
<table class="sources">
<caption class="sr">Sources, with where each is held, what it is, and the act and theme it belongs to</caption>
<thead><tr><th scope="col">Held in</th><th scope="col">Source</th><th scope="col">Act and theme</th></tr></thead>
<tbody>
%s
</tbody>
</table>
</div>
</main>
<script src="app.js"></script>
""" % (len(items), CHECKED, tagbtns, actopts, len(items), "\n".join(rows)) + foot()
    (ROOT / "sources.html").write_text(page, encoding="utf-8")


def main():
    items = []
    for act in (1, 2, 3):
        items += sources(CONTENT / ("sources-act%d.md" % act), act)
    data = [{k: s[k] for k in ("act", "section", "tag", "qual", "ident", "href")}
            for s in items]
    (ROOT / "data").mkdir(exist_ok=True)
    (ROOT / "data" / "sources.json").write_text(
        json.dumps(data, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    build_story()
    build_sources(items)
    by = {}
    for s in items:
        by.setdefault((s["act"], s["tag"]), 0)
        by[(s["act"], s["tag"])] += 1
    print(len(items), "sources")
    for act in (1, 2, 3):
        print("  act", act, {t: by.get((act, t), 0) for t in TAGS})
    missing = [s for s in items if not s["href"]]
    print(len(missing), "without a link")
    for s in missing:
        print("   ", s["act"], s["tag"], s["search"][:90])


if __name__ == "__main__":
    main()
