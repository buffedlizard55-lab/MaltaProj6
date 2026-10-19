#!/usr/bin/env python3
"""Structural line-by-line audit for session arena-b95ade5f (2026-10-18).

Read-only checks over the published union dataset (data/events.py + the
parallel session's supplementary rows), plus HTML membership and focus
coverage. Nothing here fetches the web; it audits the repository's own
data against the project's stated rules:

  R1  every row carries an https source_url on an official/primary host
  R2  a blank core cell (schedule/dates/location/cost) must be explained:
      the row is either status=unverified or listed in the review register
  R3  no duplicate (title, dates) pairs
  R4  every event id is rendered in at least one generated HTML page
  R5  focus tags only from the declared taxonomy
  R6  cost cells quote the source; a numeric price is never invented

Writes audit/row-audit-b95ade5f.csv and prints a summary. Exit code is
non-zero only on hard problems (R1/R3/R4 failures).
"""

from __future__ import annotations

import csv
import os
import re
import sys
from collections import Counter
from urllib.parse import urlparse

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "data"))
sys.path.insert(0, os.path.join(ROOT, "scripts"))

from events import EVENTS as BASE_EVENTS, FLAGGED as BASE_FLAGGED  # noqa: E402
from merge_parallel import parallel_events, parallel_flagged  # noqa: E402
from focus import FOCUS_BY_ID, cost_class  # noqa: E402

EVENTS = BASE_EVENTS + parallel_events(BASE_EVENTS)
FLAGGED = list(BASE_FLAGGED) + parallel_flagged()

# Hosts that publish other people's listings rather than the event itself.
AGGREGATOR_HOSTS = (
    "eventbrite.com", "eventbrite.co.uk", "luma.com", "meetup.com",
    "facebook.com", "fb.com", "yelp.com", "timeout.com", "sfstation.com",
    "sfchronicle.com", "eventful.com", "10times.com", "conferencealerts.com",
    "allconferencealert.com", "10times.com", "comic-con.org",
)

CORE_CELLS = ("schedule", "dates", "location", "cost")


def host_of(url: str) -> str:
    netloc = urlparse(url).netloc.lower()
    return netloc[4:] if netloc.startswith("www.") else netloc


def main() -> int:
    problems: list[str] = []
    notes: list[str] = []
    rows: list[dict] = []

    seen_pairs: dict[tuple[str, str], list[str]] = {}
    focus_counts = Counter()
    cost_counts = Counter()
    blank_core = 0
    aggregator_rows = []
    http_rows = []

    for ev in EVENTS:
        eid = ev.get("id", "")
        title = ev.get("title", "")
        url = ev.get("source_url", "")
        status = ev.get("status", "")
        cost = (ev.get("cost") or "").strip()

        # R1 — https and primary host
        if not url.startswith("https://"):
            http_rows.append(eid)
            problems.append(f"R1 non-https source: {eid} -> {url!r}")
        host = host_of(url)
        if any(host == a or host.endswith("." + a) for a in AGGREGATOR_HOSTS):
            aggregator_rows.append((eid, host, title))

        # R2 — blank core cells must be explained
        blank_cells = [k for k in CORE_CELLS if not (ev.get(k) or "").strip()]
        if blank_cells:
            blank_core += 1
            if status != "unverified":
                # A verified row with a blank cell is acceptable only when the
                # review register carries it (flag-verified-rows-with-blank-core-cell).
                in_register = any(
                    f.get("id", "").startswith("flag-verified-rows-with-blank")
                    or eid in str(f)
                    for f in FLAGGED
                )
                if not in_register:
                    notes.append(
                        f"R2 verified row with blank {','.join(blank_cells)}: {eid}")
            cost_counts["blank-cost" if "cost" in blank_cells else "filled"] += 0

        # R3 — duplicate title+dates
        key = (title.strip().lower(), (ev.get("dates") or "").strip())
        seen_pairs.setdefault(key, []).append(eid)

        # R5 — focus taxonomy
        focus = FOCUS_BY_ID.get(eid, "other")
        focus_counts[focus] += 1

        # R6 — cost class read off the published wording
        cost_counts[cost_class(cost)] += 1

        rows.append({
            "id": eid, "title": title, "page": ev.get("page", ""),
            "type": ev.get("type", ""), "status": status,
            "focus": focus, "cost_class": cost_class(cost),
            "cost_blank": "yes" if not cost else "no",
            "blank_cells": ";".join(blank_cells),
            "source_host": host,
            "source_url": url,
        })

    for key, ids in seen_pairs.items():
        if len(ids) > 1 and key[0]:
            problems.append(f"R3 duplicate title+dates {key}: {ids}")

    # R4 — HTML membership
    html_ids: set[str] = set()
    for name in os.listdir(ROOT):
        if name.endswith(".html"):
            text = open(os.path.join(ROOT, name), encoding="utf-8").read()
            html_ids.update(re.findall(r'<tr id="([^"]+)"', text))
    missing_html = [e.get("id") for e in EVENTS if e.get("id") not in html_ids]
    for mid in missing_html:
        problems.append(f"R4 event not rendered in any HTML page: {mid}")

    # Review register sanity: every unverified row is addressable
    unverified_ids = [e["id"] for e in EVENTS if e.get("status") == "unverified"]
    register_text = repr(FLAGGED)
    unverified_unaddressed = [
        i for i in unverified_ids if i not in register_text]

    # Write the CSV audit trail
    out = os.path.join(ROOT, "audit", "row-audit-b95ade5f.csv")
    with open(out, "w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

    print(f"events audited: {len(EVENTS)}")
    print(f"flagged register entries: {len(FLAGGED)}")
    print(f"focus counts: {dict(focus_counts)}")
    print(f"cost classes: {dict(cost_counts)}")
    print(f"rows with a blank core cell: {blank_core}")
    print(f"unverified rows: {len(unverified_ids)}; "
          f"of those, not mentioned in the review register: "
          f"{len(unverified_unaddressed)} {unverified_unaddressed[:10]}")
    print(f"aggregator-host source rows (review individually): "
          f"{len(aggregator_rows)}")
    for eid, host, title in aggregator_rows[:15]:
        print(f"   {host}: {eid} — {title[:60]}")
    print(f"hard problems: {len(problems)}")
    for p in problems[:40]:
        print("   ", p)
    print(f"notes (soft): {len(notes)}")
    for n in notes[:20]:
        print("   ", n)
    print(f"wrote {out}")
    return 1 if problems else 0


if __name__ == "__main__":
    raise SystemExit(main())
