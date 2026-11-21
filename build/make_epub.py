"""Make the downloadable EPUB of the whole story, with a glossary and an index.

Run after build/build.py, which writes story-print.html and glossary.html:

    python build/make_epub.py

Needs pandoc 3 on the PATH (https://pandoc.org/installing.html) and
Beautiful Soup (pip install -r requirements-pdf.txt).

What it does:
- takes story-print.html (the same page the PDF is printed from), drops its
  printed Contents (the EPUB has its own) and keeps every image, caption,
  credit and citation link;
- adds the Glossary from glossary.html as back matter;
- adds an Index from build/epub_index_terms.py: each entry links to the
  first paragraph in each section where the subject comes up;
- has pandoc write an EPUB 3, one file per chapter, with the cover in
  img/epub-cover.jpg and the metadata below.
"""
import copy
import re
import subprocess
import sys
import tempfile
import zipfile
from collections import OrderedDict
from pathlib import Path

from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "build"))
from epub_index_terms import TERMS, SEE  # noqa: E402

STORY = ROOT / "story-print.html"
GLOSSARY = ROOT / "glossary.html"
OUT = ROOT / "books" / "atomic-history-savannah-river-plant.epub"
SITE = "https://internetarchivecanada.github.io/Explorer-Atomic-History-SRS-Story/"
MAX_LOCS, TOP_LOCS = 12, 5   # past MAX_LOCS sections, list the TOP_LOCS that discuss a subject most

META = {
    "title": "Atomic History: The Savannah River Story",
    "publisher": "Democracy's Library, Internet Archive",
    "lang": "en-US",
    "date": "2026-11-09",
    "description": ("A history of the Savannah River Plant in South Carolina from 1950 to today, "
                    "told from government resources held in Democracy's Library, the Wayback "
                    "Machine and Internet Archive collections."),
    "subject": "Savannah River Plant (S.C.)--History",
}
AUTHOR = "Robin Fay, Democracy's Library, Internet Archive"
AUTHOR_SORT = "Fay, Robin"


def front_matter(s):
    t = s.select_one("section.print-title")
    h2 = t.find("h2", string="Contents")
    h2.find_next("ol").decompose()
    h2.decompose()
    h1 = t.find("h1")
    h1.string = "About This Book"
    h1["id"] = "about-this-book"


def glossary(s):
    g = BeautifulSoup(GLOSSARY.read_text(encoding="utf-8"), "html.parser")
    gmain = g.find("main") or g
    sec = s.new_tag("section")
    sec["class"] = "glossary"
    h = s.new_tag("h1", id="glossary")
    h.string = "Glossary"
    sec.append(h)
    dl = None
    for el in gmain.find_all(["h2", "dt", "dd"]):
        if el.name == "h2":
            h = s.new_tag("h2", id="gl-" + el["id"])
            h.string = el.get_text(" ", strip=True)
            sec.append(h)
            dl = s.new_tag("dl")
            sec.append(dl)
            continue
        n = copy.copy(el)
        if n.get("id"):   # pandoc drops ids on <dt>; keep the target in a span
            n.insert(0, s.new_tag("span", id="gl-" + n["id"]))
            del n["id"]
        for a in n.find_all("a"):
            href = a.get("href", "")
            if not href.startswith(("http", "#")):
                a["href"] = SITE + href
        dl.append(n)
    return sec


def paragraphs(s):
    """Every paragraph and list item of the story, with its chapter and section."""
    chap, sid, stitle, out = 0, None, None, []
    for el in s.find("body").find_all(["h1", "h2", "h4", "p", "li"]):
        if el.find_parent("section", class_="print-title"):
            continue
        if el.name == "h1" and el.get("id", "").startswith("chapter-"):
            chap = int(el["id"].split("-")[1])
            sid = el["id"]
            stitle = el.get_text(strip=True).split(". ", 1)[1].rsplit(",", 1)[0]
            continue
        if el.name in ("h2", "h4"):
            sid, stitle = el["id"], el.get_text(strip=True)
            continue
        if not chap:
            continue
        c = copy.copy(el)
        for a in c.select("a.cite"):
            a.decompose()
        out.append((chap, sid, stitle, el, re.sub(r"\s+", " ", c.get_text(" "))))
    return out


def sortkey(h):
    return re.sub(r"[^a-z0-9 ]", "", h.lower())


def index(s, paras):
    counter = {}

    def anchor(el, sid):
        # pandoc drops ids on <p> and <li>, so the target is an empty span
        # at the start of the paragraph.
        first = el.contents[0] if el.contents else None
        if getattr(first, "name", None) == "span" and first.get("id", "").startswith(sid + "-p"):
            return first["id"]
        counter[sid] = counter.get(sid, 0) + 1
        span = s.new_tag("span", id="%s-p%d" % (sid, counter[sid]))
        el.insert(0, span)
        return span["id"]

    entries = []
    for head, pats, gl in TERMS:
        rx = [re.compile(p) for p in pats]
        locs, hits = OrderedDict(), {}
        for chap, sid, stitle, el, text in paras:
            n = sum(len(r.findall(text)) for r in rx)
            if not n:
                continue
            hits[(chap, sid)] = hits.get((chap, sid), 0) + n
            if (chap, sid) not in locs:
                locs[(chap, sid)] = (stitle, anchor(el, sid))
        items, passim = list(locs.items()), False
        if len(items) > MAX_LOCS:
            keep = set(sorted(hits, key=lambda k: -hits[k])[:TOP_LOCS])
            items, passim = [i for i in items if i[0] in keep], True
        if items or gl:
            entries.append((head, items, gl, passim))
    for head, target in SEE:
        entries.append((head, None, target, False))
    entries.sort(key=lambda e: sortkey(e[0]))

    sec = s.new_tag("section")
    sec["class"] = "book-index"
    h = s.new_tag("h1", id="index")
    h.string = "Index"
    sec.append(h)
    note_div = s.new_tag("div")   # pandoc keeps classes on divs, not on p or ul
    note_div["class"] = "index-note"
    note = s.new_tag("p")
    note_div.append(note)
    note.string = ("Each entry links to the first place the subject comes up in a section, given by "
                   "chapter number and section title. For subjects that run through the whole story, "
                   "the sections that discuss them most are listed.")
    sec.append(note_div)
    letter = ul = None
    for head, locs, extra, passim in entries:
        L = sortkey(head)[0].upper()
        if L != letter:
            letter = L
            h = s.new_tag("h2", id="index-" + L)
            h["class"] = "unlisted"
            h.string = L
            sec.append(h)
            wrap = s.new_tag("div")
            wrap["class"] = "index-list"
            ul = s.new_tag("ul")
            wrap.append(ul)
            sec.append(wrap)
        li = s.new_tag("li")
        li.append(head)
        if locs is None:
            li.append(". ")
            em = s.new_tag("em")
            em.string = "See"
            li.append(em)
            li.append(" " + extra)
        else:
            li.append(" ")
            parts = []
            for (chap, _sid), (stitle, aid) in locs:
                a = s.new_tag("a", href="#" + aid)
                a.string = "%d: %s" % (chap, stitle)
                parts.append(a)
            if passim:
                parts.append("and throughout")
            if extra:
                a = s.new_tag("a", href="#gl-" + extra)
                a.string = "Glossary"
                parts.append(a)
            for i, p in enumerate(parts):
                if i:
                    li.append("; ")
                li.append(p)
        ul.append(li)
    return sec, len(entries)


def fix_opf(path):
    """pandoc reads the author through YAML, which curls apostrophes; put the
    metadata back exactly as written."""
    with zipfile.ZipFile(path) as z:
        files = [(i, z.read(i.filename)) for i in z.infolist()]
    out = []
    for info, data in files:
        if info.filename.endswith("content.opf"):
            t = data.decode("utf-8")
            head, rest = t.split("</metadata>", 1)
            head = head.replace("’", "'").replace("(S.C.)–History", "(S.C.)--History")
            data = (head + "</metadata>" + rest).encode("utf-8")
        out.append((info, data))
    with zipfile.ZipFile(path, "w") as z:
        for info, data in out:   # mimetype first and stored, as EPUB requires
            ct = zipfile.ZIP_STORED if info.filename == "mimetype" else zipfile.ZIP_DEFLATED
            z.writestr(info.filename, data, compress_type=ct)


def main():
    OUT.parent.mkdir(exist_ok=True)
    s = BeautifulSoup(STORY.read_text(encoding="utf-8"), "html.parser")
    for link in s.find_all("link"):
        link.decompose()
    for img in s.find_all("img"):
        img.attrs.pop("loading", None)
    front_matter(s)
    gsec = glossary(s)
    isec, n_entries = index(s, paragraphs(s))
    s.find("body").append(gsec)
    s.find("body").append(isec)

    with tempfile.TemporaryDirectory() as tmp:
        src = Path(tmp) / "story-epub.html"
        src.write_text(str(s), encoding="utf-8")
        meta = Path(tmp) / "author.yaml"
        meta.write_text('creator:\n  - role: author\n    text: "%s"\n    file-as: "%s"\n'
                        % (AUTHOR, AUTHOR_SORT), encoding="utf-8")
        cmd = ["pandoc", str(src), "-f", "html", "-t", "epub3", "-o", str(OUT),
               "--split-level=1", "--toc", "--toc-depth=2",
               "--css", str(ROOT / "build" / "epub.css"),
               "--epub-cover-image", str(ROOT / "img" / "epub-cover.jpg"),
               "--resource-path", str(ROOT), "--metadata-file", str(meta)]
        for k, v in META.items():
            cmd += ["--metadata", "%s=%s" % (k, v)]
        subprocess.run(cmd, check=True)
    fix_opf(OUT)
    print("wrote", OUT.name, round(OUT.stat().st_size / 1e6, 1), "MB,",
          len(gsec.find_all("dt")), "glossary terms,", n_entries, "index entries")


if __name__ == "__main__":
    main()
