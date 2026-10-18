#!/usr/bin/env python3
"""Structural row audit for session ``arena-61a46409`` (2026-10-18).

Read-only over the published union dataset. It writes
``audit/row-audit-61a46409.csv`` (one line per catalogue row) and prints a
summary. It does not fetch pages: source *contents* were checked by hand and
are recorded in ``audit/AUDIT-2026-10-18-61a46409.md``.

Usage::

    python3 audit/check_61a46409.py
"""
from __future__ import annotations

import csv
import os
import sys
from collections import Counter
from urllib.parse import urlsplit

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "data"))
sys.path.insert(0, os.path.join(ROOT, "scripts"))

from events import EVENTS as BASE_EVENTS, FLAGGED as BASE_FLAGGED, assign_views  # noqa: E402
from merge_parallel import parallel_events, parallel_flagged  # noqa: E402
from build_site import attach_focus, _next_confirmed_date  # noqa: E402
from focus import event_dates  # noqa: E402

BLOCKED_HOST_PARTS = (
    "eventbrite.", "facebook.com", "instagram.com", "twitter.com", "tiktok.com",
    "wikipedia.org", "funcheap.com", "yelp.com", "tripadvisor.", "timeout.com",
    "google.com/search", "bing.com/search",
)
NEW_IDS = {
    "rec-sfpl-mix-gaming", "rec-sfpl-gaming-citywide", "rec-sfpl-mix-music-studios",
    "rec-sfpl-dance-music", "ann-sfpl-tech-week", "spc-ai-engineer-code-2026",
    "spc-ai-week-sf-2026", "spc-current-sf-2026", "spc-microsoft-ignite-2026",
    "spc-cloudflare-connect-2026",
}


def main() -> int:
    rows = attach_focus(assign_views(BASE_EVENTS + parallel_events(BASE_EVENTS)))
    flagged = list(BASE_FLAGGED) + parallel_flagged()

    findings: Counter = Counter()
    with open(os.path.join(ROOT, "audit", "row-audit-61a46409.csv"), "w",
              encoding="utf-8", newline="") as fh:
        writer = csv.writer(fh)
        writer.writerow([
            "id", "title", "focus", "cost_class", "cost", "status", "timing",
            "date_start", "date_end", "date_source", "next_confirmed",
            "source_domain", "notes_len", "findings",
        ])
        for e in rows:
            row_findings = []
            url = e.get("source_url", "")
            parts = urlsplit(url)
            if parts.scheme != "https" or not parts.netloc:
                row_findings.append("source-not-https")
            if any(h in url.lower() for h in BLOCKED_HOST_PARTS):
                row_findings.append("source-blocked-host")
            for extra in e.get("additional_sources", []):
                xurl = extra.get("url", "")
                xparts = urlsplit(xurl)
                if xparts.scheme != "https" or not xparts.netloc:
                    row_findings.append("supporting-source-not-https")
            if not e.get("title", "").strip():
                row_findings.append("empty-title")
            if e.get("status") not in ("verified", "unverified"):
                row_findings.append("bad-status")
            # A blank "dates" cell is normal for a recurring programme, so only
            # the core cells (schedule / location / cost) are treated as a
            # verified-but-incomplete row worth surfacing.
            blanks = [k for k in ("schedule", "location", "cost") if not e.get(k)]
            if blanks and e.get("status") == "verified":
                row_findings.append("verified-with-blank-core:" + "|".join(blanks))
            if not e.get("dates"):
                row_findings.append("no-confirmed-date")
            if e.get("status") == "unverified":
                row_findings.append("unverified-row")
            start, end, src = event_dates(e)
            if (start, end) != (e.get("date_start"), e.get("date_end")):
                row_findings.append("date-parse-drift")
            nxt = _next_confirmed_date(e)
            if e.get("id") in NEW_IDS:
                row_findings.append("new-this-session")
            for f in row_findings:
                findings[f.split(":")[0]] += 1
            writer.writerow([
                e["id"], e.get("title", ""), e.get("focus", "other"),
                e.get("cost_class", "unknown"), e.get("cost", ""), e.get("status", ""),
                e.get("timing", "current"), e.get("date_start", ""), e.get("date_end", ""),
                src, nxt.isoformat() if nxt else "", parts.netloc,
                len(e.get("notes", "")), ";".join(row_findings),
            ])

    no_source = [r["id"] for r in rows if urlsplit(r.get("source_url", "")).scheme != "https"]
    print(f"rows audited           : {len(rows)}")
    print(f"review items           : {len(flagged)}")
    print(f"rows without https src : {len(no_source)}")
    print(f"new rows this session  : {sum(1 for r in rows if r['id'] in NEW_IDS)}")
    print("verified w/ blank core :", findings.get("verified-with-blank-core", 0))
    print("rows with no date      :", findings.get("no-confirmed-date", 0))
    print("findings               :", dict(sorted(findings.items())))
    hard = [k for k in findings if k in (
        "source-not-https", "source-blocked-host", "supporting-source-not-https",
        "empty-title", "bad-status", "date-parse-drift")]
    print("hard problems          :", hard or "none")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
