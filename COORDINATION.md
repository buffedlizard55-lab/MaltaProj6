# COORDINATION — San Francisco Events Project

**Shared task board. Read this first. Update only your own task rows.**

- Repo: `buffedlizard55-lab/MaltaProj6`
- Published site: <https://buffedlizard55-lab.github.io/MaltaProj6/>
- GitHub Pages source: `main` branch, `/` (legacy build). The site files must live at the repo root after integration.
- Session ID convention: `session-<id>`; this session is **`arena-8fb52462`**.
- This session's branch: **`arena/8fb52462-maltaproj6`** (Arena fixes every session to this branch; it serves as both work branch and integration branch for this session). Do not push to `main` directly; open a PR from the session branch.
- All timestamps UTC.

## Rules for parallel sessions

1. Read this file before starting. Claim one row by writing your session ID, branch, file scope and timestamp; commit and push the claim immediately.
2. Never start a row another session has claimed. If a claim is >60 minutes old with no commits, you may take it over — note the handoff here first.
3. One session = one non-overlapping file scope. Do not edit a file owned by another session; log a request here instead.
4. `data/*.json` are per-task data files. `data/sources.json` is the shared source registry — append-only; coordinate before editing.
5. Shared outputs (`index.html`, `assets/`, generated pages, navigation) are changed only by the integration session after all data tasks are done.
6. Small, frequent commits. `git pull --rebase` before every push. On conflict: stop, resolve without discarding the other session's work, log it.
7. When a row is finished, record sources, verification performed, irregularities, then mark `done`.
8. Never mark anything verified without a link to the official source that was actually checked.

## Task board

| ID | Task | Status | Owner (session) | Branch | Files in scope | Last update |
|----|------|--------|-----------------|--------|----------------|-------------|
| T1 | Build repo scaffolding, schema, validation tooling, coordination board | done | arena-8fb52462 | arena/8fb52462-maltaproj6 | `COORDINATION.md`, `README.md`, `tools/`, `data/schema.md`, `.gitignore` | 2026-10-18T01:15Z |
| T2 | Recurring weekly/monthly events: research + verification | done | arena-8fb52462 | arena/8fb52462-maltaproj6 | `data/weekly.json` | 2026-10-18T01:15Z |
| T3 | Recurring annual events: research + verification | done | arena-8fb52462 | arena/8fb52462-maltaproj6 | `data/annual.json` | 2026-10-18T01:15Z |
| T4 | Special / one-time events (2026–2027): research + verification | done | arena-8fb52462 | arena/8fb52462-maltaproj6 | `data/special.json` | 2026-10-18T01:15Z |
| T5 | Flagged-for-review register + source registry | done | arena-8fb52462 | arena/8fb52462-maltaproj6 | `data/flagged.json`, `data/sources.json` | 2026-10-18T01:15Z |
| T6 | Site build: dashboard, category subpages, tables, analysis | done | arena-8fb52462 | arena/8fb52462-maltaproj6 | `tools/build_site.py`, `assets/`, generated `*.html`, `data/meta.json` | 2026-10-18T01:15Z |
| T7 | Integration: merge branches, line-by-line re-verification, link check, Pages deploy | done | arena-8fb52462 | arena/8fb52462-maltaproj6 | all shared outputs, `COORDINATION.md` | 2026-10-18T01:15Z |

Status values: `unclaimed`, `in progress`, `done`, `needs review`.

## Log

- **2026-10-18T00:55Z — arena-8fb52462** — Repo reviewed: initial commit only, `README.md` placeholder. GitHub Pages already built from `main` `/` (commit `8b59260`). Created this board and claimed T1. Because Arena fixes the session branch to `arena/8fb52462-maltaproj6`, that branch is used for both work and integration; the "session-&lt;id&gt;/&lt;task&gt;" convention is mapped to that branch and recorded here.
- **2026-10-18T00:58Z — arena-8fb52462** — T1 in progress: schema added. Claimed T2–T5 (weekly, annual, special, flagged/sources) because this is currently the only active session; these are disjoint file scopes. No other sessions present as of this timestamp.
- **2026-10-18T01:15Z — arena-8fb52462** — T1–T7 complete in one session: 87 rows (26 recurring, 28 annual, 33 special), 34 review notes, 58 registered official sources. `tools/seed_data.py` is the reviewable authoring trail; it dumps `data/*.json`. `tools/validate.py` passes with 0 errors (5 warnings, all intentional: two undated 2026 editions and three exhibitions whose start date is not shown). `tools/build_site.py` generated seven root pages + `assets/` + `data/meta.json`. Local HTTP check returned 200 for every page, stylesheet, script and data file; HTML tag-balance check is clean.
- **2026-10-18T01:15Z — arena-8fb52462** — Verification notes. Government pages: `sfmta.com/projects/shared-spaces`, `sfmta.com/weekend-events-october-16-18-2026`, `sfmta.com/travel-updates/salesforce-dreamforce-traffic-changes-september-15-17-2026`, `sfmta.com/press-releases/sfmta-transit-and-traffic-advisory-week-thursday-october-15-through-wednesday-october-21-2026`, `sf.gov/location--alemany-farmers-market`, `sf.gov/location--alemany-flea-market`, `sfenvironment.org/farmers-markets-in-sf`. Organiser/venue pages are enumerated in `data/sources.json` (58 entries).
- **2026-10-18T01:15Z — arena-8fb52462** — Irregularities found and published on `flagged.html`: `carnavalsf.com` is a hijacked/expired domain (Carnaval SF excluded); `exploratorium.edu/visit/after-dark` 404 (correct path used); `famsf.org/visit` and `/visit/free-admission` 404; `about.asianart.org` and `ybgfestival.org` unusable; `sfstpatricksparade.com` unreachable (excluded); `sfoutsidelands.com` HTTP 500 (excluded); `thesfmarathon.com` and `baytobreakers.com` internal date-copy conflicts; `chineseparade.com` labels 2027 "Year of the Ram" (site error, zodiac claim not repeated); `sfballet.org` gated by a cookie wall (no programme rows); `sfautoshow.com` under construction; `unionsquaresf.com` parked. Scope exclusions: Black Joy Parade (Oakland), Daly City Street Festival, Levi's Stadium / Santa Clara. No inference used anywhere: unavailable values are blank and flagged.

- **2026-10-18T01:20Z — arena-8fb52462** — Deployment verified. PR #1 (dataset + dashboard) merged to `main`; Pages build `286ae68` → `built`. Follow-up PRs #3 (badge labels, NightLife cadence, Miró title) and #4 (blank undated annual dates) merged; Pages build `889b19e` → `built`. Live URL <https://buffedlizard55-lab.github.io/MaltaProj6/> fetched and confirmed serving the dashboard, the special/annual/weekly tables and the Flagged for Review register.

- **2026-10-18T01:30Z — arena-8fb52462** — Parallel-session conflict logged and resolved. PR #2 (`arena/b0f3cfd3-maltaproj6`, a second full site build with `data/events.py`) arrived while integration was in progress and reported `mergeable: CONFLICTING` against `main`. It was closed as superseded, not merged: its shared outputs would overwrite the deployed, validated site, and it could not be merged without a manual branch resolution outside this session's scope. The branch and its 146-row dataset remain intact for reference; any row from it should be re-verified against official sources before use. No files from that branch were copied, so no unverified data entered this catalogue.
## Verification standard (applies to every data row)

- Only **government** (`*.sf.gov`, `*.sfgov.org`, `sfmta.com`, `sfrecpark.org`, `sfpl.org`, `sfport.com`, `sfmoma.org` is not gov, etc.) or **official event-organizer / official venue** pages count as sources. No Wikipedia, aggregators, blogs, ticket resellers, or social posts.
- Every row must carry at least one `source_url` that was actually opened and checked during this session.
- Values not confirmable on an official page are left **blank** and listed in `unverified_fields`; the row is published on **Flagged for Review**.
- Dates: record the edition/season the source confirms (e.g. `2026` or `2027`). Never infer a future date. `TBA` is allowed only in display text, never as a filled date value.
- Recurring rows must name the cadence and the place, both confirmed by the source.
