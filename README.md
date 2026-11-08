# Atomic History: The Savannah River Plant Story

**Live explorer: [robin-ia.github.io/savannah-river-plant-explorer](https://robin-ia.github.io/savannah-river-plant-explorer/)**

**A history of the Savannah River Plant in South Carolina, from 1950 to a
site still cleaning up its past and gearing up for new weapons work, told
from government resources held in Democracy's Library, the Wayback Machine
and Internet Archive collections, with every source labeled by where it is
held.**

## What it does

Six pages, under a banner with the Internet Archive and Democracy's Library
logos:

- **Home** (`index.html`): the four chapters, each with its sections and
  source count; a search box that finds passages in all four chapters,
  events on the timeline and matching sources; and a panel charting where
  each chapter's sources are held.
- **Chapters 1–4** (`chapter-1.html` to `chapter-4.html`, with each section
  on its own page, such as `chapter-1-2.html`, linked by Previous and Next):
  the history, with a tag on every citation: **DL** Democracy's Library,
  **WB** the Wayback Machine, **IA** the Internet Archive outside Democracy's
  Library, **OL** a book cataloged in Open Library,
  **EXT** held elsewhere. Each tag links to its source. Chapter 1 covers
  building the plant (1950–1969), Chapter 2 the reactors under scrutiny
  (1970–1992), Chapter 3 the years after bomb making (1992–2020) and
  Chapter 4 what is happening now (2020 to today), including the
  controversies of each period. Every chapter has a *Living with the Plant*
  section on jobs, charity and the towns around the site, and an *SRS and
  Ecology* section on the land and wildlife.
- **Timeline** (`timeline.html`): 69 events from the story in five lanes
  (land and people, production, environment and science, oversight and law,
  cleanup and legacy), the working lives of the five production reactors, and
  labeled milestones. Each mark's shape and color say where its source is
  held, and the marks can be filtered by holder. The same events follow as a
  list, by chapter.
- **Sources** (`sources.html`, linked from About as the bibliography, not in
  the menu): all 466 sources behind the story, filterable
  by where they are held, by chapter and by word. The filters are kept in the
  URL, for example `sources.html?tag=WB&chapter=3&q=DWPF`.
- **Glossary** (`glossary.html`): the technical words, agencies and places in
  the story.
- **Controversies** (`controversies.html`): the arguments over the plant,
  each linked to the story, and the places where the sources disagree.
- **Search** (`search.html`, in the menu on every page): search the story,
  the timeline and the sources.
- **Full Story (PDF)** (`read.html`, in the menu on every page): all four
  chapters as one PDF (`atomic-history-savannah-river-plant.pdf`), with images
  and citations, shown in the browser's own PDF viewer, with a link to download
  it. The PDF is tagged for screen readers and has a bookmark outline.
- **On Television** (`television.html`): broadcasts about the plant in the
  Internet Archive's TV News Archive, by chapter, each opening at the moment
  the plant comes up. The clips live in `content/television.json`, which also
  makes each one a source tagged **TV**.
- **About** (`about.html`): the project, where the sources are held, images
  and how it was built.

**Facts:**

- **Source of materials:** archive.org items (Democracy's Library and
  others), Wayback Machine captures, and a few outside
  holders. Wherever an outside page has a working Wayback capture, the
  capture is cited instead of the live page.
- **Years covered:** 1950 to 2026.
- **Size:** 466 sources: 68 DL, 259 WB, 121 IA, 15 TV, 3 OL, 0 EXT. Counted
  November 8, 2026.
- **Not included:** sources still being sought, such as the rest of the
  *New York Times* 1988 series and the "thirty incidents" report, are tracked as
  [issues labeled `source-gap`](https://github.com/Robin-IA/savannah-river-plant-explorer/issues?q=label%3Asource-gap).
  Unsourced facts are kept out of the story.

## How it was built

### The PDF

`build/build.py` also writes `story-print.html`, the whole story on one page.
`build/make_pdf.py` prints it to `atomic-history-savannah-river-plant.pdf`
with headless Chromium. Run it after every build that changes the story:

```bash
pip install -r requirements-pdf.txt
python -m playwright install chromium
python build/make_pdf.py
```

**Every change to the story remakes the PDF in the same pull request.** The
order is: edit `content/`, run `python build/build.py`, run
`python build/make_pdf.py`, run the checks, then commit the pages and the
PDF together, so the download never falls behind the website.

### The research

Every source was found and checked live on November 6, 2026, with
`archive.org/advancedsearch.php`, archive.org full-text search, the
`archive.org/metadata` API, the Wayback CDX server and the OSTI API. A source is labeled **DL** when its identifier matches
Democracy's Library's `search_collection` scope expression; every DL and IA
label was re-tested in a second, independent pass, which moved two items from
DL to IA. Each Wayback capture was replayed and each outside link opened.
The notes for each source, including what was and was not read, are in
`content/sources-chapter1.md` to `sources-chapter4.md`.

### The code

- `content/` is the source of truth; every page is generated from it:
  `story.md` and `sources-chapter1.md` to `sources-chapter4.md` (Markdown),
  `timeline.json` (each event and reactor span, with the same source as in
  the story), `about.html` (the About page's body) and `disagree.md` (where
  sources disagree, shown on the Controversies page).
- `build/build.py` writes `index.html`, the section pages `chapter-N.html` and `chapter-N-K.html`,
  `timeline.html`, `sources.html`, `glossary.html`, `controversies.html`, `search.html`, `read.html`, `about.html`, `data/sources.json`,
  `data/timeline.json` and `data/passages.json` (the chapters' paragraphs, for
  search). It needs
  Python 3 and the `markdown` package, pinned in `requirements.txt`. It
  refuses to write a page with a link that is not http(s), `mailto:`, an
  anchor or one of the explorer's own files. The holder chart and the timeline
  are SVG drawn by the script; the banner is a detail of the DOE site map
  (`img/banner-map.jpg`).
- `style.css` and three small scripts are written by hand: `search.js` (the
  home page's search), `timeline.js` (tooltips and holder filters) and
  `app.js` (the sources filters). Every page reads completely without them.
- `img/` holds the two logos and six public-domain images from Wikimedia
  Commons (a Department of Energy map of the site, a DOE reactor diagram, a
  DOE chart of plutonium production by year, two DOE photographs from about
  1970 and 1972, and a 2006 NASA photograph of the site from the ISS),
  resized for the web. Each is credited in its caption and on the About page.
- Holder colors come from a validated categorical palette (blue, amber,
  green, violet, magenta, and gray for "held elsewhere"); shapes and text labels
  carry the same information, so nothing depends on color alone.
- Published with GitHub Pages from the `main` branch, root folder.

To rebuild after editing anything in `content/`:

```bash
pip3 install -r requirements.txt
python3 build/build.py
```

To run it on your own Mac:

```bash
python3 -m http.server 8000
```

then open http://localhost:8000/.

### Who built it

Robin Fay, Project Manager, Digital Collections, Democracy's Library, with
[Claude Code](https://claude.com/claude-code) (Claude Opus 5.5), in November
2026. Robin chose the story and how sources are labeled; Claude did the
searching, drafted the story and wrote the code. Each commit names Claude as
co-author.

Feedback? Email robin.fay@archive.org with the subject
*Feedback about Explorers: Atomic History: The Savannah River Plant Story*.
