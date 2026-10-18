# San Francisco Events

A curated, source-linked snapshot of public events in San Francisco, organized by recurrence and category. The inventory contains **211 listed entries** (112 recurring, 52 annual, 47 special/dated) and is intended to cover events physically within the City and County of San Francisco.

> **Coverage limitation:** this is not an exhaustive or live calendar of every concert, gallery opening, private event, pop-up or short-notice listing. The dataset reflects public programmes and event pages found during the recorded research pass. Check the [City's official events calendar](https://www.sf.gov/events/upcoming) and each organizer for additional or current listings.

## Verification and review status

- Every published event row has a link to an organizer, government agency, state agency or federal park source. The research log records the pages as checked on **2026-10-18**.
- **169** rows are marked `verified`; **42** rows have a review gap, conflict or unconfirmed value. Unconfirmed cells are left blank and the rows appear on the **Flagged for review** page.
- **83** discrepancy, source, scope and other review items are published on `flagged.html`.
- An independent line-by-line audit on **2026-10-18** (`audit/`, session `arena-bdaa17b4`) re-fetched a stratified sample of the official source pages plus every irregular row, removed one out-of-scope row and two duplicate rows, corrected five rows, and added nine verified missing events. See `audit/AUDIT-2026-10-18-bdaa17b4.md` for the full findings and `data/gap-candidates-bdaa17b4.json` for the gap-research trail.
- The build-time validator checks dataset integrity, source-link presence, table markup and local links. It does **not** fetch pages or independently authenticate their current contents; source freshness must be checked against the linked official pages.

## Site

The site is plain static HTML and is published with GitHub Pages.

| Page | Contents |
|---|---|
| `index.html` | Dashboard, counts, categories, analysis and coverage notice |
| `recurring.html` | 112 entries on a regular weekly, monthly or other recurring schedule |
| `annual.html` | 52 entries that recur year after year |
| `special.html` | 47 dated or time-limited entries for 2026–2027 |
| `civic.html` | 36 civic entries, boards, commissions and public meetings |
| `arts.html` | 67 arts, culture, museums, performance and screen entries |
| `sports.html` | 10 sports, races and active recreation entries |
| `markets.html` | 29 farmers markets, food halls and street markets |
| `community.html` | 69 neighbourhood programmes, festivals and free recreation entries |
| `flagged.html` | 83 review items plus the rows carrying unconfirmed values |
| `methodology.html` | Scope, sourcing rules, build process and limitations |
| `weekly.html` | Supplementary view from the parallel research session |
| `analysis.html` | Supplementary analysis view from the parallel research session |
| `sources.html` | Supplementary source registry from the parallel research session |

Each listed event appears on one recurrence-type page and one subject-category page. A source link is displayed in a dedicated table column.

## Repository layout

```
COORDINATION.md             shared task board, research log, verification notes and irregularities
data/events.py              canonical authored dataset
data/events.json             generated machine-readable mirror (211 events, 83 review items)
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

The site generator writes `data/events.json`, the canonical pages and `assets/site.css`. The validator checks the published union data, per-page row membership, source links, table structure and local links. It cannot verify source-page text or event completeness without a source review.

## Updating an event

1. Edit the relevant event record in `data/events.py`.
2. Set `source_name` and `source_url` to the official page actually checked; do not use an aggregator as evidence.
3. Leave a value blank if the official source does not state it, and use `status="unverified"` when an issue remains.
4. Add the issue to `FLAGGED` when appropriate so it is visible on the review page.
5. Run both commands above and inspect the generated diff.

## Coordination

`COORDINATION.md` records task ownership, sources, verification notes, irregularities and prior integration history. The repository's earlier research passes and their raw supporting files are retained there and under `data/` and `tools/`.
