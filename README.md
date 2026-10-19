# San Francisco Events

A curated, source-linked snapshot of public events in San Francisco, organized by recurrence, category and focus area. The inventory contains **316 listed entries** (127 recurring, 59 annual, 130 special/dated) and is intended to cover events physically within the City and County of San Francisco.

Every entry also carries a focus tag, so the same catalogue can be read the way the brief asks for — **gaming (18), music (54), AI (9), then everything else (235)** — with free admission called out explicitly: **175** entries publish free-access wording, of which **158** are free-only (not mixed with a paid tier). The homepage executive summary and main list use the free-only set.

> **Coverage limitation:** this is not an exhaustive or live calendar of every concert, gallery opening, private event, pop-up or short-notice listing. The dataset reflects public programmes and event pages found during the recorded research pass. Check the [City's official events calendar](https://www.sf.gov/events/upcoming) and each organizer for additional or current listings.

## Verification and review status

- Every published event row has a link to an organizer, government agency, state agency or federal park source. The research log records the pages as checked on **2026-10-18**.
- **194** rows are marked `verified`; **122** rows have a review gap or an unconfirmed value. Unconfirmed price cells are left blank rather than showing a generic "Ticketed" as an amount, and affected rows appear on the **Flagged for review** page.
- **233** discrepancy, source, scope and other review items are published on `flagged.html`.
- **47** rows record editions that have already finished (the 2026 state fair, Dreamforce, the Mime Troupe summer season and similar); they stay in the catalogue as records, carry a **concluded** badge, and are kept out of the "upcoming dated events" strip on the home page.
- **How cost is shown.** Each cost cell quotes the official source exactly and is rendered as a colour-coded label — free, partly free, paid, or *cost not published*. A price is never inferred: when the official page does not state an amount the cell is left blank, the row is marked `unverified`, and the official source's own wording (for example "Ticketed") is still shown underneath as *as published*, clearly separated from the price.
- **93** rows are marked `verified` yet still carry a blank schedule, location or cost cell, because the official source does not publish that value. Here `verified` means *every value the source does publish was confirmed*, not *every cell is filled*. The discrepancy is published as review item `flag-verified-rows-with-blank-core-cell` rather than silently re-badged or filled in.
- An independent line-by-line audit on **2026-10-18** (`audit/`, session `arena-bdaa17b4`; merged with session `arena-7d8015f4`'s integrity pass, which upgraded the One City One Book source and set the blank-cost Alcatraz closure row to `unverified`) re-fetched a stratified sample of the official source pages plus every irregular row, removed one out-of-scope row and two duplicate rows, corrected five rows, and added nine verified missing events. See `audit/AUDIT-2026-10-18-bdaa17b4.md` for the full findings and `data/gap-candidates-bdaa17b4.json` for the gap-research trail.
- Session `arena-23722ef3` performed a live line-by-line re-verification pass on **2026-10-18**, fetching the official pages behind 22+ high-risk rows (dated annuals, sports schedules, museum exhibitions, civic meetings) and correcting six rows whose values the sources did not support (SF Marathon, Fleet Week Parade of Ships time, Manon run start, SuperNatural times/prices, Rules/LUT committee times, Litquake title). The full row-by-row check log is in `COORDINATION.md`.
- Session `arena-3239c070` performed a full gap-research and re-verification pass on **2026-10-18**, fetching 25+ official pages (SFMTA cable cars, ArtSpan SF Open Studios, Maritime USS Pampanito, Musée Mécanique, SailGP 2026 calendar, Yerba Buena Gardens Festival, SF Design Week, Moscone Center calendar, plus spot-checks of SFMOMA, Asian Art Museum, SF Symphony, FAMSF and Exploratorium). Added four verified rows (SF Cable Cars, SF Open Studios, USS Pampanito, Musée Mécanique) and three new flagged exclusions (SailGP no SF stop in 2026, Union Square ice rink and Kaiser SF Half unverified). See `COORDINATION.md` for the full log and `data/events.py` for every source link.
- Session `arena-79993171` completed the post-merge audit on **2026-10-18**: corrected the special-event date-status/schedule mapping, removed placeholder dates, refreshed Lightscape dates, corrected pickleball sourcing and unknown access terms, separated the Board of Appeals from the Assessment Appeals Boards, and left the Escape From Alcatraz race fee blank. See `audit/POST-MERGE-2026-10-18-79993171.md` and the review page for remaining conflicts/gaps.
- Session `arena-8e8e24dc` ran an independent verification pass on **2026-10-18** (see `audit/AUDIT-2026-10-18-8e8e24dc.md`). After PR #26 released the integration claim it applied the corrections that were still outstanding: removed the Contemporary Jewish Museum (temporarily closed since 15 December 2024, and the row's 364 Ninth Street address was wrong), renamed and re-addressed the Presidio row to Presidio Visitor Center (210 Lincoln Boulevard), moved the San Francisco Symphony to Davies Symphony Hall, replaced the Haight-Ashbury Street Fair's stale June rule with the confirmed 20 September 2026 date, blanked the unconfirmed "March 2-7, 2027" Bouquets to Art dates, filled the published hours for the de Young, Legion of Honor and Exploratorium, corrected the "Quintana" typo on Secondhand Saturdays, and rendered six imported date ranges as prose instead of semicolon-separated ISO dates. Six review items record the evidence and the two source conflicts.
- Session `arena-61a46409` ran a focus-area research and site pass on **2026-10-18** (`audit/AUDIT-2026-10-18-61a46409.md`). It closed the gaming and AI gaps that earlier passes had left open by adding ten rows verified against official pages — free San Francisco Public Library gaming and music programmes (The Mix, and the library's own Gaming and Dance & Music calendars), SFPL Tech Week, AI Engineer Code Summit 2026, AI Week San Francisco, and three Moscone Center listings — leaving admission blank and marking the row `unverified` wherever the official page publishes no price. It added the **Music** page, widened **AI & gaming** to use the focus tags, added cost labels, a focus filter, a grouped and dated executive summary, and a mobile card layout, and corrected two date-parsing defects and two invented dates it found while checking the parser line by line.
- Session `arena-8cb2d3cc` ran the final integration pass on **2026-10-18**: removed the fabricated "California Museum" row (the real museum is in Sacramento, outside the city-limits scope), closed the verification gap on four San Francisco institutions that earlier passes had listed as unreachable (FOG Design+Art, Portola Music Festival, Juneteenth Fillmore, Golden State Valkyries), added the SF Mime Troupe summer season, the Yerba Buena Gardens Festival and the Conservatory of Flowers light show, and rebuilt the recurring/annual/special split, the full searchable list (`all-events.html`), the analysis page and a CSV export. It also replaced a dead Rec and Park calendar citation with the department's Meeting Info & Calendar page, added the Assessment Appeals Board session times, and flagged a hours conflict between the Musée Mécanique's two sites.
- Session `arena-3ab2abd4` performed two final integration passes on **2026-10-18**: added dedicated AI & gaming and free-events pages, re-verified GDC Festival of Gaming 2027's official dates/location and Early Rate pass prices, and added AI Council 2027 with its official date/venue but a blank, flagged cost because the organizer does not list a price. ODSC AI West 2026 was excluded because Hyatt's official property page places its named venue in Burlingame. The all-events and special pages put confirmed upcoming dates first; the dashboard shows a chronological near-term summary with cost/source links; the full list includes a free-cost filter. A strict price pass then blanked 67 generic nonnumeric paid/variable labels such as "Ticketed", marked those rows unverified and added one official-source-linked price follow-up item per row. Wording that explicitly indicates some free access is separately highlighted where applicable. Date sorting uses only written calendar dates and years; missing values are not inferred.
- Session `arena-91296e94` ran an independent verification and gap-research pass on **2026-10-18** (see `audit/AUDIT-2026-10-18-91296e94.md` and `data/gap-candidates-91296e94.json`), re-fetching 20+ official pages for the near-term dated rows and the blank-cost rows. It added seven verified rows — TechCrunch Disrupt 2026 (concluded Oct 13–15, Moscone West, full official pass pricing), Gamesforum San Francisco 2026 (Oct 26–27, Hotel Nikko, $239 standard pass), GamesBeat NEXT 2026 (Nov 2–3, Convene, $899/$499 passes) and four free weekly Ferry Building programmes (Board Game Night Fridays, Mahjong Meetup Wednesdays, Music on the Plaza Thursdays, Monday Yoga) — corrected the WNBA Finals row to the team's official schedule and source, replaced the Mime Troupe's third-party calendar-feed citation with the organiser's own schedule page, and published the Castro Menorah Lighting date-text conflict for review.
- Session `arena-fc3438db` ran the verification + requirements-alignment pass on **2026-10-18** (see `audit/AUDIT-2026-10-18-fc3438db.md` and `data/gap-candidates-fc3438db.json`): re-verified every soonest-dated row against its official page (28 live checks), corrected the Boo at the Zoo listing to the zoo's own event page (the published wording 'free with paid daytime admission or Zoo membership' is preserved in the review register under the project's blank-unless-numeric price rule) and added 14 source-verified rows not already covered by concurrent sessions (SF Symphony and SF Opera October–November programme, Exploratorium Creepatorium, Castro additions, INFORMS, SEMICON West, HumanX 2026, SFPL AI workshops) with a focus on the brief's free gaming / music / AI themes (SFPL gaming, chess and AI workshop programmes, SF Tech Week, HumanX 2026, Current SF, plus the SF Symphony / SF Opera October–November programme and the Moscone conventions). Concurrent sessions' focus taxonomy (gaming/music/AI), free-events page and cost rendering were kept as the baseline; five of this session's rows were superseded by arena-61a46409's richer-sourced SFPL and conference rows and were not duplicated.
- Session `arena-db227e31` ran a free-upcoming alignment pass on **2026-10-18** (see `audit/AUDIT-2026-10-18-db227e31.md`). The homepage executive summary and main list are now free-only and date-ordered, with gaming, music and AI before everything else, and paid or unpriced rows on `paid-events.html`. It added 12 verified free dated rows (Illuminate LIVE concerts, Bay Beats, and Family Summits) from official pages, left Sunday Streets admission blank because the official pages do not state a price, corrected the Presidio Día de los Muertos / Diwali time and address, and flagged the Rules and Land Use calendar conflicts plus the ArtSpan page that no longer re-rendered its dates.
- Session `arena-b95ade5f` ran an independent verification + gap-research + integration pass on **2026-10-18** (see `audit/AUDIT-2026-10-18-b95ade5f.md`). It re-fetched 30+ official pages — every Illuminate LIVE listing Oct 18–Nov 15, the SF.gov meeting pages behind the Oct 19 civic rows, both Family Summits, Open Source AI Week's flagships, Moscone, ArtSpan, the zoo, the Academy, Castro Merchants, the SF Rec & Park calendar, Litquake, the Ferry Building and 17 SFPL event records read through the library's own quickview pages and official ICS feeds. It added 17 dated free rows (ten gaming sessions — board games, family game time, chess, bocce, gaming hour, mahjong, Dungeons & Dragons, a JoJo tournament, puzzle swap and LEGO robotics; three music sessions — a Mix recording-studio orientation, a family dance party and the Excelsior open house during Sunday Streets; four community sessions; plus the free Ferry Building Trick-or-Treat re-verification), corrected the Open Source AI Awards Night time to the live page's 6:00–9:30 p.m. (the change is logged on the review page), and closed the ArtSpan non-rendering flag because the page now renders its dates and hours. Structural audit of all 316 rows: 0 aggregator-host sources, 0 duplicates, 0 events missing from the HTML, every blank core cell explained.
- Session `arena-fe7c710c` ran the final integration pass on **2026-10-18** (see `audit/AUDIT-2026-10-18-fe7c710c.md`). It opened the organiser's own events index and each individual event page and added **18 source-verified rows** — 13 free Illuminate LIVE concerts from 22 October to 15 November 2026, two Open Source AI Week San Francisco flagship events, and three Dogpatch Games rows carrying that venue's exact published prices. It then re-read every recently-touched page and **blanked 15 cost cells that asserted "Free" without the official page saying so** (Castro Merchants, Sunset Mercantile, the Ferry Building Marketplace, the Presidio Visitor Center, the Chinatown shopping streets and the Castro Art Mart), marking those rows unverified and flagging them, while keeping the free cells that the organisers do publish (Sunset Holiday Mercantile, the Autumn Moon Festival, the Conservatory Light Show, all Illuminate listings, the Presidio Diwali festival and the four SF.gov family summits). It date-qualified 17 repeated Illuminate titles so no two rows share a title, pointed eight Sunset Mercantile rows at each event's own page instead of the organisation home page, resolved the Castro Menorah date conflict in the organiser's favour, published 9 new review items, and made `data/meta.json` a build output so its counts can no longer drift.
- Session `arena-8eaf6c0a` ran an independent verification + gap-research pass on **2026-10-18** (`audit/AUDIT-2026-10-18-8eaf6c0a.md`), then — after `arena-fe7c710c` released the integration claim — applied its verified corrections and additions: 28 live official-source re-checks of the soonest-dated and free gaming/music/AI rows (all confirmed except two); the derived Larsen Pickleball cost wording ("Free (no reservation fee…)") blanked under the never-infer rule with `flag-price-spt-larsen-pickleball` and two stale Larsen flag texts repaired; the AI Week San Francisco 'Free' cell blanked because "100% free to use" describes the RSVP directory, not admission (`flag-price-spc-ai-week-sf-2026`); the `page` metadata corrected on the two SFPL annual programme rows; and six rows added from live-fetched official pages — GitHub Universe 2026 (Oct 28–29, Fort Mason, virtual ticket free), SOMArts In Their Name: Día de Los Muertos 2026 (opening Oct 23, $15 / free youth 16 & under; exhibition Oct 24–Nov 20), ZINETHING! monthly zine meetup (Oct 20, Main Library, cost not published), St. Francis & St. Clare relics veneration (Oct 16–Nov 28, 1111 Gough St, cost not published), SF Zine Fest 2026 concluded-edition record, and SOMArts In the Shadows of the West (Jan 23–Mar 26, 2027) — plus the verified exclusion `flag-fan-expo-no-sf-2026` (FAN EXPO San Francisco is not on the organiser's 2026–27 circuit).
- Session `arena-9fca0b37` ran the eleventh line-by-line verification pass on **2026-10-18** (see `audit/AUDIT-2026-10-18-9fca0b37.md` and `data/gap-candidates-9fca0b37.json`): 56 official pages re-fetched, then integrated after `arena-fe7c710c` released the shared-file claim. It added the **District 10 Bayview Family Summit** (free, 5 December — the event page earlier sessions could not find now exists) and six **Exploratorium After Dark** editions; it filled the four **SF Opera** rows with the organiser's published prices and times (Strauss "Starting at $30", Adlers "Starting at $34", Chorus "$49.00" at the Dianne and Tad Taube Atrium Theater, and the Opera Ball agenda with its $450–$10,000 levels) and the three **SF Symphony** rows with their published start times; it added 13 register items that took `UNVERIFIED_NOT_IN_FLAGGED_REGISTER` from 19 to 0; it closed the District 10 "page not found" item and both Castro Menorah date-conflict items after the organiser corrected its prose; and it recorded the city's own OCOFI calendar linking District 3 to a 404 slug. Overlapping corrections already merged from `arena-fe7c710c` were kept untouched.
- Session `arena-291a13ff` ran a concurrent independent verification and gap-research pass on **2026-10-18** (see `audit/AUDIT-2026-10-18-291a13ff.md` and `data/gap-candidates-291a13ff.json`), integrating after `arena-fe7c710c`'s claim was released. It re-fetched 25 official pages for the near-term and free gaming/music/AI rows (all matched; two JS-shell pages recorded as not re-rendered, nothing guessed), ran a new structural checker over the union (`audit/check_291a13ff.py`: 0 duplicate ids, all sources https, 0 broken internal links, mirror in sync), and added **five source-verified rows** — free Trick-or-Treat at the Ferry Building (Oct 29), free SFMOMA *Jennifer Steinkamp* and *In Between* installations, World of Dumplings (Oct 25) and the Fall SF International Tea Festival (Nov 14–15) with costs left blank because the official pages state no price. It also left an honest blank end date (instead of a wrong parsed one) for two running exhibitions whose museum pages publish no closing date (`DATE_OVERRIDES`), and recorded the Cloudflare "Oct 19–21 vs over four days" self-inconsistency and the stale Castro Menorah index-teaser text as review notes.
- The build-time validator checks dataset integrity, source-link presence, table markup and local links. It does **not** fetch pages; the source-fetch verification above is recorded in `COORDINATION.md` and source freshness must be re-checked against the linked official pages.

## Site

The site is plain static HTML and is published with GitHub Pages.

| Page | Contents |
|---|---|
| `index.html` | Dashboard: free-only executive summary near today, free upcoming main list (gaming, music, AI, then everything else), paid section separate |
| `all-events.html` | 316 rows, chronological upcoming-first ordering, with search, schedule, category, status, timing and cost filters (works without JavaScript) |
| `free-events.html` | 175 entries whose published official cost wording explicitly includes free access |
| `paid-events.html` | 158 paid, mixed, or price-not-published entries, kept out of the free main list |
| `recurring.html` | 127 entries on a regular weekly, monthly or other recurring schedule |
| `annual.html` | 59 entries that recur year after year |
| `special.html` | 130 dated or time-limited entries for 2026–2027 |
| `civic.html` | 37 civic entries, boards, commissions and public meetings |
| `arts.html` | 114 arts, culture, museums, performance and screen entries |
| `sports.html` | 10 sports, races and active recreation entries |
| `technology.html` | 36 AI and gaming entries — the focus-tag view, so library gaming clubs sit alongside GDC, AI Council, TechCrunch Disrupt, Gamesforum and GamesBeat NEXT; the ticket price is blank wherever the organizer has not published one |
| `music.html` | 54 music entries — concerts, festivals, opera, jazz and free music programmes |
| `markets.html` | 29 farmers markets, food halls and street markets |
| `community.html` | 112 neighbourhood programmes, festivals and free recreation entries |
| `flagged.html` | 233 review items plus the rows carrying unconfirmed values |
| `methodology.html` | Scope, sourcing rules, build process and limitations |
| `weekly.html` | Supplementary view from the parallel research session |
| `analysis.html` | Counts, schedule/category/area breakdowns, blank-field coverage and the list of source domains |
| `sources.html` | Supplementary source registry from the parallel research session |

Each listed event appears on one recurrence-type page and one subject-category page. Focus pages
(`technology.html`, `music.html`, `free-events.html`) cut across those categories. A source link is
displayed in a dedicated table column.

### Reading the site on a phone

Below 760px every wide table collapses into a stack of labelled cards, so nothing needs sideways
scrolling and no column is hidden — each cell repeats its column name. The homepage summary is
free events only, grouped into *today / already running*, *next 7 days* and *next 8–21 days*, with a
countdown and the gaming / music / AI badge on each row. Paid and unpriced rows are in a separate section.

## Repository layout

```
COORDINATION.md             shared task board, research log, verification notes and irregularities
data/events.py              canonical authored dataset
data/events.json             generated machine-readable mirror (316 events, 233 review items)
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
scripts/focus.py              focus tags (gaming / music / AI), cost classes and date parsing
scripts/merge_parallel.py     adapts the supplementary research rows to the canonical schema
audit/check_61a46409.py       read-only structural row audit -> audit/row-audit-61a46409.csv
tools/                        retained supplementary research and validation tooling
assets/site.css               generated site stylesheet
assets/style.css, app.js      supplementary session assets
*.html                        committed static pages for GitHub Pages
```

## Rebuild and validate

```bash
python3 scripts/build_site.py
python3 tools/validate.py
python3 audit/check_61a46409.py
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
