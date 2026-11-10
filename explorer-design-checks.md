# Explorer design checks

**Checked November 9, 2026** for Robin-IA/savannah-river-plant-explorer against the explorer best practices ([internetarchivecanada/Documentation-Explorer-Best-Practices](https://github.com/internetarchivecanada/Documentation-Explorer-Best-Practices)).

**Status: passing.** Nothing missing. 11 to look at by eye. 0 optional to decide.

Accessibility, security and code validity are in [security-accessibility-checks.md](security-accessibility-checks.md).

## Basis

| | Item | Detail |
|---|---|---|
| pass | Best-practices guide | checks match internetarchivecanada/Documentation-Explorer-Best-Practices as of 70b946d |

## Repository

| | Item | Detail |
|---|---|---|
| pass | Repository description | Atomic History: The Savannah River Plant Story: from 1950 to a site still cleaning up its past and gearing up for new weapons work, told from government resources in Democracy's Library, the Wayback Machine and Internet Archive collections. By Robin Fay, Democracy's Library. Reach out to collaborate! |
| pass | Topic labels | collections, democracys-library, explorers, government-resources, nuclear-weapons |
| pass | Public | public |
| pass | GitHub Pages | https://robin-ia.github.io/savannah-river-plant-explorer/ |
| pass | Website link on the repository | https://internetarchivecanada.github.io/Explorer-Atomic-History-SRS-Story/ |
| pass | README: what it does | heading “what it does” |
| pass | README: how it was built | heading “how it was built” |
| look | README: how to use it | no section; required only for a tool |

## Requirements on the page

| | Item | Detail |
|---|---|---|
| pass | Title: <title> | Atomic History: The Savannah River Story |
| pass | Title: visible <h1> | Atomic History: The Savannah River Story |
| pass | Brief description | The Savannah River Plant in South Carolina made plutonium and tritium for American nuclear… |
| pass | About page | about.html |
| look | About: source of materials | names wayback machine, archive.org, internet archive, democracy's library: check it says where the items come from |
| look | About: dates covered | mentions 1950, 1953, 1988, 1989, 2012, 2026: check these are the dates the material covers |
| look | About: topics covered | if applicable: read the About page |
| look | About: when the numbers were taken | no “numbers are from <date>” found: needed if the page shows counts |
| look | About: what is left out | …ed Images How It Was Built What Is Left Out Controversies Sources Where Source…: check it covers what a reader would expect |
| pass | Link to the Internet Archive | https://archive.org/ |
| look | Links to the collections | 16 link(s), e.g. https://archive.org/details/ciareadingroom: check every source collection is linked |
| pass | Internet Archive logo | alt “Internet Archive” |
| pass | Feedback? mailto | info@archive.org, subject “Democracy's Library Explorer” |
| pass | Nothing about the code on the page | no GitHub mention or link |
| look | About: what it is written in | …The story and the source lists are written in Markdown, and a short Python scrip…: check it names the language and tools |
| pass | No security or validity claims | none on the page |
| pass | Accessibility statement | …lication. Feedback? Email us Meets WCAG 2.2 Level AA accessibility (and WC… |
| pass | Democracy's Library logo | alt “Democracy's Library” |
| pass | Accessibility and security report | Status: passing. All three checks passed on 2026-11-09 at commit `33550aed47`. Nothing is open. Advisory items below are optional. |

## Optional elements

| | Item | Detail |
|---|---|---|
| look | Disclaimer | …checked live on November 6, 2026; not an official U.S. Department of Energy or Savan…: check it reads right |
| look | Source credit in the footer | footer links https://archive.org/details/democracys-library: check it reads right |
| skip | See also | declined: nothing related yet |
| look | Why the archive matters | …and twenty years of news releases, is gone from the live web and survives onl…: check it reads right |
| skip | Wayback Labs listing | declined: not yet |

Decisions about optional elements are in `explorer-design.json`.
