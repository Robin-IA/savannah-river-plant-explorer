# Security and accessibility checks

**Status: not passing.** 2 of 3 checks have open items. Each one below has a recommended fix. Make the fixes, then re-run the explorer-checks skill. This file is replaced on every run.

| | |
|---|---|
| Explorer | https://github.com/Robin-IA/savannah-river-plant-explorer |
| Commit | `093b8c58d3` on `explorer-checks` |
| Date | 2026-11-06 |
| Pages checked | `./`, `sources.html`, `sources.html?tag=DL&act=2&q=reactor`, `about.html` |
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
| Code validity | Pass | 0 | 0 | 1 |
| Code security | **Not passing** | 2 | 0 | 2 |
| Accessibility (WCAG 2.2 AA) | **Not passing** | 3 | 0 | 0 |

## What a pass means

Each check combines automated tools with a review of the code and pages against a written checklist. A pass means neither found anything open on the date and commit above. The standards are met as far as those checks can establish: it is a self-assessment, not third-party certification. Automated testing finds a minority of accessibility barriers. Testing with people who use assistive technology is still worth doing, and a change to the explorer needs a re-run.

## Code validity

No open items.

## Code security

### `S-cdcc06` The build's one dependency is not pinned

- **Must fix** · found by review · OWASP A03:2025 · ASVS V15
- **Where:** `README.md (pip3 install markdown)`

```text
build/build.py needs the markdown package; no requirements file names a version.
```

**Recommended fix:** Add requirements.txt with markdown==3.11.3 (the version the pages were built with) and point the README at pip3 install -r requirements.txt.

### `S-5ffaaf` Link addresses written into the pages are not checked for scheme

- **Must fix** · found by review · OWASP A05:2025 · ASVS V1
- **Where:** `build/build.py (first_link, build_story)`

```text
Story links go through Python-Markdown unchecked, and the build accepts any href; a javascript: URL typed into content/ would be published as a live link.
```

**Recommended fix:** In build/build.py, after rendering, check that every href in index.html and sources.html starts with https:// or http:// (or is a local page, mailto: or #anchor), and that every archive.org identifier matches [A-Za-z0-9._-]+; stop the build and name the offending link otherwise.

<details><summary>Manual checklist (6 pass, 3 fail, 11 n/a)</summary>

| Item | Result | Note |
|---|---|---|
| No secrets | pass | One commit; a search of every file for token, password and key patterns found nothing; the only address is the Feedback mailto. |
| Untrusted data is escaped | pass | No archive.org or Wayback data reaches the page at view time; build-time values from content/ go through html.escape() or Markdown. app.js writes only textContent. |
| URLs from data are safe | fail | See the url-scheme finding: hrefs come from hand-written notes but are not scheme-checked. |
| Harvested data is validated | fail | Nothing is harvested at build, but the build does not validate the identifiers and URLs it writes; same finding. |
| Third-party code is pinned | n/a | No CDN or third-party scripts; app.js is the only script. |
| No mixed content | pass | All assets are local; http: appears only in outbound links. |
| Dependencies are pinned and maintained | fail | markdown is unpinned; see finding. |
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

<details><summary>Cleared on review (1)</summary>

| Id | Item | Where | Why cleared |
|---|---|---|---|
| `S-d72901` | String rendered as markup or code (html) | `sources.html:104` | Not a script sink: sources.html is static HTML written at build time by build/build.py, and app.js never writes markup (it only sets row.hidden and count.textContent). The flagged row is generated from the hand-written research notes in content/; identifiers and hrefs pass through html.escape() in b |

</details>

## Accessibility (WCAG 2.2 AA)

### `A-f437db` Links must be distinguishable without relying on color

- **Must fix** · found by axe-core 4.14.0 · WCAG 1.4.1
- **Where:** `/ link-in-text-block`

```text
65 element(s): p:nth-child(4) > .cite:nth-child(1); p:nth-child(4) > .cite:nth-child(2); p:nth-child(4) > .cite:nth-child(3); p:nth-child(5) > .cite:nth-child(1); p:nth-child(7) > .cite:nth-child(1)
Fix any of the following:
  The link has insufficient color contrast of 2.12:1 with the surrounding text. (Minimum contrast is 3:1, link text: #1f5f9e, surrounding text: #2c2c2c)
  The link has no styling (such as underline) to distinguish it from the surrounding text
```

**Recommended fix:** Ensure links are distinguished from surrounding text in a way that does not rely on color See https://dequeuniversity.com/rules/axe/4.14/link-in-text-block?application=axeAPI

### `A-14005b` Links must be distinguishable without relying on color

- **Must fix** · found by axe-core 4.14.0 · WCAG 1.4.1
- **Where:** `/ link-in-text-block`

```text
60 element(s): p:nth-child(5) > .cite:nth-child(3); p:nth-child(5) > .cite:nth-child(4); p:nth-child(9) > .cite:nth-child(2); p:nth-child(10) > .cite:nth-child(2); p:nth-child(10) > .cite:nth-child(4)
Fix any of the following:
  Element's contrast ratio could not be determined because of element overlap

Review: Same links as A-f437db: story citations carry no underline, so they are told apart from body text by colour alone. Fixed by the same change.
```

**Recommended fix:** Ensure links are distinguished from surrounding text in a way that does not rely on color See https://dequeuniversity.com/rules/axe/4.14/link-in-text-block?application=axeAPI

### `A-7ed2a8` Page scrolls sideways at 320 px wide

- **Must fix** · found by explorer-checks · WCAG 1.4.10
- **Where:** `/sources.html`

```text
79px wider than the viewport
```

**Recommended fix:** Let content wrap at narrow widths: max-width:100% on media and tables in a scrolling container, no fixed widths over 320px. Data tables may scroll inside their own container.

<details><summary>Manual checklist (19 pass, 1 fail, 1 n/a)</summary>

| Item | Result | Note |
|---|---|---|
| 1.1.1 Non-text content | pass | Two logos, each with alt naming its link destination; no charts. |
| 1.3.1 Info and relationships | pass | h1 then h2/h3 in order; the legend is a list; the sources table has th scope=col and a caption; holder filters are a fieldset with legend. |
| 1.3.2 Meaningful sequence | pass | DOM order is header, intro, contents, article; the grid does not reorder. |
| 1.4.1 Use of color | fail | Holder tags carry text, but story citation links have no underline (A-f437db). |
| 1.4.11 Non-text contrast | pass | Inputs have #8a8a8a borders on white (3.5:1); focus ring is 3px #4b64ff. |
| 1.4.4 Resize text / 1.4.12 Text spacing | pass | Sizes in rem and em; story and About reflow at 320 px; the sources page fails reflow separately (A-7ed2a8). |
| 2.4.4 Link purpose | pass | Citation links read as holder tag plus title (for example 'WB: SRS at Fifty ch. 7'); bare DL or IA citations take their purpose from the sentence they close, which 2.4.4 allows. |
| 2.4.6 Headings and labels | pass | Headings name their acts and sections; Act and Search labels are visible. |
| 3.1.1 Language of page | pass | lang=en on all three pages; content is English. |
| 2.1.1 Keyboard | pass | Only native links, checkboxes, a select and a search input. |
| 2.1.2 No keyboard trap | pass | No widgets that hold focus. |
| 2.4.1 Bypass blocks | pass | Skip link to #main on every page, plus header, nav, main and footer landmarks. |
| 2.4.3 Focus order | pass | Follows reading order; filtering does not move focus. |
| 2.4.7 Focus visible | pass | A 3px :focus-visible outline in style.css. |
| 2.4.11 Focus not obscured | pass | No sticky header; the sticky contents column sits beside the article, not over it. |
| 2.5.8 Target size | pass | Checkboxes sit inside labels whose whole text is the target, well over 24 px wide and spaced apart. |
| 2.2.2 Pause, stop, hide | n/a | Nothing moves. |
| 3.2.2 On input | pass | Filters update the table in place; no navigation or focus change. |
| 3.3.2 Labels or instructions | pass | The Held in legend and the Act and Search labels are visible text, not placeholders. |
| 4.1.2 Name, role, value | pass | No custom widgets; nav uses aria-current=page. |
| 4.1.3 Status messages | pass | The result count is role=status with aria-live=polite. |

</details>

## Advisory (3)

Optional. These items never block a pass.

| Id | Check | Item | Where | Reference | Suggestion |
|---|---|---|---|---|---|
| `V-2a95c1` | validity | Ambiguous variable name: `l` | `build/build.py:257` |  | See https://docs.astral.sh/ruff/rules/ for this rule. |
| `S-fb15c8` | security | No content-security-policy header | `https://robin-ia.github.io/savannah-river-plant-explorer/` | A02:2025 · ASVS V3 | Set it; it limits the damage of any XSS that gets through; a <meta http-equiv> CSP works on static hosts. |
| `S-9a6baa` | security | No x-content-type-options header | `https://robin-ia.github.io/savannah-river-plant-explorer/` | A02:2025 · ASVS V3 | Set it; it stops browsers guessing content types. It has no <meta> form, so on a host that cannot set headers (GitHub Pages) it stays open; the explorer's owners decide whether that matters enough to change host. |

<!-- explorer-checks:state {"passing": false, "date": "2026-11-06", "commit": "093b8c58d39b6e98f6cce2877868e553d79fe096", "open": ["A-14005b", "A-7ed2a8", "A-f437db", "S-5ffaaf", "S-cdcc06"], "titles": {"A-f437db": "Links must be distinguishable without relying on color", "A-14005b": "Links must be distinguishable without relying on color", "A-7ed2a8": "Page scrolls sideways at 320 px wide", "S-5ffaaf": "Link addresses written into the pages are not checked for scheme", "S-cdcc06": "The build's one dependency is not pinned"}} -->
