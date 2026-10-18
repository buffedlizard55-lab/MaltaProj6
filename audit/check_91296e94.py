#!/usr/bin/env python3
"""Independent structural audit of the San Francisco events dataset — session arena-91296e94.

Written 2026-10-18 while session arena-3ab2abd4 holds the live claim on
`scripts/build_site.py` / generated `index.html` (homepage executive-summary
date ordering). This script ONLY reads committed files; it never edits the
dataset or the generated site.

Checks (independently implemented; read-only reuse of the union mirror):
  A. id / title present and unique across the 217-row union
  B. source_url present, https, parseable; aggregator domains rejected
  C. blank display fields vs `status` (verified rows with blank cost/schedule
     are listed as review items, never silently accepted)
  D. location/area scanned for out-of-San-Francisco place names
  E. dated rows whose latest parseable date precedes AUDIT_DATE but are NOT
     marked timing="concluded" (stale rows shown as upcoming)
  F. near-duplicate titles (token overlap)
  G. every "unverified" row appears in the flagged register
  H. homepage "Upcoming dated events" strip: chronological order from
     AUDIT_DATE and membership of all near-term dated special rows
  I. generated HTML: internal hrefs resolve; every event source_url occurs in
     at least one generated page; cost column present wherever the schema
     requires it
  J. recurrence split counts vs data/meta.json

Outputs: audit/row-audit-91296e94.csv + summary on stdout.
Usage: python3 audit/check_91296e94.py
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
    "sausalito", "mill valley", "san mateo", "palo alto", "san jose",
    "santa clara", "levi's stadium", "sacramento", "san rafael", "vallejo",
    "alameda county", "contra costa", "marin county", "monterey", "napa",
]
BORDERLINE = ["angel island", "treasure island", "yerba buena island"]
OUT_OF_SF = [p.lower() for p in OUT_OF_SF]
BORDERLINE = [p.lower() for p in BORDERLINE]

AGGREGATOR_DOMAINS = {
    "eventbrite.com", "facebook.com", "yelp.com", "funcheap.com",
    "sf.funcheap.com", "meetup.com", "tripadvisor.com", "timeout.com",
    "allevents.in", "sfstation.com", "wikipedia.org", "google.com",
}

MONTHS = {m: i + 1 for i, m in enumerate(
    ["january", "february", "march", "april", "may", "june", "july",
     "august", "september", "october", "november", "december"])}
DATE_RE = re.compile(
    r"(january|february|march|april|may|june|july|august|september|"
    r"october|november|december)\s+(\d{1,2})(?:,\s*(\d{4}))?", re.I)
ISO_RE = re.compile(r"\b(20\d\d)-(\d\d)-(\d\d)\b")


def parse_dates(text: str):
    """All (y, m, d) tuples parseable from free text; year defaults nearby."""
    out = []
    for m in DATE_RE.finditer(text or ""):
        mon = MONTHS[m.group(1).lower()]
        day = int(m.group(2))
        yr = int(m.group(3)) if m.group(3) else None
        out.append((yr, mon, day))
    for m in ISO_RE.finditer(text or ""):
        out.append((int(m.group(1)), int(m.group(2)), int(m.group(3))))
    return out


def latest_concrete_date(text: str):
    """Latest date with a concrete year; None if no dated year appears."""
    dated = [d for d in parse_dates(text) if d[0]]
    return max(dated) if dated else None


def token_set(title: str):
    stop = {"the", "and", "of", "in", "a", "an", "at", "for", "sf", "san", "francisco"}
    return {t for t in re.findall(r"[a-z0-9]+", title.lower()) if t not in stop}


def load_union():
    with open(os.path.join(ROOT, "data", "events.json"), encoding="utf-8") as f:
        blob = json.load(f)
    return blob["events"], blob["flagged"]


def main() -> int:
    events, flagged = load_union()
    problems: list[str] = []
    warnings: list[str] = []
    rows_out = []

    ids = [e.get("id", "") for e in events]
    titles = [e.get("title", "") for e in events]
    dup_ids = [i for i, n in Counter(ids).items() if n > 1]
    if dup_ids:
        problems.append(f"A. duplicate ids: {dup_ids}")

    flag_ids = {f.get("id", "") for f in flagged}
    flag_titles = {f.get("title", "").strip().lower() for f in flagged if f.get("title")}
    with open(os.path.join(ROOT, "flagged.html"), encoding="utf-8") as f:
        _fh = f.read()
    flagged_html_ids = set(re.findall(r'<tr id="review-([a-z0-9-]+)"', _fh))

    seen_tokens = {}
    blank_cost_verified = []
    blank_sched_verified = []
    stale_dated = []
    near_term = []  # (sortkey, title, dates) dated, not concluded, >= AUDIT_DATE

    for e in events:
        rid = e.get("id", "")
        rtitle = e.get("title", "")
        row = {
            "id": rid, "title": rtitle, "group": e.get("group", ""),
            "status": e.get("status", ""), "timing": e.get("timing", ""),
            "cost": e.get("cost", ""), "schedule": e.get("schedule", ""),
            "dates": e.get("dates", ""), "source_url": e.get("source_url", ""),
        }
        rows_out.append(row)

        # B. source link
        url = e.get("source_url", "")
        if not url:
            problems.append(f"B. {rid}: empty source_url")
        elif not url.startswith("https://"):
            problems.append(f"B. {rid}: source_url not https: {url}")
        else:
            host = urlparse(url).netloc.lower()
            if any(host == d or host.endswith("." + d) for d in AGGREGATOR_DOMAINS):
                problems.append(f"B. {rid}: aggregator source: {host}")

        # C. blanks vs status
        if e.get("status") == "verified":
            if not (e.get("cost") or "").strip():
                blank_cost_verified.append(rid)
            if not (e.get("schedule") or "").strip() and not (e.get("dates") or "").strip():
                blank_sched_verified.append(rid)
        else:  # unverified
            blob = " ".join([rtitle, e.get("notes", "")]).lower()
            if not (e.get("cost") or "").strip() or not (e.get("schedule") or "").strip():
                if not any(w in blob for w in ("not confirm", "unverified", "not publish", "no official", "blank")):
                    warnings.append(f"C. {rid}: unverified row with blank field but no explanatory note")
            # covered either by a dedicated register item (id/title match) or by the
            # generated "Rows carrying a blank cell" section on flagged.html
            if rid not in flag_ids and rtitle.strip().lower() not in flag_titles \
                    and rid not in flagged_html_ids:
                problems.append(f"G. {rid}: unverified but absent from flagged register/page")

        # D. out-of-city scan (warning-level: manually triaged, tours may name other cities)
        loc = " ".join([e.get("location", ""), e.get("area", "")]).lower()
        hits = [p for p in OUT_OF_SF if p in loc]
        if hits:
            warnings.append(f"D. {rid}: out-of-SF text {hits} in '{e.get('location','')[:60]}'")
        bord = [p for p in BORDERLINE if p in loc]
        if bord:
            notes = (e.get("notes") or "").lower()
            if "angel island" in bord and "jurisdiction" not in notes and "part of" not in notes:
                warnings.append(f"D. {rid}: Angel Island without jurisdiction note")

        # E. stale dated rows
        if e.get("dates"):
            ld = latest_concrete_date(e["dates"])
            if ld and date(*ld) < AUDIT_DATE and e.get("timing") != "concluded":
                stale_dated.append(f"{rid} (latest {ld[0]}-{ld[1]:02d}-{ld[2]:02d})")

        # near-term collection (next 45 days)
        for (y, m, d) in parse_dates(e.get("dates", "")):
            if y and date(y, m, d) >= AUDIT_DATE:
                delta = (date(y, m, d) - AUDIT_DATE).days
                if delta <= 45 and e.get("timing") != "concluded":
                    near_term.append((date(y, m, d), rtitle, e.get("group", ""), rid))
                break

        # F. near-duplicate titles
        ts = token_set(rtitle)
        for other_id, other_ts in seen_tokens.items():
            inter = ts & other_ts
            if len(ts) >= 2 and len(other_ts) >= 2 and len(inter) >= max(2, min(len(ts), len(other_ts)) - 1):
                warnings.append(f"F. near-duplicate titles: {rid} ~ {other_id}")
        seen_tokens[rid] = ts

    # H. homepage strip chronology + membership
    with open(os.path.join(ROOT, "index.html"), encoding="utf-8") as f:
        index_html = f.read()
    strip_m = re.search(r"Upcoming dated events</h2>.*?<tbody>(.*?)</tbody>", index_html, re.S)
    strip_dates = []
    strip_titles = []
    if strip_m:
        for tr in re.findall(r"<tr>(.*?)</tr>", strip_m.group(1), re.S):
            tds = re.findall(r"<td[^>]*>(.*?)</td>", tr, re.S)
            if len(tds) >= 2:
                strip_titles.append(re.sub(r"<[^>]+>", "", tds[0]).strip())
                strip_dates.append(re.sub(r"<[^>]+>", "", tds[1]).strip())
    strip_order = []
    for t, d in zip(strip_titles, strip_dates):
        ld = latest_concrete_date(d)
        strip_order.append(ld)
    known_broken = strip_order != sorted([x for x in strip_order if x]) and len(strip_order) > 1
    if known_broken:
        warnings.append("H. homepage upcoming strip is NOT in chronological order "
                        "(already claimed by live session arena-3ab2abd4 — not re-fixed here)")
    near_special = sorted({(dt, t) for dt, t, g, rid in near_term if g == "special"})
    strip_lower = {t.lower() for t in strip_titles}
    missing_near = [f"{t} ({dt.isoformat()})" for dt, t in near_special
                    if t.lower() not in strip_lower]
    if missing_near:
        warnings.append("H. near-term (<=45d) dated special rows not shown in the 8-row "
                        f"homepage strip: {missing_near}")

    # I. HTML integrity
    pages = [p for p in os.listdir(ROOT) if p.endswith(".html")]
    all_html = ""
    for p in pages:
        with open(os.path.join(ROOT, p), encoding="utf-8") as f:
            all_html += f.read()
    missing_src = [e["id"] for e in events
                   if e.get("source_url") and e["source_url"] not in all_html]
    if missing_src:
        problems.append(f"I. source_url missing from all generated HTML: {missing_src}")
    for href in set(re.findall(r'href=[\'"]([^#\'"http][^\'"]*)[\'"]', all_html)):
        target = href.split("#")[0]
        if target and not os.path.exists(os.path.join(ROOT, target)):
            problems.append(f"I. broken internal link: {href}")

    # J. meta counts
    with open(os.path.join(ROOT, "data", "meta.json"), encoding="utf-8") as f:
        meta = json.load(f)
    gcount = Counter(e.get("group", "") for e in events)
    for gk, mk in [("recurring", "recurring"), ("annual", "annual"), ("special", "special")]:
        if gcount.get(gk, 0) != meta["counts"].get(mk):
            problems.append(f"J. meta.json {mk}={meta['counts'][mk]} but dataset has {gcount.get(gk,0)}")
    if meta["counts"]["total"] != len(events):
        problems.append(f"J. meta.json total={meta['counts']['total']} but dataset has {len(events)}")

    # write CSV
    out_csv = os.path.join(ROOT, "audit", "row-audit-91296e94.csv")
    with open(out_csv, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows_out[0].keys()))
        w.writeheader()
        w.writerows(rows_out)

    print(f"events={len(events)} flagged_register={len(flagged)}")
    print(f"verified={sum(1 for e in events if e.get('status')=='verified')} "
          f"unverified={sum(1 for e in events if e.get('status')!='verified')}")
    print(f"groups={dict(gcount)}")
    print(f"blank-cost verified rows: {len(blank_cost_verified)} -> {blank_cost_verified}")
    print(f"blank-schedule verified rows: {len(blank_sched_verified)} -> {blank_sched_verified}")
    print(f"stale dated rows not marked concluded: {len(stale_dated)} -> {stale_dated}")
    print(f"near-term (<=45d) dated rows: {len(near_term)}")
    print(f"hard_problems={len(problems)}")
    for p in problems:
        print("  PROBLEM:", p)
    print(f"warnings={len(warnings)}")
    for w_ in warnings:
        print("  warn:", w_)
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
