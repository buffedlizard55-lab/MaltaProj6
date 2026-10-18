# San Francisco Events Index

A verified, source-linked catalogue of events in the **City and County of San Francisco**, split into:

- **Recurring weekly / monthly** events (markets, museum late nights, free days, community programmes)
- **Recurring annual** events (parades, street fairs, festivals, races, seasons)
- **Special / one-time** events (dated 2026–2027 editions and exhibitions)

Every row links to an official government, organiser, or venue page. Values that could not be confirmed from an official source are left blank and listed on the **Flagged for Review** page.

The static dashboard is published with GitHub Pages at
<https://buffedlizard55-lab.github.io/MaltaProj6/>.

## Repository layout

```
data/weekly.json      recurring weekly / monthly rows
data/annual.json      recurring annual rows
data/special.json     special / one-time rows
data/flagged.json     flagged-for-review register
data/sources.json     source registry (official domains)
data/meta.json        build metadata and counts (generated)
data/review.csv       one line per row with dates, venue and source URL (generated)
tools/seed_data.py    authoring script: sources + every verified row, dumps data/*.json
tools/build_site.py   static site generator (pages at repo root)
tools/validate.py     schema + source + link validation
assets/               stylesheet and dashboard script
research/             working notes and verification trail
COORDINATION.md       shared task board for parallel sessions
```

## Pages

| Page | Contents |
|------|----------|
| `index.html` | Overview, headline counts, what's on now and next, category cards |
| `weekly.html` | Recurring weekly and monthly programmes with cadence, schedule and venue |
| `annual.html` | Annual events, edition-specific dates, next-edition status |
| `special.html` | Dated exhibitions, performances, conventions and one-off events |
| `analysis.html` | Method, coverage, findings, limitations |
| `sources.html` | Every government, organiser and venue page used, mapped to row IDs |
| `flagged.html` | Unverified fields, source irregularities, conflicts and scope decisions |

## Rebuild

```bash
python3 tools/seed_data.py       # author data/*.json from the reviewed source list
python3 tools/validate.py        # schema, official-source, date and link checks
python3 tools/build_site.py      # regenerate the HTML pages and data/meta.json
```

`tools/validate.py` exits non-zero on any error, so it can gate a deploy. It checks that every
`source_url` is https, registered in `data/sources.json`, and not an aggregator, social or
ticketing host; that IDs are unique and categories match their file; that ISO dates are valid and
consistent with `date_status`; that every flagged row exists and is reachable from `flagged.html`;
and that no internal link is broken.

No third-party dependencies; Python 3.11+ standard library only.
