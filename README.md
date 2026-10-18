# San Francisco Events

A curated, source-linked snapshot of public events in San Francisco, organized by recurrence and category. The inventory contains **237 listed entries** (118 recurring, 57 annual, 62 special/dated) and is intended to cover events physically within the City and County of San Francisco.

> **Coverage limitation:** this is not an exhaustive or live calendar of every concert, gallery opening, private event, pop-up or short-notice listing. The dataset reflects public programmes and event pages found during the recorded research pass. Check the [City's official events calendar](https://www.sf.gov/events/upcoming) and each organizer for additional or current listings.

## Verification and review status

- Every published event row has a link to an organizer, government agency, state agency or federal park source. The research log records the pages as checked on **2026-10-18**.
- **226** rows are marked `verified`; **11** rows still have a review gap or unconfirmed value. Unconfirmed cells are left blank and the rows appear on the **Flagged for review** page.
- **108** discrepancy, source, scope and other review items are published on `flagged.html`.
- **46** rows record editions that have already finished (the 2026 state fair, Dreamforce, the Mime Troupe summer season and similar); they stay in the catalogue as records, carry a **concluded** badge, and are kept out of the "upcoming dated events" strip on the home page.
- An independent line-by-line audit on **2026-10-18** (`audit/`, session `arena-bdaa17b4`; merged with session `arena-7d8015f4`'s integrity pass, which upgraded the One City One Book source and set the blank-cost Alcatraz closure row to `unverified`) re-fetched a stratified sample of the official source pages plus every irregular row, removed one out-of-scope row and two duplicate rows, corrected five rows, and added nine verified missing events. See `audit/AUDIT-2026-10-18-bdaa17b4.md` for the full findings and `data/gap-candidates-bdaa17b4.json` for the gap-research trail.
- Session `arena-23722ef3` performed a live line-by-line re-verification pass on **2026-10-18**, fetching the official pages behind 22+ high-risk rows (dated annuals, sports schedules, museum exhibitions, civic meetings) and correcting six rows whose values the sources did not support (SF Marathon, Fleet Week Parade of Ships time, Manon run start, SuperNatural times/prices, Rules/LUT committee times, Litquake title). The full row-by-row check log is in `COORDINATION.md`.
- Session `arena-3239c070` performed a full gap-research and re-verification pass on **2026-10-18**, fetching 25+ official pages (SFMTA cable cars, ArtSpan SF Open Studios, Maritime USS Pampanito, Musée Mécanique, SailGP 2026 calendar, Yerba Buena Gardens Festival, SF Design Week, Moscone Center calendar, plus spot-checks of SFMOMA, Asian Art Museum, SF Symphony, FAMSF and Exploratorium). Added four verified rows (SF Cable Cars, SF Open Studios, USS Pampanito, Musée Mécanique) and three new flagged exclusions (SailGP no SF stop in 2026, Union Square ice rink and Kaiser SF Half unverified). See `COORDINATION.md` for the full log and `data/events.py` for every source link.
- Session `arena-79993171` completed the post-merge audit on **2026-10-18**: corrected the special-event date-status/schedule mapping, removed placeholder dates, refreshed Lightscape dates, corrected pickleball sourcing and unknown access terms, separated the Board of Appeals from the Assessment Appeals Boards, and left the Escape From Alcatraz race fee blank. See `audit/POST-MERGE-2026-10-18-79993171.md` and the review page for remaining conflicts/gaps.
- Session `arena-8e8e24dc` ran an independent verification pass on **2026-10-18** (see `audit/AUDIT-2026-10-18-8e8e24dc.md`). After PR #26 released the integration claim it applied the corrections that were still outstanding: removed the Contemporary Jewish Museum (temporarily closed since 15 December 2024, and the row's 364 Ninth Street address was wrong), renamed and re-addressed the Presidio row to Presidio Visitor Center (210 Lincoln Boulevard), moved the San Francisco Symphony to Davies Symphony Hall, replaced the Haight-Ashbury Street Fair's stale June rule with the confirmed 20 September 2026 date, blanked the unconfirmed "March 2-7, 2027" Bouquets to Art dates, filled the published hours for the de Young, Legion of Honor and Exploratorium, corrected the "Quintana" typo on Secondhand Saturdays, and rendered six imported date ranges as prose instead of semicolon-separated ISO dates. Six review items record the evidence and the two source conflicts.
- Session `arena-8cb2d3cc` ran the final integration pass on **2026-10-18**: removed the fabricated "California Museum" row (the real museum is in Sacramento, outside the city-limits scope), closed the verification gap on four San Francisco institutions that earlier passes had listed as unreachable (FOG Design+Art, Portola Music Festival, Juneteenth Fillmore, Golden State Valkyries), added the SF Mime Troupe summer season, the Yerba Buena Gardens Festival and the Conservatory of Flowers light show, and rebuilt the recurring/annual/special split, the full searchable list (`all-events.html`), the analysis page and a CSV export. It also replaced a dead Rec and Park calendar citation with the department's Meeting Info & Calendar page, added the Assessment Appeals Board session times, and flagged a hours conflict between the Musée Mécanique's two sites.
- Session `arena-fc3438db` ran the verification + requirements-alignment pass on **2026-10-18** (see `audit/AUDIT-2026-10-18-fc3438db.md` and `data/gap-candidates-fc3438db.json`): re-verified every soonest-dated row against its official page (28 live checks), corrected the Boo at the Zoo cost to 'free with paid zoo admission or membership' and upgraded the Mime Troupe source to the organiser's own page, and added 20 source-verified rows with a focus on the brief's free gaming / music / AI themes (SFPL gaming, chess and AI workshop programmes, SF Tech Week, HumanX 2026, Current SF, plus the SF Symphony / SF Opera October–November programme and the Moscone conventions). The home page now leads with an executive summary of events near the snapshot date, a date-sorted upcoming table, free spotlight and clear Free / paid cost labels; the full list gained a cost filter.
- The build-time validator checks dataset integrity, source-link presence, table markup and local links. It does **not** fetch pages; the source-fetch verification above is recorded in `COORDINATION.md` and source freshness must be re-checked against the linked official pages.

## Site

The site is plain static HTML and is published with GitHub Pages.

| Page | Contents |
|---|---|
| `index.html` | Dashboard: executive summary near today's date, free spotlight (gaming/music/AI), date-sorted upcoming dates, counts, categories, coverage notice |
| `all-events.html` | 237 rows with search, schedule, category, cost (Free/paid), status and timing filters (works without JavaScript) |
| `recurring.html` | 118 entries on a regular weekly, monthly or other recurring schedule |
| `annual.html` | 57 entries that recur year after year |
| `special.html` | 62 dated or time-limited entries for 2026–2027 |
| `civic.html` | 37 civic entries, boards, commissions and public meetings |
| `arts.html` | 80 arts, culture, museums, performance and screen entries |
| `sports.html` | 10 sports, races and active recreation entries |
| `markets.html` | 29 farmers markets, food halls and street markets |
| `community.html` | 69 neighbourhood programmes, festivals and free recreation entries |
| `flagged.html` | 103 review items plus the rows carrying unconfirmed values |
| `methodology.html` | Scope, sourcing rules, build process and limitations |
| `weekly.html` | Supplementary view from the parallel research session |
| `analysis.html` | Counts, schedule/category/area breakdowns, blank-field coverage and the list of source domains |
| `sources.html` | Supplementary source registry from the parallel research session |

Each listed event appears on one recurrence-type page and one subject-category page. A source link is displayed in a dedicated table column.

## Repository layout

```
COORDINATION.md             shared task board, research log, verification notes and irregularities
data/events.py              canonical authored dataset
data/events.json             generated machine-readable mirror (237 events, 108 review items)
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

The build also writes `data/events.csv` (a 16-column spreadsheet export of every row) for anyone who wants to sort or filter the catalogue in a spreadsheet.

The site generator writes `data/events.json`, the canonical pages and `assets/site.css`. The validator checks the published union data, per-page row membership, source links, table structure and local links. It cannot verify source-page text or event completeness without a source review.

## Updating an event

1. Edit the relevant event record in `data/events.py`.
2. Set `source_name` and `source_url` to the official page actually checked; do not use an aggregator as evidence.
3. Leave a value blank if the official source does not state it, and use `status="unverified"` when an issue remains.
4. Add the issue to `FLAGGED` when appropriate so it is visible on the review page.
5. Run both commands above and inspect the generated diff.

## Coordination

`COORDINATION.md` records task ownership, sources, verification notes, irregularities and prior integration history. The repository's earlier research passes and their raw supporting files are retained there and under `data/` and `tools/`.
