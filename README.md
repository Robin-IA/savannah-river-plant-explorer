# Bomb Making: A History of the Savannah River Plant

**Live explorer: [robin-ia.github.io/savannah-river-plant-explorer](https://robin-ia.github.io/savannah-river-plant-explorer/)**

**A history of the Savannah River Plant in South Carolina, from 1950 to now,
told from records held in Democracy's Library, the wider Internet Archive,
the Wayback Machine and elsewhere, with every source labelled by where it
is held.**

## What it does

Four pages, under a banner with the Internet Archive and Democracy's Library
logos:

- **Story** (`index.html`): the history in three acts, with a tag on every
  citation: **DL** Democracy's Library, **IA** the Internet Archive outside
  Democracy's Library, **OL** a book catalogued in Open Library, **WB** the
  Wayback Machine, **AIT** Archive-It, **EXT**
  held elsewhere. Each tag links to its source. The acts cover building the
  plant (1950–1969), the reactors under scrutiny (1970–1992) and the years
  after bomb making (1992 to now). A search box in the banner finds passages
  in the story, events on the timeline and matching sources; a side panel
  charts where each act's sources are held.
- **Timeline** (`timeline.html`): 37 events from the story in five lanes
  (land and people, production, environment and science, oversight and law,
  cleanup and legacy), the working lives of the five production reactors, and
  labelled milestones. Each mark's shape and colour say where its source is
  held, and the marks can be filtered by holder. The same events follow as a
  list, by act.
- **Sources** (`sources.html`): all 301 sources behind the story, filterable
  by where they are held, by act and by word. The filters are kept in the URL,
  for example `sources.html?tag=WB&act=3&q=DWPF`.
- **About** (`about.html`), including the controversies, the documentary
  *Building Bombs*, and where the sources disagree.

**Facts:**

- **Source of materials:** archive.org items (Democracy's Library and
  others), Wayback Machine captures, Archive-It seeds, and outside holders,
  chiefly DOE's OSTI.
- **Years covered:** 1950 to 2026.
- **Size:** 301 sources: 47 DL, 103 IA, 3 OL, 78 WB, 1 AIT, 69 EXT. Counted
  6 November 2026.
- **Not included:** sources still being sought, such as the rest of the
  *New York Times* 1988 series and the "thirty incidents" report, are tracked as
  [issues labelled `source-gap`](https://github.com/Robin-IA/savannah-river-plant-explorer/issues?q=label%3Asource-gap).
  Unsourced facts are kept out of the story.

## How it was built

### The research

Every source was found and checked live on 6 November 2026 with
`archive.org/advancedsearch.php`, archive.org full-text search, the
`archive.org/metadata` API, the Wayback CDX server, the Archive-It partner
API and the OSTI API. A source is labelled **DL** when its identifier matches
Democracy's Library's `search_collection` scope expression; every DL and IA
label was re-tested in a second, independent pass, which moved two items from
DL to IA. Each Wayback capture was replayed and each outside link opened.
The notes for each source, including what was and was not read, are in
`content/sources-act1.md`, `sources-act2.md` and `sources-act3.md`.

### The code

- `content/` is the source of truth; every page is generated from it:
  `story.md` and `sources-act1.md` to `sources-act3.md` (Markdown),
  `timeline.json` (each event and reactor span, with the same source as in
  the story), `about.html` (the About page's body) and `disagree.md` (where
  sources disagree, shown on the About page).
- `build/build.py` writes `index.html`, `timeline.html`, `sources.html`,
  `about.html`, `data/sources.json` and `data/timeline.json`. It needs
  Python 3 and the `markdown` package, pinned in `requirements.txt`. It
  refuses to write a page with a link that is not http(s), `mailto:`, an
  anchor or one of the explorer's own files. The holder chart and the timeline
  are SVG drawn by the script; the banner is a detail of the DOE site map
  (`img/banner-map.jpg`).
- `style.css` and three small scripts are written by hand: `search.js` (the
  story page's search), `timeline.js` (tooltips and holder filters) and
  `app.js` (the sources filters). Every page reads completely without them.
- `img/` holds the two logos and six public-domain images from Wikimedia
  Commons (a Department of Energy map of the site, a DOE reactor diagram, a
  DOE chart of plutonium production by year, two DOE photographs from about
  1970 and 1972, and a 2006 NASA photograph of the site from the ISS),
  resized for the web. Each is credited in its caption and on the About page.
- Holder colours come from a validated categorical palette (blue, green,
  violet, amber, magenta, and gray for "held elsewhere"); shapes and text labels
  carry the same information, so nothing depends on colour alone.
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
2026. Robin chose the story and how sources are labelled; Claude did the
searching, drafted the story and wrote the code. Each commit names Claude as
co-author.

Feedback? Email robin.fay@archive.org with the subject
*Feedback about Explorers: Bomb Making: A History of the Savannah River Plant*.
