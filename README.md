# Bomb Making: A History of the Savannah River Plant

**A history of the Savannah River Plant in South Carolina, from 1950 to now,
told from records held in Democracy's Library, the wider Internet Archive,
the Wayback Machine and elsewhere, with every source labelled by where it
is held.** Live at **https://robin-ia.github.io/savannah-river-plant-explorer/**.

## What it does

Three pages:

- **Story** (`index.html`): the history in three acts, with a tag on every
  citation: **DL** Democracy's Library, **IA** the Internet Archive outside
  Democracy's Library, **WB** the Wayback Machine, **AIT** Archive-It, **EXT**
  held elsewhere. Each tag links to its source. The acts cover building the
  plant (1950–1969), the reactors under scrutiny (1970–1992) and the years
  after bomb making (1992 to now). The end of the story sets out where
  sources disagree.
- **Sources** (`sources.html`): all 294 sources behind the story, filterable
  by where they are held, by act and by word. The filters are kept in the URL,
  for example `sources.html?tag=WB&act=3&q=DWPF`.
- **About** (`about.html`).

**Facts:**

- **Source of materials:** archive.org items (Democracy's Library and
  others), Wayback Machine captures, Archive-It seeds, and outside holders,
  chiefly DOE's OSTI.
- **Years covered:** 1950 to 2026.
- **Size:** 294 sources: 47 DL, 102 IA, 71 WB, 1 AIT, 73 EXT. Counted
  6 November 2026.
- **Not included:** the *New York Times* 1988 series, the Hagley Du Pont
  records and the Library of Congress HAER survey were not reached; Archive-It
  captures could not be listed. Unsourced facts are kept out of the story.

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

- `content/` holds the story and the three source lists in Markdown. They
  are the source of truth; the HTML is generated from them.
- `build/build.py` turns them into `index.html`, `sources.html` and
  `data/sources.json` (every source with its act, theme, label and link).
  It needs Python 3 and the `markdown` package.
- `about.html`, `style.css` and `app.js` are written by hand. `app.js` only
  filters the sources table; both pages are complete without it.
- Published with GitHub Pages from the `main` branch, root folder.

To rebuild after editing anything in `content/`:

```bash
pip3 install markdown
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
