# COORDINATION.md — San Francisco Events Project

Shared task board for all agent sessions working on this repository.
**Repo:** https://github.com/buffedlizard55-lab/MaltaProj6
**Branch model:** each session works on its own branch `session-<id>/<task>` (or a git worktree) and edits only files in its claimed scope.

> **STATUS:** ⬜ unclaimed · 🟡 in progress · ✅ done · 🔍 needs review

---

## Session registry

| Session ID | Agent / branch | Notes |
|---|---|---|
| `arena-b0f3cfd3` | `arena/b0f3cfd3-maltaproj6` | Primary session: research + data + site build + integration + PR/merge |

---

## Task board

| # | Task | Status | Owner | Files in scope | Notes |
|---|---|---|---|---|---|
| 0 | Create `COORDINATION.md` task board | ✅ done | `arena-b0f3cfd3` | `COORDINATION.md` | Board created on a repo with no other content. |
| 1 | Research: Recurring (weekly/regular) events — official sources | 🟡 in progress | `arena-b0f3cfd3` | `data/*.json`, `data/recurring.md` | Rec & Park, Library, Symphony, markets, classes |
| 2 | Research: Recurring (annual) events — official sources | ⬜ unclaimed | — | — | Parades, festivals, annual civic ceremonies |
| 3 | Research: Special / one-off events — official sources | ⬜ unclaimed | — | — | Fleet Week, holiday, seasonal |
| 4 | Research: Museums & attractions (SF city limits) | ⬜ unclaimed | — | — | FAMSF, Exploratorium, NPS Presidio/Fort Point |
| 5 | Research: Performing arts, sports, nightlife | ⬜ unclaimed | — | — | SFS, Opera, Ballet, Giants, 49ers, Warriors |
| 6 | Research: Civic/government public meetings & services | ⬜ unclaimed | — | — | SF.gov calendars, commissions |
| 7 | Verification pass — every row has an official source link | ⬜ unclaimed | — | — | Unverified values left blank + flagged |
| 8 | Site build — GitHub Pages, landing page + subpages | ⬜ unclaimed | — | — | Clean dashboard-style UI, tables, analysis |
| 9 | "Flagged for Review" page | ⬜ unclaimed | — | — | Irregularities + unverified items with links |
| 10 | Integration: merge branches, re-verify, link check, publish | ⬜ unclaimed | — | — | Only final integration session touches shared outputs |
| 11 | PR → main, merge, confirm Pages deploy | ⬜ unclaimed | — | — | Record PR link + merge result here |

---

## Rules agreed for this project

1. **No manual input required** — sessions work autonomously to completion.
2. **Official, verified sources only.** Every table row must carry a link to the official/primary source (organiser's own site, or the government agency that runs it). No aggregators (no Eventbrite, Facebook, Yelp, SF funcheap, etc.) as *primary* evidence.
3. **Never infer.** If a field (date, time, address, frequency) cannot be confirmed from the official source, leave it **blank** and mark the row **Unverified** on the "Flagged for Review" page with the reason.
4. **City-limits only.** San Francisco city limits only. Excluded: Oakland/Berkeley/Emeryville, Marin/Sausalito/Mill Valley, San Mateo/Palo Alto/San Jose, Santa Clara, Alameda, and anything else outside the SF city boundary. Presidio of San Francisco, Fort Point and Alcatraz *are* inside the SF city limits (NPS / Presidio Trust) and are included, with the jurisdiction noted.
5. **Scoping rule for changes.** If a task needs a file owned by another session, log the request here instead of editing it.
6. **Small, frequent commits; `git pull --rebase` before every push.**
7. **Shared outputs** (the consolidated table data, site index and navigation) are changed only by the final integration session, after all other tasks are done.

---

## Log

- **2026-10-18** — `arena-b0f3cfd3`: Reviewed repo (empty except `README.md`, one commit). Created this board. Claimed tasks 1–11 in sequence as a single primary session (no other sessions were active on the remote at claim time).
