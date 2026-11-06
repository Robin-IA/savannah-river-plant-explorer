#!/usr/bin/env python3
"""Build the explorer's pages from the Markdown in content/.

    python3 build/build.py

Reads content/ (story.md, sources-act{1,2,3}.md, timeline.json,
about.md, disagree.md) and writes index.html (the story), timeline.html,
sources.html, about.html, data/sources.json and data/timeline.json.

Needs the `markdown` package (pip install markdown).
"""

import html
import json
import pathlib
import re

import markdown
import markdown.extensions.toc

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

CSP = ("default-src 'self'; script-src 'self'; style-src 'self'; "
       "img-src 'self'; object-src 'none'; base-uri 'none'; form-action 'self'")

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
# Page furniture shared by every page.

PAGES = (("index.html", "Story"), ("timeline.html", "Timeline"),
         ("sources.html", "Sources"), ("about.html", "About"))
ACT_SPANS = ((1, 1950, 1970, "Building the bomb plant"),
             (2, 1970, 1992.5, "The reactors under scrutiny"),
             (3, 1992.5, 2027, "After the bombs"))


def banner_art():
    """The banner's picture: dusk over a pine horizon, five reactor
    buildings, and the river in front. Decorative, drawn here."""
    trees = []
    x = -10
    k = 0
    while x < 1620:
        h = 26 + (k * 37 % 23)
        w = 14 + (k * 13 % 9)
        trees.append("M%d %d L%d %d L%d %d Z" % (x, 268, x + w / 2, 268 - h, x + w, 268))
        x += w * 0.62
        k += 1
    reactors = []
    for i, (x, w, h) in enumerate(((1010, 70, 58), (1100, 84, 66), (1205, 76, 60),
                                    (1300, 90, 70), (1410, 72, 56))):
        top = 262 - h
        reactors.append('<rect x="%d" y="%d" width="%d" height="%d"/>' % (x, top, w, h))
        reactors.append('<rect x="%d" y="%d" width="%d" height="%d"/>' % (x + w * 0.6, top - 34 - i % 2 * 10, 9, 36 + i % 2 * 10))
    return """<svg class="banner-art" viewBox="0 0 1600 360" preserveAspectRatio="xMidYMax slice" aria-hidden="true" focusable="false">
  <defs>
    <linearGradient id="sky" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#0c1f2e"/><stop offset=".55" stop-color="#1d4a5c"/><stop offset=".9" stop-color="#c98a4b"/>
    </linearGradient>
    <linearGradient id="river" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="#2f6577"/><stop offset=".6" stop-color="#8fb9c2"/><stop offset="1" stop-color="#d9a466"/>
    </linearGradient>
    <linearGradient id="veil" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="#0c1f2e" stop-opacity=".92"/><stop offset=".55" stop-color="#0c1f2e" stop-opacity=".8"/><stop offset="1" stop-color="#0c1f2e" stop-opacity="0"/>
    </linearGradient>
  </defs>
  <rect width="1600" height="360" fill="url(#sky)"/>
  <circle cx="1250" cy="236" r="70" fill="#f1c27d" opacity=".35"/>
  <circle cx="1250" cy="236" r="34" fill="#f6d39a" opacity=".8"/>
  <path d="M0 250 Q300 225 600 246 T1200 238 T1600 244 V360 H0 Z" fill="#183a49"/>
  <g fill="#0f2633">%s<rect x="1525" y="196" width="10" height="66"/><circle cx="1530" cy="190" r="16"/></g>
  <path d="%s" fill="#0a1a24"/>
  <rect y="266" width="1600" height="94" fill="#0a1a24"/>
  <path d="M0 312 C260 280 420 334 700 300 S1180 284 1600 300 V330 C1200 318 900 346 640 330 S240 318 0 340 Z" fill="url(#river)" opacity=".85"/>
  <rect width="1600" height="360" fill="url(#veil)"/>
</svg>""" % ("".join(reactors), " ".join(trees))


def logos():
    return """<div class="banner-logos">
      <a class="logo-ia" href="https://archive.org/"><img src="img/internet-archive.png" alt="Internet Archive" width="56" height="56"></a>
      <a class="logo-dl" href="https://archive.org/details/democracys-library"><img src="img/democracys-library.png" alt="Democracy's Library" width="56" height="56"></a>
      <span class="banner-kicker">A Democracy's Library story from the Internet Archive</span>
    </div>"""


def head(title, here, h1, lede, extra="", big=False):
    nav = []
    for href, label in PAGES:
        cur = ' aria-current="page"' if href == here else ""
        nav.append('<a href="%s"%s>%s</a>' % (href, cur, label))
    return """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta http-equiv="Content-Security-Policy" content="%s">
<title>%s</title>
<meta name="description" content="%s">
<link rel="stylesheet" href="style.css">
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<header class="site">
<div class="bar">
  <div class="wrap">
    <a class="home" href="index.html">Bomb Making</a>
    <nav aria-label="Pages">%s</nav>
  </div>
</div>
<div class="banner%s">
  %s
  <div class="wrap banner-inner">
    %s
    <h1>%s</h1>
    <p class="lede">%s</p>
    %s
  </div>
</div>
</header>
""" % (CSP, html.escape(title), html.escape(DESCRIPTION, quote=True), "".join(nav),
       " big" if big else "", banner_art(), logos(), html.escape(h1), lede, extra)


# The explorer-checks passing note. The pages are generated, so the note
# lives here, not in the pages: when a later run of the checker re-dates it
# or takes it down, make the same change here.
CHECKS_NOTE = """<!-- explorer-checks:note -->
<p class="explorer-checks-note">
  Meets WCAG 2.2 Level AA accessibility (and WCAG 2.1 AA and 2.0 AA), checked
  <time datetime="2026-11-06">6 November 2026</time> by automated tests and manual review.
  Also passes security and code validity checks.
  <a href="https://github.com/Robin-IA/savannah-river-plant-explorer/blob/main/security-accessibility-checks.md">Read the report</a>.
</p>
<!-- /explorer-checks:note -->"""


def foot(scripts=()):
    tags = "".join('<script src="%s"></script>\n' % s for s in scripts)
    return """<footer class="foot">
  <div class="wrap">
    <p>Sources checked live on %s. Code and source notes on
      <a href="https://github.com/Robin-IA/savannah-river-plant-explorer">GitHub</a>.</p>
    <p>Feedback? <a href="%s">Email us</a></p>
    %s
  </div>
</footer>
%s</body>
</html>
""" % (CHECKED, FEEDBACK, CHECKS_NOTE, tags)


def legend(cls="legend"):
    rows = "".join('<li><span class="tag tag-%s">%s</span> %s</li>'
                   % (t.lower(), t, html.escape(n)) for t, n in TAGS.items())
    return '<ul class="%s" aria-label="Where each source is held">%s</ul>' % (cls, rows)


def holder_chart(items):
    """Stacked bars, one per act: how many sources each holder supplies."""
    rows, table = [], []
    w, x0, bar = 300, 0, 18
    for n, act in enumerate((1, 2, 3)):
        mine = [s for s in items if s["act"] == act]
        total = len(mine)
        y = n * 52 + 22
        rows.append('<text class="ch-label" x="0" y="%d">Act %d · %d sources</text>' % (y - 6, act, total))
        x = x0
        cells = []
        for t in TAGS:
            c = sum(1 for s in mine if s["tag"] == t)
            cells.append(str(c))
            if not c:
                continue
            seg = w * c / total
            rows.append('<rect class="seg seg-%s" x="%.1f" y="%d" width="%.1f" height="%d" rx="3"><title>Act %d: %d %s</title></rect>'
                        % (t.lower(), x, y, max(seg - 2, 1), bar, act, c, html.escape(TAGS[t])))
            if seg >= 24:
                rows.append('<text class="seg-n seg-n-%s" x="%.1f" y="%d">%d</text>' % (t.lower(), x + seg / 2 - 1, y + 13, c))
            x += seg
        table.append("<tr><th scope=\"row\">Act %d</th>%s<td>%d</td></tr>" % (act, "".join("<td>%s</td>" % c for c in cells), total))
    svg = ('<svg class="holder-chart" viewBox="0 0 %d 158" role="img" aria-labelledby="hc-t">'
           '<title id="hc-t">Sources by where they are held, for each act</title>%s</svg>' % (w, "".join(rows)))
    tbl = ('<div class="sr"><table><caption>Sources by holder and act</caption><tr><th scope="col">Act</th>%s<th scope="col">Total</th></tr>%s</table></div>'
           % ("".join('<th scope="col">%s</th>' % html.escape(TAGS[t]) for t in TAGS), "".join(table)))
    return svg + tbl


# --------------------------------------------------------------------------

def tag_links(body):
    """Give every story citation a visible holder tag."""
    def repl(m):
        attrs, tag, rest = m.group(1), m.group(2), m.group(3)
        return ('<a%s class="cite"><span class="tag tag-%s">%s</span>%s</a>'
                % (attrs, tag.lower(), tag, rest))
    return re.sub(r"<a([^>]*)>(DL|IA|WB|AIT|EXT)\b(.*?)</a>", repl, body, flags=re.S)


def story_refs():
    text = (CONTENT / "story.md").read_text(encoding="utf-8")
    return dict(re.findall(r"^\[([\w-]+)\]:\s*(\S+)", text, re.M))


SEARCH_FORM = """<form class="search" action="sources.html" method="get" role="search" aria-label="Search the story and its sources">
      <label for="site-q">Search the story, the timeline and %d sources</label>
      <div class="search-row">
        <input id="site-q" name="q" type="search" placeholder="Ellenton, tritium, glass, MOX…" autocomplete="off">
        <button type="submit">Search</button>
      </div>
    </form>"""


def build_story(items):
    text = (CONTENT / "story.md").read_text(encoding="utf-8")
    text = re.sub(r"\A# .*?\n", "", text)
    text = re.sub(r"## How to read the sources.*?\n---\n", "", text, flags=re.S)
    text = re.sub(r"\A\s*\*A draft.*?\*\n", "", text, flags=re.S)
    md = markdown.Markdown(extensions=["tables", "toc"],
                           extension_configs={"toc": {"toc_depth": "2-3"}})
    body = tag_links(md.convert(text))
    body = re.sub(r'<h2 id="(act-(\d)[^"]*)">Act \d\. (.*?)</h2>',
                  r'<h2 id="\1" class="act act-\2"><span class="act-n">Act \2</span> \3</h2>', body)
    body = re.sub(r"<hr />\s*", "", body)
    n = [0]

    def pid(m):
        n[0] += 1
        return '<%s id="s%d">' % (m.group(1), n[0])
    body = re.sub(r"<(p|li)>", pid, body)
    toc = md.toc.replace('<div class="toc">', '<nav class="toc" aria-label="Contents"><h2>Contents</h2>').replace("</div>", "</nav>")
    lede = html.escape(DESCRIPTION)
    page = head(TITLE, "index.html", TITLE, lede, SEARCH_FORM % len(items), big=True) + """<section id="results" class="wrap results" aria-labelledby="results-h" hidden>
  <div class="results-head"><h2 id="results-h">Search results</h2><button type="button" id="results-close">Clear search</button></div>
  <p id="results-count" role="status" aria-live="polite"></p>
  <div class="results-cols">
    <section aria-labelledby="rs-story"><h3 id="rs-story">In the story</h3><ol id="results-story"></ol></section>
    <section aria-labelledby="rs-time"><h3 id="rs-time">On the timeline</h3><ol id="results-time"></ol></section>
  </div>
</section>
<main id="main" class="wrap story">
<div class="cols">
%s
<article>
%s
</article>
<aside class="rail" aria-label="Where the record lives">
  <h2>Where the record lives</h2>
  <p>Each claim is tagged with where its source is held.</p>
  %s
  %s
  <a class="card" href="timeline.html"><strong>Timeline</strong><span>Seventy-six years in one view: the reactors, the people moved, the oversight and the cleanup.</span></a>
  <a class="card" href="sources.html"><strong>All %d sources</strong><span>Filter by holder, act and word.</span></a>
</aside>
</div>
</main>
""" % (toc, body, legend("legend stacked"), holder_chart(items), len(items)) + foot(["search.js"])
    write(ROOT / "index.html", page)


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
    actopts = "".join('<option value="%d">%s</option>' % (a, html.escape(name))
                      for a, name in ACTS.items())
    lede = ('All %d sources behind <a href="index.html">the story</a>, with where each is held and what it contributes. '
            'Checked live on %s, except where a note says otherwise.' % (len(items), CHECKED))
    page = head("Sources · " + TITLE, "sources.html", "Sources", lede) + """<main id="main" class="wrap">
<div class="sources-top">
<form class="filters" role="search" aria-label="Filter sources">
  <fieldset><legend>Held in</legend>%s</fieldset>
  <div class="row">
    <label for="act">Act</label>
    <select id="act" name="act"><option value="">All acts</option>%s</select>
    <label for="q">Search</label>
    <input id="q" name="q" type="search" placeholder="Ellenton, tritium, DWPF…">
  </div>
</form>
<div class="chart-box">%s</div>
</div>
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
""" % (tagbtns, actopts, holder_chart(items), len(items), "\n".join(rows)) + foot(["app.js"])
    write(ROOT / "sources.html", page)


def build_about():
    body = markdown.markdown((CONTENT / "about.md").read_text(encoding="utf-8"))
    disagree = markdown.markdown((CONTENT / "disagree.md").read_text(encoding="utf-8"))
    body = body.replace("<!-- DISAGREE -->", disagree.replace("<ul>", '<ul class="disagree">'))
    lede = ("A history of the Savannah River Plant told from the record, with every source "
            "labelled by where it is held, so a reader can open it and check.")
    page = head("About · " + TITLE, "about.html", "About this explorer", lede) + \
        '<main id="main" class="wrap about">\n%s\n</main>\n' % body + foot()
    write(ROOT / "about.html", page)


# --------------------------------------------------------------------------
# The timeline: reactor spans and events, drawn as an SVG at build time,
# with the same events as a list underneath for reading and for screens
# too narrow for the chart.

TL_X0, TL_X1, TL_Y0, TL_Y1 = 190, 1180, 1950, 2027
SHAPES = {
    "DL": '<circle r="7"/>',
    "IA": '<rect x="-6.5" y="-6.5" width="13" height="13" rx="2"/>',
    "WB": '<path d="M0 -8.5 L8.5 0 L0 8.5 L-8.5 0 Z"/>',
    "AIT": '<path d="M0 -8 L8 6.5 L-8 6.5 Z"/>',
    "EXT": '<circle r="5.5"/>',
}


def tx(year):
    return TL_X0 + (year - TL_Y0) / (TL_Y1 - TL_Y0) * (TL_X1 - TL_X0)


def shape_svg(tag, size=20):
    return ('<svg class="shape" width="%d" height="%d" viewBox="-10 -10 20 20" aria-hidden="true">'
            '<g class="mk mk-%s">%s</g></svg>' % (size, size, tag.lower(), SHAPES[tag]))


def build_timeline(tl):
    refs = story_refs()
    slug = lambda t: markdown.extensions.toc.slugify(t, "-")  # noqa: E731
    lanes = tl["lanes"]
    for i, e in enumerate(tl["events"]):
        e["i"] = i
        e["url"] = e.get("href") or refs[e["ref"]]
        e["anchor"] = slug(e["section"])
    for r in tl["reactors"]:
        r["url"] = r.get("href") or refs[r["ref"]]

    parts = []
    top = 122
    react_h = 18 * len(tl["reactors"]) + 26
    lane_h = 74
    height = top + react_h + lane_h * len(lanes) + 34
    # act bands and labels
    for a, y0, y1, name in ACT_SPANS:
        parts.append('<rect class="band band-%d" x="%.1f" y="0" width="%.1f" height="%d"/>'
                     % (a, tx(y0), tx(min(y1, TL_Y1)) - tx(y0), height - 26))
        parts.append('<text class="band-label band-label-%d" x="%.1f" y="18">Act %d</text>'
                     '<text class="band-sub" x="%.1f" y="34">%s</text>'
                     % (a, tx(y0) + 8, a, tx(y0) + 8, html.escape(name)))
    # decade grid and axis
    for y in range(1950, 2030, 10):
        parts.append('<line class="grid" x1="%.1f" x2="%.1f" y1="%d" y2="%d"/>' % (tx(y), tx(y), top, height - 26))
        parts.append('<text class="axis" x="%.1f" y="%d">%d</text>' % (tx(y), height - 8, y))
    # milestone strip: the labelled events, in up to four rows
    ends = [-1e9] * 4
    for e in sorted((e for e in tl["events"] if e.get("label")), key=lambda e: e["when"]):
        x = tx(e["when"])
        width = 6.9 * len(e["label"]) + 8
        row = next((k for k in range(4) if x >= ends[k] + 8), min(range(4), key=lambda k: ends[k]))
        ends[row] = x + width
        ty = 56 + row * 15
        parts.append('<g class="milestone" aria-hidden="true"><line x1="%.1f" x2="%.1f" y1="%d" y2="%d"/>'
                     '<text x="%.1f" y="%d">%s</text></g>'
                     % (x, x, ty + 3, top - 4, x + 4, ty, html.escape(e["label"])))
    # reactors
    y = top + 16
    parts.append('<text class="lane-label" x="12" y="%d">Reactors running</text>' % y)
    for r in tl["reactors"]:
        y += 18
        parts.append('<g class="reactor"><title>%s reactor: %s</title>' % (r["name"], html.escape(r["note"])))
        parts.append('<text class="reactor-name" x="%d" y="%d">%s</text>' % (TL_X0 - 14, y + 4, r["name"]))
        for a, b in r["spans"]:
            parts.append('<rect class="run" x="%.1f" y="%d" width="%.1f" height="9" rx="4.5"/>' % (tx(a), y - 4, tx(b) - tx(a)))
        if r.get("disputed"):
            a, b = r["disputed"]
            parts.append('<line class="disputed" x1="%.1f" x2="%.1f" y1="%.1f" y2="%.1f"/>' % (tx(a) + 3, tx(b), y + .5, y + .5))
        if r.get("test"):
            parts.append('<circle class="test" cx="%.1f" cy="%.1f" r="4"/>' % (tx(r["test"]), y + .5))
        parts.append("</g>")
    # lanes of events
    y_lane = top + react_h
    for li, lane in enumerate(lanes):
        cy = y_lane + li * lane_h + lane_h / 2
        parts.append('<line class="lane-rule" x1="0" x2="%d" y1="%.1f" y2="%.1f"/>' % (TL_X1 + 10, cy - lane_h / 2, cy - lane_h / 2))
        parts.append('<text class="lane-label" x="12" y="%.1f">%s</text>' % (cy + 4, html.escape(lane["label"])))
        last = [-99, -99, -99]
        offs = [0, -20, 20]
        for e in sorted((e for e in tl["events"] if e["lane"] == lane["id"]), key=lambda e: e["when"]):
            x = tx(e["when"])
            row = next((k for k in range(3) if x - last[k] >= 17), min(range(3), key=lambda k: last[k]))
            last[row] = x
            label = "%s: %s. Source held in %s." % (e["date"], e["text"], TAGS[e["tag"]])
            parts.append('<a class="ev" href="index.html#%s" data-tag="%s" data-i="%d" aria-label="%s">'
                         '<title>%s</title><g class="mk mk-%s" transform="translate(%.1f %.1f)">%s</g>'
                         % (e["anchor"], e["tag"], e["i"], html.escape(label, quote=True),
                            html.escape(label), e["tag"].lower(), x, cy + offs[row], SHAPES[e["tag"]]))
            parts.append("</a>")
    svg = ('<svg class="timeline" viewBox="0 0 %d %d" role="group" aria-label="Timeline, 1950 to 2026">%s</svg>'
           % (TL_X1 + 20, height, "".join(parts)))

    filters = "".join(
        '<button type="button" class="tl-filter" data-tag="%s" aria-pressed="true">%s<span>%s</span> <span class="n">%d</span></button>'
        % (t, shape_svg(t, 16), html.escape(TAGS[t]), sum(1 for e in tl["events"] if e["tag"] == t)) for t in TAGS)

    lists = []
    for a, y0, y1, name in ACT_SPANS:
        evs = [e for e in tl["events"] if y0 <= e["when"] < y1]
        lis = []
        for e in evs:
            lane = next(ln["label"] for ln in lanes if ln["id"] == e["lane"])
            lis.append(
                '<li id="ev-%d" data-tag="%s"><span class="tl-dot">%s</span><time>%s</time>'
                '<div><p>%s</p><p class="tl-meta">%s · <a class="cite" href="%s"><span class="tag tag-%s">%s</span>source</a> · '
                '<a href="index.html#%s">in the story</a></p></div></li>'
                % (e["i"], e["tag"], shape_svg(e["tag"], 18), html.escape(e["date"]), html.escape(e["text"]),
                   html.escape(lane), html.escape(e["url"], quote=True), e["tag"].lower(), e["tag"], e["anchor"]))
        lists.append('<section class="tl-act tl-act-%d"><h2 class="act act-%d"><span class="act-n">Act %d</span> %s</h2><ol class="tl-list">%s</ol></section>'
                     % (a, a, a, html.escape(name), "".join(lis)))

    rrows = "".join(
        '<tr><th scope="row">%s</th><td>%s</td><td><a class="cite" href="%s"><span class="tag tag-%s">%s</span>source</a></td></tr>'
        % (r["name"], html.escape(r["note"]), html.escape(r["url"], quote=True), r["tag"].lower(), r["tag"])
        for r in tl["reactors"])

    lede = ("From the land taken in 1950 to the tanks still being emptied: %d events from the story, "
            "and the five production reactors' working lives. Each mark is shaped and coloured by where "
            "its source is held; select one to read it in the story." % len(tl["events"]))
    page = head("Timeline · " + TITLE, "timeline.html", "Timeline", lede) + """<main id="main" class="wrap">
<div class="tl-controls" role="group" aria-label="Show events whose source is held in">
  <span class="tl-controls-label">Show sources held in</span>%s
</div>
<figure class="tl-figure">
  <div class="tl-scroll">%s</div>
  <div id="tl-tip" class="tl-tip" hidden></div>
  <figcaption>Reactor bars show when each production reactor ran; the dashed line is the span the sources dispute for P reactor, and the ring marks K reactor's 1992 test run. <a href="#tl-reactors">Reactor dates as a table</a>.</figcaption>
</figure>
<div class="tl-lists">%s</div>
<h2 id="tl-reactors">The reactors</h2>
<div class="tl-reactors">
<div class="scroll"><table class="reactors"><thead><tr><th scope="col">Reactor</th><th scope="col">Working life</th><th scope="col">Source</th></tr></thead><tbody>%s</tbody></table></div>
<figure class="fig">
<img src="img/srs-from-iss-2006.jpg" width="540" height="405" alt="Photograph from orbit of forested land crossed by straight roads. Five cleared reactor areas are labelled; the Savannah River runs along the left edge, and L Lake and Par Pond lie to the south." loading="lazy">
<figcaption>The five reactor areas from the International Space Station, 28 January 2006. <span class="credit">NASA astronaut photograph ISS012-E-16633, labels by NASA Earth Observatory; public domain, via <a href="https://commons.wikimedia.org/wiki/File:SavannahRiverSite_ISS012-E-16633.jpg">Wikimedia Commons</a>.</span></figcaption>
</figure>
</div>
</main>
""" % (filters, svg, "".join(lists), rrows) + foot(["timeline.js"])
    write(ROOT / "timeline.html", page)
    return tl["events"]


LOCAL = re.compile(r"^(index|sources|about|timeline)\.html(#[\w-]+)?$|^(style\.css|app\.js|search\.js|timeline\.js)$|^img/[\w.-]+\.(png|jpg)$")
IDENT = re.compile(r"^https://archive\.org/details/[A-Za-z0-9][\w.-]*$")


def write(path, text):
    """Write UTF-8 with LF line endings on every platform. A page is
    written only if its links pass check_links."""
    if path.suffix == ".html":
        check_links(path.name, text)
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)


def check_links(name, page):
    """Refuse any href or src that is not http(s), mailto, an anchor or one
    of the explorer's own files, so nothing like javascript: is published."""
    bad = []
    for m in re.finditer(r'\b(?:href|src)="([^"]*)"', page):
        url = html.unescape(m.group(1)).strip()
        if url.startswith("https://archive.org/details/"):
            ok = IDENT.match(url.split("#")[0].split("?")[0])
        else:
            ok = (re.match(r"^https?://[^\s<>\"']+$", url)
                  or url.startswith(("mailto:", "#")) or LOCAL.match(url))
        if not ok:
            line = page.count("\n", 0, m.start()) + 1
            bad.append("%s:%d %s" % (name, line, url))
    if bad:
        raise SystemExit("Refusing to publish these links:\n  " + "\n  ".join(bad))


def main():
    items = []
    for act in (1, 2, 3):
        items += sources(CONTENT / ("sources-act%d.md" % act), act)
    (ROOT / "data").mkdir(exist_ok=True)
    data = [{k: s[k] for k in ("act", "section", "tag", "qual", "ident", "href", "search")}
            for s in items]
    write(ROOT / "data" / "sources.json",
          json.dumps(data, ensure_ascii=False, separators=(",", ":")))
    tl = json.loads((CONTENT / "timeline.json").read_text(encoding="utf-8"))
    build_story(items)
    events = build_timeline(tl)
    write(ROOT / "data" / "timeline.json", json.dumps(
        [{k: e[k] for k in ("i", "date", "text", "tag", "anchor")} for e in events],
        ensure_ascii=False, separators=(",", ":")))
    build_sources(items)
    build_about()
    by = {}
    for s in items:
        by[(s["act"], s["tag"])] = by.get((s["act"], s["tag"]), 0) + 1
    print(len(items), "sources,", len(events), "timeline events")
    for act in (1, 2, 3):
        print("  act", act, {t: by.get((act, t), 0) for t in TAGS})


if __name__ == "__main__":
    main()
