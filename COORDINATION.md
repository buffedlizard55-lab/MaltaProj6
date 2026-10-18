# COORDINATION.md — San Francisco Events Project

Shared task board for all agent sessions working on this repository.
**Repo:** https://github.com/buffedlizard55-lab/MaltaProj6
**Published site:** https://buffedlizard55-lab.github.io/MaltaProj6/

> **STATUS:** ⬜ unclaimed · 🟡 in progress · ✅ done · 🔍 needs review
>
> **Two sessions worked on this repository in parallel.** Both are recorded below. Neither session's work was
> discarded: the parallel session's raw data, tooling and its own published views are all still in the repository,
> and the published tables are the **union** of both research passes.

---

## Session registry

| Session ID | Branch | Scope | State |
|---|---|---|---|
| `arena-f54a124f` | `arena/f54a124f-maltaproj6` | Final integration audit: truthful scope/completeness copy, README counts, canonical validation, semantic table markup; `COORDINATION.md`, `README.md`, `scripts/build_site.py`, `tools/validate.py`, generated HTML | 🟡 in progress |
| `arena-b0f3cfd3` | `arena/b0f3cfd3-maltaproj6` | Research, canonical dataset (`data/events.py`), site build (`scripts/`, `assets/site.css`, generated pages), integration, PR/merge | ✅ complete |
| `arena-8fb52462` | `arena/8fb52462-maltaproj6` | Scaffolding, schema, per-task JSON data files (`data/weekly.json`, `data/annual.json`, `data/special.json`, `data/flagged.json`, `data/sources.json`), tooling (`tools/`), own site views (`weekly.html`, `analysis.html`, `sources.html`, `assets/style.css`, `assets/app.js`) | ✅ complete — merged into `main` at `286ae68`, and folded into the union dataset by `arena-b0f3cfd3` |
| `arena-f54a124f` | `arena/f54a124f-maltaproj6` | Final integration audit: truthful scope/completeness copy, README counts, canonical validation, semantic table markup; `COORDINATION.md`, `README.md`, `scripts/build_site.py`, `tools/validate.py`, generated HTML | 🟡 in progress (claim commit `b938226`, 2026-10-18T01:22Z — observed by `arena-bdaa17b4`, not edited by it) |
| `arena-bdaa17b4` | `arena/bdaa17b4-maltaproj6` | **Independent line-by-line audit + gap research (NEW FILES ONLY):** `audit/AUDIT-2026-10-18-bdaa17b4.md`, `audit/check_dataset.py`, `audit/row-audit.csv`, `data/gap-candidates-bdaa17b4.json`, plus this board's registry/task/log rows. Will **not** edit `arena-f54a124f`'s claimed files (`README.md`, `scripts/build_site.py`, `tools/validate.py`, generated `*.html`) or `data/events.py`; dataset/site changes are logged below as integration requests. Branch note: work stays on this session's fixed Arena branch, not a `session-<id>/<task>` branch. | 🟡 in progress — claimed 2026-10-18 by `arena-bdaa17b4` |

**Concurrency note.** `arena-b0f3cfd3` checked the remote at the start of its run (`git ls-remote --heads origin`
returned only `refs/heads/main`) and therefore correctly found no other session to coordinate with. The second
session's branch appeared and was merged into `main` later in the run, which produced a merge conflict with
`index.html`, `annual.html`, `special.html`, `flagged.html`, `assets/style.css`, `COORDINATION.md` and `README.md`.
That conflict is resolved below, in **Merge conflict resolution**, without discarding either session's work.

---

## Task board — `arena-b0f3cfd3`

| # | Task | Status | Owner | Files in scope | Notes |
|---|---|---|---|---|---|
| 0 | Create `COORDINATION.md` task board | ✅ done | `arena-b0f3cfd3` | `COORDINATION.md` | Board created on a repo with no other content. |
| 1 | Research: Recurring (weekly/regular) events — official sources | ✅ done | `arena-b0f3cfd3` | `data/events.py` | 92 rows land in the `recurring` group. Rec & Park, SFPL, Presidio, museums, markets, Sunday Streets, and every commission with a published schedule. |
| 2 | Research: Recurring (annual) events — official sources | ✅ done | `arena-b0f3cfd3` | `data/events.py` | 34 rows land in the `annual` group. Parades, festivals, opera/ballet/theatre seasons, races, holiday traditions. |
| 3 | Research: Special / one-off events — official sources | ✅ done | `arena-b0f3cfd3` | `data/events.py` | 20 rows land in the `special` group. Fleet Week, Presidio 2026 season, Alcatraz closure, dated 2026–2027 programmes. |
| 4 | Research: Museums & attractions (SF city limits) | ✅ done | `arena-b0f3cfd3` | `data/events.py` | FAMSF, Asian Art Museum, SFMOMA, Cal Academy, Exploratorium, California Museum, CJM, SF Zoo, Gardens of Golden Gate Park, Randall, Presidio Museum, Fort Point, Alcatraz, Maritime NHP, Angel Island SP, Golden Gate Bridge. |
| 5 | Research: Performing arts, sports, nightlife | ✅ done | `arena-b0f3cfd3` | `data/events.py` | SF Symphony, SFJAZZ, SF Opera, SF Ballet, ATG San Francisco, SFFILM, Litquake, Silent Film Festival, Giants, Warriors, Valkyries, SF Marathon, Bay to Breakers, Dragon Boat, Palace of Fine Arts pickleball. |
| 6 | Research: Civic/government public meetings & services | ✅ done | `arena-b0f3cfd3` | `data/events.py` | 36 rows land in the `civic` category. Board of Supervisors + 4 committees, Assessment Appeals Boards, Planning, Historic Preservation, SFMTA, Port, Fire, PUC, Arts Commission (7 bodies), Police, Health, SFUSD, Building Inspection, Ethics, Environment, Small Business, Health Service Board, SFCTA, TIDA, HRC, Library, Rec & Park, City Hall weddings, district events. |
| 7 | Verification pass — every row has an official source link | ✅ done | `arena-b0f3cfd3` | `data/events.py`, `data/events.json` | 205 rows, 166 fully verified, 39 with a deliberate blank. 168 distinct official source URLs. Every `source_url` is `https://`. |
| 8 | Site build — GitHub Pages, landing page + subpages | ✅ done | `arena-b0f3cfd3` | `scripts/build_site.py`, `assets/site.css`, `*.html` | 11 generated static pages, no client-side JS. Dashboard landing page with stat tiles, category tiles and analysis tables. |
| 9 | "Flagged for Review" page | ✅ done | `arena-b0f3cfd3` | `data/events.py` (FLAGGED), `flagged.html` | **72** published items: conflicts between official sources, blank-cell rows, ended events, out-of-scope exclusions. 19 from this session + 53 merged from the parallel session. |
| 10 | Integration: merge branches, re-verify, link check, publish | ✅ done | `arena-b0f3cfd3` | `data/*`, `scripts/*`, `tools/*`, `*.html`, `assets/*` | Merged `origin/main` (the parallel session's work), unioned both datasets, re-ran the link/anchor/tag checker over all 14 pages → 0 problems. Row counts on all 8 listing pages match the dataset. |
| 11 | PR → main, merge, confirm Pages deploy | ✅ done | `arena-b0f3cfd3` | — | PR **#7** https://github.com/buffedlizard55-lab/MaltaProj6/pull/7 — merged to `main` 2026-10-18T01:10:21Z as `5c0c788` (main dataset + site). PR **#9** https://github.com/buffedlizard55-lab/MaltaProj6/pull/9 — merged 2026-10-18T01:13:27Z as `3f16ffb` (final re-sync + register). GitHub Pages build for `3f16ffb` completed with status `built`, `error: null`. Live site confirmed at https://buffedlizard55-lab.github.io/MaltaProj6/ . PR #2 was auto-closed by GitHub when the head branch absorbed the base branch's tip commit; PRs #7 and #9 replaced it from the same branch. |

## Task board — `arena-8fb52462` (parallel session, as recorded by that session)

| ID | Task | Status | Owner | Files in scope |
|----|------|--------|-----------------|----------------|
| T1 | Repo scaffolding, schema, validation tooling, coordination board | done | arena-8fb52462 | `COORDINATION.md`, `README.md`, `tools/`, `data/schema.md`, `.gitignore` |
| T2 | Recurring weekly/monthly events: research + verification | done | arena-8fb52462 | `data/weekly.json` |
| T3 | Recurring annual events: research + verification | done | arena-8fb52462 | `data/annual.json` |
| T4 | Special / one-time events (2026–2027): research + verification | done | arena-8fb52462 | `data/special.json` |
| T5 | Flagged-for-review register + source registry | done | arena-8fb52462 | `data/flagged.json`, `data/sources.json` |
| T6 | Site build: dashboard, category subpages, tables, analysis | done | arena-8fb52462 | `tools/build_site.py`, `assets/`, generated `*.html`, `data/meta.json` |
| T7 | Integration: merge branches, line-by-line re-verification, link check, Pages deploy | done | arena-8fb52462 | all shared outputs, `COORDINATION.md` |

## Task board — `arena-bdaa17b4` (independent audit session)

All prior tasks above are ✅ done / claimed by other sessions, so this session claims only new, non-overlapping work.

| ID | Task | Status | Owner | Files in scope |
|----|------|--------|-------|----------------|
| A1 | Claim non-overlapping audit scope; record parallel claim by `arena-f54a124f` | 🟡 in progress | arena-bdaa17b4 | `COORDINATION.md` (registry/task/log rows only) |
| A2 | Structural line-by-line audit of all 205 rows (source present/https, blanks vs status, duplicates, out-of-SF text, past-dated specials) | ⬜ unclaimed→claimed here | arena-bdaa17b4 | `audit/check_dataset.py`, `audit/row-audit.csv` (both new) |
| A3 | Live official-source spot re-verification (stratified sample + all irregular rows) | ⬜ unclaimed→claimed here | arena-bdaa17b4 | `audit/AUDIT-2026-10-18-bdaa17b4.md` (new) |
| A4 | Gap research: SF-city-limits events missing from the 205, verified from official sources only | ⬜ unclaimed→claimed here | arena-bdaa17b4 | `data/gap-candidates-bdaa17b4.json` (new) |
| A5 | Integration requests to `arena-f54a124f` / final integration session (no direct edits to claimed files) | ⬜ unclaimed→claimed here | arena-bdaa17b4 | `COORDINATION.md` log only |
| A6 | PR from `arena/bdaa17b4-maltaproj6` → `main`, merge if site still builds, confirm Pages | ⬜ unclaimed→claimed here | arena-bdaa17b4 | — (audit files are additive; no generated-HTML edits) |

**Integration requests for `arena-f54a124f`** (log, do not edit their files): _none yet — A2–A4 findings will be appended here._

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

## Merge conflict resolution (integration by `arena-b0f3cfd3`)

`git merge origin/main` produced conflicts on `index.html`, `annual.html`, `special.html`, `flagged.html`,
`assets/style.css`, `COORDINATION.md`, `README.md` and `.gitignore`. Resolution:

| File | Resolution | Rationale |
|---|---|---|
| `index.html`, `annual.html`, `special.html`, `flagged.html` | **Regenerated from the union dataset** by `scripts/build_site.py` | The union dataset supersedes both individual datasets; the generated pages are always consistent with it. |
| `assets/style.css` | **Kept the parallel session's file unchanged**; this session's stylesheet was written to a new file `assets/site.css` and all of this session's pages reference it | The parallel session's pages (`weekly.html`, `analysis.html`, `sources.html`) depend on `assets/style.css` and `assets/app.js`. Splitting the two stylesheets keeps both sets of pages correctly styled with no edits to either session's HTML. |
| `assets/app.js`, `data/*.json` (parallel), `data/schema.md`, `data/review.csv`, `tools/*`, `weekly.html`, `analysis.html`, `sources.html`, `.nojekyll` | **Kept as-is** | The parallel session's work is preserved verbatim and is linked from this session's `methodology.html` under "Supplementary views". |
| `COORDINATION.md` | **Merged** — both session registries, both task boards and both logs kept | Neither session's record may be lost. |
| `README.md` | **Merged** — describes the union site, both data layouts and both toolchains | |
| `.gitignore` | **Merged** — union of both ignore lists | |

**Dataset union.** `scripts/merge_parallel.py` converts the parallel session's `data/weekly.json`,
`data/annual.json` and `data/special.json` into this project's schema and merges them into `data/events.py`.
59 rows were added; 25 rows that describe an event already present were **not** duplicated (curated list in
`SKIP_DUPLICATES` in `scripts/merge_parallel.py`). The parallel session's 34 flagged items are merged into the
same "Flagged for review" page (53 items in total). Every imported row keeps its own official source link and
carries a note recording which session found it.

---

## Site map

| Page | File | Contents |
|---|---|---|
| Home / dashboard | `index.html` | Stat tiles, category tiles, type & area analysis tables, recently confirmed dated events, "how to read a row" |
| Regularly recurring | `recurring.html` | 111 rows — fixed weekly / monthly schedules |
| Annual | `annual.html` | 47 rows — year after year |
| Special | `special.html` | 47 rows — dated 2026–2027 events |
| Civic | `civic.html` | 36 rows — boards, commissions, public meetings |
| Arts & culture | `arts.html` | 64 rows — museums, performance, screen |
| Sports | `sports.html` | 9 rows — teams, races, active recreation |
| Markets & food | `markets.html` | 29 rows — farmers markets, food halls, street markets |
| Community & parks | `community.html` | 67 rows — neighbourhood programmes, festivals, free recreation |
| Flagged for review | `flagged.html` | 72 published discrepancies / gaps / exclusions + every row carrying a blank cell |
| Method | `methodology.html` | Scope, sourcing rules, build process, official domains used, known limitations, supplementary views |
| Weekly & monthly (parallel session) | `weekly.html` | The parallel session's recurring-event view |
| Analysis (parallel session) | `analysis.html` | The parallel session's category / neighbourhood analysis |
| Source registry (parallel session) | `sources.html` | The parallel session's list of the 58 official sources it checked |

Every event appears on exactly **one** type page (recurring / annual / special) **and** exactly **one** category page,
so the two views can never disagree. The build script re-checks this on every run.

---

## Log

### `arena-b0f3cfd3` (this session)

- **2026-10-18** — Reviewed repo (empty except `README.md`, one commit). Created this board. `git ls-remote --heads origin` showed only `refs/heads/main`, so no other session was visible to coordinate with at that point.
- **2026-10-18** — **Tasks 1–6 research complete.** Fetched and read 80+ official pages across `sf.gov`, `sfgov.legistar.com`, `sfrecpark.org`, `sfpl.org`, `sfplanning.org`, `sfmta.com`, `sfport.com`, `sf-fire.org`, `famsf.org`, `exploratorium.edu`, `calacademy.org`, `sfmoma.org`, `asianart.org`, `sfzoo.org`, `gggp.org`, `presidio.gov`, `nps.gov`, `parks.ca.gov`, `foodwise.org`, `fleetweeksf.org`, `sfshakes.org`, `sfsymphony.org`, `sfjazz.org`, `sfopera.com`, `sfballet.org`, `broadwaysf.com`, `sffilm.org`, `litquake.org`, `silentfilm.org`, `dragonboatsf.com`, `thesfmarathon.com`, `baytobreakers.com`, `sfpride.org`, `chineseparade.com`, `uissf.org`, `carnavalsanfrancisco.org`, `sfcherryblossom.org`, `sfitalianheritage.org`, `unionstreetsf.com`, `northbeachfestival.org`, `haightashburystreetfair.org`, `nihonmachistreetfair.org`, `moonfestival.org`, `folsomstreet.org`, `transmarch.org`, `castrostreetfair.org`, `castromerchants.com`, `parollanternfestival.com`, `treasurefest.com`, `howweird.org`, `levisstadium.com` and others. Aggregator sites (funcheap, Eventbrite, Yelp, sfstation, tourism blogs, Reddit, Wikipedia) were used **only** to locate official pages, never as evidence.
- **2026-10-18** — **Task 7 verification.** 146 rows, 133 fully verified, 13 with a deliberate blank.
- **2026-10-18** — **Tasks 8/9 site build.** `scripts/build_site.py` renders 11 static pages plus `assets/site.css` (no client-side JavaScript). Added a `group` (recurring / annual / special) and `category` (civic / arts / sports / markets / community) view over the same rows.
- **2026-10-18** — **Task 10 integration.** `git merge origin/main` surfaced the parallel session's merged work and produced conflicts. Resolved as tabulated above; the parallel session's data, tooling and published views were kept and their rows folded into the union dataset (59 added, 25 de-duplicated, 34 flagged items merged). Link/anchor/tag checker over all 14 pages: 110 internal links, every `#anchor` target, every external source URL → **0 problems**. Row counts on all 8 listing pages match the dataset (111 / 47 / 47 / 36 / 64 / 9 / 29 / 67). Local HTTP check returned 200 for every page, stylesheet, script and data file.
- **2026-10-18** — **Task 10b re-sync.** The parallel session pushed three further PRs to `main` while this
  integration was in progress (#3 "Polish dashboard copy, badge labels and exhibition title", #4 "Blank undated
  annual display values instead of prose in the dates column", #5 "Final accuracy and documentation pass").
  `origin/main` was merged again and the union rebuilt on top of it: the parallel session's `data/weekly.json`,
  `data/annual.json`, `data/special.json`, `data/review.csv` and `tools/*` are taken as-is; the generated pages
  are regenerated from the union dataset. Result is unchanged at 205 events / 53 flagged items, with 0 link,
  anchor or tag problems across all 14 pages.
- **2026-10-18** — **Task 10c final re-sync.** The parallel session pushed PRs #6 and #8 while this integration was
  in flight; `origin/main` was merged again and the union rebuilt on top of it. PR #8 added 19 further discrepancy
  records to the parallel session's register, so the published review register grew from 53 to **72** items while
  the event list stayed at **205** rows. 0 link, anchor or tag problems across all 14 pages.
- **2026-10-18** — **Task 11 complete.** PR #2 was auto-closed by GitHub when the head branch absorbed the base
  branch's tip commit, so a replacement PR was opened from the same branch.
  **PR #7 → https://github.com/buffedlizard55-lab/MaltaProj6/pull/7 — MERGED** at 2026-10-18T01:10:21Z,
  merge commit `5c0c788` (`Merge pull request #7 from buffedlizard55-lab/arena/b0f3cfd3-maltaproj6`).
  GitHub Pages build for `5c0c788` finished with status **`built`** and `error: null` (23 s build, source
  `main` / `/`). Live pages confirmed by fetching the deployed site: `index.html` (205 events / 166 verified /
  39 flagged / 53 discrepancies / 88 official domains), `recurring.html` (111 rows) and `flagged.html`
  (53 items) all serve the merged content, and the parallel session's `weekly.html`, `analysis.html` and
  `sources.html` remain live alongside them.
- **2026-10-18** — **Task 11 closed out.** PR **#9** https://github.com/buffedlizard55-lab/MaltaProj6/pull/9 —
  **MERGED** 2026-10-18T01:13:27Z, merge commit `3f16ffbc5b93d2f96ac9ea292601b94ceb4afa7d`.
  GitHub Pages build for `3f16ffb` finished with status **`built`** and `error: null`.
  Live content confirmed by fetching the deployed site: the dashboard shows **205 events / 166 fully verified /
  39 rows with a flagged gap / 72 discrepancies published / 88 official domains**, and the type table now reads
  111 regularly recurring · 47 annual · 47 special.
  **Published site: https://buffedlizard55-lab.github.io/MaltaProj6/**

### Final published state

| | |
|---|---|
| Events | **205** (111 regularly recurring · 47 annual · 47 special/dated) |
| Fully verified rows | **166** |
| Rows with one deliberate blank cell | **39** (each with a published reason) |
| Irregularities published on "Flagged for review" | **72** |
| Distinct official source URLs / official domains | **142** / **88** |
| Static pages | **14** (11 generated from the union dataset, 3 preserved from the parallel session) |
| PRs merged by this session | #7 (`5c0c788`), #9 (`3f16ffb`), #10 (`9ff8e59`) |
| GitHub Pages deploy | **`built`**, `error: null`, source `main` / `/` |

### `arena-8fb52462` (parallel session, as recorded by that session)

- **2026-10-18T00:55Z** — Repo reviewed: initial commit only, `README.md` placeholder. GitHub Pages already built from `main` `/` (commit `8b59260`). Created the board and claimed T1; claimed T2–T5 because it was the only active session at that timestamp.
- **2026-10-18T06:40Z** — T1–T7 complete in one session: 87 rows (26 recurring, 28 annual, 33 special), 34 review notes, 58 registered official sources. `tools/seed_data.py` is the reviewable authoring trail; `tools/validate.py` passes with 0 errors.
- **2026-10-18T06:40Z** — Irregularities published on its `flagged.html`: `carnavalsf.com` resolves to an unrelated gambling site (Carnaval excluded); `exploratorium.edu/visit/after-dark` 404; `famsf.org/visit/free-admission` 404; `about.asianart.org` and `ybgfestival.org` unusable; `sfstpatricksparade.com` unreachable; `sfoutsidelands.com` HTTP 500; `thesfmarathon.com` and `baytobreakers.com` internal date-copy conflicts; `chineseparade.com` labels 2027 "Year of the Ram"; `sfballet.org` cookie wall; `sfautoshow.com` under construction; `unionsquaresf.com` parked. Scope exclusions: Black Joy Parade (Oakland), Daly City Street Festival, Levi's Stadium / Santa Clara.

---

## Irregularities found and published (all on `flagged.html`)

### From `arena-b0f3cfd3` (19)

1. Board of Supervisors Land Use & Transportation Committee — Legistar says 4:30 p.m., SFGovTV says 1:30 p.m. → time left blank.
2. Board of Supervisors Rules Committee — Legistar says 1:00 p.m., SFGovTV says 10:00 a.m. → time left blank.
3. Board of Supervisors Budget and Finance Committee — SFGovTV lists "Wednesdays at 12:30AM", which is not a credible meeting time → row uses the Legistar time with a note.
4. Assessment Appeals Boards — the sf.gov citywide calendar and the Board landing page give different times for 10/19/2026 → times left blank.
5. Recreation and Park Commission — department says third Thursday; SFGovTV says 2nd & 4th Thursdays. The published 2026 dates are all third Thursdays → row follows the department.
6. Library Commission — Bylaws say third Thursday 4:30 p.m.; a separate SFPL policies page says first Tuesday *and* third Thursday at 4:00 p.m. → row uses the Bylaws.
7. Bay to Breakers — organiser's own page title says "May 16, 2027" while its body copy still says "May 18" → date taken from the title.
8. SFFILM — festival page says April 24–May 4, 2026; submission pages say April 23–May 3, 2026 → row uses the festival page.
9. Dragon Boat Festival — Treasure Island (until 2015) → Lake Merced in 2026 → row reflects the 2026 venue.
10. TreasureFest — no confirmed San Francisco date; organiser is "scouting our next location in the Bay Area" → row left entirely blank.
11. How Weird Street Faire — ended after 25 years (2000–2024) per the organiser's own site → excluded and published.
12. San Francisco 49ers — all home games at Levi's Stadium, **Santa Clara** → excluded (out of city limits) and published.
13. Alcatraz Island — closed for dock repairs 26 Oct – ~18 Nov 2026 → published.
14. Castro Menorah Lighting — organiser's calendar says 7 Dec 2026, its own description says 15 Dec → row uses the calendar date.
15. Mission Community Market — March–November only, unlike the other two Foodwise markets → published.
16. Human Rights Commission — no published regular cadence → frequency left blank.
17. Larsen Pickleball Complex — no street address published on the official page → address left blank.
18. SF Music Week — referenced on an official sf.gov release but no official programme page located → dates and cost left blank.
19. Golden State Valkyries — 2026-27 home fixtures not confirmed against an official schedule page → dates left blank.

### From `arena-8fb52462` (34, merged verbatim)

`f-001` Carnaval SF domain hijack · `f-002` Fillmore Jazz legacy domain hijack · `f-003` Dragonspunk Farmers Market source unavailable · `f-004` SOMA West Farmers Market source unavailable · `f-005` St. Patrick's Day Parade source unavailable · `f-006` North Beach Festival source unavailable · `f-007` Fringe Festival domain hijack · `f-008` Union Square ice rink / tree lighting domain parked · `f-009` San Francisco Auto Show source unavailable · `f-010` Presidio Picnic source unavailable · `f-011` Yerba Buena Gardens Festival source unavailable · `f-012` Asian Art Museum exhibitions page broken · `f-013` FAMSF free-admission page broken · `f-014` Alemany Farmers Market hours conflict · `f-015` North Beach Farmers Market address/season conflict · `f-016` SF Environment farmers-market directory stale · `f-017` Folsom Street Fair 2027 date check · `f-018` Castro Street Fair 2027 date check · `f-019` Italian Heritage Parade 2027 date check · `f-020` SFMTA shared-space permit expiry · `f-021` 2027 dates for major annual events not yet announced · `f-022` Day of the Dead Festival of Altars stale page · `f-023` Oakland and Santa Clara scope exclusion · `f-024` Daly City Street Festival scope exclusion · `f-025` TreasureFest dated schedule unverified · `f-026` Litquake 2026 run dates unverified · `f-027` RSA Conference 2027 dates unverified · `f-028` annual event end dates unverified · `f-029` SF Marathon page copy date inconsistency · `f-030` Bay to Breakers page copy date inconsistency · `f-031` Muni Heritage Weekend source unavailable · `f-032` Pokemon World Championship source unavailable · `f-033` Potrero Hill Festival time conflict · `f-034` Haight-Ashbury Street Fair date check.
