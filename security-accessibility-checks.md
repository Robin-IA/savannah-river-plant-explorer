# Security and accessibility checks

**Status: passing.** All three checks passed on 2026-11-07 at commit `4df3f078cd`. Nothing is open. Advisory items below are optional.

| | |
|---|---|
| Explorer | https://github.com/Robin-IA/savannah-river-plant-explorer |
| Commit | `4df3f078cd` on `collapsible-menu` |
| Date | 2026-11-07 |
| Pages checked | `./`, `./?q=tritium`, `chapter-1.html`, `chapter-2.html`, `chapter-3.html`, `chapter-4.html`, `timeline.html`, `sources.html`, `sources.html?tag=DL&chapter=2&q=reactor`, `about.html` |
| Served from | repository root, served locally |
| Live site (headers) | https://robin-ia.github.io/savannah-river-plant-explorer/ |
| Standard | WCAG 2.2 Level AA |
| Security references | OWASP Top 10:2025 and ASVS 5.0.0 |
| Tools | axe-core 4.14.0, html5lib, ruff, bandit, pip-audit, headless Chromium |
| Reviewed by | Claude (claude-opus-5-5) via the explorer-checks skill |
| Skill version | 2026.11.05.8 |

## Summary

| Check | Result | Must fix | Needs review | Advisory |
|---|---|---:|---:|---:|
| Code validity | Pass | 0 | 0 | 0 |
| Code security | Pass | 0 | 0 | 1 |
| Accessibility (WCAG 2.2 AA) | Pass | 0 | 0 | 0 |

## Standards met

Checked 7 November 2026 at commit `4df3f078cd`, on the pages listed above:

- **WCAG 2.2 Level AA**: every Level A and AA success criterion, by automated tests and a manual review of each criterion (checklists under each check below).
- **WCAG 2.1 Level AA** and **WCAG 2.0 Level AA**, which WCAG 2.2 includes. 4.1.1 Parsing, dropped from 2.2 but still in 2.0 and 2.1, is covered by the code validity check (no HTML parse errors, no duplicate ids).
- These are the web content requirements of **Section 508** (US federal; WCAG 2.0 AA) and **EN 301 549** clause 9 (WCAG 2.1 AA).
- Security was checked against the OWASP Top 10:2025 risks and ASVS 5.0.0 chapters that apply to an explorer; each finding and checklist item names its category. That is not an ASVS verification at any level.

## What a pass means

Each check combines automated tools with a review of the code and pages against a written checklist. A pass means neither found anything open on the date and commit above. The standards are met as far as those checks can establish: it is a self-assessment, not third-party certification. Automated testing finds a minority of accessibility barriers. Testing with people who use assistive technology is still worth doing, and a change to the explorer needs a re-run.

## Code validity

No open items.

## Code security

No open items.

<details><summary>Manual checklist (9 pass, 0 fail, 11 n/a)</summary>

| Item | Result | Note |
|---|---|---|
| No secrets | pass | One commit; a search of every file for token, password and key patterns found nothing; the only address is the Feedback mailto. |
| Untrusted data is escaped | pass | No archive.org or Wayback data reaches the page at view time. Build-time values go through html.escape() or Markdown. search.js and timeline.js build results and tooltips with textContent and createElement only; timeline.js positions the tooltip through style.setProperty with numbers it computes. |
| URLs from data are safe | pass | build/build.py check_links() refuses, before writing any page, an href or src that is not http(s), mailto:, an anchor or one of the explorer's own files. search.js builds only '#'+id, 'timeline.html#ev-'+number and 'sources.html?q='+encodeURIComponent(query). |
| Harvested data is validated | pass | Nothing is harvested at build; the identifiers and URLs written into the pages are validated by check_links() as above. |
| Third-party code is pinned | n/a | No CDN or third-party scripts; app.js is the only script. |
| No mixed content | pass | All assets are local; http: appears only in outbound links. A Content-Security-Policy meta limits every page to its own scripts, styles and images. |
| Dependencies are pinned and maintained | pass | requirements.txt pins markdown==3.11.3; no CI workflows. |
| Dependencies have no known vulnerabilities | pass | No front-end libraries; pip-audit reported nothing. |
| Third parties a visitor's browser contacts | pass | None: images, CSS and JS are all served from the explorer. |
| What Pages publishes | pass | Repository is public by design; Pages serves content/ (the story source and research notes, meant to be public), build/ and data/sources.json. No logs or dumps. |
| Server input is validated | n/a | Static site, no server. |
| Configuration is safe to serve | n/a | Static site. |
| Errors are handled and do not leak | n/a | Static site; search is a substring filter in the browser with no query syntax. |
| Commands built from data | n/a | No subprocess calls. |
| Who can write | n/a | No contributions. |
| Fetches of submitted URLs | n/a | No contributions. |
| Scope of writes | n/a | No uploads. |
| Limits | n/a | No queue. |
| Model output is untrusted | n/a | No AI component at runtime; the story was drafted with Claude and is static, reviewed text. |
| Models are pinned | n/a | No models. |

</details>

<details><summary>Cleared on review (4)</summary>

| Id | Item | Where | Why cleared |
|---|---|---|---|
| `S-d1a00b` | String rendered as markup or code (html) | `sources.html:202` | Not a script sink: sources.html is static HTML written at build time by build/build.py, and app.js never writes markup (it only sets row.hidden and count.textContent). The flagged rows come from the hand-written source notes in content/; identifiers and hrefs pass through html.escape() in build_sour |
| `S-f296f3` | String rendered as markup or code (html) | `sources.html:211` | Not a script sink: sources.html is static HTML written at build time by build/build.py, and app.js never writes markup (it only sets row.hidden and count.textContent). The flagged rows come from the hand-written source notes in content/; identifiers and hrefs pass through html.escape() in build_sour |
| `S-b18eba` | String rendered as markup or code (html) | `sources.html:224` | Not a script sink: sources.html is static HTML written at build time by build/build.py, and app.js never writes markup (it only sets row.hidden and count.textContent). The flagged rows come from the hand-written source notes in content/; identifiers and hrefs pass through html.escape() in build_sour |
| `S-1cd70a` | String rendered as markup or code (html) | `sources.html:234` | Not a script sink: sources.html is static HTML written at build time by build/build.py, and app.js never writes markup (it only sets row.hidden and count.textContent). The flagged rows come from the hand-written source notes in content/; identifiers and hrefs pass through html.escape() in build_sour |

</details>

## Accessibility (WCAG 2.2 AA)

No open items.

<details><summary>Manual checklist (20 pass, 0 fail, 1 n/a)</summary>

| Item | Result | Note |
|---|---|---|
| 1.1.1 Non-text content | pass | Logos have alt naming their destination; the banner map is decorative (alt="") and the same map appears in the story with full alt text; the holder chart has a title and a visually hidden data table; timeline marks are links whose names give date, event and holder, with the same events as a list. Th |
| 1.3.1 Info and relationships | pass | h1 in the banner, then h2 and h3 in order; legends are lists; the sources and reactor tables have th scope; filters are a fieldset with legend; the timeline filters are a labelled group of toggle buttons. Holder tags include OL (Open Library) with its own text label. |
| 1.3.2 Meaningful sequence | pass | DOM order is header, intro, contents, article; the grid does not reorder. |
| 1.4.1 Use of color | pass | Holder tags carry text; timeline marks differ in shape (circle, square, diamond, triangle, ring) as well as colour; story citations are underlined. |
| 1.4.11 Non-text contrast | pass | Inputs have #8a8a8a borders on white (3.5:1); focus ring is 3px #4b64ff. |
| 1.4.4 Resize text / 1.4.12 Text spacing | pass | Sizes in rem and em; every page reflows at 320 px with no sideways page scroll. Figures are centred blocks between paragraphs, never wider than their image, at their true proportions. |
| 2.4.4 Link purpose | pass | Citation links read as holder tag plus title (for example 'WB: SRS at Fifty ch. 7'); bare DL or IA citations take their purpose from the sentence they close, which 2.4.4 allows. Chapter cards and the chapter list link with the chapter's full title; previous/next links name the chapter they lead to. |
| 2.4.6 Headings and labels | pass | Each page has one h1 in the banner; chapter pages use h2 for their sections; the home page's chapter cards are h2 sections; Chapter and Search labels are visible on the sources page. |
| 3.1.1 Language of page | pass | lang=en on all three pages; content is English. |
| 2.1.1 Keyboard | pass | Native links, buttons, checkboxes, select and inputs only. Timeline marks are SVG links in the tab order; the holder filters are buttons. The holder index buttons and the chart's segment links are ordinary links in the tab order. |
| 2.1.2 No keyboard trap | pass | No widgets that hold focus. |
| 2.4.1 Bypass blocks | pass | Skip link to #main on every page; header, nav, main and footer landmarks; on chapter pages the chapter list and the previous/next links are separately named navigation landmarks. |
| 2.4.3 Focus order | pass | Follows reading order; filtering does not move focus. |
| 2.4.7 Focus visible | pass | A 3px :focus-visible outline everywhere; timeline marks and the holder chart's segment links get an outline and a blue stroke on focus; the holder index buttons use the default outline. |
| 2.4.11 Focus not obscured | pass | No sticky header; the sticky contents and side panel sit beside the story, not over it; the timeline tooltip sits above the focused mark, not on it. |
| 2.5.8 Target size | pass | Checkboxes sit inside labels whose whole text is the target, well over 24 px wide and spaced apart. |
| 2.2.2 Pause, stop, hide | n/a | Nothing moves. |
| 3.2.2 On input | pass | Filters and search update results in place; submitting the search scrolls to the results panel, which the user asked for by submitting. |
| 3.3.2 Labels or instructions | pass | The Held in legend and the Act and Search labels are visible text, not placeholders. |
| 4.1.2 Name, role, value | pass | Timeline filters are buttons with aria-pressed that follows their state; the chapter menu uses native details/summary, so its open or closed state is exposed by the browser; nav uses aria-current=page; filtered-out marks leave the tab order. |
| 4.1.3 Status messages | pass | The sources count and the home page search's result count are role=status with aria-live=polite; search does not move focus while typing. |

</details>

<details><summary>Cleared on review (8)</summary>

| Id | Item | Where | Why cleared |
|---|---|---|---|
| `A-6c64c1` | Elements must meet minimum color contrast ratio thresholds | `/ color-contrast` | The banner is a toned map image under a CSS gradient veil (#0c1f2e), which axe cannot resolve. Checked by calculation against the lightest pixel in img/banner-map.jpg, #e3e1ec: the veil is solid to 34% of the width, 0.88 at 48% and 0.8 by about 52%. All banner text (logos, kicker, title, lede, searc |
| `A-1ac6d2` | Elements must meet minimum color contrast ratio thresholds | `/chapter-1.html color-contrast` | The banner is a toned map image under a CSS gradient veil (#0c1f2e), which axe cannot resolve. Checked by calculation against the lightest pixel in img/banner-map.jpg, #e3e1ec: the veil is solid to 34% of the width, 0.88 at 48% and 0.8 by about 52%. All banner text (logos, kicker, title, lede, searc |
| `A-83beea` | Elements must meet minimum color contrast ratio thresholds | `/chapter-2.html color-contrast` | The banner is a toned map image under a CSS gradient veil (#0c1f2e), which axe cannot resolve. Checked by calculation against the lightest pixel in img/banner-map.jpg, #e3e1ec: the veil is solid to 34% of the width, 0.88 at 48% and 0.8 by about 52%. All banner text (logos, kicker, title, lede, searc |
| `A-8e2348` | Elements must meet minimum color contrast ratio thresholds | `/chapter-3.html color-contrast` | The banner is a toned map image under a CSS gradient veil (#0c1f2e), which axe cannot resolve. Checked by calculation against the lightest pixel in img/banner-map.jpg, #e3e1ec: the veil is solid to 34% of the width, 0.88 at 48% and 0.8 by about 52%. All banner text (logos, kicker, title, lede, searc |
| `A-5a3e6f` | Elements must meet minimum color contrast ratio thresholds | `/chapter-4.html color-contrast` | The banner is a toned map image under a CSS gradient veil (#0c1f2e), which axe cannot resolve. Checked by calculation against the lightest pixel in img/banner-map.jpg, #e3e1ec: the veil is solid to 34% of the width, 0.88 at 48% and 0.8 by about 52%. All banner text (logos, kicker, title, lede, searc |
| `A-fcf340` | Elements must meet minimum color contrast ratio thresholds | `/timeline.html color-contrast` | The banner is a toned map image under a CSS gradient veil (#0c1f2e), which axe cannot resolve. Checked by calculation against the lightest pixel in img/banner-map.jpg, #e3e1ec: the veil is solid to 34% of the width, 0.88 at 48% and 0.8 by about 52%. All banner text (logos, kicker, title, lede, searc |
| `A-2d464c` | Elements must meet minimum color contrast ratio thresholds | `/sources.html color-contrast` | The banner is a toned map image under a CSS gradient veil (#0c1f2e), which axe cannot resolve. Checked by calculation against the lightest pixel in img/banner-map.jpg, #e3e1ec: the veil is solid to 34% of the width, 0.88 at 48% and 0.8 by about 52%. All banner text (logos, kicker, title, lede, searc |
| `A-2c8611` | Elements must meet minimum color contrast ratio thresholds | `/about.html color-contrast` | The banner is a toned map image under a CSS gradient veil (#0c1f2e), which axe cannot resolve. Checked by calculation against the lightest pixel in img/banner-map.jpg, #e3e1ec: the veil is solid to 34% of the width, 0.88 at 48% and 0.8 by about 52%. All banner text (logos, kicker, title, lede, searc |

</details>

## Advisory (1)

Optional. These items never block a pass.

| Id | Check | Item | Where | Reference | Suggestion |
|---|---|---|---|---|---|
| `S-9a6baa` | security | No x-content-type-options header | `https://robin-ia.github.io/savannah-river-plant-explorer/` | A02:2025 · ASVS V3 | Set it; it stops browsers guessing content types. It has no <meta> form, so on a host that cannot set headers (GitHub Pages) it stays open; the explorer's owners decide whether that matters enough to change host. |

<!-- explorer-checks:state {"passing": true, "date": "2026-11-07", "commit": "4df3f078cd5f71e8ec7af5156f997c09ab05d59c", "open": [], "titles": {}} -->
