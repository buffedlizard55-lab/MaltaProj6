#!/usr/bin/env python3
"""Independent line-by-line structural audit for arena-fc3438db (2026-10-18).

Checks every published row in data/events.json and every review item in the
flagged register, then scans every generated HTML page:

  1. source_url present, https, not a known aggregator/secondary host
  2. status/blanks consistency (unverified rows must explain themselves)
  3. cost column coverage (blank cost only on rows whose status explains it)
  4. duplicate ids / exact-duplicate titles
  5. every event appears in the HTML tables, with its source link
  6. upcoming dated rows on index.html are present and date-sortable
  7. every HTML data row keeps a source anchor

Outputs a short report to stdout. Exit code 1 only on hard problems.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# Secondary / aggregator hosts that must never be a row's primary source.
AGGREGATOR_HOSTS = (
    "wikipedia.org", "tripadvisor.", "yelp.", "eventbrite.", "facebook.com",
    "instagram.com", "timeout.com", "sftravel.com", "do411.", "funcheap.",
    "allevents.in", "meetup.com", "reddit.com", "flickr.com", "youtube.com",
    "linkedin.com", "x.com", "twitter.com", "tiktok.com", "pinterest.",
    "google.com", "patch.com", "kqed.org", "sfchronicle.com", "sfgate.com",
)

MONTHS = {m: i for i, m in enumerate(
    ["january", "february", "march", "april", "may", "june", "july",
     "august", "september", "october", "november", "december"], start=1)}


def parse_leading_date(text: str):
    """Return (y, m, d) for the first 'Month D, YYYY' pattern, else None."""
    m = re.search(r"\b(january|february|march|april|may|june|july|august|"
                  r"september|october|november|december)\s+(\d{1,2})(?:st|nd|rd|th)?,\s*(\d{4})", text.lower())
    if not m:
        return None
    return (int(m.group(3)), MONTHS[m.group(1)], int(m.group(2)))


def main() -> int:
    hard: list[str] = []
    soft: list[str] = []

    data = json.loads((ROOT / "data" / "events.json").read_text())
    events = data["events"]
    flagged = data["flagged"]

    ids = [e["id"] for e in events]
    if len(ids) != len(set(ids)):
        hard.append(f"duplicate ids: {[i for i in ids if ids.count(i) > 1]}")

    titles = [e["title"].strip().lower() for e in events]
    dup_titles = sorted({t for t in titles if titles.count(t) > 1})
    if dup_titles:
        soft.append(f"exact-duplicate titles: {dup_titles}")

    n_no_cost = 0
    for e in events:
        eid = e["id"]
        url = (e.get("source_url") or "").strip()
        if not url:
            hard.append(f"{eid}: missing source_url")
        elif not url.startswith("https://"):
            hard.append(f"{eid}: source_url not https: {url}")
        host = url.split("/")[2] if "//" in url else ""
        if any(bad in host for bad in AGGREGATOR_HOSTS):
            hard.append(f"{eid}: aggregator/secondary host as source: {host}")
        if e.get("status") not in ("verified", "unverified"):
            hard.append(f"{eid}: bad status {e.get('status')!r}")
        if e.get("status") == "unverified" and not (e.get("notes") or "").strip():
            hard.append(f"{eid}: unverified row without explanatory note")
        cost = (e.get("cost") or "").strip()
        if not cost:
            n_no_cost += 1
            if e.get("status") == "verified" and not (e.get("notes") or "").strip():
                soft.append(f"{eid}: blank cost on verified row without note")
        if not (e.get("title") or "").strip():
            hard.append(f"{eid}: empty title")

    # Flagged register
    flag_ids = [f.get("id", "") for f in flagged]
    if len(flag_ids) != len(set(flag_ids)):
        hard.append("duplicate flagged ids")
    for f in flagged:
        if not (f.get("evidence") or f.get("source_url") or f.get("link") or ""):
            # some register rows use 'evidence_url'
            if not (f.get("evidence_url") or ""):
                soft.append(f"flag {f.get('id')}: no evidence link field found")

    # HTML presence: every event id must appear as an anchor somewhere
    html_files = sorted(ROOT.glob("*.html"))
    all_html = {p.name: p.read_text() for p in html_files}
    joined = "\n".join(all_html.values())
    missing = [e["id"] for e in events if e["id"] not in joined]
    if missing:
        hard.append(f"events missing from HTML: {missing}")

    # Every <tr> data row in category tables must contain an https link
    rows_missing_links = 0
    for name, text in all_html.items():
        for m in re.finditer(r"<tr[^>]*>(.*?)</tr>", text, re.S):
            row = m.group(1)
            if "<th" in row or "<td" not in row:
                continue
            if "colspan" in row.split(">", 1)[0] or 'class="row-note"' in row:
                continue  # analyst-note continuation row; the data row above carries the link
            if "https://" not in row:
                rows_missing_links += 1
                soft.append(f"{name}: table row without https link: {row[:80]!r}")
    if rows_missing_links:
        soft.append(f"total table rows without https link: {rows_missing_links}")

    # index.html upcoming section: collect (title, date-text) pairs in order
    index = all_html.get("index.html", "")
    upcoming = re.findall(
        r"<tr><td>(.*?)</td><td>(.*?)</td><td>(.*?)</td><td>", index, re.S)
    order = []
    for title, dates, _where in upcoming:
        d = parse_leading_date(dates) or parse_leading_date(title)
        order.append((title.strip()[:48], d))
    if order:
        seq = [d for _t, d in order if d]
        sorted_seq = sorted(seq)
        if seq != sorted_seq:
            soft.append("index.html 'Upcoming dated events' is NOT sorted soonest-first: "
                        + " -> ".join(f"{t}{d}" for t, d in order))

    print(f"events={len(events)} flagged={len(flagged)} html_files={len(html_files)} "
          f"rows_blank_cost={n_no_cost}")
    print(f"hard_problems={len(hard)} soft_findings={len(soft)}")
    for h in hard:
        print("HARD:", h)
    for s in soft[:40]:
        print("soft:", s)
    return 1 if hard else 0


if __name__ == "__main__":
    sys.exit(main())
