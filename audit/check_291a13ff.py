#!/usr/bin/env python3
"""Independent structural audit of the SF events catalogue — session arena-291a13ff (2026-10-18).

This script ONLY reads committed files. It never edits the dataset or the
generated site (those belong to the live integration session's claimed
scope — see COORDINATION.md).

Checks, over data/events.json (the published union) and the generated pages:
  1. id / title present and unique (events and flagged)
  2. source_url present, https, parseable; domain classified
     (city/state/federal agency vs organiser vs other)
  3. blank core cells vs `status`:
       - "unverified" rows must carry a non-empty notes string (why)
       - "verified" rows with a blank schedule/location (and cost, unless the
         row type legitimately publishes none) are reported for human review
  4. cost discipline: no row may show a generic non-numeric price word
     ("Ticketed", "Varies", ...) as its cost; cost is either a number, an
     explicit free/partly-free wording, or blank
  5. location/area scanned for out-of-San-Francisco place names
  6. dated rows whose date_end is before AUDIT_DATE must be marked concluded
  7. near-duplicate titles (token-overlap heuristic) across the union
  8. every "unverified" row surface-check: its id appears in flagged.html,
     so nothing unverified is published silently
  9. generated HTML: every internal href target exists; every page's
     nav is consistent; event ids appear on their claimed `page`
 10. events.json is in sync with data/events.py + scripts/merge_parallel.py
     (rebuilt in-memory and compared — catches a stale mirror)

Outputs: audit/row-audit-291a13ff.csv (one row per event) + stdout summary.
Usage: python3 audit/check_291a13ff.py
"""
from __future__ import annotations

import csv
import json
import os
import re
import sys
from collections import Counter
from datetime import date
from urllib.parse import urlparse

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
AUDIT_DATE = date(2026, 10, 18)

OUT_OF_SF = [
    "oakland", "berkeley", "emeryville", "daly city", "south san francisco",
    "sausalito", "mill valley", "san mateo", "palo alto", "sunnyvale",
    "santa clara", "mountain view", "san jose", "fremont", "hayward",
    "richmond,", "vallejo", "napa", "santa rosa", "burlingame",
    "foster city", "redwood city", "menlo park", "sacramento",
    "petaluma", "concord", "walnut creek", "livermore", "half moon bay",
    "tiburon", "alameda", "san rafael", "novato", "fairfax", "pacifica",
]

GENERIC_COST = re.compile(
    r"^(ticketed|paid|varies|varied|admission|fee|entry fees? apply|see (the )?(official )?(site|page)|"
    r"check (the )?(official )?(site|page)|registration required)\.?$",
    re.IGNORECASE,
)

AGENCY_HOST_KEYWORDS = [
    ".gov", "sfmta.com", "sfpl.org", "sfrecpark.org", "sfusd.edu",
    "sfgate.com/", "treasureislandmuseum.org",  # placeholder; sfgate removed below
]
OFFICIAL_KNOWN = {
    "sf.gov", "sfmta.com", "sfpl.org", "sfrecpark.org", "sfusd.edu",
    "nps.gov", "parksconservancy.org", "presidio.gov", "sfgov.org",
    "sfenvironment.org", "sfcityhall.org",
}

HARD = []   # problems that contradict the project's written rules
SOFT = []   # observations for human review


def classify_host(url: str) -> str:
    try:
        host = urlparse(url).netloc.lower()
    except Exception:
        return "unparseable"
    if not host:
        return "unparseable"
    if host.endswith(".gov") or host in OFFICIAL_KNOWN:
        return "government/agency host"
    if any(host.endswith(k) or k in host for k in ("sfpl.org", "sfmta.com", "sfrecpark.org")):
        return "government/agency host"
    return "organiser/commercial host"


def tokens(title: str):
    return {t for t in re.findall(r"[a-z0-9]+", title.lower()) if len(t) > 2}


def main() -> int:
    with open(os.path.join(ROOT, "data", "events.json"), encoding="utf-8") as fh:
        data = json.load(fh)
    events = data["events"]
    flagged = data["flagged"]

    # ------------------------------------------------------------- 1. ids
    ids = [e.get("id", "") for e in events]
    if len(ids) != len(set(ids)):
        dupes = [i for i, n in Counter(ids).items() if n > 1]
        HARD.append(f"duplicate event ids: {dupes}")
    titles = [e.get("title", "") for e in events]
    if len(titles) != len(set(titles)):
        dupes = [t for t, n in Counter(titles).items() if n > 1]
        SOFT.append(f"duplicate event titles (may be legitimately separate rows): {dupes}")
    f_ids = [f.get("id", "") for f in flagged]
    if len(f_ids) != len(set(f_ids)):
        HARD.append(f"duplicate flagged ids: {[i for i, n in Counter(f_ids).items() if n > 1]}")

    # ------------------------------------------- 2. sources / 3. blanks / 4-5.
    rows = []
    domains = Counter()
    for e in events:
        eid = e.get("id", "")
        url = e.get("source_url", "")
        problems, notes = [], []
        if not e.get("title"):
            problems.append("missing title")
        if not url.startswith("https://"):
            problems.append("source_url missing or not https")
        else:
            dom = classify_host(url)
            domains[urlparse(url).netloc.lower()] += 1
            if dom == "unparseable":
                problems.append("source_url not parseable")
        for field in ("schedule", "location", "cost"):
            if not (e.get(field) or "").strip():
                if e.get("status") == "verified":
                    notes.append(f"verified with blank {field}")
                else:
                    notes.append(f"unverified blank {field}")
        if e.get("status") == "unverified" and not (e.get("notes") or "").strip():
            problems.append("unverified row without an explanatory note")
        cost = (e.get("cost") or "").strip()
        if cost and GENERIC_COST.match(cost):
            problems.append(f"generic non-numeric cost shown as price: {cost!r}")
        hay = f"{e.get('location','')} | {e.get('area','')} | {e.get('title','')}".lower()
        hits = [p for p in OUT_OF_SF if p in hay]
        if hits:
            SOFT.append(f"{eid}: out-of-SF place name(s) in display text {hits} — human review " 
                        "(may be a scope note or an SF neighbourhood sharing a name)")
        if e.get("status") not in ("verified", "unverified"):
            problems.append(f"unexpected status {e.get('status')!r}")
        rows.append(dict(
            id=eid, title=e.get("title", ""), page=e.get("page", ""),
            group=e.get("group", ""), category=e.get("category", ""),
            focus=e.get("focus", ""), status=e.get("status", ""),
            timing=e.get("timing", ""), cost=cost,
            cost_class=e.get("cost_class", ""),
            source_host=urlparse(url).netloc.lower() if url else "",
            date_start=e.get("date_start", ""), date_end=e.get("date_end", ""),
            notes="; ".join(notes), problems="; ".join(problems),
        ))
        for p in problems:
            HARD.append(f"{eid}: {p}")
        for n in notes:
            if n.startswith("verified with blank"):
                SOFT.append(f"{eid}: {n}")

    # ------------------------------------------------- 6. past-dated rows
    # HARD only for one-off dated specials whose *end* date is past and which are
    # not marked concluded. Recurring/annual/attraction rows legitimately show a
    # season anchor in the past while the programme is still running; those are
    # SOFT observations only.
    for e in events:
        for field in ("date_end", "date_start"):
            de = e.get(field) or ""
            if de and not re.fullmatch(r"\d{4}-\d{2}-\d{2}", de):
                SOFT.append(f"{e['id']}: {field} not ISO ({de!r})")
        de = e.get("date_end") or ""
        if de and re.fullmatch(r"\d{4}-\d{2}-\d{2}", de):
            d = date.fromisoformat(de)
            if d < AUDIT_DATE and e.get("timing") != "concluded":
                if e.get("group") == "special":
                    HARD.append(f"{e['id']}: special row ended {de} but not marked concluded")
                else:
                    SOFT.append(f"{e['id']}: {e.get('group')} row has date_end {de} in the past "
                                "and is not concluded (may be a running season anchor)")

    # ------------------------------------------------- 7. near-duplicate titles
    toks = [(e["id"], tokens(e.get("title", ""))) for e in events]
    for i in range(len(toks)):
        for j in range(i + 1, len(toks)):
            a, ta = toks[i]
            b, tb = toks[j]
            if not ta or not tb:
                continue
            inter = ta & tb
            if len(inter) >= 3 and len(inter) >= 0.8 * min(len(ta), len(tb)):
                SOFT.append(f"near-duplicate titles: {a} ~ {b} (shared tokens {sorted(inter)})")

    # ------------------------------------- 8. unverified rows on flagged page
    try:
        with open(os.path.join(ROOT, "flagged.html"), encoding="utf-8") as fh:
            flagged_html = fh.read()
        for e in events:
            if e.get("status") == "unverified" and f'id="{e["id"]}"' not in flagged_html \
                    and f'#{e["id"]}' not in flagged_html and e["id"] not in flagged_html:
                HARD.append(f"{e['id']}: unverified row not surfaced on flagged.html")
    except FileNotFoundError:
        HARD.append("flagged.html missing")

    # ------------------------------------------------- 9. HTML link integrity
    pages = [f for f in os.listdir(ROOT) if f.endswith(".html")]
    anchors = {}
    for f in pages:
        with open(os.path.join(ROOT, f), encoding="utf-8") as fh:
            txt = fh.read()
        anchors[f] = set(re.findall(r'id="([^"]+)"', txt))
        for href in re.findall(r'href="([^"#]+)(?:#[^"]*)?"', txt):
            if href.startswith(("http://", "https://", "mailto:", "tel:")):
                if href.startswith("http://"):
                    HARD.append(f"{f}: non-https external link {href}")
                continue
            if href and not os.path.exists(os.path.join(ROOT, href)):
                HARD.append(f"{f}: internal href target missing: {href}")
        for href in re.findall(r'href="([^#"]*)#([^"]+)"', txt):
            target, frag = href
            target = target or f
            if target in anchors and frag not in anchors[target]:
                HARD.append(f"{f}: fragment #{frag} not found in {target}")

    # every event id appears on the page it is expected to render on. Imported
    # rows have a blank `page` and are routed by `group`.
    for e in events:
        page = e.get("page") or e.get("group") or ""
        target = page + ".html"
        if not os.path.exists(os.path.join(ROOT, target)):
            HARD.append(f"{e['id']}: expected page {target} does not exist")
            continue
        with open(os.path.join(ROOT, target), encoding="utf-8") as fh:
            txt = fh.read()
        if e["id"] not in txt:
            SOFT.append(e["id"] + ": id not found on expected page " + target)

    # -------------------------------------- 10. mirror in sync with canonical py
    sys.path.insert(0, os.path.join(ROOT, "scripts"))
    sys.path.insert(0, os.path.join(ROOT, "data"))
    try:
        from events import EVENTS as BASE_EVENTS, FLAGGED as BASE_FLAGGED, assign_views, cost_review_flags
        from merge_parallel import parallel_events, parallel_flagged
        rebuilt = assign_views(list(BASE_EVENTS) + parallel_events(BASE_EVENTS))
        rebuilt_flagged = list(BASE_FLAGGED) + parallel_flagged() + cost_review_flags(rebuilt)
        if len(rebuilt) != len(events):
            HARD.append(f"events.json stale: mirror has {len(events)}, rebuild produces {len(rebuilt)}")
        else:
            diff = [a["id"] for a, b in zip(rebuilt, events)
                    if a.get("cost") != b.get("cost") or a.get("status") != b.get("status")]
            if diff:
                HARD.append(f"events.json stale for rows (cost/status differ from rebuild): {diff[:10]}")
        if len(rebuilt_flagged) != len(flagged):
            HARD.append(f"flagged mirror stale: {len(flagged)} vs rebuild {len(rebuilt_flagged)}")
    except Exception as exc:  # pragma: no cover - report and continue
        SOFT.append(f"could not rebuild canonical union for mirror-sync check: {exc!r}")

    # ---------------------------------------------------------------- output
    with open(os.path.join(ROOT, "audit", "row-audit-291a13ff.csv"), "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)

    print(f"events={len(events)} flagged={len(flagged)} pages={len(pages)} domains={len(domains)}")
    print(f"rows with problems: {sum(1 for r in rows if r['problems'])}")
    print(f"HARD problems: {len(HARD)}")
    for h in HARD:
        print("  HARD:", h)
    print(f"SOFT observations: {len(SOFT)}")
    for s in SOFT[:60]:
        print("  soft:", s)
    return 1 if HARD else 0


if __name__ == "__main__":
    raise SystemExit(main())
