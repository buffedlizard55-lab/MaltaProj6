# San Francisco Events

A curated, source-linked snapshot of public events in San Francisco, organized by recurrence and category. The inventory contains **225 listed entries** (119 recurring, 55 annual, 51 special/dated) and is intended to cover events physically within the City and County of San Francisco.

> **Coverage limitation:** this is not an exhaustive or live calendar of every concert, gallery opening, private event, pop-up or short-notice listing. The dataset reflects public programmes and event pages found during the recorded research pass. Check the [City's official events calendar](https://www.sf.gov/events/upcoming) and each organizer for additional or current listings.

## Verification and review status

- Every published event row has a link to an organizer, government agency, state agency or federal park source. The research log records the pages as checked on **2026-10-18**.
- **149** rows are marked `verified`; **76** rows have a review gap or an unconfirmed value. Unconfirmed price cells are left blank rather than showing generic "Ticketed" as an amount; affected rows appear on the **Flagged for review** page.
- **173** discrepancy, source, scope and other review items are published on `flagged.html`.
- **43** rows record editions that have already finished (the 2026 state fair, Dreamforce, the Mime Troupe summer season and similar); they stay in the catalogue as records, carry a **concluded** badge, and are kept out of the "upcoming dated events" strip on the home page.
- An independent line-by-line audit on **2026-10-18** (`audit/`, session `arena-bdaa17b4`; merged with session `arena-7d8015f4`'s integrity pass, which upgraded the One City One Book source and set the blank-cost Alcatraz closure row to `unverified`) re-fetched a stratified sample of the official source pages plus every irregular row, removed one out-of-scope row and two duplicate rows, corrected five rows, and added nine verified missing events. See `audit/AUDIT-2026-10-18-bdaa17b4.md` for the full findings and `data/gap-candidates-bdaa17b4.json` for the gap-research trail.
- Session `arena-23722ef3` performed a live line-by-line re-verification pass on **2026-10-18**, fetching the official pages behind 22+ high-risk rows (dated annuals, sports schedules, museum exhibitions, civic meetings) and correcting six rows whose values the sources did not support (SF Marathon, Fleet Week Parade of Ships time, Manon run start, SuperNatural times/prices, Rules/LUT committee times, Litquake title). The full row-by-row check log is in `COORDINATION.md`.
- Session `arena-3239c070` performed a full gap-research and re-verification pass on **2026-10-18**, fetching 25+ official pages (SFMTA cable cars, ArtSpan SF Open Studios, Maritime USS Pampanito, Musée Mécanique, SailGP 2026 calendar, Yerba Buena Gardens Festival, SF Design Week, Moscone Center calendar, plus spot-checks of SFMOMA, Asian Art Museum, SF Symphony, FAMSF and Exploratorium). Added four verified rows (SF Cable Cars, SF Open Studios, USS Pampanito, Musée Mécanique) and three new flagged exclusions (SailGP no SF stop in 2026, Union Square ice rink and Kaiser SF Half unverified). See `COORDINATION.md` for the full log and `data/events.py` for every source link.
- Session `arena-79993171` completed the post-merge audit on **2026-10-18**: corrected the special-event date-status/schedule mapping, removed placeholder dates, refreshed Lightscape dates, corrected pickleball sourcing and unknown access terms, separated the Board of Appeals from the Assessment Appeals Boards, and left the Escape From Alcatraz race fee blank. See `audit/POST-MERGE-2026-10-18-79993171.md` and the review page for remaining conflicts/gaps.
- Session `arena-8e8e24dc` ran an independent verification pass on **2026-10-18** (see `audit/AUDIT-2026-10-18-8e8e24dc.md`). After PR #26 released the integration claim it applied the corrections that were still outstanding: removed the Contemporary Jewish Museum (temporarily closed since 15 December 2024, and the row's 364 Ninth Street address was wrong), renamed and re-addressed the Presidio row to Presidio Visitor Center (210 Lincoln Boulevard), moved the San Francisco Symphony to Davies Symphony Hall, replaced the Haight-Ashbury Street Fair's stale June rule with the confirmed 20 September 2026 date, blanked the unconfirmed "March 2-7, 2027" Bouquets to Art dates, filled the published hours for the de Young, Legion of Honor and Exploratorium, corrected the "Quintana" typo on Secondhand Saturdays, and rendered six imported date ranges as prose instead of semicolon-separated ISO dates. Six review items record the evidence and the two source conflicts.
- Session `arena-8cb2d3cc` ran the final integration pass on **2026-10-18**: removed the fabricated "California Museum" row (the real museum is in Sacramento, outside the city-limits scope), closed the verification gap on four San Francisco institutions that earlier passes had listed as unreachable (FOG Design+Art, Portola Music Festival, Juneteenth Fillmore, Golden State Valkyries), added the SF Mime Troupe summer season, the Yerba Buena Gardens Festival and the Conservatory of Flowers light show, and rebuilt the recurring/annual/special split, the full searchable list (`all-events.html`), the analysis page and a CSV export. It also replaced a dead Rec and Park calendar citation with the department's Meeting Info & Calendar page, added the Assessment Appeals Board session times, and flagged a hours conflict between the Musée Mécanique's two sites.
- Session `arena-3ab2abd4` performed two final integration passes on **2026-10-18**: added dedicated AI & gaming and free-events pages, re-verified GDC Festival of Gaming 2027's official dates/location and Early Rate pass prices, and added AI Council 2027 with its official date/venue but a blank, flagged cost because the organizer does not list a price. ODSC AI West 2026 was excluded because Hyatt's official property page places its named venue in Burlingame. The all-events and special pages put confirmed upcoming dates first; the dashboard shows a chronological near-term summary with cost/source links; the full list includes a free-cost filter. A strict price pass then blanked 67 generic nonnumeric paid/variable labels such as "Ticketed", marked those rows unverified and added one official-source-linked price follow-up item per row. Wording that explicitly indicates some free access is separately highlighted where applicable. Date sorting uses only written calendar dates and years; missing values are not inferred.
- Session `arena-91296e94` ran an independent verification and gap-research pass on **2026-10-18** (see `audit/AUDIT-2026-10-18-91296e94.md` and `data/gap-candidates-91296e94.json`), re-fetching 20+ official pages for the near-term dated rows and the blank-cost rows. It added seven verified rows — TechCrunch Disrupt 2026 (concluded Oct 13–15, Moscone West, full official pass pricing), Gamesforum San Francisco 2026 (Oct 26–27, Hotel Nikko, $239 standard pass), GamesBeat NEXT 2026 (Nov 2–3, Convene, $899/$499 passes) and four free weekly Ferry Building programmes (Board Game Night Fridays, Mahjong Meetup Wednesdays, Music on the Plaza Thursdays, Monday Yoga) — corrected the WNBA Finals row to the team's official schedule and source, replaced the Mime Troupe's third-party calendar-feed citation with the organiser's own schedule page, and published the Castro Menorah Lighting date-text conflict for review.
- The build-time validator checks dataset integrity, source-link presence, table markup and local links. It does **not** fetch pages; the source-fetch verification above is recorded in `COORDINATION.md` and source freshness must be re-checked against the linked official pages.

## Site

The site is plain static HTML and is published with GitHub Pages.

| Page | Contents |
|---|---|
| `index.html` | Dashboard, counts, categories, analysis and coverage notice |
| `all-events.html` | 225 rows, chronological upcoming-first ordering, with search, schedule, category, status, timing and cost filters (works without JavaScript) |
| `free-events.html` | 135 entries whose published official cost wording explicitly includes free access |
| `recurring.html` | 119 entries on a regular weekly, monthly or other recurring schedule |
| `annual.html` | 55 entries that recur year after year |
| `special.html` | 51 dated or time-limited entries for 2026–2027 |
| `civic.html` | 37 civic entries, boards, commissions and public meetings |
| `arts.html` | 72 arts, culture, museums, performance and screen entries |
| `sports.html` | 10 sports, races and active recreation entries |
| `technology.html` | 7 AI and gaming events (GDC Festival of Gaming, AI Council, TechCrunch Disrupt, Gamesforum, GamesBeat NEXT, and the Ferry Building's weekly Board Game Night and Mahjong Meetup); the ticket price is blank for AI Council because the organizer has not published it |
| `markets.html` | 29 farmers markets, food halls and street markets |
| `community.html` | 70 neighbourhood programmes, festivals and free recreation entries |
| `flagged.html` | 173 review items plus the rows carrying unconfirmed values |
| `methodology.html` | Scope, sourcing rules, build process and limitations |
| `weekly.html` | Supplementary view from the parallel research session |
| `analysis.html` | Counts, schedule/category/area breakdowns, blank-field coverage and the list of source domains |
| `sources.html` | Supplementary source registry from the parallel research session |

Each listed event appears on one recurrence-type page and one subject-category page. A source link is displayed in a dedicated table column.

## Repository layout

```
COORDINATION.md             shared task board, research log, verification notes and irregularities
data/events.py              canonical authored dataset
data/events.json             generated machine-readable mirror (225 events, 173 review items)
data/gap-candidates-bdaa17b4.json  independent-audit gap-research trail (added / not-added candidates)
audit/                        independent audit: report, structural row checker, integration script
data/weekly.json              supplementary raw recurring rows
data/annual.json              supplementary raw annual rows
data/special.json             supplementary raw special rows
data/flagged.json             supplementary review register
data/sources.json             supplementary source registry
data/review.csv               supplementary line-by-line review sheet
data/schema.md                supplementary JSON schema documentation
scripts/build_site.py         builds the site and data mirror from the union dataset
scripts/merge_parallel.py     adapts the supplementary research rows to the canonical schema
tools/                        retained supplementary research and validation tooling
assets/site.css               generated site stylesheet
assets/style.css, app.js      supplementary session assets
*.html                        committed static pages for GitHub Pages
```

## Rebuild and validate

```bash
python3 scripts/build_site.py
python3 tools/validate.py
```

The build also writes `data/events.csv` (a 17-column spreadsheet export of every row, including supporting source URLs) for anyone who wants to sort or filter the catalogue in a spreadsheet.

The site generator writes `data/events.json`, the canonical pages and `assets/site.css`. The validator checks the published union data, per-page row membership, source links, table structure and local links. It cannot verify source-page text or event completeness without a source review.

## Updating an event

1. Edit the relevant event record in `data/events.py`.
2. Set `source_name` and `source_url` to the official page actually checked; do not use an aggregator as evidence.
3. Leave a value blank if the official source does not state it, and use `status="unverified"` when an issue remains.
4. Add the issue to `FLAGGED` when appropriate so it is visible on the review page.
5. Run both commands above and inspect the generated diff.

## Coordination

`COORDINATION.md` records task ownership, sources, verification notes, irregularities and prior integration history. The repository's earlier research passes and their raw supporting files are retained there and under `data/` and `tools/`.
