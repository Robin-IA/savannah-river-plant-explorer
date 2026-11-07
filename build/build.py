#!/usr/bin/env python3
"""Build the explorer's pages from the Markdown in content/.

    python3 build/build.py

Reads content/ (story.md, sources-chapter{1,2,3}.md, timeline.json,
about.md, disagree.md) and writes index.html (the home page),
chapter-1.html to chapter-3.html (the story), timeline.html,
sources.html, about.html, data/sources.json, data/timeline.json and
data/passages.json (the story's paragraphs, for search).

Needs the `markdown` package (pip install markdown).
"""

import hashlib
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
CHECKED = "November 6, 2026"
FEEDBACK = ("mailto:robin.fay@archive.org?subject=Feedback%20about%20Explorers"
            "%3A%20Bomb%20Making%3A%20A%20History%20of%20the%20Savannah%20River"
            "%20Plant")

CSP = ("default-src 'self'; script-src 'self'; style-src 'self'; "
       "img-src 'self'; object-src 'none'; base-uri 'none'; form-action 'self'")

TAGS = {
    "DL": "Democracy's Library",
    "WB": "Wayback Machine",
    "IA": "Internet Archive",
    "OL": "Open Library",
    "AIT": "Archive-It",
    "EXT": "Held elsewhere",
}
ACTS = {
    1: "Chapter 1. Building the bomb plant, 1950–1969",
    2: "Chapter 2. The reactors under scrutiny, 1970–1992",
    3: "Chapter 3. After the bombs, 1992–2020",
    4: "Chapter 4. What's happening now, 2020 to today",
}
HELD = {"DL": "in Democracy's Library", "WB": "in the Wayback Machine", "IA": "in the Internet Archive",
        "OL": "in Open Library", "AIT": "in Archive-It", "EXT": "elsewhere"}
CHAPTER_PAGE = {1: "chapter-1.html", 2: "chapter-2.html", 3: "chapter-3.html", 4: "chapter-4.html"}
CHAPTER_BLURB = {
    1: "The site chosen, the towns moved off it, the plant built and its reactors running, who was hired, and what it released.",
    2: "Releases and monitoring, the L reactor restart, contaminated groundwater, the secret accidents and the 1988 shutdowns, and the end of production.",
    3: "The turn to cleanup: the waste tanks, sealing the reactors, fights over plutonium, sick workers, the laboratories and how the site is remembered.",
    4: "The site today: making plutonium pits again, emptying the last waste tanks, moving plutonium out of the state, and who is watching.",
}
TAG_RE = re.compile(r"^(DL|IA|OL|WB|AIT|EXT)\b\s*:?\s*(.*)$", re.S)


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
             (3, 1992.5, 2020.5, "After the bombs"),
             (4, 2020.5, 2027, "Now"))


def banner_art():
    """The banner's picture: a detail of the Department of Energy's map of
    the site and the towns around it (credited on the About page), behind a
    veil that keeps the title side dark."""
    return ('<img class="banner-map" src="img/banner-map.jpg" alt="" width="1120" height="696">'
            '<div class="banner-veil"></div>')


def logos():
    return """<div class="banner-logos">
      <a class="logo-ia" href="https://archive.org/"><img src="img/internet-archive.png" alt="Internet Archive" width="56" height="56"></a>
      <a class="logo-dl" href="https://archive.org/details/democracys-library"><img src="img/democracys-library-crop.png" alt="Democracy's Library" width="99" height="60"></a>
      <span class="banner-kicker">A Democracy's Library story from the Internet Archive</span>
    </div>"""


def asset(name):
    """A local asset's URL with a fingerprint of its contents, so a browser
    fetches the new file after every change instead of a cached old one."""
    digest = hashlib.sha256((ROOT / name).read_bytes()).hexdigest()[:8]
    return "%s?v=%s" % (name, digest)


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
<link rel="stylesheet" href="%s">
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
""" % (CSP, html.escape(title), html.escape(DESCRIPTION, quote=True), asset("style.css"), "".join(nav),
       " big" if big else "", banner_art(), logos(), html.escape(h1), lede, extra)


# The explorer-checks passing note. The pages are generated, so the note
# lives here, not in the pages: when a later run of the checker re-dates it
# or takes it down, make the same change here.
CHECKS_NOTE = """<!-- explorer-checks:note -->
<p class="explorer-checks-note">
  Meets WCAG 2.2 Level AA accessibility (and WCAG 2.1 AA and 2.0 AA), checked
  <time datetime="2026-11-06">November 6, 2026</time> by automated tests and manual review.
  Also passes security and code validity checks.
</p>
<!-- /explorer-checks:note -->"""


def foot(scripts=()):
    tags = "".join('<script src="%s"></script>\n' % asset(s) for s in scripts)
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


def holder_index(items):
    """The holders as buttons, each opening the sources page filtered to it."""
    rows = "".join(
        '<li><a class="holder-btn" href="sources.html?tag=%s"><span class="tag tag-%s">%s</span>'
        '<span class="hb-name">%s</span><span class="hb-n">%d</span></a></li>'
        % (t, t.lower(), t, html.escape(n), sum(1 for s in items if s["tag"] == t))
        for t, n in TAGS.items())
    return '<ul class="holder-index" aria-label="Sources by where they are held">%s</ul>' % rows


def legend(cls="legend"):
    rows = "".join('<li><span class="tag tag-%s">%s</span> %s</li>'
                   % (t.lower(), t, html.escape(n)) for t, n in TAGS.items())
    return '<ul class="%s" aria-label="Where each source is held">%s</ul>' % (cls, rows)


def holder_chart(items):
    """Stacked bars, one per chapter: how many sources each holder supplies."""
    rows, table = [], []
    w, x0, bar = 300, 0, 18
    for n, act in enumerate((1, 2, 3, 4)):
        mine = [s for s in items if s["act"] == act]
        total = len(mine)
        y = n * 52 + 22
        rows.append('<text class="ch-label" x="0" y="%d">Chapter %d · %d sources</text>' % (y - 6, act, total))
        x = x0
        cells = []
        for t in TAGS:
            c = sum(1 for s in mine if s["tag"] == t)
            cells.append(str(c))
            if not c:
                continue
            seg = w * c / total
            label = "Chapter %d: %d %s held %s" % (act, c, "source" if c == 1 else "sources", HELD[t])
            rows.append('<a class="seg-link" href="sources.html?tag=%s&amp;chapter=%d" aria-label="%s"><title>%s</title>'
                        '<rect class="seg seg-%s" x="%.1f" y="%d" width="%.1f" height="%d" rx="3"/>'
                        % (t, act, html.escape(label, quote=True), html.escape(label), t.lower(), x, y, max(seg - 2, 1), bar))
            if seg >= 24:
                rows.append('<text class="seg-n seg-n-%s" x="%.1f" y="%d" aria-hidden="true">%d</text>' % (t.lower(), x + seg / 2 - 1, y + 13, c))
            rows.append('</a>')
            x += seg
        table.append("<tr><th scope=\"row\">Chapter %d</th>%s<td>%d</td></tr>" % (act, "".join("<td>%s</td>" % c for c in cells), total))
    svg = ('<svg class="holder-chart" viewBox="0 0 %d 210" role="group" aria-labelledby="hc-t">'
           '<title id="hc-t">Sources by where they are held, for each chapter; select a bar to see them</title>%s</svg>' % (w, "".join(rows)))
    tbl = ('<div class="sr"><table><caption>Sources by holder and chapter</caption><tr><th scope="col">Chapter</th>%s<th scope="col">Total</th></tr>%s</table></div>'
           % ("".join('<th scope="col">%s</th>' % html.escape(TAGS[t]) for t in TAGS), "".join(table)))
    return svg + tbl


# --------------------------------------------------------------------------

def tag_links(body):
    """Give every story citation a visible holder tag."""
    def repl(m):
        attrs, tag, rest = m.group(1), m.group(2), m.group(3)
        return ('<a%s class="cite"><span class="tag tag-%s">%s</span>%s</a>'
                % (attrs, tag.lower(), tag, rest))
    return re.sub(r"<a([^>]*)>(DL|IA|OL|WB|AIT|EXT)\b(.*?)</a>", repl, body, flags=re.S)


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


def story_chapters():
    """The story's chapters as (number, title, markdown), and its link definitions."""
    text = (CONTENT / "story.md").read_text(encoding="utf-8")
    text = re.sub(r"\A# .*?\n", "", text)
    text = re.sub(r"## How to read the sources.*?\n---\n", "", text, flags=re.S)
    defs = "\n".join(m.group(0) for m in re.finditer(r"^\[[\w-]+\]:\s*\S+.*$", text, re.M))
    body = re.sub(r"^\[[\w-]+\]:\s*\S+.*$\n?", "", text, flags=re.M)
    parts = re.split(r"^## Chapter (\d)\. (.*)$", body, flags=re.M)
    chapters = []
    for i in range(1, len(parts), 3):
        md_text = re.sub(r"^### ", "## ", parts[i + 2], flags=re.M)
        md_text = re.sub(r"^---\s*$", "", md_text, flags=re.M)
        chapters.append((int(parts[i]), parts[i + 1].strip(), md_text))
    return chapters, defs


def chapter_nav(current, sections):
    """The chapter menu: every chapter folds open to list its sections.
    Built on <details>, so it opens and closes without script and works from
    the keyboard; the chapter being read starts open."""
    items = []
    for n, page in CHAPTER_PAGE.items():
        name = ACTS[n].split(". ", 1)[1]
        here = n == current
        target = "" if here else page
        links = ['<li><a href="%s#main"%s>Start of chapter</a></li>'
                 % (page, ' aria-current="page"' if here else "")]
        links += ['<li><a href="%s#%s">%s</a></li>' % (target, hid, html.escape(t))
                  for hid, t in sections[n]]
        items.append('<li class="ch-%d"><details%s><summary><span class="ch-n">Chapter %d</span> %s</summary>'
                     '<ul>%s</ul></details></li>'
                     % (n, " open" if here else "", n, html.escape(name), "".join(links)))
    return ('<nav class="toc" aria-label="Chapters"><h2>Chapters</h2><ol class="ch-list">%s</ol></nav>'
            % "".join(items))


def rail(items):
    return """<aside class="rail" aria-label="Where the record lives">
  <h2>Where the record lives</h2>
  %s
  %s
  <a class="card" href="timeline.html"><strong>Timeline</strong><span>Seventy-six years in one view: the reactors, the people moved, the oversight and the cleanup.</span></a>
  <a class="card" href="sources.html"><strong>All %d sources</strong><span>Filter by holder, chapter and word.</span></a>
</aside>""" % (holder_index(items), holder_chart(items), len(items))


def build_chapters(items):
    """Write the chapter pages; return heading slug -> page,
    the passages for search, and each chapter's section titles."""
    chapters, defs = story_chapters()
    pages, passages, sections, built = {}, [], {}, []
    for n, title, md_text in chapters:
        page = CHAPTER_PAGE[n]
        md = markdown.Markdown(extensions=["tables", "toc"],
                               extension_configs={"toc": {"toc_depth": "2-2"}})
        body = tag_links(md.convert(md_text + "\n\n" + defs))
        body = re.sub(r"<hr />\s*", "", body)
        k = [0]

        def pid(m):
            k[0] += 1
            return '<%s id="c%d-%d">' % (m.group(1), n, k[0])
        body = re.sub(r"<(p|li)>", pid, body)
        sections[n] = []
        for hid, htext in re.findall(r'<h2 id="([^"]+)">(.*?)</h2>', body):
            pages[hid] = page
            sections[n].append((hid, re.sub("<[^>]+>", "", htext)))
        # passages for search: each paragraph with the section it sits in
        current = ""
        for m in re.finditer(r'<h2 id="[^"]+">(.*?)</h2>|<(p|li) id="(c\d-\d+)">(.*?)</\2>', body, re.S):
            if m.group(1) is not None:
                current = html.unescape(re.sub("<[^>]+>", "", m.group(1)))
            else:
                t = html.unescape(re.sub(r"\s+", " ", re.sub("<[^>]+>", "", m.group(4)))).strip()
                if t:
                    passages.append({"p": page, "id": m.group(3), "c": n, "s": current, "t": t})
        built.append((n, title, page, body))
    for n, title, page, body in built:
        nav = chapter_nav(n, sections)
        prev_next = []
        if n > 1:
            prev_next.append('<a class="pn prev" href="%s"><span>Previous</span> %s</a>' % (CHAPTER_PAGE[n - 1], html.escape(ACTS[n - 1])))
        if n < len(CHAPTER_PAGE):
            prev_next.append('<a class="pn next" href="%s"><span>Next</span> %s</a>' % (CHAPTER_PAGE[n + 1], html.escape(ACTS[n + 1])))
        else:
            prev_next.append('<a class="pn next" href="about.html#where-the-sources-disagree"><span>Next</span> Where the sources disagree</a>')
        h1 = "Chapter %d. %s" % (n, title)
        page_html = head("%s · %s" % (h1, TITLE), page, h1, html.escape(CHAPTER_BLURB[n])) + """<main id="main" class="wrap story chapter chapter-%d">
<div class="cols">
%s
<article>
%s
<nav class="prev-next" aria-label="Previous and next chapter">%s</nav>
</article>
%s
</div>
</main>
""" % (n, nav, body, "".join(prev_next), rail(items)) + foot()
        write(ROOT / page, page_html)
    return pages, passages, sections


def build_home(items, sections):
    counts = {n: sum(1 for s in items if s["act"] == n) for n in CHAPTER_PAGE}
    cards = []
    for n, page in CHAPTER_PAGE.items():
        name = ACTS[n].split(". ", 1)[1]
        secs = "".join('<li><a href="%s#%s">%s</a></li>' % (page, hid, html.escape(t)) for hid, t in sections[n])
        cards.append("""<section class="ch-card ch-%d" aria-labelledby="ch%d-h">
  <p class="ch-n"><a href="%s">Chapter %d</a></p>
  <h2 id="ch%d-h"><a href="%s">%s</a></h2>
  <p>%s</p>
  <p><a class="read" href="%s">Read Chapter %d<span aria-hidden="true"> →</span></a></p>
  <ul class="ch-secs" aria-label="Sections of Chapter %d">%s</ul>
  <p class="ch-count">%d sources · <a href="sources.html?chapter=%d">see them</a></p>
</section>""" % (n, n, page, n, n, page, html.escape(name), html.escape(CHAPTER_BLURB[n]), page, n, n, secs, counts[n], n))
    lede = html.escape(DESCRIPTION)
    start = '<p class="start"><a class="read big" href="chapter-1.html">Start reading: Chapter 1<span aria-hidden="true"> →</span></a></p>'
    page = head(TITLE, "index.html", TITLE, lede, start + SEARCH_FORM % len(items), big=True) + """<section id="results" class="wrap results" aria-labelledby="results-h" hidden>
  <div class="results-head"><h2 id="results-h">Search results</h2><button type="button" id="results-close">Clear search</button></div>
  <p id="results-count" role="status" aria-live="polite"></p>
  <div class="results-cols">
    <section aria-labelledby="rs-story"><h3 id="rs-story">In the story</h3><ol id="results-story"></ol></section>
    <section aria-labelledby="rs-time"><h3 id="rs-time">On the timeline</h3><ol id="results-time"></ol></section>
  </div>
</section>
<main id="main" class="wrap home">
<div class="home-cols">
<div class="chapters">
%s
</div>
%s
</div>
</main>
""" % ("\n".join(cards), rail(items)) + foot(["search.js"])
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
            '<tr data-tag="%s" data-chapter="%d"><td><span class="tag tag-%s">%s</span>%s</td>'
            '<td><div class="src">%s</div><div class="note">%s</div></td>'
            '<td class="where">Chapter %d<br><span>%s</span></td></tr>'
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
    <label for="chapter">Chapter</label>
    <select id="chapter" name="chapter"><option value="">All chapters</option>%s</select>
    <label for="q">Search</label>
    <input id="q" name="q" type="search" placeholder="Ellenton, tritium, DWPF…">
  </div>
</form>
<div class="chart-box">%s</div>
</div>
<p id="count" class="count" role="status" aria-live="polite">%d sources</p>
<div class="scroll">
<table class="sources">
<caption class="sr">Sources, with where each is held, what it is, and the chapter and theme it belongs to</caption>
<thead><tr><th scope="col">Held in</th><th scope="col">Source</th><th scope="col">Chapter and theme</th></tr></thead>
<tbody>
%s
</tbody>
</table>
</div>
</main>
""" % (tagbtns, actopts, holder_chart(items), len(items), "\n".join(rows)) + foot(["app.js"])
    write(ROOT / "sources.html", page)


def build_about(pages):
    body = markdown.markdown((CONTENT / "about.md").read_text(encoding="utf-8"))
    body = re.sub(r'href="index\.html#([\w-]+)"', lambda m: 'href="%s#%s"' % (pages[m.group(1)], m.group(1)), body)
    disagree = markdown.markdown((CONTENT / "disagree.md").read_text(encoding="utf-8"))
    body = body.replace("<!-- DISAGREE -->", disagree.replace("<ul>", '<ul class="disagree">'))
    lede = ("A history of the Savannah River Plant told from the record, with every source "
            "labeled by where it is held, so a reader can open it and check.")
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
    "OL": '<path d="M-7 -4 L0 -8 L7 -4 L7 4 L0 8 L-7 4 Z"/>',
    "WB": '<path d="M0 -8.5 L8.5 0 L0 8.5 L-8.5 0 Z"/>',
    "AIT": '<path d="M0 -8 L8 6.5 L-8 6.5 Z"/>',
    "EXT": '<circle r="5.5"/>',
}


def tx(year):
    return TL_X0 + (year - TL_Y0) / (TL_Y1 - TL_Y0) * (TL_X1 - TL_X0)


def shape_svg(tag, size=20):
    return ('<svg class="shape" width="%d" height="%d" viewBox="-10 -10 20 20" aria-hidden="true">'
            '<g class="mk mk-%s">%s</g></svg>' % (size, size, tag.lower(), SHAPES[tag]))


def build_timeline(tl, pages):
    refs = story_refs()
    slug = lambda t: markdown.extensions.toc.slugify(t, "-")  # noqa: E731
    lanes = tl["lanes"]
    for i, e in enumerate(tl["events"]):
        e["i"] = i
        e["url"] = e.get("href") or refs[e["ref"]]
        e["anchor"] = slug(e["section"])
        e["page"] = pages[e["anchor"]]
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
        parts.append('<text class="band-label band-label-%d" x="%.1f" y="18">Chapter %d</text>'
                     '<text class="band-sub" x="%.1f" y="34">%s</text>'
                     % (a, tx(y0) + 8, a, tx(y0) + 8, html.escape(name)))
    # decade grid and axis
    for y in range(1950, 2030, 10):
        parts.append('<line class="grid" x1="%.1f" x2="%.1f" y1="%d" y2="%d"/>' % (tx(y), tx(y), top, height - 26))
        parts.append('<text class="axis" x="%.1f" y="%d">%d</text>' % (tx(y), height - 8, y))
    # milestone strip: the labeled events, in up to four rows
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
            parts.append('<a class="ev" href="%s#%s" data-tag="%s" data-i="%d" aria-label="%s">'
                         '<title>%s</title><g class="mk mk-%s" transform="translate(%.1f %.1f)">%s</g>'
                         % (e["page"], e["anchor"], e["tag"], e["i"], html.escape(label, quote=True),
                            html.escape(label), e["tag"].lower(), x, cy + offs[row], SHAPES[e["tag"]]))
            parts.append("</a>")
    svg = ('<svg class="timeline" viewBox="0 0 %d %d" role="group" aria-label="Timeline, 1950 to 2026">%s</svg>'
           % (TL_X1 + 20, height, "".join(parts)))

    filters = "".join(
        '<button type="button" class="tl-filter" data-tag="%s" aria-pressed="true">%s<span>%s</span> <span class="n">%d</span></button>'
        % (t, shape_svg(t, 16), html.escape(TAGS[t]), sum(1 for e in tl["events"] if e["tag"] == t))
        for t in TAGS if any(e["tag"] == t for e in tl["events"]))

    lists = []
    for a, y0, y1, name in ACT_SPANS:
        evs = [e for e in tl["events"] if y0 <= e["when"] < y1]
        lis = []
        for e in evs:
            lane = next(ln["label"] for ln in lanes if ln["id"] == e["lane"])
            lis.append(
                '<li id="ev-%d" data-tag="%s"><span class="tl-dot">%s</span><time>%s</time>'
                '<div><p>%s</p><p class="tl-meta">%s · <a class="cite" href="%s"><span class="tag tag-%s">%s</span>source</a> · '
                '<a href="%s#%s">in the story</a></p></div></li>'
                % (e["i"], e["tag"], shape_svg(e["tag"], 18), html.escape(e["date"]), html.escape(e["text"]),
                   html.escape(lane), html.escape(e["url"], quote=True), e["tag"].lower(), e["tag"], e["page"], e["anchor"]))
        lists.append('<section class="tl-act tl-act-%d"><h2 class="act act-%d"><span class="act-n">Chapter %d</span> %s</h2><ol class="tl-list">%s</ol></section>'
                     % (a, a, a, html.escape(name), "".join(lis)))

    rrows = "".join(
        '<tr><th scope="row">%s</th><td>%s</td><td><a class="cite" href="%s"><span class="tag tag-%s">%s</span>source</a></td></tr>'
        % (r["name"], html.escape(r["note"]), html.escape(r["url"], quote=True), r["tag"].lower(), r["tag"])
        for r in tl["reactors"])

    lede = ("From the land taken in 1950 to the tanks still being emptied: %d events from the story, "
            "and the five production reactors' working lives. Click on a shape to read it in the story."
            % len(tl["events"]))
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
<figcaption>The five reactor areas from the International Space Station, January 28, 2006. <span class="credit">NASA astronaut photograph ISS012-E-16633, labels by NASA Earth Observatory; public domain, via <a href="https://commons.wikimedia.org/wiki/File:SavannahRiverSite_ISS012-E-16633.jpg">Wikimedia Commons</a>.</span></figcaption>
</figure>
</div>
</main>
""" % (filters, svg, "".join(lists), rrows) + foot(["timeline.js"])
    write(ROOT / "timeline.html", page)
    return tl["events"]


LOCAL = re.compile(r"^sources\.html\?(chapter=[1-4]|tag=(DL|WB|IA|OL|AIT|EXT)(&chapter=[1-4])?)$|^(index|sources|about|timeline|chapter-[1-4])\.html(#[\w-]+)?$|^(style\.css|app\.js|search\.js|timeline\.js)(\?v=[0-9a-f]{8})?$|^img/[\w.-]+\.(png|jpg)$")
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
    for act in CHAPTER_PAGE:
        items += sources(CONTENT / ("sources-chapter%d.md" % act), act)
    (ROOT / "data").mkdir(exist_ok=True)
    data = [dict({k: s[k] for k in ("section", "tag", "qual", "ident", "href", "search")}, chapter=s["act"])
            for s in items]
    write(ROOT / "data" / "sources.json",
          json.dumps(data, ensure_ascii=False, separators=(",", ":")))
    tl = json.loads((CONTENT / "timeline.json").read_text(encoding="utf-8"))
    pages, passages, sections = build_chapters(items)
    build_home(items, sections)
    write(ROOT / "data" / "passages.json",
          json.dumps(passages, ensure_ascii=False, separators=(",", ":")))
    events = build_timeline(tl, pages)
    write(ROOT / "data" / "timeline.json", json.dumps(
        [{k: e[k] for k in ("i", "date", "text", "tag", "page", "anchor")} for e in events],
        ensure_ascii=False, separators=(",", ":")))
    build_sources(items)
    build_about(pages)
    by = {}
    for s in items:
        by[(s["act"], s["tag"])] = by.get((s["act"], s["tag"]), 0) + 1
    print(len(items), "sources,", len(events), "timeline events")
    for act in CHAPTER_PAGE:
        print("  chapter", act, {t: by.get((act, t), 0) for t in TAGS})


if __name__ == "__main__":
    main()
