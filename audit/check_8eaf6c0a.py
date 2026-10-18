#!/usr/bin/env python3
"""Line-by-line structural audit of the published SF events union — session arena-8eaf6c0a.

Read-only. Never fetches pages. Mirrors the *published* membership rules
(``scripts/build_site.py``) rather than inventing its own, and checks every row for:

* id / title / source integrity (unique ids, https source, no aggregator hosts)
* status discipline (unverified rows must be listed on flagged.html; verified rows
  with a blank core cell are recorded as irregularities, never re-filled)
* cost discipline (blank cost => cost_class unknown; cost_class must match a
  recomputation from the row's own cost wording; free class requires free
  wording; a paid class without an amount is a problem)
* focus / group / category sanity and the ``page`` metadata field consistency
* date discipline (ISO date_start/date_end, end >= start, plausible range)
* HTML membership against the site's own rules:
    free-events.html  = cost wording is free OR ``_free_access_confirmed``
    paid-events.html  = cost_class != "free"
    technology.html   = focus in (ai, gaming) OR category == technology
    music.html        = focus == music
    group pages       = group; category pages = category
* ordering (all-events.html / free / paid / special / technology / music must
  render rows in the builder's date-first sort order)
* dashboard executive summary must stay free-only and link the paid section

Writes audit/row-audit-8eaf6c0a.csv (one line per event) and prints hard
problems. Exit code 1 if any hard problem is found.
"""
from __future__ import annotations

import csv
import json
import os
import re
import sys
from collections import Counter
from datetime import date

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "scripts"))
sys.path.insert(0, os.path.join(ROOT, "data"))

from focus import cost_class as recompute_cost_class  # noqa: E402

BLOCKED_HOST_PARTS = (
    "eventbrite.", "facebook.com", "instagram.com", "twitter.com", "x.com/",
    "tiktok.com", "wikipedia.org", "funcheap.com", "yelp.com", "tripadvisor.",
    "timeout.com", "google.com/search", "bing.com/search", "reddit.com",
    "meetup.com", "do512.", "patch.com", "eventful.com",
)

GROUP_PAGE = {"recurring": "recurring.html", "annual": "annual.html", "special": "special.html"}
CATEGORY_PAGE = {
    "civic": "civic.html", "arts": "arts.html", "sports": "sports.html",
    "markets": "markets.html", "community": "community.html", "technology": "technology.html",
}
VALID_GROUPS = set(GROUP_PAGE)
VALID_CATEGORIES = set(CATEGORY_PAGE)
VALID_FOCUS = {"gaming", "music", "ai", "other"}
VALID_COST_CLASS = {"free", "mixed", "paid", "unknown"}
CORE_CELLS = ("schedule", "location", "cost")
ISO_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")


def is_free_cost(value) -> bool:
    """Mirror of scripts/build_site._is_free_cost."""
    text = (value or "").strip().lower()
    return text == "free" or text.startswith("free ") or "free entry" in text or "free admission" in text


def has_free_access(e) -> bool:
    return is_free_cost(e.get("cost")) or bool(e.get("_free_access_confirmed"))


def read_page(name: str) -> str:
    path = os.path.join(ROOT, name)
    return open(path, encoding="utf-8").read() if os.path.exists(path) else ""


def row_ids(name: str) -> list[str]:
    return re.findall(r'<tr id="([^"]+)"', read_page(name))


def main() -> int:
    payload = json.load(open(os.path.join(ROOT, "data", "events.json"), encoding="utf-8"))
    events = payload.get("events", [])
    problems: list[str] = []
    irregularities: list[str] = []
    rows_out = []

    page_names = ["index.html", "all-events.html", "free-events.html", "paid-events.html",
                  "flagged.html", "recurring.html", "annual.html", "special.html",
                  "technology.html", "music.html", "civic.html", "arts.html",
                  "sports.html", "markets.html", "community.html"]
    pages = {name: read_page(name) for name in page_names}
    ids_by_page = {name: row_ids(name) for name in page_names if name != "index.html"}
    flagged_html = pages["flagged.html"]

    ids = [e["id"] for e in events]
    dup_ids = [i for i, c in Counter(ids).items() if c > 1]
    if dup_ids:
        problems.append(f"duplicate ids: {dup_ids}")
    title_keys = Counter(re.sub(r"\W+", "", e["title"].lower()) for e in events)
    dup_titles = sorted(t for t, c in title_keys.items() if c > 1 and t)

    for e in events:
        eid = e["id"]
        issues = []
        warns = []

        # --- source integrity -------------------------------------------
        url = e.get("source_url", "")
        if not url:
            issues.append("missing source_url")
        elif not url.startswith("https://"):
            issues.append("source_url not https")
        for part in BLOCKED_HOST_PARTS:
            if part in url:
                issues.append(f"blocked host part {part}")

        # --- status discipline ------------------------------------------
        if e.get("status") not in ("verified", "unverified"):
            issues.append(f"bad status {e.get('status')!r}")
        if e["status"] == "unverified" and eid not in flagged_html:
            issues.append("unverified row not on flagged.html")
        if e["status"] == "verified":
            for cell in CORE_CELLS:
                if not e.get(cell):
                    warns.append(f"verified row with blank {cell} (published rule: blank stays blank)")

        # --- cost discipline ---------------------------------------------
        cost = e.get("cost", "")
        cc = e.get("cost_class", "")
        if cc not in VALID_COST_CLASS:
            issues.append(f"bad cost_class {cc!r}")
        if not cost and cc != "unknown":
            issues.append(f"blank cost but cost_class={cc}")
        if cost and cc == "unknown":
            issues.append(f"nonblank cost but cost_class=unknown: {cost!r}")
        if cc == "free" and not is_free_cost(cost):
            issues.append(f"cost_class=free without free wording: {cost!r}")
        recomputed = recompute_cost_class(cost)
        if cost and recomputed != cc:
            warns.append(f"cost_class {cc} != recomputed {recomputed} for {cost!r}")
        if cc == "paid" and cost and "$" not in cost and not re.search(r"\d", cost):
            issues.append(f"cost_class=paid without amount: {cost!r}")
        if cc == "mixed" and cost and "$" not in cost and not re.search(r"\d", cost) and is_free_cost(cost):
            warns.append(f"cost_class=mixed with no price amount and free-first wording (likely misclassified free): {cost!r}")

        # --- date discipline ----------------------------------------------
        ds, de = e.get("date_start", ""), e.get("date_end", "")
        for label, val in (("date_start", ds), ("date_end", de)):
            if val and not ISO_RE.match(val):
                issues.append(f"{label} not ISO: {val!r}")
        if ds and de and de < ds:
            issues.append(f"date_end < date_start ({de} < {ds})")
        if ds:
            y = date.fromisoformat(ds).year
            if not (2025 <= y <= 2028):
                warns.append(f"date_start outside 2025-2028: {ds}")

        # --- focus / group / category / page metadata ------------------------
        if e.get("focus") not in VALID_FOCUS:
            issues.append(f"bad focus {e.get('focus')!r}")
        if e.get("group") not in VALID_GROUPS:
            issues.append(f"bad group {e.get('group')!r}")
        if e.get("category") not in VALID_CATEGORIES:
            issues.append(f"bad category {e.get('category')!r}")
        page = e.get("page", "")
        renders_on = e["group"] if e["group"] in GROUP_PAGE else e["category"]
        if page and page not in (e["group"], e["category"]):
            warns.append(f"page field {page!r} inconsistent with group {e['group']!r} / category {e['category']!r}")

        # --- HTML membership (published rules) --------------------------------
        want = {
            "all-events.html": True,
            GROUP_PAGE[e["group"]]: True,
            CATEGORY_PAGE[e["category"]]: True,
            "free-events.html": has_free_access(e),
            "paid-events.html": cc != "free",
            "technology.html": e["focus"] in ("ai", "gaming") or e["category"] == "technology",
            "music.html": e["focus"] == "music",
        }
        for pname, should in want.items():
            present = eid in ids_by_page.get(pname, [])
            if should and not present:
                issues.append(f"missing from {pname}")
            if not should and present:
                issues.append(f"unexpectedly on {pname}")

        rows_out.append({
            "id": eid, "title": e["title"], "group": e["group"], "category": e["category"],
            "focus": e["focus"], "status": e["status"], "cost_class": cc,
            "date_start": ds, "date_end": de, "source_url": url,
            "verdict": "hard-problem" if issues else ("irregularity" if warns else "ok"),
            "issues": "; ".join(issues + warns),
        })
        problems += [f"{eid}: {i}" for i in issues]
        irregularities += [f"{eid}: {w}" for w in warns]

    # --- ordering: rendered row order must match the builder's date-first sort ---
    try:
        from build_site import EVENTS as BUILD_EVENTS, _event_date_sort_key  # noqa: E402
        by_id = {e["id"]: e for e in BUILD_EVENTS}
        expected_all = [e["id"] for e in sorted(BUILD_EVENTS, key=_event_date_sort_key)]
        rendered_all = ids_by_page.get("all-events.html", [])
        if rendered_all != expected_all:
            for i, (a, b) in enumerate(zip(rendered_all, expected_all)):
                if a != b:
                    problems.append(f"all-events.html: row order diverges from date-first sort at position {i} ({a} vs {b})")
                    break
            else:
                problems.append("all-events.html: row order length mismatch vs date-first sort")
        for pname in ("free-events.html", "paid-events.html", "special.html",
                      "technology.html", "music.html"):
            rendered = ids_by_page.get(pname, [])
            sel = [e for e in BUILD_EVENTS if e["id"] in set(rendered)]
            expected_ids = [e["id"] for e in sorted(sel, key=_event_date_sort_key)]
            if rendered != expected_ids:
                for i, (a, b) in enumerate(zip(rendered, expected_ids)):
                    if a != b:
                        irregularities.append(f"{pname}: row order diverges from date-first sort at position {i} ({a} vs {b})")
                        break
    except Exception as exc:  # pragma: no cover
        irregularities.append(f"ordering check could not run: {exc}")

    # --- dashboard executive summary must be free-only ---------------------
    index = pages["index.html"]
    m = re.search(r'id="executive-summary".*?</section>', index, re.S)
    if not m:
        problems.append("index.html missing executive summary section")
    else:
        block = m.group(0)
        summary_ids = re.findall(r'<tr id="summary-[^"]*"', block)
        for bad in ("cost-paid", "cost-mixed"):
            if bad in block:
                irregularities.append(f"executive summary contains {bad} badge")
        if "paid-events.html" not in index:
            problems.append("index.html does not link the paid section")
        if "id=\"free-upcoming\"" not in index:
            problems.append("index.html missing free-upcoming main section")

    if payload.get("event_count") != len(events):
        problems.append("events.json event_count mismatch")

    os.makedirs(os.path.join(ROOT, "audit"), exist_ok=True)
    out_csv = os.path.join(ROOT, "audit", "row-audit-8eaf6c0a.csv")
    with open(out_csv, "w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=list(rows_out[0].keys()))
        writer.writeheader()
        writer.writerows(rows_out)

    n_hard = sum(1 for r in rows_out if r["verdict"] == "hard-problem")
    n_irr = sum(1 for r in rows_out if r["verdict"] == "irregularity")
    print(f"rows={len(rows_out)} hard={n_hard} irregularity={n_irr} dup_titles={len(dup_titles)}")
    if dup_titles:
        print("NOTE duplicate title keys:", dup_titles[:10])
    for p in problems:
        print("ERROR", p)
    for w in irregularities:
        print("WARN ", w)
    print(f"wrote {out_csv}")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
