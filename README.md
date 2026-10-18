# San Francisco Events

A verified, source-linked directory of **every event happening inside the City of San Francisco** —
organised by how often it happens, and by subject area.

- **Scope:** the City and County of San Francisco only. Events in other Bay Area cities are excluded
  (and the exclusions are published).
- **Sourcing:** every single row links to the official organiser, city agency, state agency or national-park
  page that was opened and checked. Nothing is inferred — if an official source did not state a value, the
  cell is left blank and the row is listed on the **Flagged for review** page.

## Site

The site is plain static HTML and is published with GitHub Pages.

| Page | Contents |
|---|---|
| `index.html` | Dashboard — stat tiles, category tiles, type & neighbourhood analysis, recently confirmed dated events |
| `recurring.html` | 111 rows — events on a fixed weekly / monthly schedule |
| `annual.html` | 47 rows — events that repeat year after year |
| `special.html` | 47 rows — dated 2026–2027 events |
| `civic.html` | 36 rows — boards, commissions and public meetings |
| `arts.html` | 64 rows — museums, performance and screen |
| `sports.html` | 9 rows — teams, races and active recreation |
| `markets.html` | 29 rows — farmers markets, food halls and street markets |
| `community.html` | 67 rows — neighbourhood programmes, festivals and free recreation |
| `flagged.html` | 53 published discrepancies, gaps and out-of-scope decisions + every row carrying a blank cell |
| `methodology.html` | Scope, sourcing rules, build process, official domains used, known limitations |
| `weekly.html` | Supplementary view from the parallel agent session (see below) |
| `analysis.html` | Supplementary analysis view from the parallel agent session |
| `sources.html` | Supplementary source registry from the parallel agent session |

Each event appears on exactly **one** type page (recurring / annual / special) **and** exactly **one**
category page, so the two views can never disagree.

## Two parallel sessions

Two agent sessions worked on this repository at the same time. Neither session's work was thrown away:

- `arena-b0f3cfd3` built the canonical dataset (`data/events.py`), the generator
  (`scripts/build_site.py`) and the dashboard site, and performed the final integration.
- `arena-8fb52462` built the scaffolding and schema (`data/schema.md`), a parallel per-task dataset
  (`data/weekly.json`, `data/annual.json`, `data/special.json`), a flagged register and source registry
  (`data/flagged.json`, `data/sources.json`), validation tooling (`tools/`) and its own site views
  (`weekly.html`, `analysis.html`, `sources.html`).

`scripts/merge_parallel.py` folds the second session's rows into the first session's schema. 59 rows were
added to the published list and 25 that describe an event already present were not duplicated. The parallel
session's raw data, tooling and published pages all remain in the repository and are linked from
`methodology.html`. `COORDINATION.md` records exactly how the merge conflict was resolved.

## Repository layout

```
COORDINATION.md        shared task board (both sessions, sources, verification, irregularities, merge log)
data/events.py         canonical dataset: 205 events + 53 flagged items
data/events.json       machine-readable mirror emitted by the build
data/weekly.json       parallel session — recurring rows (raw, preserved)
data/annual.json       parallel session — annual rows (raw, preserved)
data/special.json      parallel session — special rows (raw, preserved)
data/flagged.json      parallel session — flagged register (raw, preserved)
data/sources.json      parallel session — source registry (raw, preserved)
data/review.csv        parallel session — line-by-line review sheet
data/schema.md         parallel session — JSON schema documentation
scripts/build_site.py  renders the static site from the dataset (no client-side JavaScript)
scripts/merge_parallel.py  converts + merges the parallel session's dataset
tools/                 parallel session — seed_data.py, build_site.py, validate.py
assets/site.css        this session's stylesheet (used by the generated pages)
assets/style.css       parallel session's stylesheet (used by its pages)
assets/app.js          parallel session's script
*.html                 generated pages (committed so the site works straight from the branch)
```

## Rebuilding the site

```bash
python3 scripts/build_site.py
```

This regenerates `data/events.json` and every HTML page from `data/events.py` plus the parallel session's
JSON files, so the tables, the counts on the dashboard and the flagged list can never drift apart.

## Adding or changing an event

1. Edit the relevant `dict(...)` in `data/events.py`.
2. Fill in `source_name` and `source_url` with the **official** page you checked. Never cite an aggregator.
3. Leave a field as `""` if the official source does not state it, and set `status="unverified"`.
4. Add a matching entry to `FLAGGED` so the gap is published rather than hidden.
5. Run `python3 scripts/build_site.py` and commit.

## Verification rules

- Official sources only: organiser sites, `sf.gov`, `sfgov.legistar.com`, `sfrecpark.org`, `sfpl.org`,
  `sfmta.com`, `sfport.com`, `parks.ca.gov`, `nps.gov` and similar. Aggregators may be used to *find* an
  official page but never as the evidence for a value.
- Never infer. Blank means "the source did not say".
- Disagreements between two official pages are published, not silently resolved.
- Ended and cancelled events are listed on the Flagged for review page rather than quietly dropped.

Last verification pass: **18 October 2026** (see `COORDINATION.md` for the full log and the list of
irregularities from both sessions).
