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
| `arena-3239c070` | `arena/3239c070-maltaproj6` | **Deep line-by-line re-verification, gap research, site polish, flagged registry expansion** — 25+ live official-source checks, 4 verified rows added (Cable Cars, SF Open Studios, USS Pampanito, Musée Mécanique), 3 new flagged exclusions, site rebuilt 215/88/95 domains | ✅ complete — PR #20 merged to `main` 2026-10-18T03:03:43Z (`96eb60b`), Pages `built`; see closing record below + PR #21 record commit |
| `arena-79993171` | `arena/79993171-maltaproj6` | Final post-merge repository/site review; verify current data, source-link/table coverage, local build and live Pages state; document results and fix only confirmed defects | ✅ complete — corrective PR #22 merged to `main` at `6d0e777`; Pages `built` and cache-busted live content verified at 216/176/40/89/95. See closing record below. |
| `arena-76d2c635` | `arena/76d2c635-maltaproj6` | Independent line-by-line re-verification + gap research (new files only while `arena-7141e086` holds the final-integration claim): `audit/AUDIT-2026-10-18-76d2c635.md`, `data/gap-candidates-76d2c635.json`, `audit/row-audit-76d2c635.csv`, registry/task/log rows in this board. No edits to `data/events.py`, generated `*.html`, `data/events.json`, `scripts/`, `tools/` until `arena-7141e086` releases/merges or its claim goes stale (>60 min, no commits) — integration needs are logged as requests here. Arena-fixed branch used; no branch switch. | ✅ complete — PR #24 merged to `main` 2026-10-18T03:27:56Z (`7e2207e`), Pages `built`; see closing record below |
| `arena-8cb2d3cc` | `arena/8cb2d3cc-maltaproj6` | **Final integration session (2026-10-18, seventh pass).** Independent repo review, line-by-line official-source re-verification of the published dataset, gap research, defect repair, site UX/full-list page, rebuild, PR to `main`, merge and Pages deploy confirmation. Scope: `COORDINATION.md`, `README.md`, `data/events.py`, generated `data/events.json`, generated `*.html`, `scripts/build_site.py`, `scripts/merge_parallel.py`, `tools/validate.py`, `assets/`, `data/meta.json`, `data/events.csv` (new). No other session is live (verified via `gh api compare`: every other branch is behind `main`; `arena/7141e086` is ahead by one stale claim-only commit and never merged). | ✅ complete — PR #26 merged to `main` at `1cdd3ab`, Pages `built`, live site verified at 218/208/10/97/42/98; see the closing record below |
| `arena-8e8e24dc` | `arena/8e8e24dc-maltaproj6` | **Independent line-by-line verification + gap research (2026-10-18, concurrent with `arena-8cb2d3cc`'s final-integration claim).** New files only while that claim is live: `audit/AUDIT-2026-10-18-8e8e24dc.md`, `audit/check_8e8e24dc.py`, `audit/row-audit-8e8e24dc.csv`, `data/gap-candidates-8e8e24dc.json`, plus registry/task/log rows in this board. No edits to `data/events.py`, `data/events.json`, generated `*.html`, `scripts/`, `tools/`, `assets/` until the integration claim is released or goes stale (>60 min, no commits); integration needs logged as requests. Arena-fixed branch used; no branch switch. | ✅ complete — claim released by PR #26 at 05:57:11Z; corrections applied and merged in **PR #29** (`a6b9770`, 06:01:51Z); Pages `built` for that commit and the live dashboard verified at 217 / 206 / 11 / 103 / 42 / 97. See the closing record below. |
| `arena-ef213634` | `arena/ef213634-maltaproj6` | Final-integration / source-recheck takeover attempt (claim commits `846ae85` 05:46Z, `e0c4fc6` 05:53Z; tasks F1/F2 marked in progress, F3 unclaimed). Never produced any file changes beyond the claim rows and never opened a PR. | 🔍 needs review — claim went stale (>60 min with no commits; at takeover check 09:45Z it was ~4 h old). Per the board's 60-minute rule `arena-fc3438db` takes over this scope; superseded by PRs #26–#31 which completed the claimed work first. Handoff noted in the `arena-fc3438db` log below. |
| `arena-fc3438db` | `arena/fc3438db-maltaproj6` | **Verification + requirements-alignment pass (2026-10-18, eighth pass).** Take over stale `arena-ef213634` integration claims. Line-by-line re-verification of the published dataset against official sources (sampled + all soonest-dated rows), gap research for the user's stated focus (free events: gaming, music, AI), site alignment with the stated requirements (executive summary of events near today's date, date-sorted upcoming listings, clear cost labels, mobile-friendly UX), rebuild, PR to `main`, merge and Pages confirmation. Scope: `COORDINATION.md`, `README.md`, `data/events.py`, generated `data/events.json` + `data/*.json` + `data/events.csv`, generated `*.html`, `scripts/build_site.py`, `tools/validate.py`, `assets/site.css`, `data/gap-candidates-fc3438db.json` (new), `audit/AUDIT-2026-10-18-fc3438db.md` (new). No other live session (all other branches behind `main`; `arena/ef213634` stale, claim-only). | 🟡 in progress |

**Concurrency note.** `arena-b0f3cfd3` checked the remote at the start of its run (`git ls-remote --heads origin`
returned only `refs/heads/main`) and therefore correctly found no other session to coordinate with. The second
session's branch appeared and was merged into `main` later in the run, which produced a merge conflict with
`index.html`, `annual.html`, `special.html`, `flagged.html`, `assets/style.css`, `COORDINATION.md` and `README.md`.
That conflict is resolved below, in **Merge conflict resolution**, without discarding either session's work.

---

## Task board — `arena-76d2c635` (independent re-verification / gap-research session)

Session branch: `arena/76d2c635-maltaproj6` (Arena-fixed branch for this session; all work stays on this
branch rather than a `session-<id>/<task>` branch).

**Concurrency observed on arrival (2026-10-18).** `main` is at `98d8528` (PR #19 merge; 211 events /
170 verified / 41 review-gap rows / 85 review items, Pages `built`). `git ls-remote origin` shows a
second live session branch `arena/7141e086-maltaproj6` ahead of `main` by 1 commit `9199715`
(`2026-10-18T02:57:00Z`, "docs: claim final integration audit", `COORDINATION.md` only, verified via
`gh api …/compare/main...arena/7141e086-maltaproj6` — this sandbox's fetch spec covers `main` and this
session's branch only, so the compare API was used to read the claim). That session claims final
integration review (tasks I0–I2) including, as verified fixes, `data/events.py`, `data/events.json`,
`*.html`, `scripts/`, `assets/`. All earlier board tasks are ✅ done. This session therefore claims
only new, non-overlapping work and will not edit files in `arena-7141e086`'s scope while its claim is
live; needed corrections are logged here as integration requests instead.

| # | Task | Status | Owner | Files in scope | Notes |
|---|---|---|---|---|---|
| R0 | Register on the shared board and claim non-overlapping scope | ✅ done | `arena-76d2c635` | `COORDINATION.md` (registry/task/log rows only) | Claim commit `707aa7d` pushed before any other file edits. Repo review on arrival: 211 events / 170 verified / 41 gap rows / 85 review items; build + validator + prior structural checker all pass; Pages `built` (see R1). |
| R1 | Programmatic line-by-line structural audit of all 211 rows + 85 review items | ✅ done | `arena-76d2c635` | `audit/check_76d2c635.py` (new), `audit/row-audit-76d2c635.csv` (new), `audit/AUDIT-2026-10-18-76d2c635.md` (new) | Source present/https/official-host, blanks vs status, duplicates, out-of-city text, past-dated rows, HTML membership/link integrity. Reuses `audit/check_dataset.py` read-only plus this session's own checks. |
| R2 | Live official-source spot re-verification (stratified sample + highest-risk dated/annual rows) | ✅ done (scoped sample; unchecked remainder stated in audit) | `arena-76d2c635` | `audit/AUDIT-2026-10-18-76d2c635.md` (new) | Page-fetch tool against official pages only; JS-shell/app pages recorded as content-not-re-verified, never guessed. |
| R3 | Gap research: candidates recorded by `arena-bdaa17b4` as not yet checked (Union Square ice rink, Kaiser SF Half, SailGP, SF Open Studios, Moscone conventions, USS Pampanito, Musée Mécanique, cable cars) + Yerba Buena Gardens Festival / SF Design Week re-check | ✅ done | `arena-76d2c635` | `data/gap-candidates-76d2c635.json` (new) | Official sources only; every field from a fetched official page; unconfirmed fields left blank in the candidate record. |
| R4 | Integration requests + handoff: if findings require `data/events.py` / `*.html` changes, log them here for `arena-7141e086`; only integrate directly after that session merges/releases or its claim is >60 min stale with no commits (handoff noted here) | ✅ done — requests IR-1…IR-16 logged in `audit/AUDIT-2026-10-18-76d2c635.md` §Integration requests; this session's new-files PR merged separately (see closing record) | `arena-76d2c635` | `COORDINATION.md` | No shared-output edits before then. |

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
| W0 | Register on the shared board and claim | ✅ done | `arena-3239c070` | `COORDINATION.md` | Claim commit `984cedd` pushed before any file edits (2026-10-18T02:56Z). |
| W1 | Full line-by-line re-verification against official sources | ✅ done | `arena-3239c070` | `COORDINATION.md` (log only) | 25+ live fetches of official pages; spot-checked SFMOMA, Asian Art Museum, SF Symphony, FAMSF, Exploratorium + all gap candidates. No hallucinations found in existing 211 rows; prior sessions' corrections confirmed. |
| W2 | Gap research: find SF-city events not yet in catalogue, verified from official sources | ✅ done | `arena-3239c070` | `data/events.py`, `audit/row-audit.csv`, `data/events.json` | 11 official pages fetched (Stern Grove, Hardly Strictly, SF Design Week, SailGP calendar, SFMTA cable cars, ArtSpan SF Open Studios, Moscone calendar, Maritime USS Pampanito, Musée Mécanique, etc.). Added 4 verified rows; 3 new flagged exclusions documented. |
| W3 | Site polish & verification artifacts (validator, flagged page, methodology) | ✅ done | `arena-3239c070` | `scripts/build_site.py`, `*.html`, `assets/site.css`, `README.md` | `python3 scripts/build_site.py` → 215 events, 88 flagged; `python3 tools/validate.py` OK; `python3 audit/check_dataset.py` 0 hard problems, 0 broken links. Domain list auto-updated to 95. README counts updated. |
| W4 | PR to `main`, merge, confirm GitHub Pages deploy, record on this board | ✅ done | `arena-3239c070` | `COORDINATION.md` | **PR #20** https://github.com/buffedlizard55-lab/MaltaProj6/pull/20 — MERGED 2026-10-18T03:03:43Z as `96eb60b`. GitHub Pages build for the merge: status `built`, `error: null`. Live site confirmed serving the 215-event / 88-review-item / 95-domain state. Closing record commit `record-pr20` follows as PR #21. |

---

## Session log — `arena-3239c070` — deep re-verification & gap research (2026-10-18)

**Scope.** Final verification session per the project's "line by line, official sources only, no hallucinations" rule. The repository at `main` already held the 211-event union dataset with 85 flagged items (all prior PRs #1–#19 merged, including `arena-bdaa17b4`'s 9 gap rows and `arena-23722ef3`'s 6 corrections). This session acted as an independent re-check: it re-fetched official pages for the entire gap-candidate list, spot-checked high-value existing rows, added missing SF-city events that have official sources, and re-published.

**Repo review.** Read `COORDINATION.md` (451 lines, all prior session registries, task boards and logs), `README.md`, `data/events.py` (152 base events + 59 parallel imports = 211 total), `data/events.json`, `data/annual.json`/`weekly.json`/`special.json`, `scripts/build_site.py`, `scripts/merge_parallel.py`, `tools/validate.py`, `audit/AUDIT-2026-10-18-bdaa17b4.md`, `audit/check_dataset.py`, `data/gap-candidates-bdaa17b4.json`. Rebuilt the site from scratch (`python3 scripts/build_site.py` → "Wrote 11 pages, 211 events, 85 flagged items") and confirmed `python3 tools/validate.py` → 211/170/41/85/92 — OK. Spot-checked 10 existing high-risk rows against live official pages before any edits.

**Live source checks (25+ official pages fetched via fetch_page — bash curl to sf.gov is blocked in this sandbox, so the page-fetch tool was used):**

```text
1. stern grove festival | https://www.sterngrove.org/ | ✅ "Thank you for an amazing 2026 season — See you next summer for our 90th season" — already in catalogue as x-a-007 (unverified, dates not announced) — CONFIRMED, no new row needed.
2. hardly strictly bluegrass | https://hardlystrictlybluegrass.com/ | ✅ 2026 edition Oct 2-4 has concluded; merch store open Oct 13-27; 2027 not yet announced — already in catalogue as x-a-013 — CONFIRMED.
3. yerba buena gardens festival | https://ybgfestival.org/ | ✅ reCAPTCHA wall — cannot verify from official page — already flagged as f-011, not added — CONFIRMED as not addable.
4. SF Design Week | https://sfdesignweek.org/ | ✅ "That's a Wrap! 20th Anniversary Edition June 1-12, 2026 — Multitudes" — organiser page says events happen "throughout the Bay Area" and end date conflicts with aigasf (Jun 12 vs 13) — correctly excluded by prior audit — CONFIRMED.
5. SailGP 2026 calendar | https://sailgp.com/general/2026/calendar/ | ✅ 13 events listed (Perth, Auckland, Sydney, Rio, Bermuda, New York, Halifax, Portsmouth, Sassnitz, Valencia, Geneva, Dubai, Abu Dhabi) — NO San Francisco stop in 2026 — gap candidate correctly not added; published as new flagged item flag-sailgp-no-sf-2026.
6. SFMTA Cable Cars | https://www.sfmta.com/getting-around/muni/cable-cars | ✅ Three lines (Powell-Hyde, Powell-Mason, California), turntables at Powell & Market, Bay & Taylor, Hyde & Beach, MuniMobile/Clipper, National Historic Landmark — NEW VERIFIED ROW ADDED: art-cable-cars.
7. ArtSpan SF Open Studios | https://www.artspan.org/visitsfopenstudios | ✅ "September 26 - October 25 | Weekends | 11AM-5PM" — NEW VERIFIED ROW ADDED: ann-sf-open-studios (Annual).
8. ArtSpan guide | https://www.artspan.org/sfosguide | ✅ 2026 SF Open Studios Guide — confirms citywide, 5 weekends, interactive maps — supports same row.
9. USS Pampanito | https://maritime.org/uss-pampanito/ | ✅ "Open Daily 10am-6pm (Last boarding 5:30pm)" — Pier 45 — NEW VERIFIED ROW ADDED: art-uss-pampanito.
10. Maritime home | https://maritime.org/ | ✅ Confirms USS Pampanito is independent non-profit partner to SF Maritime NHP, 100k visitors/year — supports same row.
11. Musée Mécanique visit | https://museemecanique.com/visit | ✅ "Open 365 Days a Year — Admission is free! — Pier 45 Fisherman's Wharf 10AM-8PM" — NEW VERIFIED ROW ADDED: art-musee-mecanique.
12. Musée Mécanique location | https://museemecanique.com/location | ✅ Pier 45 Fisherman's Wharf, 10AM-8PM — supports same row.
13. SFMTA cable-cars alias | https://www.sfmta.com/getting-around/muni/routes/cable-cars | ❌ 404 Content Not Found — correct canonical URL is /getting-around/muni/cable-cars (used).
14. Moscone Center events | https://www.moscone.com/events | ✅ October 2026 calendar shows CoreWeave Fully Connected, SEMICON West, TechCrunch Disrupt, Cloudflare Connect, INFORMS — Moscone Center already has a venue row (1045 Moscone Center) — no duplicate rows needed; noted as not added.
15. SF Open Studios not-found check | https://sfopenstudios.artspan.org/ | ❌ 404 — correct organiser URL is artspan.org — confirms no separate domain to cite.
16. Union Square ice rink search | https://www.sf.gov/event/ice-rink-union-square | ❌ 404 "We can't find that page" — no official ice-rink page located — published as flag-union-square-ice-rink.
17. Kaiser SF Half search | https://www.sfhalf.com/ + https://healthy.kaiserpermanente.org/ | ❌ sfhalf.com 500, kaiser front-door generic — no official 2026 SF Half page with dates/venue/organiser — published as flag-kaiser-sf-half.
18. SFMOMA visit | https://www.sfmoma.org/visit/ | ✅ Adult $30 / Senior $25 / Student $23 / 18 & under free; Mon-Tue 10-5, Wed closed, Thu noon-8, Fri-Sun 10-5; entrance 151 Third Street — CONFIRMED (existing row art-sfmoma unchanged).
19. Asian Art Museum | https://asianart.org/ | ✅ Hours Thu 1-8PM, Fri-Mon 10AM-5PM, Tue-Wed closed; address 200 Larkin Street — CONFIRMED (existing row art-asian-art-museum unchanged).
20. SF Symphony | https://www.sfsymphony.org/ | ✅ 2026-27 Season with Music Director Designate Elim Chan, Dvořák Symphony No. 8 Oct 16-18 — CONFIRMED (existing row rec-sfsymphony unchanged).
21. FAMSF de Young | https://www.famsf.org/visit/de-young | ✅ Treasures of the Pharaohs through Jan 31 2027, Nengi Omuku through May 2028, Rose B. Simpson through Feb 7 2027 — consistent with existing flagged note about opening dates not published — CONFIRMED.
22. Exploratorium | https://www.exploratorium.edu/visit/calendar | ✅ After Dark Thursday Nights 18+; Daytime Members-Only Sundays 10am-12pm; Storytime Science Halloween Oct 17-18 Sat/Sun 12-1pm & 2-3pm — CONFIRMED (existing rows rec-explatorium-* unchanged).
23. Maritime tickets | https://maritime.org/pampanito-tickets | ✅ Ticket page loading via Stripe — supports USS Pampanito admission values.
24. Musée Mécanique via sftravel | https://www.sftravel.com/article/san-francisco-cable-car-museum-guide | ❌ 404 — official organiser site used instead.
25. Musée Mécanique Wikipedia | https://en.wikipedia.org/wiki/Mus%C3%A9e_M%C3%A9canique | ✅ Confirms Pier 45 location, 37.8093N 122.4161W, but Wikipedia is never used as primary source — official site used.
```

**Corrections to existing data.** None required beyond the prior sessions' corrections (SF Marathon 2027, Fleet Week Parade 11:00 a.m., Manon Oct 15, etc. — all re-confirmed). No hallucinations or aggregator sources found. No duplicate IDs or titles. No out-of-SF rows (all locations re-checked against SF city limits: Presidio, Alcatraz, Maritime NHP are inside the city; Angel Island remains excluded).

**Additions (4 verified rows, each with an official https source and leaving blanks where the official page did not state a value):**
1. `art-cable-cars` — San Francisco Cable Cars (SFMTA) — https://www.sfmta.com/getting-around/muni/cable-cars — verified — Attraction - Open regularly.
2. `ann-sf-open-studios` — SF Open Studios (ArtSpan) — https://www.artspan.org/visitsfopenstudios — verified — Annual (Sep 26-Oct 25 2026).
3. `art-uss-pampanito` — USS Pampanito (Maritime Association) — https://maritime.org/uss-pampanito/ — verified — Attraction - Open regularly.
4. `art-musee-mecanique` — Musée Mécanique — https://museemecanique.com/visit — verified — Attraction - Open regularly.

All four were absent from the 211-row union (title-keyword scan confirmed) and are physically inside SF city limits.

**New flagged items (3):**
- `flag-sailgp-no-sf-2026` — SailGP 2026 calendar has no SF stop (13 events, no SF) — evidence https://sailgp.com/general/2026/calendar/
- `flag-union-square-ice-rink` — ice rink has no official 2026 page (sf.gov 404) — evidence https://www.sf.gov/
- `flag-kaiser-sf-half` — Kaiser Permanente SF Half Marathon has no official 2026 race page — evidence https://healthy.kaiserpermanente.org/

**Build & validation after edits:**
- `python3 scripts/build_site.py` → "Wrote 11 pages, 215 events, 88 flagged items."
- `python3 tools/validate.py` → "events=215 verified=174 review_gap=41 review_items=88 domains=95 pages=14 — OK"
- `python3 audit/check_dataset.py` → events=215 flagged_register=88 · verified=174 unverified=41 · 0 hard problems, 0 broken internal links, 0 events missing from HTML · wrote audit/row-audit.csv
- Internal link/anchor audit over all 14 HTML files → 0 problems.

**Limitations stated plainly.** ~120 source URLs from earlier sessions were not re-fetched this session and still rely on those sessions' recorded checks (see their logs). App-shell pages (sfrecpark Legistar JS calendars) cannot be re-rendered by this fetcher and are recorded as not re-verified, never guessed. The catalogue is labelled a curated snapshot, not an exhaustive live calendar.

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

### Closing record — `arena-3239c070` merge and deploy (2026-10-18)

- **PR #20**: https://github.com/buffedlizard55-lab/MaltaProj6/pull/20 — **MERGED** to `main` at 2026-10-18T03:03:43Z, merge commit `96eb60bb29d494d039baa73e9f099cdebba1d4cd`.
- **GitHub Pages:** build for `96eb60b` finished with status **`built`**, `error: null` (build source `main` / `/`).
- **Live content confirmed** by fetching https://buffedlizard55-lab.github.io/MaltaProj6/ after the build: dashboard shows **215 events listed · 174 rows marked verified · 41 rows needing review · 88 review items published · 95 distinct official domains**, with 115 regularly recurring · 53 annual · 47 special and categories civic 36 · arts 71 · sports 10 · markets 29 · community 69. New rows: SF Cable Cars (SFMTA), SF Open Studios (ArtSpan), USS Pampanito (Maritime), Musée Mécanique.
- Local pre-merge smoke test served HTTP 200 for all 14 pages plus `assets/site.css` and `data/events.json`; `python3 scripts/build_site.py`, `python3 tools/validate.py` and `python3 audit/check_dataset.py` all pass on the merged tree (215/174/41/88/95 pages=14 — OK, 0 hard problems, 0 broken internal links, 0 events missing from HTML).
- Flagged irregularities and unverified rows (88 + 41) remain published on https://buffedlizard55-lab.github.io/MaltaProj6/flagged.html for post-launch review, per the board's `needs review` rule. This record commit follows via a small record-only PR (#21), as earlier sessions did.
## Task board — `arena-79993171` (final post-merge review)

Session branch: `arena/79993171-maltaproj6` (fixed Arena branch; work remains on this branch).

| # | Task | Status | Owner | Files in scope | Notes |
|---|---|---|---|---|---|
| F0 | Register and claim final post-merge review | ✅ done | `arena-79993171` | `COORDINATION.md` | Claim commit `5cf7cf6` (rebased onto `main` after PR #21) and expanded scope commits were pushed before data edits. Rebase conflicts were resolved by preserving all merged-session registry/closing records and this session’s claim. |
| F1 | Recheck current canonical data, generated pages, build/validation and published Pages deployment | ✅ complete | `arena-79993171` | `audit/POST-MERGE-2026-10-18-79993171.md`, `audit/row-audit.csv`, `data/events.py`, `data/events.json`, `data/weekly.json`, `data/annual.json`, `data/special.json`, `README.md`, `scripts/build_site.py`, `scripts/merge_parallel.py`, `tools/validate.py`, generated HTML, `COORDINATION.md` | PR #22 deployment for `6d0e777` is `built`; cache-busted live home, flagged, civic, special, annual, sports, and JSON pages were checked. Final live counts: 216/176/40/89/95. This remains a curated, non-exhaustive snapshot. |
| F2 | Fix confirmed final-integration defects, rebuild, verify links and pages | ✅ done | `arena-79993171` | `data/events.py`, `data/weekly.json`, `data/annual.json`, `data/special.json`, `scripts/merge_parallel.py`, `tools/validate.py`, `README.md`, `data/events.json`, generated HTML, `audit/row-audit.csv`, `COORDINATION.md` | Corrected date-status leakage/placeholders, Lightscape dates, Palace/Larsen pickleball sources and unknown terms, Escape From Alcatraz cost, and split the two civic bodies. Rebuilt 216 rows/89 flags; validator and dataset audit pass. Details: `audit/POST-MERGE-2026-10-18-79993171.md`. |
| F3 | Publish audit record, open/merge PR if there are changes, verify Pages result | ✅ complete | `arena-79993171` | `audit/POST-MERGE-2026-10-18-79993171.md`, `README.md`, `COORDINATION.md` | Corrective PR #22 was merged after local build/validation; the `main` Pages workflow succeeded and live content was verified. This record-only closeout documents the merge/deploy result. |

### Audit trail — `arena-79993171` (2026-10-18)

- `main` advanced during this pass from the older `98d8528` baseline through PR #20 and PR #21 to `1a49e45` (215 events). The rebase conflict was limited to `COORDINATION.md`; resolution retained both newly merged session registry/closing records and this session's claim/task board. The rebased session history was pushed only to `arena/79993171-maltaproj6` using `--force-with-lease` after pulling/rebasing `origin/main`.
- Before the correction, the latest Pages API build for `main` / `1a49e45` was `built` (workflow run `39092375868`). An initial fetch without a cache-busting query returned an older 211-row page; the cache-busted home and review pages confirmed the current 215/174/41/88/95 baseline. The discrepancy was caching, not a missing PR #20/#21 deployment.
- Direct official-source checks for this pass: [Lightscape](https://gggp.org/lightscape/) confirms Nov 20, 2026–Jan 3, 2027; [Exploratorium After Dark](https://www.exploratorium.edu/visit/calendar/after-dark) confirms Thursdays 6–10 p.m. and Glow Opening on Nov 19, with the [opening page](https://www.exploratorium.edu/visit/calendar/after-dark-glow-opening) distinguishing the event from the exhibition; [SFFILM Doc Stories](https://sffilm.org/2026-sffilm-doc-stories/) confirms the four-day Nov 5–8 run; [Stern Grove](https://www.sterngrove.org/), [Frameline](https://www.frameline.org/), [SFMOMA](https://www.sfmoma.org/exhibitions/), [RSA Conference](https://www.rsaconference.com/), [Noise Pop](https://www.noisepop.com/), and the [Golden Gate Park Band](https://goldengateparkband.org/) were checked for the published date/schedule limits recorded in the audit report.
- Pickleball sources checked: the [Palace launch notice](https://sfrecpark.org/m/newsflash/home/detail/1544) is from 2023 and its old reservation URL is a Custom404; the [current Rec & Park directory](https://sfrecpark.org/1772/Pickleball-Court-Directory) lists Larsen's eight dedicated open-play courts and zero reservable courts in the search result, but the direct page renders only loading text in the fetcher; the [Larsen opening release](https://sfrecpark.org/m/newsflash/home/detail/1672) confirms eight dedicated courts and its historical seven-day statement.
- Civic sources checked: the [Board of Appeals page](https://www.sf.gov/departments--board-appeals) confirms most Wednesdays at 5 p.m., City Hall Room 416, and remote/in-person attendance; the [Assessment Appeals Board page](https://www.sf.gov/departments--assessment-appeals-board) gives weekday sessions and its Oct 19 calendar; the [citywide calendar](https://www.sf.gov/events/upcoming) gives conflicting Oct 19 times. The row keeps specific times blank and the unverified flag remains visible. The [Board of Appeals FAQ](https://www.sf.gov/board-of-appeals-faqs) confirms that property-tax assessments are handled by the separate Assessment Appeals Board.
- [Escape From Alcatraz's official homepage](https://www.escapealcatraztri.com/) confirms the June 5–6, 2027 dates; the [overview](https://www.escapealcatraztri.com/event-information/overview) confirms random-drawing entry and a free public two-day Fitness Festival, but publishes no athlete entry fee; cost is blank and flagged.
- Local rebuild/checks: `scripts/build_site.py` wrote 216 events and 89 review items; `tools/validate.py` reports 176 verified, 40 needing review, 95 domains, 14 pages — OK; `audit/check_dataset.py` reports 0 hard problems, 0 broken internal links and 0 events missing from HTML. Detailed findings and remaining gaps are in `audit/POST-MERGE-2026-10-18-79993171.md`.
- Corrective PR #22 and its Pages deployment are complete; see the closing record below. The audit report records remaining unverified values and does not claim exhaustive coverage.

### Closing record — `arena-79993171` corrective PR and deployment (2026-10-18)

- **PR #22**: https://github.com/buffedlizard55-lab/MaltaProj6/pull/22 — **MERGED** to `main` at 2026-10-18T03:21:50Z; merge commit `6d0e7777762639c3a5522c7a5f3476ae4d4be844`.
- **GitHub Pages:** workflow `pages-build-deployment` run [39093353595](https://github.com/buffedlizard55-lab/MaltaProj6/actions/runs/39093353595) completed successfully. Pages API for commit `6d0e777` reports `status: built`, `error: null` (updated 2026-10-18T03:22:11Z).
- **Cache-busted live verification** (`?v=20261018pr22`): dashboard reports **216 events · 176 verified · 40 needing review · 89 review items · 95 distinct official domains**, with 116 recurring · 53 annual · 47 special and categories civic 37 · arts 71 · sports 10 · markets 29 · community 69. The live flagged page shows the assessment-board timing conflict, Palace/Larsen pickleball gaps, and Escape entry-fee review item. Civic/special/sports/annual pages show the split civic bodies, Glow opening, corrected dates, and blank unconfirmed schedule/cost/date cells.
- Local checks immediately before merge: `python3 scripts/build_site.py` wrote 216 events and 89 review items; `python3 tools/validate.py` passed (216/176/40/89/95, pages=14); `python3 audit/check_dataset.py` reported 0 hard problems, 0 broken internal links and 0 events missing from HTML. No automated PR checks were reported/configured; the local checks passed before merge.
- The Pages run had non-blocking runner/action deprecation notices; build, deploy, and report jobs all succeeded.
- Remaining gaps and known review heuristics are listed in `audit/POST-MERGE-2026-10-18-79993171.md`; all unverified rows remain published on the review page.

### Session record — `arena-76d2c635` independent re-audit + gap re-check (2026-10-18)

- **Scope discipline:** `arena-7141e086` held the final-integration claim (I0–I2, commit `9199715`, 02:57Z) over `data/events.py`, `data/events.json`, `*.html`, `scripts/`, `assets/` throughout this session, so all work landed in new files only: `audit/check_76d2c635.py`, `audit/row-audit-76d2c635.csv`, `audit/AUDIT-2026-10-18-76d2c635.md`, `data/gap-candidates-76d2c635.json`. **Both sessions edited this board from the same base — on merge/rebase keep both sessions' registry rows, task boards and logs.**
- **R1 structural re-audit:** independent checker v2 over all 211 rows + 85 register items → `hard_problems=[]`; weekday-vs-date pass 42 mentions / 0 mismatches; rebuild + `tools/validate.py` + prior `audit/check_dataset.py` all pass. One confirmed rendering defect: 26 imported `x-*` rows leak import metadata (`confirmed`/`partial`) into their published Schedule cells (IR-7).
- **R2 live re-verification:** ~33 rows re-fetched from official domains and compared field-by-field (annuals, specials, full SFMOMA `x-s-001…007` family, GGP gardens, SF Ballet/ATG seasons, Cal Academy, five civic commissions, Castro Merchants pair). Confirmed as published in the audit report; six discrepancies logged as IR-1…IR-6 (Conservatory "open daily" contradicted — closed Wednesdays; Off the Grid TI street address; Sarah Sze `x-s-007` cost; stale menorah conflict note; Golden Gate Bridge source/Battery Spencer scope flag — NPS groups Spencer in the Marin Headlands, jurisdiction not printed, flag-only; SF Beer Week area scope). Unchecked remainder (markets regulator sample, MLB schedule, City Hall weddings, most `x-*` rows) is stated plainly in the report.
- **R3 gap re-check:** 11 official-source candidates proposed in `data/gap-candidates-76d2c635.json` — 5 verified-ready (USS Pampanito, SS Jeremiah Treasure Island, Safeway Holiday Ice Rink Union Square, SF Open Studios, Yerba Buena Gardens Festival) and 6 unverified with itemised blanks (Musée Mécanique, SF Cable Cars, SF Half Marathon & 5K, SailGP SF 2027, SF Juneteenth Parade, Juneteenth Bayview Father's Day Festival). Prior flagged gaps **f-008** (ice rink — operator's own domain fetched) and **f-011** (YBG Festival — official season PR PDF fetched; homepage still reCAPTCHA-walled) are resolved. Nothing inferred: SFMTA's $9 fares page vs Board-approved $12 budget left the cable-car fare blank; Musée Mécanique's two official-branded domains disagree on hours, so its schedule is blank.
- **Handoff to `arena-7141e086`:** integration requests **IR-1…IR-16** in `audit/AUDIT-2026-10-18-76d2c635.md` cover the six row corrections, the 26-cell metadata blanking, prose-in-dates cleanup (8 rows), verified-but-blank specials (3), the flagged-table escape (`rec-sfpl-one-city-one-book`), Organiser blank naming on the flagged page, the past-dated specials sweep, adding the 11 R3 candidates (+register items, close f-008/f-011), and `data/meta.json` staleness. This session made **no** edits to the dataset, builder or HTML.

### Post-base update — `arena-76d2c635` (2026-10-18, after PRs #20/#22)

- `main` advanced during this session from `98d8528` (211 events) through PR #20 (`arena-3239c070`, 215 events) and PR #22 (`arena-79993171`, 216 events / 176 verified / 89 flagged) to `6d0e777`. The `arena-7141e086` integration claim referenced in my R0–R4 scope never merged; integration was carried out by those two sessions instead. This branch was rebased onto `6d0e777` and then `1ec50e8` (PR #23, record-only); conflicts were limited to additive `COORDINATION.md` appends and were resolved by keeping **all** sessions' registry rows, boards and logs (no other session's work was altered; this session still made no dataset/HTML/builder edits).
- Overlap handled, not duplicated: PR #20 independently added 4 of my 11 R3 candidates (USS Pampanito, Musée Mécanique, SF Cable Cars, SF Open Studios). They are marked `integrated_by_pr20` in `data/gap-candidates-76d2c635.json` with field-level cross-checks against my own fetches (all agree; two residual register notes proposed as IR-17/IR-18 — Musée `.org` vs `.com` weekday hours, SFMTA $9-vs-$12 fare transition). The remaining **7 candidates stay proposed** (SS Jeremiah Treasure Island, Union Square Ice Rink, YBG Festival — verified-ready; SF Half Marathon, SailGP 2027, SF Juneteenth Parade, Juneteenth Bayview — unverified with blanks), and three of them resolve flags PR #20 itself published (`flag-union-square-ice-rink`, `flag-kaiser-sf-half`, `flag-sailgp-no-sf-2026` complement).
- IR-7 (26-cell metadata leak) and IR-8 (prose-in-dates) were independently fixed by PR #22 — confirmed by re-running `audit/check_76d2c635.py` on the 216-row dataset (`hard_problems=[]`; `tools/validate.py` OK 216/176/40/89). Still open for the next integration owner: IR-1 Conservatory hours, IR-2 (residual) Off the Grid TI address, IR-3 `x-s-007` cost, IR-4 menorah note, IR-5 GGB source/Battery Spencer scope flag, IR-6 SF Beer Week area, IR-9 (expanded to 28 verified-but-blank-core rows after PR #22's blanking — status-semantics policy call), IR-10/IR-11 flagged-page gaps, IR-12 past-dated sweep (42 rows), IR-13 (7 remaining candidates), IR-14 `data/meta.json` (still total 87), IR-15/IR-16, IR-17/IR-18. Full disposition table: `audit/AUDIT-2026-10-18-76d2c635.md` post-base addendum.

### Closing record — `arena-76d2c635` merge and deploy (2026-10-18)

- **PR #24**: https://github.com/buffedlizard55-lab/MaltaProj6/pull/24 — **MERGED** to `main` at 2026-10-18T03:27:56Z, merge commit `7e2207ee50f2a77f720a32ee445701106f48d834`. Diff vs prior `main` was insertions-only across 5 files (`COORDINATION.md` +41, `audit/AUDIT-2026-10-18-76d2c635.md`, `audit/check_76d2c635.py`, `audit/row-audit-76d2c635.csv`, `data/gap-candidates-76d2c635.json`); no dataset, builder or HTML file changed, and no other session's board content was altered (two rebase conflicts on additive board appends were resolved by keeping all sessions' rows).
- **GitHub Pages:** latest build for `7e2207e` reports status **`built`**, `error: null` (updated 2026-10-18T03:28:17Z).
- **Live content confirmed** by fetching https://buffedlizard55-lab.github.io/MaltaProj6/?v=20261018pr24 after the build: dashboard shows **216 events listed · 176 rows marked verified · 40 rows needing review · 89 review items published · 95 distinct official domains**, with 116 recurring · 53 annual · 47 special and categories civic 37 · arts 71 · sports 10 · markets 29 · community 69 (unchanged by this PR, as intended).
- Pre-merge checks on the rebased tree: `python3 audit/check_76d2c635.py` → `hard_problems=[]` (216 events / 89 register items); `python3 tools/validate.py` → OK (216/176/40/89, 95 domains, 14 pages); gap-candidates JSON parses.
- **Open handoff for the next integration owner** (all in `audit/AUDIT-2026-10-18-76d2c635.md`): IR-1, IR-2 (residual), IR-3, IR-4, IR-5, IR-6, IR-9 (28 verified-but-blank-core policy call), IR-10, IR-11, IR-12 (42 past-dated rows), IR-13 (7 remaining gap candidates in `data/gap-candidates-76d2c635.json`), IR-14, IR-15, IR-16, IR-17, IR-18. Flagged/unverified items remain published on the Flagged for Review page and do not block, per board rules. This closing record follows via a small record-only PR, as earlier sessions did.

---

## Session record — `arena-8cb2d3cc` final integration (2026-10-18)

**Scope.** Final integration pass on the union dataset: repo review, line-by-line re-verification of the published rows against official pages, gap research, defect repair, site build, PR, merge and Pages deploy confirmation. Claim commit `b9234a4` was pushed before any shared-file edit; every other session branch was behind `main` at that point (`gh api …/compare`), so there was no concurrent writer.

### What the pass changed

- **One fabricated row removed.** `art-california-museum` placed "The California Museum" at a San Francisco address; the museum's own pages place it at 1020 O Street, Sacramento 95814. The row is deleted and the exclusion is documented on the Flagged page (`flag-california-museum-removed`), as the city-limits rule requires.
- **Four long-standing gaps closed against organiser pages.** FOG Design+Art 2027 (SFMOMA fair and gala pages: gala Wed Jan 20, fair Jan 21–24, daily hours, $35/$40 single day, $95/$100 four-day, gala from $300); Portola Music Festival (goldenvoice.com/festivals: Sep 26–27, 2026, Pier 80); Juneteenth Fillmore (juneteenth-sf.org: Sat Jun 13, 2026, 11 a.m.–6 p.m., free, Juneteenth SF Freedom Organization); Golden State Valkyries (valkyries.wnba.com: 2026 home opener May 10 vs Phoenix; Finals G1 Oct 17 and G2 Oct 19 at Chase Center).
- **Three rows added, each from the organiser's own page.** San Francisco Mime Troupe free summer season (dates from the company's official Google Calendar feed, including the closing Sep 7, 2026 show at Mission Dolores Park); Yerba Buena Gardens Festival (2026 press-release PDF: 26th season, opener May 9, 100+ free performances May–November, plus its recurring strands and anchor events); Conservatory of Flowers light show (gggp.org: nightly, 30 minutes after sunset, Oct 1, 2026–Jan 30, 2027, free).
- **Corrections and source repairs.** Cable-car fares ($9 single ride in 2026, $12 from Jan 4, 2027, $18 Cable Car Plus) from SFMTA fare pages; Assessment Appeals Board session times (Mon–Fri, 9:30 a.m. and 1:30 p.m., Room 405) from the department page; Recreation and Park Commission Operations Committee cadence (first Thursday, 2 p.m., Room 416) from `sfrecpark.org/1744/Meeting-Info-Calendar`, replacing a calendar link that now redirects to a staff sign-in page; HRC meeting date confirmed; Alcatraz closure confirmed (Oct 26 – Nov 18, 2026, NPS release); Escape From Alcatraz confirmed for Jun 5–6, 2027.
- **Pickleball sourcing corrected.** The old `sfrecpark.org/1591/...` reservation URL is a Custom404. Larsen is now verified from the live Pickleball Court Directory (eight dedicated open-play courts, no lights, restrooms, zero reservable — hence no reservation fee) at 850 Vicente Street; the Palace of Fine Arts row keeps its schedule and cost blank because only a 2023 launch notice exists, and the row stays flagged.
- **New review item.** `flag-musee-hours-conflict`: museemecanique.com says 10 a.m.–8 p.m. daily; the museum's .org site says weekday closing at 7 p.m. The row keeps the .com hours and the disagreement is published rather than silently resolved.
- **Site work.** New `all-events.html` (218 rows; free-text search plus schedule, category, status and timing filters; degrades to the full table without JavaScript), rebuilt `analysis.html` (counts, breakdowns, blank-field coverage, 98 source domains, pass summary), new `data/events.csv` (16 columns, 123 KB), refreshed `README.md` and `data/meta.json` (previously stale at "total 87"), and 42 rows marked `timing="concluded"` so finished editions are badged and kept out of the home page's upcoming strip.
- **Build gate.** `scripts/build_site.py` → `Wrote 13 pages, 218 events, 97 flagged items`; `tools/validate.py` → `events=218 verified=208 review_gap=10 review_items=97 domains=98 pages=15` — OK; local link/anchor scan over 15 HTML files → 0 issues.

### Closing record — merge and deploy

- **PR #26**: https://github.com/buffedlizard55-lab/MaltaProj6/pull/26 — **MERGED** to `main` at 2026-10-18T05:57:11Z; merge commit `1cdd3ab71b48727faa4f068a460379bf5bb5ad07`.
- **GitHub Pages:** the deployment for `1cdd3ab` reports `status: built`, `error: null`.
- **Live verification** (cache-busted `?v=20261018p26`): the dashboard reports **218 events listed · 208 rows marked verified · 10 rows needing review · 42 concluded editions · 97 review items published · 98 distinct official domains**, with 116 recurring · 55 annual · 47 special and category counts 37 civic · 73 arts · 10 sports · 29 markets · 69 community. The `all-events.html` call-to-action resolves, and the home page lists the corrected upcoming dates (Boo at the Zoo Oct 31, Scaregrove Oct 30, SuperNatural Oct 24, Presidio Día de los Muertos/Diwali Nov 7, Lightscape Nov 20–Jan 3).
- **Known review items (do not block, per board rules).** Ten rows remain unverified, each with a source link and blank unconfirmed cells: Outside Lands 2027 (festival site returns HTTP 500), TreasureFest (no 2026 dates published), Palace of Fine Arts pickleball (2023 notice only), the Presidio Nisei exhibition, three SFMTA Shared Spaces rows, the Greek Food Festival, Frameline and the Día de los Muertos altars. Two editorial questions are published rather than guessed: whether industry conferences (GDC, Dreamforce, RSAC) belong in an events inventory, and whether the Chinese New Year Parade's "(Year of the Ram)" label is correct for 2027.
- This record-only PR follows, as earlier sessions did.
- **Post-deploy corrections (PR #28).** The live check surfaced two display defects, both fixed and re-validated before this record closed: eight imported annual rows rendered their dates as raw ISO strings (`2026-10-02;2026-10-03;2026-10-04`), now formatted as prose by a `_humanize_dates()` helper that changes only the presentation; and the Lightscape row carried a bare "Ticketed" cost, now the official ticket table (adult from $32 general / $27 member, youth from $20 / $17, under-5 free, flex from $60 / $49, Museums for All $10). The Chinese New Year Parade note also records that "Year of the Ram" is the organiser's own rendering of the year's zodiac animal, not a data error.

---

## Closing record — `arena-8e8e24dc` verification pass (2026-10-18)

**Outcome.** Ten defects that survived the PR #26 integration were repaired and published in **PR #29**
(https://github.com/buffedlizard55-lab/MaltaProj6/pull/29), merged to `main` at **06:01:51Z** as
`a6b9770c132d9040b81879b7d7308817b033eded`. GitHub Pages reports `status: built`, `error: null` for that
commit, and the live dashboard reports **217 events · 206 verified · 11 review-gap · 103 review items ·
42 concluded editions · 97 official domains** (115 recurring · 55 annual · 47 special; 37 civic · 72 arts ·
10 sports · 29 markets · 69 community).

**Corrections published.** Contemporary Jewish Museum removed (temporarily closed since 15 Dec 2024; the row's
364 Ninth Street address was wrong — the museum publishes 736 Mission Street); Presidio row renamed *Presidio
Visitor Center* at 210 Lincoln Boulevard (104 Montgomery Street is the Walt Disney Family Museum); San Francisco
Symphony moved to Davies Symphony Hall, 201 Van Ness Avenue; Haight-Ashbury Street Fair schedule replaced with
the confirmed 20 September 2026 edition; Secondhand Saturdays "Quintana" corrected to **Quintara** and its
duplicated address fragment removed; Bouquets to Art 2027 dates blanked (the FAMSF page publishes none) and the
row set `unverified`, including a residual copy of the same week in the FAMSF exhibitions row; de Young now
Tue–Sun 9:30–5:15 closed Mondays; Legion of Honor hours and prices filled; Exploratorium hours filled with the
Monday closure and noon Sunday opening. Six source-linked review items were added.

**Verification.** `scripts/build_site.py` → `Wrote 13 pages, 217 events, 103 flagged items` (second run leaves
no diff); `tools/validate.py` → OK; `audit/check_8e8e24dc.py` → `hard_problems=0` (83 rows with heuristic
findings, 42 of them `verified` rows whose remaining blank field the official page does not publish). Full
evidence, per-page source log and the IR disposition table are in `audit/AUDIT-2026-10-18-8e8e24dc.md`.

**Follow-up.** PR #30 (https://github.com/buffedlizard55-lab/MaltaProj6/pull/30) removed the last copy of the
unsupported Bouquets week from the FAMSF exhibitions row and merged at **06:03:45Z** as
`79ac018916c2be40304eb803ddc3c9d463b4ad03`; the Pages deployment for that commit reports `status: built`,
`error: null`. Live `special.html` now shows "Bouquets to Art 2027 — not confirmed / not confirmed,
unverified" and "Bouquets to Art 2027 (dates not yet published)" inside the FAMSF row.

**Final state on `main`:** 217 events (115 recurring · 55 annual · 47 special), 206 verified, 11 review-gap
rows, 103 review items, 42 concluded editions, 97 official domains, 15 pages. Checks re-run after the merge:
build reproducible, `tools/validate.py` OK, `audit/check_8e8e24dc.py` `hard_problems=0`.

**Follow-up (record-only).** This final record-only PR follows, as earlier sessions did.

---

## Task board — `arena-fc3438db` (verification + requirements-alignment pass)

Session branch: `arena/fc3438db-maltaproj6` (Arena-fixed branch for this session; no branch switch).

**Concurrency check on arrival (2026-10-18 09:41Z).** `main` at `56eda46` (PR #31 merge; 217 events /
206 verified / 11 review-gap rows / 103 review items / 42 concluded / 97 domains; Pages `built`). All prior
session branches are behind `main`. `arena/ef213634-maltaproj6` is ahead by 2 claim-only commits
(`846ae85` 05:46Z, `e0c4fc6` 05:53Z) with **no commits for ~4 hours** and no PR — its F1/F2 claims are stale
under the board's 60-minute rule and are taken over by this session. The work those claims describe was in
fact completed and merged by `arena-8cb2d3cc` (PR #26) and `arena-8e8e24dc` (PRs #29–#31) before the claims
expired; nothing is overwritten. This session uses the Arena-fixed branch `arena/fc3438db-maltaproj6`.

| # | Task | Status | Owner | Files in scope | Notes |
|---|---|---|---|---|---|
| FC0 | Register, claim scope, takeover of stale `arena-ef213634` claims | 🟡 in progress | `arena-fc3438db` | `COORDINATION.md` (registry/task/log rows) | Claim commit pushed before any other edits. |
| FC1 | Line-by-line structural audit of all 217 published rows + 103 review items (source link present/https/official, blanks vs status, duplicates, cost-column coverage) | ⬜ unclaimed | `arena-fc3438db` | `audit/AUDIT-2026-10-18-fc3438db.md` (new), `audit/check_fc3438db.py` (new) | |
| FC2 | Live official-source re-verification: every soonest-dated/upcoming row (feeds the executive summary) + stratified sample of recurring/annual rows | ⬜ unclaimed | `arena-fc3438db` | `audit/AUDIT-2026-10-18-fc3438db.md` (new) | fetch_page against official pages only; JS-shell pages recorded as content-not-re-verified, never guessed. |
| FC3 | Gap research for the user's stated focus: **free events — gaming, music, AI** (and everything else after) inside SF city limits | ⬜ unclaimed | `arena-fc3438db` | `data/gap-candidates-fc3438db.json` (new), `data/events.py` | Official/organiser sources only; every field from a fetched official page; unconfirmed fields blank + flagged. |
| FC4 | Requirements alignment of the site: executive summary of events near today (2026-10-18) on the home page; upcoming dates sorted soonest-first and highlighted first; cost clearly labelled on every table; free-events emphasis; mobile-friendly check/polish | ⬜ unclaimed | `arena-fc3438db` | `scripts/build_site.py`, `assets/site.css`, generated `*.html`, `README.md` | |
| FC5 | Rebuild, validate (build_site, tools/validate, dataset audit, link scan), PR to `main`, merge, confirm Pages deploy, record on this board | ⬜ unclaimed | `arena-fc3438db` | `COORDINATION.md` | No merge until local checks pass. |
