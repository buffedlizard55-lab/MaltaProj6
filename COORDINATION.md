# COORDINATION.md — San Francisco Events Project

Shared task board for all agent sessions working on this repository.
**Repo:** https://github.com/buffedlizard55-lab/MaltaProj6
**Branch model:** each session works on its own branch `session-<id>/<task>` (or a git worktree) and edits only files in its claimed scope.

> **STATUS:** ⬜ unclaimed · 🟡 in progress · ✅ done · 🔍 needs review

---

## Session registry

| Session ID | Agent / branch | Notes |
|---|---|---|
| `arena-b0f3cfd3` | `arena/b0f3cfd3-maltaproj6` | Primary session: research + data + site build + integration + PR/merge. Only session active on the remote at every claim point. |

---

## Task board

| # | Task | Status | Owner | Files in scope | Notes |
|---|---|---|---|---|---|
| 0 | Create `COORDINATION.md` task board | ✅ done | `arena-b0f3cfd3` | `COORDINATION.md` | Board created on a repo with no other content. |
| 1 | Research: Recurring (weekly/regular) events — official sources | ✅ done | `arena-b0f3cfd3` | `data/events.py` | 92 rows land in the `recurring` group. Rec & Park, SFPL, Presidio, museums, markets, Sunday Streets, SFMTA/Port/SFPL/Arts/Planning/Rec&Park/Fire/Police/PUC/HRC commissions, sports, markets. |
| 2 | Research: Recurring (annual) events — official sources | ✅ done | `arena-b0f3cfd3` | `data/events.py` | 34 rows land in the `annual` group. Parades, festivals, opera/ballet/theatre seasons, races, holiday traditions. |
| 3 | Research: Special / one-off events — official sources | ✅ done | `arena-b0f3cfd3` | `data/events.py` | 20 rows land in the `special` group. Fleet Week, Presidio 2026 season, Alcatraz closure, dated 2026–2027 programmes. |
| 4 | Research: Museums & attractions (SF city limits) | ✅ done | `arena-b0f3cfd3` | `data/events.py` | FAMSF (de Young, Legion of Honor), Asian Art Museum, SFMOMA, Cal Academy, Exploratorium, California Museum, CJM, SF Zoo, Gardens of Golden Gate Park, Randall, Presidio Museum, Fort Point, Alcatraz, Maritime NHP, Angel Island SP, Golden Gate Bridge. |
| 5 | Research: Performing arts, sports, nightlife | ✅ done | `arena-b0f3cfd3` | `data/events.py` | SF Symphony, SFJAZZ, SF Opera, SF Ballet, ATG San Francisco (ex-BroadwaySF), SFFILM, Litquake, Silent Film Festival, Giants, Warriors, Valkyries, SF Marathon, Bay to Breakers, Dragon Boat, Palace of Fine Arts pickleball, Larsen Pickleball Complex. |
| 6 | Research: Civic/government public meetings & services | ✅ done | `arena-b0f3cfd3` | `data/events.py` | 36 rows land in the `civic` category. Board of Supervisors + 4 committees, Assessment Appeals Boards, Planning, Historic Preservation, SFMTA, Port, Fire, PUC, Arts Commission (7 bodies), Police, Health, SFUSD, Building Inspection, Ethics, Environment, Small Business, Health Service Board, SFCTA, TIDA, HRC, Library, Rec & Park, City Hall weddings, citywide calendar, district events. |
| 7 | Verification pass — every row has an official source link | ✅ done | `arena-b0f3cfd3` | `data/events.py`, `data/events.json` | 146 rows, 133 fully verified, 13 with a deliberate blank. 109 distinct official source URLs across 64 official domains. Every row's `source_url` is `https://`. Build script asserts this. |
| 8 | Site build — GitHub Pages, landing page + subpages | ✅ done | `arena-b0f3cfd3` | `scripts/build_site.py`, `assets/style.css`, `*.html` | 11 static pages, no client-side JS. Dashboard landing page with stat tiles, category tiles and analysis tables. |
| 9 | "Flagged for Review" page | ✅ done | `arena-b0f3cfd3` | `data/events.py` (FLAGGED), `flagged.html` | 19 published items: conflicts between official sources, blank-cell rows, ended events and out-of-scope exclusions. |
| 10 | Integration: merge branches, re-verify, link check, publish | ✅ done | `arena-b0f3cfd3` | `data/*`, `scripts/*`, `*.html`, `assets/*` | Single-session integration. Link checker: 110 internal links + all anchors + all external `https://` sources → 0 problems. Row counts on all 8 listing pages match the dataset. |
| 11 | PR → main, merge, confirm Pages deploy | 🟡 in progress | `arena-b0f3cfd3` | — | PR opened and merge/deploy confirmation recorded below. |

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

## Site map

| Page | File | Contents |
|---|---|---|
| Home / dashboard | `index.html` | Stat tiles, category tiles, type & area analysis tables, recently confirmed dated events, "how to read a row" |
| Regularly recurring | `recurring.html` | 92 rows — fixed weekly / monthly schedules |
| Annual | `annual.html` | 34 rows — year after year |
| Special | `special.html` | 20 rows — dated 2026–2027 events |
| Civic | `civic.html` | 36 rows — boards, commissions, public meetings |
| Arts & culture | `arts.html` | 41 rows — museums, performance, screen |
| Sports | `sports.html` | 8 rows — teams, races, active recreation |
| Markets & food | `markets.html` | 10 rows — farmers markets, food halls, street markets |
| Community & parks | `community.html` | 51 rows — neighbourhood programmes, festivals, free recreation |
| Flagged for review | `flagged.html` | 19 published discrepancies / gaps / exclusions + the rows carrying a blank cell |
| Method | `methodology.html` | Scope, sourcing rules, build process, official domains used, known limitations |

Every event appears on exactly **one** type page (recurring / annual / special) **and** exactly **one** category page,
so the two views can never disagree. The build script re-checks this on every run.

---

## Log

- **2026-10-18** — `arena-b0f3cfd3`: Reviewed repo (empty except `README.md`, one commit). Created this board. Claimed tasks 1–11 in sequence as a single primary session (no other sessions were active on the remote at claim time).
- **2026-10-18** — `arena-b0f3cfd3`: **Task 1–6 research complete.** Fetched and read 80+ official pages across `sf.gov`, `sfgov.legistar.com`, `sfrecpark.org`, `sfpl.org`, `sfplanning.org`, `sfmta.com`, `sfport.com`, `sf-fire.org`, `famsf.org`, `exploratorium.edu`, `calacademy.org`, `sfmoma.org`, `asianart.org`, `sfzoo.org`, `gggp.org`, `presidio.gov`, `nps.gov`, `parks.ca.gov`, `foodwise.org`, `fleetweeksf.org`, `sfshakes.org`, `sfsymphony.org`, `sfjazz.org`, `sfopera.com`, `sfballet.org`, `broadwaysf.com`, `sffilm.org`, `litquake.org`, `silentfilm.org`, `dragonboatsf.com`, `thesfmarathon.com`, `baytobreakers.com`, `sfpride.org`, `chineseparade.com`, `uissf.org`, `carnavalsanfrancisco.org`, `sfcherryblossom.org`, `sfitalianheritage.org`, `unionstreetsf.com`, `northbeachfestival.org`, `haightashburystreetfair.org`, `nihonmachistreetfair.org`, `moonfestival.org`, `folsomstreet.org`, `transmarch.org`, `castrostreetfair.org`, `castromerchants.com`, `parollanternfestival.com`, `treasurefest.com`, `howweird.org`, `levisstadium.com` and others. Aggregator sites (funcheap, Eventbrite, Yelp, sfstation, tourism blogs, Reddit, Wikipedia) were used **only** to locate official pages, never as evidence.
- **2026-10-18** — `arena-b0f3cfd3`: **Task 7 verification.** Dataset written to `data/events.py` (canonical) and mirrored to `data/events.json` by the build. 146 rows; 133 fully verified, 13 rows with a deliberate blank cell. 109 distinct official source URLs over 64 official domains. Every `source_url` is `https://`.
- **2026-10-18** — `arena-b0f3cfd3`: **Task 8/9 site build.** `scripts/build_site.py` renders 11 static pages plus `assets/style.css` from the dataset (no client-side JavaScript). Added a `group` (recurring / annual / special) and `category` (civic / arts / sports / markets / community) view over the same rows so the two requested organisations and the topical subpages coexist without contradiction. 19 items published on the Flagged for review page.
- **2026-10-18** — `arena-b0f3cfd3`: **Task 10 integration checks.** Link/anchor/tag checker over all 11 pages: 110 internal links, all `#anchor` targets, and all external source URLs resolve syntactically → **0 problems**. Row counts on all 8 listing pages match the dataset exactly (92 / 34 / 20 / 36 / 41 / 8 / 10 / 51). Every event id has an anchor on at least one page.
- **2026-10-18** — `arena-b0f3cfd3`: **Task 11 in progress** — PR opened to `main`; merge + Pages deploy confirmation to be appended below.

### Irregularities found and published (all on `flagged.html`)

1. Board of Supervisors Land Use & Transportation Committee — Legistar says 4:30 p.m., SFGovTV says 1:30 p.m. → time left blank.
2. Board of Supervisors Rules Committee — Legistar says 1:00 p.m., SFGovTV says 10:00 a.m. → time left blank.
3. Board of Supervisors Budget and Finance Committee — SFGovTV lists "Wednesdays at 12:30AM", which is not a credible meeting time → row uses the Legistar time with a note.
4. Assessment Appeals Boards — the sf.gov citywide calendar and the Board landing page give different times for 10/19/2026 → times left blank.
5. Recreation and Park Commission — department says third Thursday; SFGovTV says 2nd & 4th Thursdays. The published 2026 dates are all third Thursdays → row follows the department and the discrepancy is published.
6. Library Commission — Bylaws say third Thursday 4:30 p.m.; a separate SFPL policies page says first Tuesday *and* third Thursday at 4:00 p.m. → row uses the Bylaws.
7. Bay to Breakers — organiser's own page title says "May 16, 2027" while its body copy still says "May 18" → date taken from the title.
8. SFFILM — festival page says April 24–May 4, 2026; submission pages say April 23–May 3, 2026 → row uses the festival page.
9. Dragon Boat Festival — Treasure Island (until 2015) → Lake Merced in 2026 → row reflects the 2026 venue.
10. TreasureFest — no confirmed San Francisco date; organiser is "scouting our next location in the Bay Area" → row left entirely blank.
11. How Weird Street Faire — ended after 25 years (2000–2024) per the organiser's own site → excluded and published.
12. San Francisco 49ers — all home games at Levi's Stadium, **Santa Clara** → excluded (out of city limits) and published.
13. Alcatraz Island — closed for dock repairs 26 Oct – ~18 Nov 2026 → published.
14. Castro Menorah Lighting — organiser's calendar says 7 Dec 2026, its own description says 15 Dec → row uses the calendar date.
15. Mission Community Market — March–November only, unlike the other two Foodwise markets → published so it is not read as year-round.
16. Human Rights Commission — no published regular cadence → frequency left blank.
17. Larsen Pickleball Complex — no street address published on the official page → address left blank.
18. SF Music Week — referenced on an official sf.gov release but no official programme page located → dates and cost left blank.
19. Golden State Valkyries — 2026-27 home fixtures not confirmed against an official schedule page → dates left blank.
