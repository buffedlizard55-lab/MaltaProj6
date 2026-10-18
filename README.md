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
data/meta.json        build metadata, counts, analysis
tools/build_site.py   static site generator (pages at repo root)
tools/validate.py     schema + source + link validation
assets/               stylesheet and dashboard script
research/             working notes and verification trail
COORDINATION.md       shared task board for parallel sessions
```

## Rebuild

```bash
python3 tools/validate.py        # schema, official-source, link checks
python3 tools/build_site.py      # regenerate HTML pages at repo root
```

No third-party dependencies; Python 3.11+ standard library only.
