#!/usr/bin/env python3
"""Structural checks for the arena-db227e31 free-upcoming pass.

Does not fetch pages. Confirms the new rows exist, carry HTTPS sources, and
that the homepage executive summary is limited to free-cost rows.
"""
from __future__ import annotations

import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "scripts"))
sys.path.insert(0, os.path.join(ROOT, "data"))

from build_site import EVENTS, executive_summary_rows, _is_explicitly_free  # noqa: E402
from datetime import date

REQUIRED = [
    "spc-illuminate-reggae-2026-10-18",
    "spc-illuminate-ccs-2026-10-20",
    "spc-illuminate-midweek-2026-10-21",
    "spc-illuminate-happyhour-2026-10-23",
    "spc-illuminate-baybeats-2026-10-24",
    "spc-illuminate-reggae-2026-10-25",
    "spc-illuminate-halloween-2026-10-31",
    "spc-family-summit-d1-2026-10-22",
    "spc-family-summit-d11-2026-10-29",
    "spc-family-summit-d2-2026-11-07",
    "spc-family-summit-d4-2026-11-14",
    "spc-family-summit-d3-2026-12-12",
    "spc-sunday-streets-excelsior-2026",
]

def main() -> int:
    problems = []
    by_id = {e["id"]: e for e in EVENTS}
    for event_id in REQUIRED:
        row = by_id.get(event_id)
        if not row:
            problems.append(f"missing {event_id}")
            continue
        url = row.get("source_url", "")
        if not url.startswith("https://"):
            problems.append(f"{event_id}: source is not https")
        if event_id != "spc-sunday-streets-excelsior-2026" and row.get("cost") != "Free":
            problems.append(f"{event_id}: expected cost Free, got {row.get('cost')!r}")
        if event_id == "spc-sunday-streets-excelsior-2026" and row.get("cost"):
            problems.append("Sunday Streets dated row has a cost; official pages did not state one")
    streets = by_id.get("rec-sunday-streets", {})
    if streets.get("cost"):
        problems.append("rec-sunday-streets cost was not blanked")
    today = date(2026, 10, 18)
    summary = executive_summary_rows(EVENTS, today)
    for row in summary:
        if not _is_explicitly_free(row):
            problems.append(f"summary includes non-free row {row['id']}")
    index = open(os.path.join(ROOT, "index.html"), encoding="utf-8").read()
    if 'id="executive-summary"' not in index or 'id="free-upcoming"' not in index:
        problems.append("homepage is missing the free summary or free main section")
    if "paid-events.html" not in index:
        problems.append("homepage does not link the paid section")
    payload = json.load(open(os.path.join(ROOT, "data", "events.json"), encoding="utf-8"))
    if payload.get("event_count") != len(payload.get("events", [])):
        problems.append("events.json count mismatch")
    print(f"events={len(EVENTS)} summary_free={len(summary)} problems={len(problems)}")
    for item in problems:
        print("ERROR", item)
    return 1 if problems else 0

if __name__ == "__main__":
    sys.exit(main())
