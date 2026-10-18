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
| `index.html` | Dashboard — stat tiles, category tiles, type & area analysis, recently confirmed dated events |
| `recurring.html` | 92 rows — events on a fixed weekly / monthly schedule |
| `annual.html` | 34 rows — events that repeat year after year |
| `special.html` | 20 rows — dated 2026–2027 events |
| `civic.html` | 36 rows — boards, commissions and public meetings |
| `arts.html` | 41 rows — museums, performance and screen |
| `sports.html` | 8 rows — teams, races and active recreation |
| `markets.html` | 10 rows — farmers markets, food halls and street markets |
| `community.html` | 51 rows — neighbourhood programmes, festivals and free recreation |
| `flagged.html` | 19 published discrepancies, gaps and out-of-scope decisions |
| `methodology.html` | Scope, sourcing rules, build process, official domains used, known limitations |

Each event appears on exactly **one** type page (recurring / annual / special) **and** exactly **one**
category page, so the two views can never disagree.

## Repository layout

```
COORDINATION.md        shared task board (status, owners, file scope, log, irregularities)
data/events.py         canonical dataset: 146 events + 19 flagged items
data/events.json       machine-readable mirror emitted by the build
scripts/build_site.py  renders the static site from the dataset (no client-side JavaScript)
assets/style.css       site stylesheet
*.html                 generated pages (committed so the site works straight from the branch)
```

## Rebuilding the site

```bash
python3 scripts/build_site.py
```

This regenerates `data/events.json` and every HTML page from `data/events.py`, so the tables, the counts on
the dashboard and the flagged list can never drift apart.

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
irregularities).
