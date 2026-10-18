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
| `arena-f54a124f` | `arena/f54a124f-maltaproj6` | Final integration audit: truthful scope/completeness copy, README counts, canonical validation, semantic table markup; `COORDINATION.md`, `README.md`, `scripts/build_site.py`, `tools/validate.py`, generated HTML | ✅ complete |
| `arena-b0f3cfd3` | `arena/b0f3cfd3-maltaproj6` | Research, canonical dataset (`data/events.py`), site build (`scripts/`, `assets/site.css`, generated pages), integration, PR/merge | ✅ complete |
| `arena-8fb52462` | `arena/8fb52462-maltaproj6` | Scaffolding, schema, per-task JSON data files (`data/weekly.json`, `data/annual.json`, `data/special.json`, `data/flagged.json`, `data/sources.json`), tooling (`tools/`), own site views (`weekly.html`, `analysis.html`, `sources.html`, `assets/style.css`, `assets/app.js`) | ✅ complete — merged into `main` at `286ae68`, and folded into the union dataset by `arena-b0f3cfd3` |
| `arena-bdaa17b4` | `arena/bdaa17b4-maltaproj6` | **Independent line-by-line audit, live source re-verification, gap research, then integration.** Phase 1 (while `arena-f54a124f` was in progress): new files only — `audit/AUDIT-2026-10-18-bdaa17b4.md`, `audit/check_dataset.py`, `audit/row-audit.csv`, `data/gap-candidates-bdaa17b4.json`. Phase 2 (after `arena-f54a124f` completed and merged PRs #12/#13, releasing its claim): integration edits to `data/events.py`, regenerated `*.html`/`data/events.json`, this board. Branch note: work stays on this session's fixed Arena branch, not a `session-<id>/<task>` branch. | ✅ complete — PR #16 merged to `main` 2026-10-18T01:44:12Z (`6d7d63a`), Pages build for that commit `built`, `error: null`; see closing record below |
| `arena-7d8015f4` | `arena/7d8015f4-maltaproj6` | Post-merge integrity audit and repair (`tools/validate.py` reproducibility/blocked-host checks, One City One Book current-selection source, Alcatraz closure row → `unverified`) | ✅ complete — PRs #14/#15 merged to `main` (`2660263`); registry row recorded by `arena-bdaa17b4` during merge resolution (that session logged itself in a "Current session" section, kept below) |
| `arena-23722ef3` | `arena/23722ef3-maltaproj6` | Verification / final-check: 39 live official-source checks, 6 row corrections, 2 new review items, re-merge with `arena-bdaa17b4`, site rebuild | ✅ complete — PR #18 merged to `main` 2026-10-18T02:00:43Z (`9056bd2`), Pages `built`; see log below |
| `arena-3239c070` | `arena/3239c070-maltaproj6` | **Current audit: deep line-by-line re-verification, gap research for missing SF-city events, site polish, flagged registry expansion** | 🟡 in progress — claimed 2026-10-18 |

**Concurrency note.** `arena-b0f3cfd3` checked the remote at the start of its run (`git ls-remote --heads origin`
returned only `refs/heads/main`) and therefore correctly found no other session to coordinate with. The second
session's branch appeared and was merged into `main` later in the run, which produced a merge conflict with
`index.html`, `annual.html`, `special.html`, `flagged.html`, `assets/style.css`, `COORDINATION.md` and `README.md`.
That conflict is resolved below, in **Merge conflict resolution**, without discarding either session's work.

---

## Task board — `arena-23722ef3` (verification / final-check session)

Session branch: `arena/23722ef3-maltaproj6` (Arena-fixed branch for this session; per Arena rules all work
stays on this branch rather than a `session-<id>/<task>` branch).

| # | Task | Status | Owner | Files in scope | Notes |
|---|---|---|---|---|---|
| V0 | Register on the shared board and claim | ✅ done | `arena-23722ef3` | `COORDINATION.md` | Claim commit `c222bcf` pushed before any file edits. |
| V1 | Independent line-by-line re-verification of the published dataset against official sources | ✅ done | `arena-23722ef3` | `COORDINATION.md` (log only) | 39 live checks against official pages (see the session log below). 4 rows corrected, 2 rows' time conflicts resolved, 2 new review items added. |
| V2 | Build + validator + link integrity of the published site | ✅ done | `arena-23722ef3` | — | `python3 scripts/build_site.py` + `python3 tools/validate.py` (OK after both the pre-merge 205-event state and the post-rebase 211-event merge) + independent link/anchor audit (0 problems) + row-coverage audit (all unverified and verified-with-blank rows published on `flagged.html`). |
| V3 | Fix irregularities found by V1/V2 | ✅ done | `arena-23722ef3` | `data/events.py`, `scripts/merge_parallel.py`, `scripts/build_site.py`, `README.md`, `data/events.json`, `*.html` | `tools/validate.py`'s 34 cross-toolchain errors were already resolved by `arena-f54a124f`'s canonical validator (checked, not re-fixed). Corrections are itemised in the session log. |
| V4 | PR to `main`, merge, confirm GitHub Pages deploy, record on this board | ✅ done | `arena-23722ef3` | `COORDINATION.md` | **PR #18** https://github.com/buffedlizard55-lab/MaltaProj6/pull/18 — MERGED 2026-10-18T02:00:43Z as `9056bd2`. GitHub Pages build for the merge: status `built`, `error: null`. Live site confirmed serving the 211-event / 85-review-item state. |

---

## Task board — `arena-3239c070` — deep re-verification & gap research (2026-10-18)

Session branch: `arena/3239c070-maltaproj6` (Arena-fixed branch for this session; per Arena rules all work stays on this branch rather than a `session-<id>/<task>` branch).

| # | Task | Status | Owner | Files in scope | Notes |
|---|---|---|---|---|---|
| W0 | Register on the shared board and claim | 🟡 in progress | `arena-3239c070` | `COORDINATION.md` | This claim commit — pushed before any file edits. |
| W1 | Full line-by-line re-verification against official sources (all 211 rows) | ⬜ unclaimed | `arena-3239c070` | `COORDINATION.md` (log), `data/events.py`, `data/events.json` | Every row's source_url must be fetched and compared; conflicts blanked, flagged. |
| W2 | Gap research: find SF-city events not yet in catalogue, verified from official sources | ⬜ unclaimed | `arena-3239c070` | `data/events.py`, `audit/*.md`, `data/gap-*.json` | Only adds rows where every field is confirmed from official source; leaves blank otherwise. |
| W3 | Site polish & verification artifacts (validator, flagged page, methodology) | ⬜ unclaimed | `arena-3239c070` | `scripts/build_site.py`, `*.html`, `assets/*`, `README.md` | Ensure clean dashboard, tables, analysis, no broken links. |
| W4 | PR to `main`, merge, confirm GitHub Pages deploy, record on this board | ⬜ unclaimed | `arena-3239c070` | `COORDINATION.md` | Merge only after build+validator pass and link audit 0 errors. |

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

## Task board — `arena-f54a124f`

| # | Task | Status | Owner | Files in scope | Notes |
|---|---|---|---|---|---|
| 12 | Final integration audit: scope claims, documentation counts, HTML semantics and canonical validation | ✅ done | `arena-f54a124f` | `COORDINATION.md`, `README.md`, `scripts/build_site.py`, `tools/validate.py`, generated HTML, `assets/site.css`, `data/events.json` | Replaced unsupported exhaustiveness claims with an explicit curated-snapshot limitation; fixed stale review counts; rendered a dedicated source column and valid 9-cell event rows; rebuilt all pages; validator passes. Validator is structural and does not fetch/authenticate source content. |

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
| A1 | Claim non-overlapping audit scope; record parallel claim by `arena-f54a124f` | ✅ done | arena-bdaa17b4 | `COORDINATION.md` (registry/task/log rows only) |
| A2 | Structural line-by-line audit of all 205 rows (source present/https, blanks vs status, duplicates, out-of-SF text, past-dated specials) | ✅ done | arena-bdaa17b4 | `audit/check_dataset.py`, `audit/row-audit.csv` (both new) |
| A3 | Live official-source spot re-verification (stratified sample + all irregular rows) | ✅ done | arena-bdaa17b4 | `audit/AUDIT-2026-10-18-bdaa17b4.md` (new) |
| A4 | Gap research: SF-city-limits events missing from the 205, verified from official sources only | ✅ done | arena-bdaa17b4 | `data/gap-candidates-bdaa17b4.json` (new) |
| A5 | Merge `origin/main` after `arena-f54a124f` completed (PRs #12/#13); resolve board without discarding work | ✅ done | arena-bdaa17b4 | `COORDINATION.md` | Merged with no conflicts (later linearised by `git pull --rebase`); duplicate `arena-f54a124f` registry row (their ✅ row + this session's earlier 🟡 observation row) de-duplicated, keeping theirs. `tools/validate.py` passes on merged tree (`events=205 … pages=14`). |
| A6 | PR from `arena/bdaa17b4-maltaproj6` → `main`, merge if site still builds, confirm Pages | ✅ done | arena-bdaa17b4 | — |
| A7 | Integration fixes for audit irregularities + add verified gap rows; regenerate site | ✅ done | arena-bdaa17b4 | `data/events.py`, generated `*.html`, `data/events.json`, `README.md` counts if changed | Only started **after** `arena-f54a124f` released its claim. |

**Integration requests for `arena-f54a124f`**: none needed — that session finished and merged before A7 started, so `arena-bdaa17b4` performs the integration itself and records every change in the audit report and the log below.

**Audit findings queued for A7** (all re-verified live 2026-10-18; detail in `audit/AUDIT-2026-10-18-bdaa17b4.md`):
`art-angel-island` jurisdiction note contradicted by official CA State Parks facility listing (Tiburon / Marin County) · `rec-bandshell-illuminate-live` ≡ `ann-illuminate-live` duplicate · `ann-trans-march` ≡ `spc-sf-pride-trans-march-2026` duplicate · `ann-parol-lantern` 2025 prose in the confirmed-dates cell · `spc-opera-in-the-park` venue *is* stated (Robin Williams Meadow) in its cited source · `x-s-020` Manon start date conflicts with SF Opera's season release and `art-sfopera` · `civ-recpark-operations` schedule contradicts its own note, source now redirects to a CivicPlus login · 32 dated rows whose latest date precedes the audit date.

---

## Session log — `arena-23722ef3` (line-by-line verification / final-check session, 2026-10-18)

**Scope.** Independent re-verification pass over the published catalogue and site, per the task's
"verify line by line, official sources only, no hallucinations" requirement. This session found the
project already complete on `main` (PRs #1–#13 from `arena-8fb52462`, `arena-b0f3cfd3` and
`arena-f54a124f`) and therefore acted as the final verification session: it re-checked the data
against the live official pages, corrected what the sources did not support, and re-published.

**Repo review.** Read `COORDINATION.md`, `README.md`, `data/events.py`, `data/events.json`, the
parallel session's `data/*.json`, `scripts/build_site.py`, `scripts/merge_parallel.py`,
`tools/validate.py`. Rebuilt the site from scratch (`python3 scripts/build_site.py`) — output matches
the committed pages byte-for-byte (clean `git status` after rebuild). Ran `python3 tools/validate.py`
(0 errors) and an independent link/anchor/coverage audit (0 problems). Historical note: the earlier
validator reported 34 "unverified row not listed" errors caused by the two toolchains' different row
ids (`w-*`/`a-*`/`s-*` vs `x-*`); `arena-f54a124f` replaced it with the canonical union validator,
and this session separately confirmed that every gap row in **both** datasets is reachable from
`flagged.html` (39/39 unverified rows + 3 verified rows carrying a not-stated value).

**Programmatic checks over all 205 rows.** Every row has an absolute `https://` source URL on an
official/organiser/government domain (88 distinct domains, 142 distinct URLs); no aggregator hosts;
no duplicate ids; every row appears exactly once on its type page and once on its category page;
`event_count`/`flagged_count` match the data; no stale 2024/2025 values presented as upcoming
(the only 2025 dates are explicitly labelled past editions).

**Live source checks (39 items).** Each row below was fetched from the official page(s) named and
compared with the published row:

```text

1. ann-bay-to-breakers | "May 16, 2027" | https://www.baytobreakers.com/ | CONFIRMED — page title + H2 "May 16, 2027"; body copy still says "before May 18!" twice (known conflict, already in register f-030 + task-7 flag #7).
2. ann-cny-parade | "Saturday, February 20, 2027 (Year of the Ram)"; 5:15 PM from 2nd & Market | https://chineseparade.com/faq/ | CONFIRMED verbatim ("celebrating the Year of the Ram, ... Saturday, February 20, 2027 ... starts at 5:15 PM from 2nd and Market St"). Organiser's "Year of the Ram" wording already flagged in register.
3. ann-fleet-week | "October 9-11, 2026 (air show)" | https://fleetweeksf.org/air-show/ | CONFIRMED ("October 9, 10, 11, 2026 Friday, Saturday, & Sunday 12:00 Noon - 4:00 PM").
4. ann-cherry-blossom | "April 10-11 and April 17-18, 2027; Grand Parade April 18" | https://sfcherryblossom.org/ | CONFIRMED ("April 10-11 and 17-18, 2027 ... Grand Parade (April 18)"; 60th anniversary).
5. ann-sf-pride | "June 26-27, 2027" (57th) | https://sfpride.org/ | CONFIRMED (banner "June 26-27, 2027 • 57th Annual Celebration & Parade"; registration deadlines May 24 / May 1 2027 as in notes).
6. ann-sf-marathon | "Race weekend July 24-26, 2026; marathon Sunday July 26 2026; start 5:15 a.m." | https://www.thesfmarathon.com/ (+ /faq/ 404, /2027-50th-anniversary/) | DISCREPANCY — page title says "July 25 - 26, 2026"; banner says "July 24-25, 2027"; no current page states "July 24-26, 2026" or a 5:15 a.m. start. Parallel a-006 records the 2027 edition (July 24-25, 2027, 50th anniversary). FIX NEEDED on ann-sf-marathon.
7. ann-fleet-week | air show Oct 9-11 2026 12:00-4:00 p.m.; Fleet Fest Oct 10-11 10-7/10-5; ship tours Oct 7-12 | fleetweeksf.org /air-show/, /, /events/ship-tours/ | CONFIRMED (all three).
8. ann-fleet-week | "Parade of Ships 10:30 a.m.-12:00 p.m. Fri" | https://fleetweeksf.org/events/parade-of-ships/ | DISCREPANCY — official page states Friday 10/9, 11:00 am - 12:00 pm. FIX NEEDED (10:30 -> 11:00).
9. ann-cherry-blossom | April 10-11 + 17-18 2027; Grand Parade Apr 18 | https://sfcherryblossom.org/ | CONFIRMED.
10. ann-trans-march | Friday of Pride weekend; Dolores Park 3-6pm; march 6pm; 2026 edition June 26 | https://transmarch.org/ | CONFIRMED ("kicks off Pride weekend on Friday every year. Dolores Park: 3 - 6pm, March @ 6pm"; video "Trans March 2026: June 26 @ Dolores Park").
11. ann-litquake | "October 8-24, 2026; Lit Crawl SF on Saturday, October 24, 2026" | https://www.litquake.org/2026-schedule + official 2026 program PDF (linked from that page) | CONFIRMED — program: pre-fest Sun Oct 4 (Small Press Book Fair) + Tue Oct 6 (Ayad Akhtar); "THURSDAY OCT 8 Litquake's Opening Night Bash ... Kick off the 2026 festival"; "Lit Crawl SF on October 24"; post-fest Tue Nov 10 + Wed Nov 18. NOTE: programme includes some East Bay (out-of-city) venues — festival itself is SF. NOTE to add to row: run dates + Lit Crawl confirmed from the PDF linked from the schedule page.
12. spc-famssf-exhibitions + spc-bouquets-to-art | "Pharaohs thru Jan 31 2027; LEXICON thru Feb 7 2027; Eternal Paris thru Apr 4 2027; Rooted in Place thru Jun 4 2027; Miro thru Jul 25 2027; Arts of Indigenous America thru Aug 31 2028; Bouquets to Art Mar 2-7 2027; 14 exhibitions" | https://www.famsf.org/exhibitions/ | CONFIRMED line-by-line — every through-date + Bouquets Mar 2-7 2027 + "14 of 14 results" match exactly. Start dates are NOT published on the index (closing dates only) — consistent with parallel unverified start_date findings; will record as a published gap note.
13. x-s-020 Manon | "October 18 - November 1, 2026" | https://www.sfopera.com/ | PARTIAL — homepage banner: "Manon opens October 15"; Upcoming Events lists Oct 18, 21, 24, 27, 30 + Nov 1 (Oct 15-17 run dates already past). FIX NEEDED: run is October 15 - November 1, 2026.
14. x-s-021 Marriage of Figaro | "October 31 - November 29, 2026" | https://www.sfopera.com/ | CONFIRMED (OCT 31 + NOV 3,7,10,13,15,18,21,27,29).
15. x-s-022 Das Rheingold | "May 29 - June 22, 2027" | https://www.sfopera.com/ | CONFIRMED (MAY 29 + JUN 3,6,11,16,19,22).
16. x-s-023 Tosca | "June 4 - July 2, 2027" | https://www.sfopera.com/ | CONFIRMED (JUN 4,8,12,17,20,26,29 + JUL 2).
17. spc-supernatural | "Saturday, October 24, 2026" (schedule blank) | https://www.calacademy.org/supernatural | CONFIRMED date + TIMES NOW PUBLISHED: "6:30-9 p.m., VIP/Early entry 5 p.m."; GA adult $60 ($55 members), youth 3-17 $45 ($40 members). FIX: fill schedule/cost from official page; row can become verified.
18. art-deyoung + art-legion-honor | "free on designated days (first Tuesday of the month)" | https://www.famsf.org/visit/free-reduced-admission (linked in notes) | CONFIRMED ("General admission is free the first Tuesday of every month"; also free Saturdays for 9-county Bay Area residents — permanent galleries only). Old f-013 URL (/visit/free-admission) is dead but the correct official page exists.
19. spt-warriors | "home opener Friday, October 23, 2026 vs Memphis Grizzlies, 7:00 p.m." | https://warriors.com/news/warriors-announce-2026-27-regular-season-schedule-20260813 + official printable schedule PDF (cdn.nba.com 2627Schedule) | CONFIRMED — PDF shows Oct 23 MEM 7:00P (date/opponent/time match exactly).
20. x-a-020 SF Restaurant Week | Fall edition Oct 16-25, 2026 | https://www.sfrestaurantweek.com/ | CONFIRMED ("Fall SF Restaurant Week October 16 - 25, 2026").
21. spc-alcatraz-closure | "From October 26, 2026 to approximately November 18, 2026" | https://www.nps.gov/goga/learn/news/alcatraz-island-to-temporarily-close-for-dock-repairs-this-fall.htm | CONFIRMED verbatim ("beginning on Oct. 26, 2026 ... completed by Nov. 18, 2026").
22. spc-supernatural schedule/cost | filled from official page (6:30-9 p.m., VIP/early 5 p.m.; GA $60/$55, youth $45/$40) | https://www.calacademy.org/supernatural | CONFIRMED + row updated.
23. ann-sf-marathon | unconfirmable values removed; row now shows official 2027 edition July 24-25, 2027 (50th anniversary) | https://www.thesfmarathon.com/ | CORRECTED + new flag item flag-sf-marathon-dates.
24. ann-fleet-week Parade of Ships | 10:30 a.m. -> 11:00 a.m. | https://fleetweeksf.org/events/parade-of-ships/ | CORRECTED (official page: Friday 10/9, 11:00 am - 12:00 pm).
25. x-s-020 Manon | run start Oct 18 -> Oct 15 ("Manon opens October 15") | https://www.sfopera.com/ | CORRECTED via merge_parallel FIELD_OVERRIDES.
26. ann-litquake | "(27th edition)" removed — not stated on official pages; East Bay venue scope note added | https://www.litquake.org/2026-schedule + program PDF | CORRECTED.
27. flag-famsf-opening-dates | new flagged item: FAMSF index publishes closing dates only | https://www.famsf.org/exhibitions/ | ADDED to register.

28. x-s-034 WNBA Finals G1/G2 | "Game 1 October 17 and Game 2 October 19, 2026" | https://www.sfmta.com/press-releases/sfmta-transit-and-traffic-advisory-week-thursday-october-15-through-wednesday-october-21-2026 | CONFIRMED ("Saturday, Oct. 17 ... WNBA Finals Game 1 ... Atlanta Dream ... 12:30 p.m."; "Monday, Oct. 19 ... WNBA Finals Game 2 ... 5 p.m.").
29. x-a-025 Potrero Hill Festival | "2026-10-17" | same SFMTA advisory | CONFIRMED ("Saturday, Oct. 17 ... 10 a.m. to 4:30 p.m. on 20th Street between Wisconsin and Missouri streets").
30. x-a-027 Bearrison Street Fair | "2026-10-17" | same SFMTA advisory | CONFIRMED ("Saturday, Oct. 17 ... noon to 6 p.m., ... Harrison Street between 10th and 13th").
31. x-s-033 No Kings Rally | "October 17, 2026" | same SFMTA advisory | CONFIRMED ("Saturday, Oct. 17: A march will gather at Dolores Park at 18th and Dolores streets ... to the Pelosi Federal Building").
32. spc-boo-at-zoo | "Saturday, October 31, 2026", "10:00 a.m.-3:00 p.m." | https://sfzoo.org/event/boo-at-the-zoo/ | CONFIRMED ("Date October 31, 2026 / Time 10:00 AM - 3:00 PM").
33. spc-nye-fireworks | "December 31, 2025 - January 1, 2026 (most recent edition)", "11:59 p.m. (midnight), ~15 minutes", Embarcadero 94111, free, Promenade viewing | https://www.sfport.com/meetings/new-years-eve-fireworks-celebration-1 | CONFIRMED line-by-line (page: "December 31, 2025 11:59 pm to January 1, 2026 12:15 am", "begins at midnight and lasts approximately 15 minutes over the Bay", "The Embarcadero San Francisco, CA 94111", Pricing "Free", "areas around the Ferry Building and the open area along the Promenade").
34. rec-ferry-plaza-farmers-market | "Tuesday/Thursday 10:00 a.m.-2:00 p.m.; Saturday 8:00 a.m.-2:00 p.m., year round, rain or shine"; Saturday rear bay plaza + Embarcadero | https://www.ferrybuildingmarketplace.com/shops/the-ferry-plaza-farmers-market/ | CONFIRMED verbatim (incl. "Merchant hours may vary" caveat).
35. civ-bos | "Weekly, Tuesdays at 2:00 p.m."; Room 250, 1 Dr. Carlton B. Goodlett Place 94102 | https://sfgov.legistar.com/Calendar.aspx | CONFIRMED (BOS 10/20/2026 2:00 PM Regular Meeting, Room 250, 1 Dr. Carlton B. Goodlett Place, 94102-4689; also 10/6 2:00 PM).
36. civ-bos-budget-finance | "Weekly, Wednesdays, 10:00 a.m." | Legistar | CONFIRMED (B&F 10/7 and 10/21/2026 both 10:00 AM). SFGovTV "12:30AM" outlier remains flagged.
37. civ-bos-psns | "Weekly, Thursdays, 10:00 a.m." | Legistar | CONFIRMED (PSNS 10/22/2026 10:00 AM Regular; a 10/8 rescheduled meeting was held 12:30 PM).
38. civ-bos-rules | time was blank (Legistar 1:00 p.m. vs SFGovTV 10:00 a.m.) | Legistar re-check | RESOLVED — Legistar now lists 10/5 and 10/19/2026 regular meetings at 10:00 a.m. (matching SFGovTV). Row filled 10:00 a.m.; flag updated.
39. civ-bos-lut | time was blank (Legistar 4:30 p.m. vs SFGovTV 1:30 p.m.) | Legistar re-check | RESOLVED — Legistar 10/5/2026 regular meeting is 1:30 p.m. (matching SFGovTV); no LUT meeting posted for 10/19. Row filled 1:30 p.m.; flag updated.
```

**Corrections published by this session (6).**
1. `ann-sf-marathon` — removed unconfirmable "Race weekend July 24-26, 2026", "marathon start
   5:15 a.m.", the Embarcadero/Golden Gate Bridge course description and "(49th)"; the row now shows
   the officially published 2027 edition (July 24–25, 2027, 50th anniversary). New review item
   `flag-sf-marathon-dates`.
2. `ann-fleet-week` — Parade of Ships time corrected 10:30 a.m. → **11:00 a.m.** per
   https://fleetweeksf.org/events/parade-of-ships/ .
3. `x-s-020` (SF Opera *Manon*) — run start corrected Oct 18 → **Oct 15** ("Manon opens October 15");
   applied through `scripts/merge_parallel.py` `FIELD_OVERRIDES` so the parallel session's raw
   `data/special.json` stays untouched.
4. `spc-supernatural` — schedule and general-admission prices now published on the official page
   were filled in (previously blank): 6:30–9 p.m. (VIP/early entry 5 p.m.), GA adult $60 ($55
   members), youth $45 ($40 members).
5. `civ-bos-rules` / `civ-bos-lut` — start times filled from the current Legistar meeting records
   (10:00 a.m. / 1:30 p.m.), where Legistar and SFGovTV now agree; both flagged conflicts marked
   "resolved on re-check" and the old listings kept in the register for the record.
6. `ann-litquake` — "(27th edition)" removed (not stated on official pages); run dates + Lit Crawl
   date confirmed from the official 2026 programme PDF; scope note added that some programme events
   take place at East Bay venues outside the city limits.

**New irregularities published (2).**
- `flag-famsf-opening-dates` — FAMSF's exhibitions index publishes closing dates only; opening dates
  for Treasures of the Pharaohs / Eternal Paris / Miró are not stated and are not inferred.
- `flag-sf-marathon-dates` — official site date-copy conflict (title "July 25 – 26, 2026" vs banner
  "July 24–25, 2027") plus the removed unconfirmable values, itemised for manual review.

**Blank-cell publication strengthened.** `flagged.html`'s "Rows carrying a blank cell" table now also
lists rows that are otherwise `verified` but still carry a blank Schedule/Location/Cost cell
(`spc-flower-piano`, `spc-bouquets-to-art`, `spc-alcatraz-closure`) with the reason "not stated on
the official source; left blank, nothing inferred".

**Still open for human review (does not block).** All 74 items on `flagged.html`, notably: committee
time history (SFGovTV outliers), Bay to Breakers and SFFILM copy conflicts, Dragon Boat venue change,
TreasureFest relocation, SF Music Week programme page, Valkyries 2026-27 fixtures, HRC cadence,
Larsen address, Litquake/East Bay scope, FAMSF opening dates, SF Marathon date copy, and the
unreachable/parked/hijacked legacy domains recorded by `arena-8fb52462` (`f-001`–`f-034`).

**Merge conflict resolution (this session, against `arena-bdaa17b4`).** While this verification pass
was in flight, `arena-bdaa17b4` (with `arena-7d8015f4`) merged PRs #14–#17 to `main`, integrating an
independent audit and 9 further verified events (211-event state). `git pull --rebase` then replayed
this session's commits on top and produced conflicts in the **generated** files only
(`data/events.json`, `index.html`, `flagged.html`, `arts.html`, `recurring.html`, `special.html`) and
in `README.md`. Resolution, without discarding either side:
- `data/events.py`, `scripts/build_site.py`, `scripts/merge_parallel.py` merged cleanly — the merged
  dataset contains this session's six corrections and two new flags **and** `arena-bdaa17b4`'s nine
  added events and audit fixes (verified programmatically before continuing the rebase).
- All generated files were **regenerated from the merged dataset** with `python3 scripts/build_site.py`
  (211 events, 85 review items) — consistent with both sessions' authored data.
- `README.md` was merged keeping both audit paragraphs; counts updated to the merged reality
  (211 events · 170 verified · 41 gaps · 85 review items · 92 domains).
- Re-checked after the rebase: `tools/validate.py` passes; all 41 unverified rows and all
  verified-with-blank rows are listed on `flagged.html`; the extended blank-cell table (Row status
  column) is intact.

**Counts after this pass (merged with `arena-bdaa17b4`).** 211 events (112 recurring · 52 annual ·
47 special) · 170 verified · 41 rows with a review gap · 85 review items · 92 official domains ·
14 pages. `python3 scripts/build_site.py` and `python3 tools/validate.py` both pass; internal
link/anchor audit reports 0 problems.

**Task V4 closed out.** PR **#18** https://github.com/buffedlizard55-lab/MaltaProj6/pull/18 —
**MERGED** 2026-10-18T02:00:43Z, merge commit `9056bd2`
(`Merge pull request #18 from buffedlizard55-lab/arena/23722ef3-maltaproj6`).
GitHub Pages build for the merge finished with status **`built`**, `error: null`.
Live content confirmed by fetching https://buffedlizard55-lab.github.io/MaltaProj6/ : the dashboard
serves **211 events · 170 verified · 41 rows needing review · 85 review items · 92 official domains**,
the type table reads 112 regularly recurring · 52 annual · 47 special, and the Flagged for Review page
carries all 85 items plus every row with an unconfirmed value.

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
same "Flagged for review" page (72 items in the final union: 19 from the first pass plus 53 from the parallel pass). Every imported row keeps its own official source link and carries a note recording which session found it.

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
| Flagged for review | `flagged.html` | 72 published review items + 39 rows marked unverified for a gap or conflict |
| Method | `methodology.html` | Scope, sourcing rules, build process, official domains used, known limitations, supplementary views |
| Weekly & monthly (parallel session) | `weekly.html` | The parallel session's recurring-event view |
| Analysis (parallel session) | `analysis.html` | The parallel session's category / neighbourhood analysis |
| Source registry (parallel session) | `sources.html` | The parallel session's list of the 58 official sources it checked |

Each listed event appears on exactly **one** type page (recurring / annual / special) **and** exactly **one** category page,
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

## Final audit log — `arena-f54a124f` (2026-10-18)

- Reviewed the repo and the existing board before claiming task 12. The prior sessions' research, 205-row dataset, 72 review items and published pages were already present on `main`.
- Replaced front-page and README wording that implied a literally exhaustive citywide event list. The catalogue is now described accurately as a curated snapshot, with an explicit coverage warning and the official SF.gov citywide calendar linked as another discovery source. Checked that SF.gov calendar page directly on 2026-10-18: [Citywide meetings and events](https://www.sf.gov/events/upcoming). This supports the discovery link only; it is not evidence that the catalogue is exhaustive.
- Corrected stale README and coordination summary counts (review items 72, not 53) and distinguished the 39 rows marked for review from the review-item count.
- Fixed invalid event-table markup (title content previously sat outside a `<td>`, and rows had fewer data cells than the header). The rebuilt listing rows now have nine cells, including a dedicated official-source column; unverified rows on `flagged.html` have stable anchors.
- Replaced the old validator's checks against the parallel session's raw files with checks against the published union dataset: unique IDs, HTTPS source links, event membership on type/category pages, row-level source links, unverified flags, review-row links, table cell counts, and local links/fragments. **Validation result:** `events=205 verified=166 review_gap=39 review_items=72 domains=88 pages=14`; `python3 tools/validate.py` passes. `python3 -m py_compile scripts/build_site.py tools/validate.py` and `python3 scripts/build_site.py` also pass.
- Limitation: the audit validator is structural; it does not fetch or authenticate the 205 source-page contents or prove inventory completeness. Source verification recorded by prior sessions remains as logged above and should be refreshed against official pages as schedules change.
- **PR #12**: https://github.com/buffedlizard55-lab/MaltaProj6/pull/12 — merged to `main` at 2026-10-18T01:26:12Z as `1a3ca2130ff49109cf33f5a5b5def03bf4730d05`. GitHub Pages build `1293279602` completed with status `built`, `error: null` (22.5 seconds). The live dashboard was confirmed at https://buffedlizard55-lab.github.io/MaltaProj6/?refresh=20261018 and shows the new curated-snapshot coverage notice and updated counts.


### Merge-resolution note (arena-bdaa17b4, 2026-10-18)

`origin/main` advanced with `arena-7d8015f4`'s integrity pass (PRs #14/#15) while this session's integration was in flight, so `origin/main` was merged here before this session's PR. Generated pages and `data/events.json` were **regenerated from the merged dataset** (the established precedent on this board), `tools/validate.py` took the `main` version verbatim (it is a strict superset of this branch's copy: reproducibility check, blocked-host check, status check), and both sessions' logs are kept below. `arena-7d8015f4`'s two data changes are preserved: the One City One Book source was upgraded to the current selection page, and the Alcatraz dock-repair closure row is now `unverified` (cost not stated on the NPS source) — which moves this session's totals from 169 verified / 42 gap to **168 verified / 43 gap** at the same 211 events / 83 review items. Rebuilt and re-validated on the merged tree: `events=211 verified=168 review_gap=43 review_items=83 domains=92 pages=14 — OK`, plus `audit/check_dataset.py` with no hard problems. **Heads-up for session `arena-23722ef3`**, which claimed board tasks V0–V4 at 2026-10-18T01:29Z from an older board state: this session's integration (dataset corrections + 9 gap rows + `AUDIT_CORRECTIONS` in `scripts/merge_parallel.py`) was already pushed when that claim appeared and is being merged first; please rebase/merge `main` before starting V3 so the fixes are not duplicated.

## Current session — `arena/7d8015f4-maltaproj6`

| Task | Status | Owner | Files in scope | Notes |
|---|---|---|---|---|
| Post-merge integrity audit and repair | ✅ done | `arena/7d8015f4-maltaproj6` | `COORDINATION.md`, `scripts/build_site.py`, `tools/validate.py`, generated HTML pages, `README.md`, `data/events.py`, `data/events.json`, `data/schema.md` | Repaired malformed event table rows, synchronized validator with the merged source data, corrected overclaiming coverage text, recorded one missing admission-cost value as unverified, and re-built/re-validated all published pages. See audit log below. |


### `arena/7d8015f4-maltaproj6` — post-merge integrity audit (2026-10-18)

- **Structural verification:** ran `python3 scripts/build_site.py` (11 canonical pages generated; 205 rows; 72 review items), then `python3 tools/validate.py`. Result: 205 canonical rows; 165 recorded verified / 40 unverified; 111 recurring / 47 annual / 47 special; 14 total HTML pages. The check passed source-link presence/match on both type and category views, each unverified row's address on `flagged.html`, nine-cell listing row shape, data-union reproducibility from `data/events.py` + preserved per-session JSON, review-register source links, and local files/anchors. Also ran `git diff --check` and `python3 -m py_compile scripts/build_site.py scripts/merge_parallel.py tools/validate.py`; both passed.
- **Code issues fixed:** event rows previously emitted a bare `<span>` before their first `<td>` and embedded a source link in that title content while the table also declared a separate source header. Rows now have a proper title cell and a separate official-source cell. Unverified table rows have stable event-ID anchors. `tools/validate.py` previously compared the 87-row legacy tranche against IDs on the merged review page and reported 34 stale false positives; it now checks the canonical 205-row union and verifies the mirror can be reproduced from its inputs.
- **Rebase coordination:** before pushing, `git pull --rebase origin main` found that `arena-f54a124f` had merged audit improvements to `main`. Conflicts overlapped on shared docs, generated pages, site builder and validator. Resolved by retaining the newer `main` coverage and validation work, then applying this session's source correction, stricter unverified status, reproducibility check and verification notes; no other session's work was discarded. The remote session branch also retained the original claim commit; it was merged into this branch after rebase to avoid a force-push, preserving its ancestry. Its stale in-progress board text was reconciled with this completed record.
- **Coverage statement corrected:** the previous landing page and README asserted “every event” despite the known scope gap (for example individual venue performances and private events). The site now calls itself a curated catalogue and explicitly states it is not exhaustive. No claim is made that 205 rows enumerate the city's entire event universe.
- **Targeted official-source checks performed in this audit:** National Park Service Alcatraz closure release, https://www.nps.gov/goga/learn/news/alcatraz-island-to-temporarily-close-for-dock-repairs-this-fall.htm — confirms a scheduled closure beginning October 26, 2026, repairs expected complete by November 18; admission cost is not stated, so that cell remains blank and the row is `unverified`. San Francisco Public Library's current One City One Book page, https://sfpl.org/books-and-media/read/awake-floating-city — inspected and substituted for the stale generic route on the recurring-program row. SFMOMA's official exhibition listing, https://www.sfmoma.org/exhibitions/ — inspected for live exhibition listing context.
- **Verification limitation / irregularity:** this audit did not fetch and re-confirm every mutable date, schedule, address, or cost across all 205 source pages. The prior research passes record 2026-10-18 as their verification date; the fresh automated check verifies URL presence and rendering, not live source truth. 40 rows remain explicitly unverified, and all 72 review items remain published. The full-list goal is not demonstrably complete; the dashboard now labels this limitation rather than claiming exhaustiveness.
- **PR #14:** https://github.com/buffedlizard55-lab/MaltaProj6/pull/14 — merged to `main` at `2026-10-18T01:30:17Z` as `aae18265a751fdbd8d833d4cebeb53cd5ee6c6a4`. GitHub Pages deployment run **39086728303** completed successfully: build and deploy jobs passed; latest Pages build status is `built`, `error: null`, updated `2026-10-18T01:30:50Z`. Cache-busted live checks confirmed the dashboard coverage notice and 165/40 counts, methodology scope, recurring table structure, special page's unverified Alcatraz row, and flagged page are deployed at https://buffedlizard55-lab.github.io/MaltaProj6/. No PR checks were configured for #14; the local build and validation passed.

## Final audit + integration log — `arena-bdaa17b4` (2026-10-18)

- **Reviewed the repo without editing claimed files.** On arrival `main` held the merged 205-row site and `arena-f54a124f` held an in-progress claim over `README.md`, `scripts/build_site.py`, `tools/validate.py` and generated HTML, so this session first claimed new-files-only scope and pushed that claim (`c1737de`). Integration edits began only after `arena-f54a124f` merged PRs #12/#13 and released its claim.
- **Structural audit (task A2).** `audit/check_dataset.py` + `audit/row-audit.csv` over all 205 rows: 0 missing/non-https sources, 0 duplicate ids/titles, 0 aggregator sources, 0 broken internal links, 0 rows missing from generated HTML. Soft patterns (blank `dates` by design on recurring rows, past-dated 2026 editions, unverified rows covered by the flagged page's auto-list rather than the register) are interpreted in `audit/AUDIT-2026-10-18-bdaa17b4.md`, including a bug found and fixed in this session's own checker.
- **Live re-verification (task A3).** 22 official pages re-fetched and compared field by field (bash cannot reach official sites in this sandbox — `curl` to sf.gov returns `000` — so the page-fetch tool was used; JS-shell pages such as sfrecpark.org programme pages are recorded as content-not-re-verified, never guessed). Exact matches: Ferry Plaza Farmers Market, Exploratorium After Dark, SFMTA Sunday Streets, Bay to Breakers (whose published date-copy irregularity is still live). Conflicts are the items below.
- **Removed 3 rows:** `art-angel-island` (California State Parks' facility listing places Angel Island State Park in **Tiburon, Marin County** — https://dbw.parks.ca.gov/BoatingFacilities/f/420 — so it fails the city-limits rule; the row's contrary note was wrong); `ann-illuminate-live` (duplicate of the weekly Bandshell row; Mayor's Office release now cited in the kept row); `spc-sf-pride-trans-march-2026` (duplicate 2026 edition of the annual Trans March row; SFMTA notice now cited in the kept row).
- **Corrected 5 rows:** Opera in the Park's venue **is** stated in its cited SF Opera release (Robin Williams Meadow, Golden Gate Park; "free, annual" concert, Sun Sep 13 2026) → reclassified Annual and verified, unconfirmed 1:30 p.m./presenter removed; Parol Lantern's 2025 prose blanked from the confirmed-dates cell (organiser site still shows only Dec 13 2025); Rec & Park Operations Committee schedule blanked to match its own note (cited entry now redirects to a CivicPlus login); Human Rights Commission stale "(next listed)" label removed; imported Manon row's start date corrected Oct 18 → **Oct 15, 2026** per SF Opera's season announcement, via a documented `AUDIT_CORRECTIONS` override in `scripts/merge_parallel.py` (the parallel session's raw `data/special.json` was not rewritten).
- **Gap research (task A4)** — added **9 rows**, each field taken from a fetched official page, blanks left blank (`data/gap-candidates-bdaa17b4.json` is the trail): Outside Lands (annual, unverified — SFMTA page used because sfoutsidelands.com returned HTTP 500, organiser/cost blank), JuneteenthSF Freedom Celebration Fillmore (annual, unverified — SF.gov HRC page; organiser site showed a hosting error), SF City Guides free walking tours (recurring, verified), Walt Disney Family Museum (verified — waltdisney.org admission + visit pages), CAAMFest (annual, verified — caamedia.org + official festival schedule/box office; organiser's "five days" copy vs four-day May 7–10 range noted), Escape From Alcatraz Triathlon (annual, verified — official overview/homepage, Jun 5–6 2027), Let's Glow SF (annual, verified — Downtown SF Partnership, Dec 4–13 2026), Portola 2026 (special, unverified — SFMTA dates/Pier 80/2–11 p.m.; organiser not inferred from newsletter text), FOG Design+Art 2027 (special, unverified — SFMOMA series page; cost blank). Checked and **not added:** Yerba Buena Gardens Festival (reCAPTCHA wall), SF Design Week (organiser says Bay-Area-wide; Jun 12 vs 13 end-date conflict), Juneteenth Parade/Bayview (named on sf.gov, organiser pages not separately verified). Further candidates (Union Square ice rink, Kaiser SF Half, SailGP, SF Open Studios, more Moscone conventions, USS Pampanito, Musée Mécanique, cable cars) are recorded as not checked this session.
- **Published 11 new flagged items** (`flag-angel-island-scope`, `flag-illuminate-duplicate`, `flag-trans-march-duplicate`, `flag-opera-park-venue`, `flag-parol-dates-cell`, `flag-Manon-date`, `flag-recpark-ops-source`, `flag-outside-lands-source`, `flag-juneteenth-organiser`, `flag-portola-organiser`, `flag-fog-cost`), taking the register to **83**. Per the amended methodology, `needs review` items live on the Flagged for Review page and do not block the merge.
- **Past-dated rows:** 31 rows' latest dates precede 2026-10-18 (22 annual 2026 editions already held; 9 specials, incl. one parser caveat) — listed for the next refresh in the audit report §6 and `audit/row-audit.csv`.
- **Rebuild + validation:** `python3 scripts/build_site.py` → "Wrote 12 pages, 211 events, 83 flagged items." `python3 tools/validate.py` → `events=211 verified=168 review_gap=43 review_items=83 domains=92 pages=14 — OK` (merged-tree figures; pre-merge this session alone was 169/42). `python3 audit/check_dataset.py` → no hard problems, no broken internal links, no event source URL missing from the HTML, and both true-duplicate title pairs are gone. The validator's 92 "domains" vs the audit checker's 91 hosts is a `www.`-normalisation difference only.
- **Limitations, stated plainly:** about 120 source URLs were not re-fetched this session and still rely on earlier sessions' recorded checks; app-style official pages (sfrecpark.org, Legistar) could not be re-rendered by this sandbox's fetcher; nothing proves the catalogue exhaustive (it is labelled a curated snapshot on the site itself).

### Published state after this session's integration, merged with `arena-7d8015f4` (PR/merge result appended below on completion)

| | |
|---|---|
| Events | **211** (112 regularly recurring · 52 annual · 47 special/dated) |
| Fully verified rows | **168** (merged tree; 169 before merging `arena-7d8015f4`) |
| Rows with a published gap | **43** (merged tree; 42 before) |
| Irregularities published on "Flagged for Review" | **83** |
| Static pages | **14** |
| Integration commits by `arena-bdaa17b4` | claim `c1737de` · audit `6fb0a54`, `9307385` · scope `6af5b5f` · integration `b633f15` |

### Closing record — `arena-bdaa17b4` merge and deploy (2026-10-18)

- **PR #16**: https://github.com/buffedlizard55-lab/MaltaProj6/pull/16 — **MERGED** to `main` at 2026-10-18T01:44:12Z, merge commit `6d7d63a9ea29eaac88da0ce5715b7a10f613273f`.
- **GitHub Pages:** build for `6d7d63a` finished with status **`built`**, `error: null` (21.3 s build, source `main` / `/`).
- **Live content confirmed** by fetching https://buffedlizard55-lab.github.io/MaltaProj6/ after the build: dashboard shows **211 events listed · 168 rows marked verified · 43 rows needing review · 83 review items published · 92 distinct official domains**, with 112 regularly recurring · 52 annual · 47 special and categories civic 36 · arts 67 · sports 10 · markets 29 · community 69. The out-of-scope "Bay (Angel Island)" area no longer appears.
- Local pre-merge smoke test served HTTP 200 for all 14 pages plus `assets/site.css` and `data/events.json`; `python3 scripts/build_site.py`, `python3 tools/validate.py` and `python3 audit/check_dataset.py` all pass on the merged tree.
- Flagged irregularities and unverified rows (83 + 43) remain published on https://buffedlizard55-lab.github.io/MaltaProj6/flagged.html for post-launch review, per the board's `needs review` rule. This record commit follows via a small record-only PR, as earlier sessions did.
