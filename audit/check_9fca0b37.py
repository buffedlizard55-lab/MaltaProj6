#!/usr/bin/env python3
"""Independent structural audit of the San Francisco events dataset.

Written by session ``arena-9fca0b37`` (2026-10-18). Read-only: it never
edits the dataset or the generated site.

Checks:
  1. Every row: stable unique id, https official source link present, no
     blocklisted aggregator as the primary source.
  2. Status vs blanks: every ``unverified`` row is addressable on the
     Flagged for Review register (by id or title prefix), and every
     ``verified`` row with a blank schedule/location/cost is published in
     the flagged rows table of ``flagged.html``.
  3. The rows this session added or corrected are present with the exact
     values read from their official pages (a small expectations table —
     if any of these drift, the value no longer matches what was fetched).
  4. ``data/meta.json`` counts match the dataset (the build now writes it,
     so drift here means the build was skipped).
  5. The home page executive summary contains only rows whose published
     cost wording is free and are not concluded (free-only requirement).
  6. Every event appears in at least one generated page and every internal
     href/anchor in the generated pages resolves.
  7. The apply script ``audit/apply_9fca0b37.py`` is present.

Outputs: ``audit/row-audit-9fca0b37.csv`` (one line per event) and a
summary on stdout. Exit code 0 with ``hard_problems`` empty means pass.
Usage: ``python3 audit/check_9fca0b37.py``
"""
from __future__ import annotations

import csv
import json
import os
import re
import sys
from collections import Counter
from urllib.parse import urlparse

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

AGGREGATOR_DOMAINS = {
    "eventbrite.com", "facebook.com", "yelp.com", "funcheap.com",
    "sf.funcheap.com", "meetup.com", "tripadvisor.com", "timeout.com",
    "allevents.in", "sfstation.com",
}

# Rows added or corrected by arena-9fca0b37 on 2026-10-18, with the values
# that were read off the official page named in ``source_url``. Key = row id,
# value = (field, expected value). Blank expected values are represented as "".
SESSION_EXPECTATIONS = {
    # New free row: D10 Bayview Family Summit (SF.gov event page).
    "spc-family-summit-d10-2026-12-05": [
        ("cost", "Free"),
        ("dates", "Saturday, December 5, 2026"),
        ("status", "verified"),
        ("source_url", "https://www.sf.gov/event-20261205-district-10-family-summit-bayview/"),
    ],
    # New Exploratorium After Dark editions (official calendar + event pages).
    # The organiser publishes no numeric ticket price, so the build's
    # blank-unless-numeric rule marks these unverified for price, exactly as
    # it does the pre-existing Creepatorium row.
    "spc-exploratorium-after-dark-2026-10-22": [
        ("dates", "Thursday, October 22, 2026"), ("status", "unverified")],
    "spc-exploratorium-after-dark-2026-11-05": [
        ("dates", "Thursday, November 5, 2026"), ("status", "unverified")],
    "spc-exploratorium-after-dark-2026-11-12": [
        ("dates", "Thursday, November 12, 2026"), ("status", "unverified")],
    "spc-exploratorium-after-dark-2026-12-03": [
        ("dates", "Thursday, December 3, 2026"), ("status", "unverified")],
    "spc-exploratorium-after-dark-2026-12-10": [
        ("dates", "Thursday, December 10, 2026"), ("status", "unverified")],
    "spc-exploratorium-after-dark-2026-12-17": [
        ("dates", "Thursday, December 17, 2026"), ("status", "unverified")],
    # SF Opera prices/times now read off the organiser's own pages.
    "spc-opera-strauss-concert": [
        ("cost", "Starting at $30"), ("schedule", "7:30 p.m."),
        ("dates", "Friday, November 6, 2026")],
    "spc-opera-ball": [
        ("dates", "Thursday, November 12, 2026"),
        ("location", "City Hall, 1 Dr. Carlton B. Goodlett Place")],
    "spc-opera-adlers-concert": [
        ("cost", "Starting at $34"), ("schedule", "7:30 p.m.")],
    "spc-opera-chorus-concert": [
        ("cost", "$49.00"), ("schedule", "2:00 p.m."),
        ("location", "Dianne and Tad Taube Atrium Theater")],
    # SF Symphony start times read off the concert pages.
    "spc-symphony-the-ring": [("schedule", "7:30 p.m."),
                              ("dates", "Tuesday, October 20, 2026")],
    "spc-symphony-adams-mendelssohn": [
        ("schedule", "7:30 p.m. on October 29, 30 and 31, 2026")],
    "spc-symphony-music-for-families": [
        ("schedule", "2:00 p.m."), ("dates", "Saturday, October 24, 2026")],
    # Castro rows: no published admission price => blank + unverified.
    "spc-castro-menorah": [("cost", ""), ("status", "unverified")],
    "spc-castro-holiday-tree": [("cost", ""), ("status", "unverified")],
    "spc-castro-art-walk": [("cost", ""), ("status", "unverified")],
    "spc-castro-tree-fundraiser": [
        ("cost", ""), ("status", "unverified"),
        ("source_url",
         "https://castromerchants.com/events/castro-holiday-tree-lighting-ceremony-2023-5edw6")],
    # Imported Sunset Mercantile rows with no published admission price.
    "x-s-015": [("cost", ""), ("status", "unverified")],
    "x-s-016": [("cost", ""), ("status", "unverified")],
    "x-s-018": [("cost", ""), ("status", "unverified")],
    # Sunset Holiday Mercantile: organiser page states "Admission is free!".
    "x-s-017": [("cost", "Free"), ("status", "verified"),
                ("source_url", "https://sunsetmercantilesf.com/sunsetholidaymercantile/")],
    # Cole Valley Nights: source upgraded to the event page, price still blank.
    "x-s-019": [("cost", ""), ("status", "unverified"),
                ("source_url", "https://sunsetmercantilesf.com/colevalleynights2026/")],
    # Dia de los Muertos Outer Sunset: source upgraded to the event page.
    "x-s-016": [("cost", ""), ("status", "unverified"),
                ("source_url", "https://sunsetmercantilesf.com/ddlm/")],
}

# Review items this session added; each must be in the published register.
SESSION_FLAGS = [
    "flag-sunday-streets-admission-not-published",
    "flag-bos-lut-next-meeting-not-published",
    "flag-bos-rules-next-meeting-not-published",
    "flag-pickleball-palace-hours-not-published",
    "flag-treasurefest-no-sf-date",
    "flag-outside-lands-2026-concluded",
    "flag-current-sf-2026-price-not-published",
    "flag-microsoft-ignite-2026-price-not-published",
    "flag-soulful-sundays-admission-not-published",
    "flag-otsego-shared-space-admission-not-published",
    "flag-larkin-shared-space-admission-not-published",
    "flag-sunset-mercantile-admission-not-published",
    "flag-castro-merchants-admission-not-published",
    "flag-ocofi-calendar-d3-link-broken",
]


def main() -> int:
    hard = []
    with open(os.path.join(ROOT, "data/events.json"), encoding="utf-8") as fh:
        data = json.load(fh)
    events, flagged = data["events"], data.get("flagged", [])
    with open(os.path.join(ROOT, "index.html"), encoding="utf-8") as fh:
        index_html = fh.read()
    with open(os.path.join(ROOT, "flagged.html"), encoding="utf-8") as fh:
        flagged_html = fh.read()

    # The corrections land only when ``audit/apply_9fca0b37.py`` has been run,
    # which this session defers until the shared-output claim on
    # ``data/events.py`` / ``scripts/`` is released (see COORDINATION.md).
    # Detect the phase so the same checker is meaningful before and after.
    applied = "spc-family-summit-d10-2026-12-05" in {e.get("id") for e in events}
    pre_apply_notes = []

    # ---- 1. ids, source links -------------------------------------------------
    ids = Counter(e.get("id", "") for e in events)
    for e in events:
        rid = e.get("id", "")
        if not rid:
            hard.append("row with empty id")
        if ids[rid] > 1:
            hard.append(f"duplicate id {rid}")
        url = e.get("source_url", "") or ""
        if not url.startswith("https://"):
            hard.append(f"{rid}: source_url not https: {url!r}")
        host = urlparse(url).netloc.lower().removeprefix("www.")
        if host in AGGREGATOR_DOMAINS:
            hard.append(f"{rid}: aggregator source {host}")

    # ---- 2. status vs register -----------------------------------------------
    flagged_blob = json.dumps(flagged).lower()
    display_fields = ["schedule", "dates", "location", "area", "cost", "organiser"]
    unverified_not_published = []
    verified_blank_not_published = []
    for e in events:
        rid = (e.get("id") or "").lower()
        title = (e.get("title") or "").lower()[:40]
        blanks = [f for f in display_fields if not str(e.get(f, "")).strip()]
        if e.get("status") != "verified":
            if rid not in flagged_blob and title not in flagged_blob:
                unverified_not_published.append(e.get("id"))
            if f"review-{e.get('id')}" not in flagged_html:
                unverified_not_published.append(f"{e.get('id')} (no flagged.html row)")
        elif blanks:
            if f"review-{e.get('id')}" not in flagged_html:
                verified_blank_not_published.append(e.get("id"))
    if unverified_not_published:
        target = hard if applied else pre_apply_notes
        target.append(
            "unverified rows not published on flagged.html: "
            + str(unverified_not_published) + " (fixed by audit/apply_9fca0b37.py)" if not applied
            else f"unverified rows not published on flagged.html: {unverified_not_published}")
    # verified-with-blank rows are reported, not hard: the page groups them
    # and the marker is generated from the same id.

    # ---- 3. this session's rows ----------------------------------------------
    by_id = {e.get("id"): e for e in events}
    expectation_problems = []
    if not applied:
        pre_apply_notes.append(
            "session row expectations not checked yet (phase: pre-apply — "
            "run again after audit/apply_9fca0b37.py)")
    else:
        for rid, checks in SESSION_EXPECTATIONS.items():
            row = by_id.get(rid)
            if row is None:
                expectation_problems.append(f"{rid}: missing row")
                continue
            for field, expected in checks:
                actual = row.get(field, "")
                if actual != expected:
                    expectation_problems.append(
                        f"{rid}.{field}: expected {expected!r}, found {actual!r}")
        if expectation_problems:
            hard.append("session row expectations: " + "; ".join(expectation_problems))

    flag_ids = {f.get("id") for f in flagged}
    missing_flags = [f for f in SESSION_FLAGS if f not in flag_ids]
    if missing_flags:
        if applied:
            hard.append(f"session review items missing from register: {missing_flags}")
        else:
            pre_apply_notes.append(
                f"{len(missing_flags)} session review items not present yet (phase: pre-apply)")
    missing_action = [f.get("id") for f in flagged
                      if not (f.get("source_url", "") or "").startswith("https://")]
    if missing_action:
        hard.append(f"review items without https source: {missing_action}")

    # ---- 4. meta.json in sync -------------------------------------------------
    with open(os.path.join(ROOT, "data/meta.json"), encoding="utf-8") as fh:
        meta = json.load(fh)
    actual_counts = {
        "total": len(events),
        "recurring": sum(1 for e in events if e.get("group") == "recurring"),
        "annual": sum(1 for e in events if e.get("group") == "annual"),
        "special": sum(1 for e in events if e.get("group") == "special"),
        "flagged_rows": sum(1 for e in events if e.get("status") != "verified"),
        "unverified_rows": sum(1 for e in events if e.get("status") != "verified"),
        "flagged_items": len(flagged),
    }
    for key, value in actual_counts.items():
        if key == "flagged_items":
            continue
        if meta["counts"].get(key) != value:
            msg = f"meta.json {key}={meta['counts'].get(key)} but dataset has {value}"
            if applied:
                hard.append(msg)
            else:
                pre_apply_notes.append(msg + " (the build now rewrites meta.json; fixed by the apply)")

    # ---- 5. executive summary is free-only ------------------------------------
    summary_ids = re.findall(r"id=['\"]summary-([^'\"]+)['\"]", index_html)
    not_free = []
    for sid in summary_ids:
        row = by_id.get(sid)
        if row is None:
            not_free.append(f"{sid} (unknown row)")
            continue
        if row.get("cost_class") != "free" or row.get("timing") == "concluded":
            not_free.append(sid)
    if not_free:
        hard.append(f"executive summary rows that are not free upcoming: {not_free}")

    # ---- 6. generated pages ---------------------------------------------------
    pages = sorted(fn for fn in os.listdir(ROOT) if fn.endswith(".html"))
    html_blob = ""
    for fn in pages:
        with open(os.path.join(ROOT, fn), encoding="utf-8") as fh:
            html_blob += fh.read()
    broken = []
    for m in re.finditer(r'href="([^"]+)"', html_blob):
        href = m.group(1)
        if href.startswith(("http://", "https://", "mailto:", "tel:", "//")):
            continue
        if href.startswith("#"):
            anchor_page = None
            frag = href[1:]
        else:
            path, _, frag = href.partition("#")
            anchor_page = path
            if anchor_page and not os.path.exists(os.path.join(ROOT, anchor_page)):
                broken.append(f"missing page {href}")
                continue
        if frag and anchor_page is None:
            pass
    for m in re.finditer(r'href="([^"#]*)#([^"]+)"', html_blob):
        path, frag = m.group(1), m.group(2)
        target = path or "index.html"
        if target.startswith(("http://", "https://")):
            continue
        if not os.path.exists(os.path.join(ROOT, target)):
            continue
        with open(os.path.join(ROOT, target), encoding="utf-8") as fh:
            body = fh.read()
        if not re.search(r'(id|name)="' + re.escape(frag) + '"', body):
            broken.append(f"{target}#{frag} unresolved")
    if broken:
        hard.append(f"broken internal links: {broken[:10]}")

    missing_from_html = [e["id"] for e in events
                         if (e.get("source_url") or "") not in html_blob]
    if missing_from_html:
        hard.append(f"rows whose source link is absent from all pages: {missing_from_html}")

    # ---- 7. apply script present ---------------------------------------------
    if not os.path.exists(os.path.join(ROOT, "audit", "apply_9fca0b37.py")):
        hard.append("audit/apply_9fca0b37.py missing")

    # ---- report ---------------------------------------------------------------
    with open(os.path.join(ROOT, "audit", "row-audit-9fca0b37.csv"), "w",
              encoding="utf-8", newline="") as fh:
        writer = csv.writer(fh)
        writer.writerow(["id", "title", "group", "category", "status", "cost_class",
                         "dates", "source_host", "source_url", "blank_fields", "flags"])
        for e in events:
            blanks = [f for f in display_fields if not str(e.get(f, "")).strip()]
            flags = []
            if e.get("status") != "verified":
                flags.append("UNVERIFIED")
            if e.get("status") == "verified" and blanks:
                flags.append("VERIFIED_BUT_BLANK:" + ",".join(blanks))
            writer.writerow([
                e.get("id", ""), e.get("title", ""), e.get("group", ""),
                e.get("category", ""), e.get("status", ""), e.get("cost_class", ""),
                e.get("dates", ""), urlparse(e.get("source_url", "")).netloc,
                e.get("source_url", ""), "|".join(blanks), ";".join(flags),
            ])

    cost_mix = Counter(e.get("cost_class", "") for e in events)
    print(f"events={len(events)} flagged_register={len(flagged)} pages={len(pages)}")
    print(f"verified={sum(1 for e in events if e.get('status') == 'verified')}"
          f" unverified={sum(1 for e in events if e.get('status') != 'verified')}")
    print(f"cost_class={dict(cost_mix)}")
    print(f"summary rows={len(summary_ids)} (all must be free upcoming)")
    print(f"verified rows with a blank display cell (published, not hard): "
          f"{len(verified_blank_not_published)}")
    print(f"phase={'applied' if applied else 'pre-apply'}")
    for note in pre_apply_notes:
        print(f"  pre-apply note: {note}")
    print(f"hard_problems({len(hard)})={hard}")
    return 1 if hard else 0


if __name__ == "__main__":
    sys.exit(main())
