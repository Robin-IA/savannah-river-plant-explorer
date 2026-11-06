# Bomb Making, Act 1 (1950–1969): sources

> Research notes behind [README.md](README.md), compiled 6 November 2026.
> Every identifier and URL was checked live that day. Every archive.org
> identifier labelled DL or IA was re-tested against the Democracy's Library
> scope expression in a second, independent pass; corrections from that pass
> are marked in place. "The brief" means the research instructions.

Every source was checked on **2026-11-06**:
- archive.org items: `archive.org/metadata/<id>` returned a `metadata` object.
- DL membership: tested with `identifier:X AND (<DL scope expression>)`. DL = 1 hit. Anything not labelled DL returned 0.
- Wayback: the capture was fetched (id_ replay, HTTP 200).
- External: HTTP 200, or the OSTI API returned the record and `osti.gov/biblio/<id>` returned 200.

"lending" means the item is in `inlibrary`. "printdisabled only" means it is not in `inlibrary`.

Where an item is cited for what it says, the claim comes from the full-text-search highlight I saw. I did not read whole items unless noted.

**Labels:** DL = Democracy's Library · IA = archive.org, not DL · OL = Open Library · WB = Wayback · AIT = Archive-It · EXT = held outside IA.

---

## 1. Land, site selection and displacement

| Label | Identifier / URL | Title | Date | Holder / collection | Contribution |
|---|---|---|---|---|---|
| WB | https://web.archive.org/web/20250524063547/https://www.srs.gov/general/about/50anniv/SRSat50.pdf | Mary Beth Reed et al., *Savannah River Site at Fifty* (full book PDF, 55.9 MB) | 2002 | srs.gov (dead), Wayback | The standard official history. **Not on IA as a book** (Open Library has no `ia`); it survives only as Wayback captures. The %PDF header was verified. |
| WB | https://web.archive.org/web/20060909012514/http://www.srs.gov:80/general/about/50anniv/CONTENTS.pdf | *SRS at Fifty*, contents | 2002 | Wayback | The chapter map: ch. 4–10 "Savannah River Project (1950–1956)", ch. 11 Startup, ch. 12 Heavy water, ch. 13 Reactors, ch. 14 Separations, ch. 15 SRL, ch. 17 Early Stewardship. Appendices list churches and cemeteries within the acquisition area. |
| WB | https://web.archive.org/web/20161222003153/http://www.srs.gov/general/about/50anniv/Chapter%2007.pdf | *SRS at Fifty* ch. 7, "Site Selection" | 2002 | Wayback | The Du Pont site survey (Plant 124, Charles Topping), the 700-sq-mi exclusion logic and the towns on the site, with populations. |
| WB | https://web.archive.org/web/20070928081912/http://www.srs.gov/general/about/50anniv/Chapter%2008.pdf | *SRS at Fifty* ch. 8, "Changing Identity" | 2002 | Wayback | The 28 Nov 1950 announcement text, 1,500 families, 6,000–8,000 people, appraisals, condemnation, grave removal, a segregated Ellenton meeting and a displaced farmer's diary. **The key secondary source for displacement.** |
| WB | https://web.archive.org/web/20051025030030/http://www.srs.gov:80/general/about/history1.htm | SRS – History Highlights | captured 2005 | srs.gov, Wayback | The official timeline of 1950s milestones. Only 2021 captures exist for `srs-1950.htm` and `srs-1960.htm`. |
| WB | https://web.archive.org/web/20210622195758/https://www.srs.gov/general/about/srs-1950.htm | SRS history, 1950s page | captured 2021 | Wayback | Covers the Nelson/Mason appointments, the Truman letter to Du Pont, CMX, 305-M, R startup 1953 and the first plutonium and tritium shipments. |
| WB | https://web.archive.org/web/20141020061628/http://www.srarp.org:80/former-towns/ | SRARP, "Former Towns" web exhibit | captured 2014 | Wayback (srarp.org is dead) | Says "approximately 5000 people were relocated". Describes the oral-history and photo collecting begun in 1990 and the 8 photo-gallery series. |
| WB | https://web.archive.org/web/20150920142228/http://www.srarp.org/pdf_documents/Memories%20of%20Home/Ellenton/00_Preface-1.pdf | SRARP Heritage Series #2, *Memories of Home: Reminiscences of Ellenton* (chapter PDFs 00–12) | 1996 | Wayback | Ellenton oral history. The PDF is valid but image-only with no text layer. The CDX lists all chapters. |
| WB | https://web.archive.org/web/20141020060536/http://www.srarp.org:80/former-towns/memories-of-home/ellenton-sc-my-life-its-death-hs4-1999/ | SRARP Heritage Series #4, *Ellenton, SC: My life…its death* (part PDFs) | 1999 | Wayback | A first-person Ellenton memoir. Open Library lists *Ellenton, S.C.* by Sid O'Berry (SRARP, 1999), probably the same work (unconfirmed). |
| WB | https://web.archive.org/web/20141020061238/http://www.srarp.org:80/former-towns/displaced/ | SRARP page for the documentary *Displaced* | captured 2014 | Wayback | Points to a documentary on the displaced towns. I could not resolve the film's own site because Wayback rate-limited me. |
| EXT: OSTI | https://www.osti.gov/biblio/272945 | Browder & Brooks, *Memories of home: reminiscences of Ellenton* (DOE/SR/15199-T3) | 1996-08 | OSTI (citation only) | The abstract states the 28 Nov 1950 announcement and that Ellenton was one of six towns displaced. |
| EXT: OSTI | https://www.osti.gov/biblio/10171577 | Browder & Brooks, *Memories of home: Dunbarton and Meyers Mill remembered* (DOE/SR/15199-T2) | 1993 | OSTI (citation only) | Oral history of Dunbarton and Meyers Mill. Its Wayback chapter PDFs are in the CDX, but the replay of 00_Preface returned 404 on 2026-11-06. |
| EXT: OSTI | https://www.osti.gov/biblio/10135682 | Brooks & Crass, *A desperate poor country: History and settlement patterning on the Savannah River Site* (DOE/SR/15199-T1) | 1991 | OSTI (citation) | Pre-1950 settlement and land tenure on the site: the "before" picture. |
| IA (lending) | `maninthickleadsu0000lang` | Daniel Lang, *The Man in the Thick Lead Suit* | 1954 | inlibrary | A contemporary New Yorker-style reportage of Ellenton ("pop. 700"). It covers farmers' relocation, Agriculture Department help and the "hydrogen-bomb counterpart" of Oak Ridge. Also `fromhiroshimatom00lang` (*From Hiroshima to the Moon*, 1959, lending). |
| IA | `sim_reporter_1951-03-06_4_5` | *The Reporter*, 6 Mar 1951 | 1951-03-06 | sim_microfilm | "The peaceful doom of Ellenton, South Carolina" (p. 17). It quotes Audley H. Ward on small white farmers. The highlight sits next to "George McMillan", but I have not confirmed the byline. |
| IA | `sim_jet_1951-12-20_1_8` | *Jet*, 20 Dec 1951 | 1951-12-20 | sim_microfilm | A Black press view: "Negro families" moving entire homes to New Ellenton, 15 miles away. |
| IA (lending) | `bwb_T5-ANV-709` | Murray, Bowens & Hogrefe, *Group Work in Community Life* | 1954 | inlibrary | Has a section on New Ellenton, the replacement town, and names Dunbarton, "Meyers Hill" [sic] and Ellenton as the three villages enclosed. |
| IA (lending) | `impactoflargeins0000unse` (also `_k9c5`, 1968 ed. `impactoflargeins0000unse_r4m1`) | *The Impact of Large Installations on Nearby Areas* (HHFA-sponsored) | 1965 | inlibrary | A Savannah River case study: "about 30 white families and 120 Negro families relocated near New Ellenton". Also housing tables and the Du Pont/AEC housing need. |
| IA (lending) | `coontaillagoonce00cass` | Louis Cassels, *Coontail Lagoon: A Celebration of Life* | 1974 | inlibrary | An Ellenton-born UPI writer: "not even ruins to mark where my hometown, Ellenton, stood". |
| OL | Open Library OL9858335W | Louise Cassels, *The Unexpected Exodus* (Sand Hill Press 1971; USC Press 2007) | 1971 | Open Library catalogue record; no copy to read or borrow (checked 2026-11-06) | The classic Ellenton exodus memoir. `localfamilyhisto0000cote` (IA, printdisabled only) cites the 1971 edition. |
| IA (lending) | `southcarolina00edwa` | Sally Edwards, *South Carolina* | 1968 | inlibrary | Popular-history framing: "Ellenton and Dunbarton … were evacuated". |
| IA (printdisabled only) | `killemleavesearc0000mcbr` | James McBride, *Kill 'Em and Leave* | 2016 | internetarchivebooks | James Brown's kin among Black sharecroppers forced to evacuate Ellenton. A literary angle on Black displacement. |
| IA (printdisabled only) | `isbn_9781941069042` | Don Bozeman, *Blackberries in the Summer* | 2014 | internetarchivebooks | A memoir: in 1952 "the entire property, along with the city of Ellenton … fell" to the plant. Covers local racial hierarchy. |
| IA (lending) | `dreamsparables0000synn` | Jim Synnott, *Dreams & Parables* | 1994 | inlibrary | "The government promised Ellenton would be replaced with New Ellenton…" (fiction or memoir; genre unconfirmed). |
| IA (lending) | `swallowsavannahs0000burg` | Ken Burger, *Swallow Savannah* | 2009 | inlibrary | A novel set around the bomb plant. Literary context only. |
| IA (newspaper) | `per_atlanta-constitution_1950-11-29_83_142` | *Atlanta Constitution*, 29 Nov 1950 | 1950-11-29 | microfilm/newspapers | Day-after coverage of the announcement: "Woman Finds Ellenton Is No Place To Hide", with a map of Ellenton and Dunbarton. |
| IA (newspaper) | `victoriadailytimes1950-11-29` | *Victoria Daily Times*, 29 Nov 1950 | 1950-11-29 | universityofvictorialibraries | The announcement as international wire news. It matched "H-bomb plant" Ellenton. |
| IA | `sim_newsweek-us_1950-12-25_36_26` · `sim_town-journal_1950-12-27_57` (*Pathfinder*) · `per_daily-worker_daily-worker_1950-12-12_27_247` | National magazine and press coverage | Dec 1950 | sim_microfilm / newspapers | Mainstream, rural-weekly and Communist-press framings of the "H-bomb plant" at Ellenton. Each matched the FTS query; I did not read the articles. |
| IA (newspaper) | `circleville-herald-1952-02-28` · `gettysburg-times-1952-02-29` | Small-town dailies | 28–29 Feb 1952 | newspaperarchive | Both matched "H-bomb plant" Ellenton on the eve of the town's final vacating. Possibly an AP last-days story; the content was not read. |
| DL | `sim_united-states-congress-hearings-prints-and-reports_1951-11-27` | US Congress, Hearings, Prints & Reports, 27 Nov 1951 | 1951-11-27 | sim_microfilm, DL | Land-acquisition progress: "A total of 265 tracts is being acquired in Ellenton". Also has Du Pont hourly wage schedules for Project 8980. |
| DL | `sim_united-states-congress-hearings-prints-and-reports_june-16-17-22-and-23-1953` | Hearings, June 1953 | 1953 | sim_microfilm, DL | An "inequity" excluding New Ellenton from aid eligibility, i.e. the aftermath for the relocated town. |
| DL | `micro_IA41152659_0884` | *Environmental Consequences of the Proposed Restart of the L-Reactor*, Senate Armed Services hearing, North Augusta | 1983-02-09 | USGovernmentDocuments | Out of period but useful: it includes testimony from the City of New Ellenton and shows L's 1954–68 operating span. |
| IA | `AikenCC102010` | James CSRA Coin Club newsletter | 2010-10 | newmannumismatic | A local-memory note: "Ellenton and Dumbarton had to be moved". This is low-weight local history. |
| EXT: OSTI | https://www.osti.gov/biblio/807799 | White & Gaines, *The Savannah River: Site Description, Land Use and Management History* | 2000 | OSTI (citation) | Land-use history of the acquired tract (farming and timber), leading into the Forest Service era. |
| DL | `savannahSC1990` | *Soil Survey of Savannah River Plant Area* (USDA) | 1990 | fedlink, DL | The physical landscape of the taken land. It is a peripheral source, but it is DL. |

## 2. Du Pont, construction workforce and the regional boom

| Label | Identifier / URL | Title | Date | Holder / collection | Contribution |
|---|---|---|---|---|---|
| WB | (ch. 4–6, 9, 10 are in `SRSat50.pdf` above; no separate captures exist) | *SRS at Fifty* ch. 4 "Large-Scale Gamble", ch. 5 "Like Picking Babe Ruth in His Prime", ch. 6 "Boomers, Boosters, and Economic Statesmen", ch. 9 "One Mighty Force" | 2002 | Wayback | Du Pont's selection, the boom towns and construction. |
| IA | `sim_atomic-energy-newsletter_1950-12-05_4_8` | *Atomic Energy Newsletter*, 5 Dec 1950 | 1950-12-05 | sim_microfilm | A contemporary trade report: 18 miles of river frontage, the "Savannah River Plant" name and the first Du Pont officials on the scene. |
| IA (lending) | `atomicshield19470000hewl` | Hewlett & Duncan, *Atomic Shield, 1947/1952* (official AEC history) | 1990 repr. | inlibrary | The AEC–Du Pont negotiation and Du Pont's terms for the Savannah River assignment. |
| IA (lending) | `nylonbombsdupont0000ndia` | Pap Ndiaye, *Nylon and Bombs: DuPont and the March of Modern America* | 2007 | inlibrary | Corporate history of Du Pont's nuclear role. |
| IA | `sim_monthly-labor-review_1952-06_74_6`, `…1952-07_75_1`, `…1952-08_75_2`, `…1952-09_75_3` | M. Mead Smith, "Labor and the Savannah River AEC Project", parts I–IV (Manpower & Wages; Unionization & Industrial Relations; Housing; Community Facilities) | Jun–Sep 1952 | sim_microfilm | **The best primary source on the construction workforce.** It also reprinted as BLS Bulletin 1100 (1952), per `sim_monthly-labor-review_1953-01_76_1`. It records Black tenant farmers arriving in Augusta in search of jobs (May 1951) and an NAACP meeting in Aiken (Sept 1951) charging Du Pont over hiring. |
| IA | `bulletinofunited1095unse` | BLS Bulletin volume containing no. 1100 | n.d. | university_of_illinois_urbana-champaign | Bulletin 1100 is bound in this volume. |
| DL | `sim_united-states-congress-hearings-prints-and-reports_1951-02-28_0` | Defense Housing Act hearings, Part 2, **hearing held in Aiken, S.C.**, 28 Feb 1951 | 1951-02-28 | sim_microfilm, DL | Local testimony on housing the construction force. It projects a construction-worker peak around the beginning of 1953. |
| DL | `sim_united-states-congress-hearings-prints-and-reports_1951-02-16_1` | Hearings, 16 Feb 1951 | 1951-02-16 | DL | "Savannah River Housing": the number of Du Pont construction workers needed. |
| DL | `sim_united-states-congress-hearings-prints-and-reports_1952-01-30_2` | Hearings, 30 Jan 1952 | 1952-01-30 | DL | Sections on "Misconduct at Savannah River", "A Savannah River contract problem" and the "Du Pont Office Building". Labor and contract problems. |
| DL | `sim_united-states-congress-hearings-prints-and-reports_1952-02-22_3` | Hearings, 22 Feb 1952 | 1952-02-22 | DL | Witnesses include the mayors of New Ellenton (Arthur Foreman) and Augusta (Hugh L. Hamilton), plus North Augusta. Covers dormitories at Barnwell for single construction workers and Du Pont's cooperation on housing. |
| DL | `sim_united-states-congress-hearings-prints-and-reports_november-5-9-1951_13` | Hearings, 5–9 Nov 1951 | 1951-11 | DL | The top full-text hit for "Savannah River Project". Content not read. |
| DL | `sim_congressional-record-proceedings-and-debates_october-03-20-1951_97` | *Congressional Record*, 3–20 Oct 1951 | 1951-10 | DL | Matched "Savannah River" + JCAE + Ellenton. Content not read. |
| DL | `micro_IA40386417_2698` | *Lyles & Lang Construction Co. v. E. I. du Pont de Nemours & Co.*, 349 U.S. 956 (1955) | 1955 | us-supreme-court, DL | Litigation by a Savannah River housing contractor (House & Home names Lyles & Lang as builder of the project housing). |
| DL | `micro_IA40385001_0003` | *Livingston v. United States*, 364 U.S. 281 (1960) | 1960 | us-supreme-court, DL | South Carolina's attempt to tax Du Pont's work under the AEC contract: the legal status of the "government-owned, contractor-operated" plant. |
| IA | `usmodernist-HH-1953-08` (also `sim_housing_1953-08_4_2`) | *House & Home*, Aug 1953 | 1953-08 | usmodernist | AEC housing: 4,000 trailers for married workers and dormitories for single ones. Lyles & Lang built the Savannah River housing. Workers chose to live in only two towns. |
| IA | `sim_enr_1951-09-20_147_12`, `sim_enr_1952-06-19_148_25`, `sim_enr_1952-07-31_149_5` | *Engineering News-Record* | 1951–52 | sim_microfilm | Construction-press coverage. The 19 Jun 1952 issue covers Gross-Morton "housing the thousands" at Aiken. |
| IA | `sim_contractors-and-engineers-magazine_1951-07_48_7` · `sim_chemical-week_1952-03-15_70_11` · `sim_chemical-week_1952-07-05_71_1` · `sim_popular-science_1952-06_160_6` | Trade and popular press | 1951–52 | sim_microfilm | Each matched "H-bomb plant"/Dunbarton queries. Engineering and popular framings; content not read. |
| IA (newspaper) | `per_atlanta-constitution_1951-04-30_83_270` · `per_atlanta-constitution_1951-06-21_84_5` · `per_atlanta-constitution_1951-11-26_84_137` | *Atlanta Constitution* | 1951 | microfilm | Apr 1951: a tour of the "Savannah River Project" and Knox pre-fab housing. Jun 1951: "Buildings rise at new hydrogen bomb plant". |
| IA | `per_tuskegee-institute-news-clippings-file_employment_1951_16c` | Tuskegee Institute News Clippings File: Employment 1951 | 1951 | uncg_microfilm | Black-press employment clippings that mention the Aiken boom. |
| IA (lending) | `yesterdaysaugust0000rowl` | A. Ray Rowland, *Yesterday's Augusta* | 1976 | inlibrary | Augusta's view of the "tremendous" growth driven by Du Pont's plant. |
| IA (lending) | `augustachronicle0000kenn` | Earl L. Bell & Kenneth C. Crabbe, *The Augusta Chronicle: Indomitable Voice of Dixie, 1785–1960* | 1960 | inlibrary | The regional newspaper's own history up to 1960. |
| IA (lending) | `circlingsavannah0000mack` | Tom Mack, *Circling the Savannah* | 2009 | inlibrary | Cultural landmarks of the CSRA (Central Savannah River Area), including the SRS area. |
| IA (lending) | `stateofheartsout0000unse` | *State of the Heart: South Carolina Writers on the Places They Love* | 2013 | inlibrary | Includes an essay with SRP-construction photos: "Moving earth to defend a nation". |
| IA (lending) | `topsecrettourism0000helm` | Harry L. Helms, *Top Secret Tourism* | 2007 | inlibrary | A lay description of the F and H canyons. |
| IA | `0738_Partners_in_Progress_22_31_21_00` | *Partners in Progress* (Charles O. Beeland Productions film) | c.1954 | prelinger | Matched the metadata search for "savannah river plant". Its subject was not confirmed by viewing. |
| IA | `26052TheMarchOfTime` | *The March of Time* 26052 (film) | n.d. | PeriscopeFilm | Subject-tagged "Savannah River Site". Not viewed. |
| EXT: OSTI | https://www.osti.gov/biblio/10159481 | *Savannah River Plant construction [100 Area History]*, Vol. 3 (DPES-1403) | 1957 | OSTI, **full text** | Du Pont's own construction history of the five reactor areas. |
| EXT: OSTI | https://www.osti.gov/biblio/10161087 | *SRP – Project 8980 engineering and design history*, Vol. II (DPE-971) | 1957 | OSTI, full text | Reactor-area design history. |
| EXT: OSTI | https://www.osti.gov/biblio/10158632 · /10161230 · /10161320 | Project 8980 engineering & design histories: Vol. 4 (300/700 Areas), Vol. 5 (400-D heavy water), Vol. 6 (power) | 1957 | OSTI, full text | The fuel fabrication, heavy-water and power plant design records. |
| EXT: OSTI | https://www.osti.gov/biblio/10151705 | *SRP history: plantwide activities, July 1954–Dec 1972* (DPSP-55-454-5) | 1972 | OSTI, full text | A year-by-year account of personnel and plant-wide events. |
| WB | https://web.archive.org/web/20250917151711/https://findingaids.hagley.org/repositories/3/resources/1264 | Hagley Museum and Library, *E. I. du Pont de Nemours & Company, Atomic Energy Division records*, 1942–1989 (Acc. 1957, 80 linear ft), finding aid | captured 2025 | Hagley (live site behind a bot check), Wayback | Series II, Savannah River Project administrative records: contracts, Manufacturing Division files, policy correspondence from 1950 (site selection, design and construction, environment and community impact, safety, waste disposal) and monthly reports. **Verified 2026-11-06 through the Wayback capture**; the live site returned HTTP 202 (a bot challenge). Also corroborated by the DOE OHRE finding aid. A PDF of the guide is at https://hagley-aspace-pdf.s3.amazonaws.com/1957.pdf (200). |
| WB | https://web.archive.org/web/20251216181520/https://findingaids.hagley.org/repositories/2/resources/224 | Hagley, *DuPont Company Atomic Energy Division, Savannah River Plant photographs and films*, 1951–1984 (Acc. 1989-335, 20 linear ft), finding aid | captured 2025 | Hagley, Wayback | Construction and progress views and technical photographs: 1,412 8×10 prints and 388 lantern slides. Verified 2026-11-06 through the Wayback capture. PDF guide: https://hagley-aspace-pdf.s3.amazonaws.com/1989.335.pdf (200). |
| OL | Open Library OL19537992W | Kari Frederickson, *Cold War Dixie: Militarization and Modernization in the American South* (UGA Press) | 2013 | Open Library catalogue record; no copy to read or borrow (checked 2026-11-06) | The main scholarly study of SRP and the Aiken/Barnwell transformation. No IA copy; ISBN 9780820345192. |
| OL | Open Library OL4493022W | *History of Du Pont at the Savannah River Plant* (E. I. du Pont de Nemours, ISBN 0934870276) | 1990 | Open Library catalogue record; no copy to read or borrow (checked 2026-11-06) | The company's own history. |

## 3. Reactors, separations, heavy water and production

| Label | Identifier / URL | Title | Date | Holder / collection | Contribution |
|---|---|---|---|---|---|
| WB | https://web.archive.org/web/20250804145026/https://www.srs.gov/general/about/50anniv/Chapter%2011.pdf | *SRS at Fifty* ch. 11, "Startup and First Years in Operation (1953–1963)" | 2002 | Wayback | R critical Dec 1953, P on 20 Feb 1954, all five operating by end of March 1955, a first-plutonium-shipment photo dated 28 Dec 1954, and C reactor's power history. |
| WB | https://web.archive.org/web/20251217165229/https://www.srs.gov/general/about/50anniv/Chapter%2012.pdf · https://web.archive.org/web/20070928081926/http://www.srs.gov/general/about/50anniv/Chapter%2013.pdf · https://web.archive.org/web/20150906112958/http://www.srs.gov:80/general/about/50anniv/Chapter%2014.pdf | *SRS at Fifty* ch. 12 Heavy-Water Production, ch. 13 Reactors/Fuels/Power Ascension, ch. 14 Separations & Waste | 2002 | Wayback | Technical narrative. Status 200 per CDX; ch. 12 replay was rate-limited (429) when I tried it, and ch. 13–14 were not re-fetched. |
| WB | https://web.archive.org/web/20210622210711/https://www.srs.gov/general/about/srs-1960.htm | SRS history, 1960s page | captured 2021 | Wayback | Covers HWCTR 1962, curium-244 1963, R and HWCTR shut down 1964, Cf-252, L shut down 1968 and the 1961 ecology lab. |
| EXT: SC SHPO | https://scdah.sc.gov/sites/scdah/files/Documents/Historic%20Preservation%20(SHPO)/Research/Historic%20Contexts/SRS%20Reactor%20Areas.pdf | Reed, Swanson & Gillett (New South Associates), *SRS Cold War Historic Property Documentation: Thematic Study of Savannah River's Five Reactor Areas* | c.2010 (date line garbled in text layer) | SC Dept. of Archives & History | A 930-page narrative and photographic documentation of R, P, L, K and C. |
| EXT: SC SHPO | https://scdah.sc.gov/sites/scdah/files/Documents/Historic%20Preservation%20%28SHPO%29/Research/SRS_Separations.pdf | SRS Cold War Historic Property Documentation: Separations | n.d. | SC SHPO | Documentation of the F and H canyons. Verified 200 (20.6 MB); I did not read past the response. |
| EXT: SC SHPO | https://scdah.sc.gov/sites/scdah/files/Documents/Historic%20Preservation%20(SHPO)/Research/Historic%20Contexts/SRS%20Infrastructure.pdf | SRS Cold War Historic Property Documentation: Infrastructure | n.d. | SC SHPO | Roads, rail, utilities and other site infrastructure. Verified 200. |
| WB | https://web.archive.org/web/20250203072742/https://www.loc.gov/item/sc1142/ | Historic American Engineering Record, HAER SC-43, *Physics Assembly Laboratory, Area A/M, Savannah River Site* (Buildings 777-M and 777-10A) | captured 2025 | Library of Congress (live site refuses automated requests), Wayback | The zero-power Process Development Pile that set the physics parameters for plutonium and tritium production in the five reactors; 107 photographs, 123 data pages. Verified 2026-11-06 through the Wayback capture. A loc.gov search of HABS/HAER for "savannah river site" returns only this record; the state archives (SCDAH) list further Savannah River studies not at LOC. |
| EXT: OSTI | https://www.osti.gov/biblio/10149809 | *Separations Areas: SRP history, July 1954–Dec 1972* (DPSP-55-454-2) | 1972 | OSTI, full text | Year-by-year history of F and H operations. |
| EXT: OSTI | https://www.osti.gov/biblio/10172719 | *History of the Savannah River Laboratory*, Vol. III (DPST-62-200) | 1984 | OSTI, full text | An SRL history series. Only Vols. III and X were found; Vol. I (the founding years) did not surface. |
| IA (lending) | `supplyingnuclear0000carl` | Carlisle & Zenzen, *Supplying the Nuclear Arsenal: American Production Reactors, 1942–1992* | 1996 | inlibrary | **The best secondary source on the reactors.** It has a table of construction-start and startup dates and R-reactor piping schematics. |
| IA (lending) | `usnuclearwarhead0002unse` | Cochran et al. (NRDC), *U.S. Nuclear Warhead Production* (Nuclear Weapons Databook) | 1987 | inlibrary | A reactor table giving construction start and first criticality: R 6/1951–12/1953, P 7/1951–2/1954, L 10/1951–7/1954. |
| IA | `sim_chemical-engineering-progress_1959-09_55_9` | *Chemical Engineering Progress*, Sept 1959 | 1959-09 | sim_microfilm | A declassified technical account of the Dana and Savannah River heavy-water (GS process) plants. |
| IA (lending) | `atomsforpeaceusa0000unse` | Hogerton / A. D. Little, *Atoms for Peace, U.S.A. 1958* | 1958 | inlibrary | Public 1950s description: SRP operated by Du Pont, with CP-5 heavy-water lineage. |
| IA (lending) | `nuclearmilestone0000seab` | Glenn Seaborg, *Nuclear Milestones* | 1972 | inlibrary | AEC chairman's speeches. Mentions SRP manager Donald A. Miller and heavy-water reactor lineage. |
| IA (lending) | `bwb_S0-BMA-297` | *Annual Report to Congress of the AEC for 1964* | 1965 | inlibrary | Covers the 1964 Savannah River workforce reduction and heavy-water sales. |
| IA | `DTIC_ADA398004` | *Stainless Steel Information Manual for the SRP*, Vol. II | 1964 | dticarchive (not DL) | A Du Pont technical manual from the period. |
| IA | `DTIC_ADA438487` | *Aeroradioactivity Survey and Areal Geology of the SRP Area* | 1962 | dticarchive (not DL) | An early-1960s radiological survey. |
| IA (folkscanomy) | `SavannahRiverEnvironmentalImpactStatements` | *Savannah River environmental impact statements* (DOE, compiled) | 1980s | folkscanomy | Later EIS material with operating-history background. Uploader-compiled. |
| IA | `micro_IA41152840_0671` | *Reactors at the Savannah River Plant*, Senate Armed Services hearing | 1988-02-29 | us-gpo microfiche (not DL) | A retrospective on Du Pont's reactor operation. Out of period. |

## 4. Early ecology: Odum, the baseline surveys, the origins of SREL

| Label | Identifier / URL | Title | Date | Holder / collection | Contribution |
|---|---|---|---|---|---|
| IA (printdisabled only) | `isbn_9780820324739` | Betty Jean Craige, *Eugene Odum: Ecosystem Ecologist & Environmentalist* | 2001 | internetarchivebooks | **The Odum biography.** Covers the Savannah River work and Eniwetok in 1954. |
| IA (lending) | `historyofecosyst0000unse` | Frank B. Golley, *A History of the Ecosystem Concept in Ecology* | 1993 | inlibrary | An insider account: the Savannah River program "headed by Eugene Odum and me". |
| IA (printdisabled only) | `bigecologyemerge0000cole` | David C. Coleman, *Big Ecology: The Emergence of Ecosystem Science* | 2010 | internetarchivebooks | States Odum "was approached by AEC officials in 1951 to study ecosystems on the Savannah River reservation". |
| WB | https://web.archive.org/web/20160620134206/http://srel.uga.edu:80/outreach/snapshots/history_radioecology.html | SREL Research Snapshot, "The History of Radioecology Research at the SREL" | captured 2016 | Wayback | SREL's own claim of a 1951 founding by Odum, and its 1950s–60s radiation-effects field studies. |
| IA | `micro_IA41159405_0033` | Gold, Scott, Hirsch, Ruchhoft et al. (USPHS), *Savannah River Studies, July 1951–July 1952* | 1954 | NTIS microfiche (not DL) | A pre-operation baseline water-quality survey of the river. |
| IA | `micro_IA41159413_0274` | Ruchhoft, Setter, Goldin et al., *The Background Radioactivity of Water and Biota of the Savannah River (1951–1952)* | 1952 | NTIS microfiche | The pre-operation radiological baseline. |
| IA | `micro_IA41159431_0962` | Gold, Ingram et al. (Taft Sanitary Engineering Center), *Interim Report on the Savannah River Studies, 1955* | 1957 | NTIS microfiche | A follow-up after the reactors started. |
| IA | `micro_IA41159405_0227` | USPHS, *Municipal, Industrial and Domestic Water Supplies… Savannah River* | 1962 | NTIS microfiche | Cites Du Pont Health Physics, "The Effect of the Savannah River Plant on Environmental…". |
| IA | `asbbulletin2022asso` | *ASB Bulletin* (Assoc. of Southeastern Biologists) | 1954 | biodiversity | R. S. Harvey (SRL, Du Pont) on environmental research and stream organisms in Upper Three Runs: Du Pont's in-house ecology. |
| IA | `biostor-199812` | Norris, Connell & Johnston, ruby-throated hummingbird notes, "Savannah River Plant area" | 1957 | biostor | An example of 1950s Odum-era UGA field ornithology on the plant. |
| IA | `odonatologica-16-009-023` | Kondratieff & Pyott, "The Anisoptera of the SRP… thirty years later" | 1987 | taxonomyarchive | Explicitly resurveys a 1950s baseline. |
| IA (lending) | `mammalsofgeorgia0000fran` | Golley, *Mammals of Georgia* | 1962 | inlibrary | Matched "Savannah River Project". Golley's SRP-era work. |
| EXT: OSTI | https://www.osti.gov/biblio/14349 | Auerbach & Reichle, *U.S. Radioecology Research Programs Initiated in the 1950s* (ORNL/CP-104856) | 1999 | OSTI | Puts Odum's AEC-funded Savannah River program in national context. |
| EXT: OSTI | https://www.osti.gov/biblio/305940 | Vaughan (ed.), *A Vital Legacy: Biological and Environmental Research in the Atomic Age* (PUB-800) | 1997 | OSTI | DOE's account of the founding of its ecology programs. |
| EXT: OSTI | https://www.osti.gov/biblio/754224 | A. G. Phillips, *50 Years of Excellence in Science and Engineering at the SRS* (WSRC-MS-2000-00061) | 2000 | OSTI | An SRL/SRTC retrospective. |
| DL | `gov.gpo.fdsys.CHRG-110hhrg36143` | *DOE's Support for the Savannah River Ecology Laboratory (SREL)*, House Science hearing | 2007-07-19 | USGovernmentDocuments, DL | Out of period, but its testimony recounts SREL's history and its relation to SRS. |

## Archive-It

- **AIT:** none verified. `wayback.archive-it.org/12263/...` (srswatch.org, UGA) served a "Session Verification" bot-challenge page to both the CDX and the calendar URLs, so I could not list any captures. srswatch.org is a modern watchdog site and has little relevance to 1950–69 in any case.

---

## Key facts (each with its source)

1. **The site was announced on 28 Nov 1950** at noon, as about 250,000 acres in Aiken and Barnwell counties, named the "Savannah River Plant", to be designed, built and operated by Du Pont. Source: *SRS at Fifty* ch. 8 (WB). OSTI 272945 also states the 28 Nov 1950 announcement.
2. **The war in Korea expanded the plan.** In June 1950 the AEC added three heavy-water reactors to Du Pont's scope, bringing the total to five. A sixth, power-producing reactor was dropped in November 1952, and a third separations unit was also dropped. Source: *SRS at Fifty* ch. 7.
3. **The towns on the site.** Ellenton (population 600), Dunbarton (231), Meyers Mill, Jackson, Hawthorne, Robbins, Leigh, Snelling and Hattieville. Source: *SRS at Fifty* ch. 7. Lang (1954) gives Ellenton as "pop. 700".
4. **Displacement figures disagree; quote them with their source.**
   - The press release said about 1,500 families would relocate within 18 months.
   - Early reports said "up to 8,000 farmers", the majority African American.
   - The AEC refined its estimate to 6,000 people (1,500 families).
   - Sources for those three: *SRS at Fifty* ch. 8.
   - SRARP's "Former Towns" page says "approximately 5000 people were relocated".
   - The HHFA *Impact of Large Installations* study reports about 30 white and 120 Black families relocated near New Ellenton (a partial figure, not the total).
5. **Most farms were tenant-operated**, and the majority of the agricultural workforce was African American. Source: *SRS at Fifty* ch. 7, citing Du Pont field inspections and appraisers.
6. **Land acquisition was run by the Army Corps of Engineers** (authorized by an AEC letter of 28 Nov 1950).
   - At least 4,500 graves had to be relocated, at an estimated cost of $300,000.
   - Residents of priority Area 1 had to leave by 15 March 1951 and those of Area 2 by 1 June 1951.
   - Owners who disputed appraisals went to federal condemnation proceedings.
   - Source for all of the above: *SRS at Fifty* ch. 8.
   - As of the late-1951 hearing, 265 tracts were being acquired in Ellenton. Source: DL hearing of 27 Nov 1951.
7. **An informational meeting in Ellenton** drew over 500 people and was apparently segregated. Source: *SRS at Fifty* ch. 8, caption.
8. **Construction started in 1951.** Source: srs-1950.htm and energy.gov/srs/history. Reactor construction began June 1951 (R), July 1951 (P) and October 1951 (L). Source: NRDC *U.S. Nuclear Warhead Production* table (IA highlight).
9. **R reactor went critical in December 1953.** P went critical on 20 Feb 1954, and all five were operating by the end of March 1955. Source: *SRS at Fifty* ch. 11. P, L and K started in 1954 and C in 1955, per srs-1950.htm and history1.htm.
10. **Heavy-water production began in D Area in 1952**, and the 305-M test pile was the first reactor to go critical at the site (1952). Source: srs-1950.htm.
11. **F Area was the first separations plant to operate (1954); H Canyon followed in 1955.** Source: srs-1950.htm and history1.htm.
12. **First plutonium shipment: sources conflict.**
    - *SRS at Fifty* ch. 11 has a photo commemorating the first shipment, dated 28 Dec 1954.
    - srs-1950.htm says "1954".
    - history1.htm and energy.gov/srs/history say "1955".
13. **First tritium shipment to the AEC, and the permanent tritium facilities, were in 1955.** Source: srs-1950.htm and energy.gov/srs/history.
14. **The basic plant was complete in 1956.** Source: history1.htm and energy.gov.
15. **Later 1950s–60s milestones.**
    - The neutrino was confirmed at P reactor in 1956.
    - R reactor and HWCTR were shut down in 1964, and L in 1968.
    - C reactor reached a record 2,915 MW in 1967.
    - Sources: srs-1960.htm and *SRS at Fifty* ch. 11.
16. **SREL's founding date: sources conflict.**
    - SREL's own page and history1.htm say the ecology work began, and SREL was "founded", in 1951 by Odum.
    - srs-1960.htm says the AEC established a *permanent* onsite "Laboratory of Radiation Ecology" in 1961, later SREL.
    - Coleman (*Big Ecology*) says AEC officials approached Odum in 1951.
    - Treat 1951 as the start of the survey contract and 1961 as the permanent lab.
17. **Two different baseline surveys started in 1951.**
    - srs-1950.htm credits "Dr. Ruth Patrick's baseline survey" (Academy of Natural Sciences) in 1951.
    - Separately, USPHS ran "Savannah River Studies, July 1951–July 1952" (IA microfiche).
18. **The construction workforce was studied by BLS** in "Labor and the Savannah River AEC Project", parts I–IV (*Monthly Labor Review*, Jun–Sep 1952). Its highlights note:
    - Black tenant farmers arriving in Augusta seeking jobs (May 1951).
    - An NAACP-sponsored meeting in Aiken (Sept 1951) charging Du Pont over hiring.
19. **Housing.**
    - About 4,000 trailers were provided for married workers.
    - Lyles & Lang built the Savannah River housing.
    - Sources: *House & Home*, Aug 1953.
    - A Feb 1951 hearing in Aiken projected the construction-worker peak around early 1953.
20. **Truman's letter to Du Pont.** energy.gov/srs/history's timeline dates it **20 Oct 1950**. *Unsourced beyond that page*: I did not confirm it against Hewlett & Duncan.

**Unsourced background (my knowledge only; not verified this session):**
- The peak construction force of roughly 38,000 in 1952.
- Ellenton's final evacuation date around 1 March 1952.
- Du Pont's nominal $1 fee.

Do not use any of these without a source.

---

## Gaps

- **Library of Congress / HAER:** the loc.gov JSON API and item pages returned 503/403 to automated requests. HAER sc1142 is known only from a search snippet. Chronicling America was not searched; it largely ends before 1964 anyway.
- **Hagley:** the finding-aid site sat behind a bot challenge (HTTP 202 with an empty body). The holdings are corroborated only by the DOE OHRE finding aid.
- **NARA** (RG 326, Atlanta regional archives): not checked, because the catalog API needs a key and I did not attempt it.
- **Archive-It:** the bot challenge blocked all listing. No AIT sources.
- ***SRS at Fifty* chapters 4, 5, 6, 9 and 10** (the core Act 1 chapters) have no separate Wayback captures. They are available only inside the 55.9 MB full-book capture, which I verified by header only. Ch. 12 replay hit a 429 rate limit.
- ***Cold War Dixie*** (Frederickson) and ***The Unexpected Exodus*** (L. Cassels) are not on IA in any form found (metadata, full text or Open Library `ia`).
- **SRARP *Dunbarton and Meyers Mill* PDFs:** the CDX lists 200 captures, but the replay of the preface returned 404 today. The Ellenton volume PDFs are image-only, so they are not searchable.
- **SRS Heritage Foundation, the SRS Museum and the SRARP live site:** srarp.org and srsheritagefoundation.org did not resolve, and current SRS/SC pages 404.
- **Atomic Heritage Foundation:** the AHF location page for SRS 404s. Its "Voices" oral-history search returned 404, so I identified no SRS interviews.
- **SREL archives at UGA (Hargrett) and South Caroliniana:** not checked.
- **Primary Odum documents:** the 1950s AEC contract reports (e.g. Odum's annual reports to the AEC) did not surface in the OSTI API.
- **First volume of the *History of the Savannah River Laboratory*:** not found (only Vols. III and X).
- **`www.srs.gov/general/pubs/` CDX:** run with limit 3000, it returned mostly `envbul/cx_docs` and no history titles. The full 12.8k-URL pass was not completed.
- **Not yet confirmed:** the bylines and content of most magazine and newspaper hits (Newsweek, Pathfinder, Popular Science, ENR, Chemical Week, 1952 small-town dailies). They are listed because full-text search matched them; read them before citing.
- **Hearing titles:** the four DL Congress-hearing items carry only generic titles ("Hearings, Prints and Reports" plus a date). The committee and hearing titles need reading.
