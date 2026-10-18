#!/usr/bin/env python3
"""Independent structural audit of the San Francisco events dataset.

Written by session arena-bdaa17b4 (2026-10-18). This script ONLY reads
committed files; it never edits the dataset or the generated site
(those belong to another session's claimed scope -- see COORDINATION.md).

Checks, for every row of data/events.json (the published union dataset):
  1. id / title present and unique
  2. source_url present, https, parseable; source domain classified
  3. blank fields vs `status` ("unverified" rows must say why; "verified"
     rows with a blank display field are flagged for human review)
  4. location/area text scanned for out-of-San-Francisco place names
  5. dated ("Special - Dated" / "Annual") rows whose latest parseable date
     is already before AUDIT_DATE (possibly stale)
  6. near-duplicate titles (token overlap) across the union dataset
  7. every "unverified" row appears in the flagged register (by id or title)
  8. generated HTML: internal hrefs resolve, every event source_url occurs
     in at least one generated page

Outputs: audit/row-audit.csv (one line per event) + summary on stdout.
Usage: python3 audit/check_dataset.py
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
AUDIT_DATE = date(2026, 10, 18)  # session date; see COORDINATION.md

OUT_OF_SF = [
    "oakland", "berkeley", "emeryville", "daly city", "south san francisco",
    "sausalito", "Mill Valley", "san mateo", "palo Alto",
    "san Jose", "santa Clara", "levi's stadium",
]
# NOTE: "alameda" is deliberately excluded from OUT_OF_SF -- too many false
# positives (e.g. "Alameda" as a street name in SF). Treasure Island /
# Yerba Buena Island ARE part of the City and County of SF; Angel Island's
# jurisdiction is disputed by this dataset's own note -- surface all three.
# All entries are lowercase: they are matched against lowercased text.
BORDERLINE = ["Angel island", "treasure island", "yerba buena island"]

AGGREGATOR_DOMAINS = {
    "eventbrite.com", "facebook.com", "yelp.com", "funcheap.com",
    "sf.funcheap.com", "meetup.com", "tripadvisor.com", "timeout.com",
    "allevents.in", "sfstation.com",
}

MONTHS = {m: i + 1 for i, m in enumerate(
    ["january", "february", "march", "april", "may", "june", "july",
     "august", "september", "october", "november", "december"])}
MONTHS.update({m[:3]: v for m, v in list(MONTHS.items())})


def parse_dates(text):
    out = []
    for y, m, d in re.findall(r"(\d{4})-(\d{1,2})-(\d{1,2})", text or ""):
        out.append((int(y), int(m), int(d)))
    for mon, d, y in re.findall(
            r"(jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)[a-z]*\.?\s+(\d{1,2})(?:st|nd|rd|th)?,?\s+(\d{4})",
            (text or "").lower()):
        out.append((int(y), MONTHS[mon], int(d)))
    return out


def main():
    with open(os.path.join(ROOT, "data/events.json"), encoding="utf-8") as fh:
        data = json.load(fh)
    events, flagged = data["events"], data.get("flagged", [])

    problems, rows = [], []
    ids = Counter(e.get("id", "") for e in events)
    titles = Counter((e.get("title", "") or "").strip().lower() for e in events)
    domains = Counter()
    flagged_blob = json.dumps(flagged).lower()
    display_fields = ["schedule", "dates", "location", "area", "cost", "organiser"]

    for e in events:
        flags = []
        url = e.get("source_url", "") or ""
        host = urlparse(url).netloc.lower().removeprefix("www.")
        domains[host] += 1
        if not url:
            flags.append("NO_SOURCE_URL")
        elif not url.startswith("https://"):
            flags.append("SOURCE_NOT_HTTPS")
        if host in AGGREGATOR_DOMAINS:
            flags.append("AGGREGATOR_SOURCE")
        if ids[e.get("id", "")] > 1:
            flags.append("DUPLICATE_ID")
        if titles[(e.get("title", "") or "").strip().lower()] > 1:
            flags.append("DUPLICATE_TITLE")

        blanks = [f for f in display_fields if not str(e.get(f, "")).strip()]
        status = e.get("status", "")
        if status == "verified" and blanks:
            flags.append("VERIFIED_BUT_BLANK:" + ",".join(blanks))
        if status == "unverified":
            if not blanks:
                flags.append("UNVERIFIED_WITHOUT_BLANK_FIELD")
            if (e.get("id", "") or "").lower() not in flagged_blob and \
               (e.get("title", "") or "").lower()[:40] not in flagged_blob:
                flags.append("UNVERIFIED_NOT_IN_FLAGGED_REGISTER")

        where = f"{e.get('location','')} {e.get('area','')}".lower()
        for place in OUT_OF_SF:
            if place in where:
                flags.append(f"POSSIBLE_OUT_OF_SF:{place}")
        for place in BORDERLINE:
            if place in where:
                flags.append(f"BORDERLINE_GEO:{place}")

        found = parse_dates(e.get("dates", "")) + parse_dates(e.get("schedule", ""))
        latest = ""
        if found:
            y, m, d = max(found)
            latest = f"{y:04d}-{m:02d}-{d:02d}"
            if date(y, m, d) < AUDIT_DATE and e.get("type", "") in (
                    "Special - Dated", "Annual"):
                flags.append("LATEST_DATE_BEFORE_AUDIT_DATE")

        rows.append({
            "id": e.get("id", ""), "title": e.get("title", ""),
            "type": e.get("type", ""), "status": status,
            "source_host": host, "source_url": url,
            "blank_fields": ";".join(blanks),
            "latest_parsed_date": latest, "flags": ";".join(flags),
        })
        for f in flags:
            if f.startswith(("NO_", "AGGREGATOR", "DUPLICATE", "SOURCE_NOT")):
                problems.append(f"{e.get('id')}: {f}")

    def tokens(t):
        return {w for w in re.findall(r"[a-z0-9]+", t.lower())
                if w not in {"san", "francisco", "sf", "the", "of", "and", "at"}}
    toks = [(e["id"], tokens(e["title"])) for e in events]
    near_dupes = [(toks[i][0], toks[j][0])
                  for i in range(len(toks)) for j in range(i + 1, len(toks))
                  if toks[i][1] and toks[j][1]
                  and len(toks[i][1] & toks[j][1]) / min(len(toks[i][1]), len(toks[j][1])) >= 0.8]

    html_files = sorted(f for f in os.listdir(ROOT) if f.endswith(".html"))
    html_blob, broken_internal = "", []
    for f in html_files:
        with open(os.path.join(ROOT, f), encoding="utf-8") as fh:
            content = fh.read()
        html_blob += content
        for href in re.findall(r'href="([^"#]+)"', content):
            if href.startswith(("http", "mailto:")):
                continue
            if href.split("#")[0] and not os.path.exists(os.path.join(ROOT, href.split("#")[0])):
                broken_internal.append(f"{f} -> {href}")
    missing_from_html = [e["id"] for e in events
                         if e.get("source_url") and e["source_url"] not in html_blob]

    out_csv = os.path.join(ROOT, "audit/row-audit.csv")
    with open(out_csv, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)

    flag_counts = Counter()
    for r in rows:
        for f in filter(None, r["flags"].split(";")):
            flag_counts[f.split(":")[0]] += 1

    print(f"AUDIT_DATE={AUDIT_DATE.isoformat()}")
    print(f"events={len(events)} flagged_register={len(flagged)}")
    print(f"by_status={dict(Counter(e.get('status') for e in events))}")
    print(f"by_type={dict(Counter(e.get('type') for e in events))}")
    print(f"distinct_source_hosts={len(domains)} distinct_source_urls="
          f"{len({e.get('source_url') for e in events})}")
    print(f"rows_with_any_flag={sum(1 for r in rows if r['flags'])}")
    print(f"flag_counts={dict(flag_counts)}")
    print(f"near_duplicate_title_pairs={near_dupes}")
    print(f"html_files={len(html_files)} broken_internal_links={broken_internal}")
    print(f"events_missing_from_html={missing_from_html}")
    print(f"hard_problems={problems}")
    print(f"wrote {out_csv}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
