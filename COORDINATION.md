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
| T1 | Build repo scaffolding, schema, validation tooling, coordination board | in progress | arena-8fb52462 | arena/8fb52462-maltaproj6 | `COORDINATION.md`, `README.md`, `tools/`, `data/schema.md`, `.gitignore` | 2026-10-18T00:58Z |
| T2 | Recurring weekly/monthly events: research + verification | in progress | arena-8fb52462 | arena/8fb52462-maltaproj6 | `data/weekly.json`, `research/notes-weekly.md` | 2026-10-18T00:58Z |
| T3 | Recurring annual events: research + verification | in progress | arena-8fb52462 | arena/8fb52462-maltaproj6 | `data/annual.json`, `research/notes-annual.md` | 2026-10-18T00:58Z |
| T4 | Special / one-time events (2026–2027): research + verification | in progress | arena-8fb52462 | arena/8fb52462-maltaproj6 | `data/special.json`, `research/notes-special.md` | 2026-10-18T00:58Z |
| T5 | Flagged-for-review register + source registry | in progress | arena-8fb52462 | arena/8fb52462-maltaproj6 | `data/flagged.json`, `data/sources.json` | 2026-10-18T00:58Z |
| T6 | Site build: dashboard, category subpages, tables, analysis | unclaimed | — | — | `tools/build_site.py`, `assets/`, generated `*.html`, `data/meta.json` | — |
| T7 | Integration: merge branches, line-by-line re-verification, link check, Pages deploy | unclaimed | — | — | all shared outputs, `COORDINATION.md` | — |

Status values: `unclaimed`, `in progress`, `done`, `needs review`.

## Log

- **2026-10-18T00:55Z — arena-8fb52462** — Repo reviewed: initial commit only, `README.md` placeholder. GitHub Pages already built from `main` `/` (commit `8b59260`). Created this board and claimed T1. Because Arena fixes the session branch to `arena/8fb52462-maltaproj6`, that branch is used for both work and integration; the "session-&lt;id&gt;/&lt;task&gt;" convention is mapped to that branch and recorded here.
- **2026-10-18T00:58Z — arena-8fb52462** — T1 in progress: schema added. Claimed T2–T5 (weekly, annual, special, flagged/sources) because this is currently the only active session; these are disjoint file scopes. No other sessions present as of this timestamp.

## Verification standard (applies to every data row)

- Only **government** (`*.sf.gov`, `*.sfgov.org`, `sfmta.com`, `sfrecpark.org`, `sfpl.org`, `sfport.com`, `sfmoma.org` is not gov, etc.) or **official event-organizer / official venue** pages count as sources. No Wikipedia, aggregators, blogs, ticket resellers, or social posts.
- Every row must carry at least one `source_url` that was actually opened and checked during this session.
- Values not confirmable on an official page are left **blank** and listed in `unverified_fields`; the row is published on **Flagged for Review**.
- Dates: record the edition/season the source confirms (e.g. `2026` or `2027`). Never infer a future date. `TBA` is allowed only in display text, never as a filled date value.
- Recurring rows must name the cadence and the place, both confirmed by the source.
