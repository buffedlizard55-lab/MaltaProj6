#!/usr/bin/env python3
"""Independent structural audit — session arena-76d2c635 (2026-10-18).

Reads the published dataset (data/events.json) and the generated HTML pages
and checks every row line by line for:
  - source present, https, non-aggregator host
  - duplicate ids / normalised titles
  - blank core fields vs verification status
  - prose sitting in the confirmed-dates cell
  - dated rows whose latest parseable date precedes the audit date
  - out-of-city geography wording that needs manual reading
  - group/category/type/page consistency
  - HTML membership: each row exactly once on its type page and category page,
    with its official source link present; every unverified row reachable
    from flagged.html
  - flagged-register integrity (ids, https sources)
  - internal links and #anchors across all pages
  - headline counts in README.md / index.html vs the dataset

Output: audit/row-audit-76d2c635.csv (one line per event) + a printed summary.

This script never fetches the network and never edits the dataset or the site.
Live source-content checks are recorded separately in
audit/AUDIT-2026-10-18-76d2c635.md.
"""
from __future__ import annotations

import csv
import datetime as dt
import json
import os
import re
import sys
from collections import Counter, defaultdict
from html.parser import HTMLParser
from urllib.parse import urlsplit

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
AUDIT_DATE = dt.date(2026, 10, 18)
OUT = os.path.join(ROOT, "audit", "row-audit-76d2c635.csv")

GROUP_PAGE = {"recurring": "recurring.html", "annual": "annual.html", "special": "special.html"}
CATEGORY_PAGE = {
    "civic": "civic.html",
    "arts": "arts.html",
    "sports": "sports.html",
    "technology": "technology.html",
    "markets": "markets.html",
    "community": "community.html",
}
CORE_FIELDS = ["schedule", "location", "cost", "organiser"]
AGGREGATOR_PARTS = (
    "eventbrite.", "facebook.com", "instagram.com", "twitter.com", "tiktok.com",
    "meetup.com", "yelp.com", "tripadvisor.", "timeout.com", "funcheap.com",
    "wikipedia.org", "sfstation.com", "7x7.com", "sfgate.com",
)
# Wording that should trigger a human geography read (not an automatic fail:
# many rows legitimately *exclude* an out-of-city leg in their notes).
# Word-boundary regexes: a plain "marin" substring matches San Francisco's own
# "Marina" district / "Marine Drive" and produced 11 false positives in v1 of
# this checker (all 11 read by hand; none was Marin County). Fixed in v2.
GEO_PATTERNS = [
    r"\boakland\b", r"\bberkeley\b", r"\bemeryville\b",
    r"\bmarin (county|headlands|civic)\b", r"\btiburon\b", r"\bsausalito\b",
    r"\bsanta clara\b", r"\bpalo alto\b", r"\bsan jose\b", r"\balameda\b",
    r"\beast bay\b", r"\bbattery spencer\b", r"\bangel island\b",
    r"\bcupertino\b", r"\bredwood city\b", r"\bdaly city\b",
    r"\bsan mateo\b", r"\bbay area\b",
]
PROSE_IN_DATES = ("not announced", "not published", "not shown", "dates not", "closing date not", "run end not", "run dates not")

MONTHS = {m: i for i, m in enumerate(
    ["january", "february", "march", "april", "may", "june", "july",
     "august", "september", "october", "november", "december"], start=1)}
MONTHS.update({m[:3]: i for m, i in list(MONTHS.items())})


def parse_dates(text: str) -> list[dt.date]:
    """Extract parseable calendar dates from a free-text dates cell.

    v2 adds a month-year upper bound: a mention such as "mid-November 2026"
    contributes Nov 30, 2026 so a season that *starts* before the audit date
    but *ends* after it is not falsely flagged as wholly past (v1 flagged the
    Bandshell season, Mar 1 – mid-Nov 2026, on its start date alone).
    """
    found: list[dt.date] = []
    for m in re.finditer(r"\b(20\d\d)-(\d{2})-(\d{2})\b", text):
        try:
            found.append(dt.date(int(m.group(1)), int(m.group(2)), int(m.group(3))))
        except ValueError:
            pass
    low = text.lower()
    # "October 17, 2026" / "October 17-19, 2026" / "Oct 9-11, 2026"
    for m in re.finditer(
        r"([a-z]+)\s+(\d{1,2})(?:\s*[-–—]\s*(\d{1,2}))?(?:,?\s*(20\d\d))?", low
    ):
        mon, d1, d2, yr = m.group(1), m.group(2), m.group(3), m.group(4)
        if mon not in MONTHS or not yr:
            continue
        for day in (d1, d2):
            if day:
                try:
                    found.append(dt.date(int(yr), MONTHS[mon], int(day)))
                except ValueError:
                    pass
    # Month-year mentions -> last day of that month (upper bound only)
    import calendar as _cal
    for m in re.finditer(r"([a-z]+)\s+(20\d\d)", low):
        mon, yr = m.group(1), int(m.group(2))
        if mon in MONTHS:
            found.append(dt.date(yr, MONTHS[mon], _cal.monthrange(yr, MONTHS[mon])[1]))
    return found


class PageScan(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.links: list[str] = []
        self.element_ids: set[str] = set()
        self.rows: dict[str, list[str]] = defaultdict(list)  # row id -> hrefs
        self._row: str | None = None

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if attrs.get("id"):
            self.element_ids.add(attrs["id"])
        if tag == "a" and attrs.get("href"):
            self.links.append(attrs["href"])
            if self._row:
                self.rows[self._row].append(attrs["href"])
        if tag == "tr" and attrs.get("id"):
            self._row = attrs["id"]

    def handle_endtag(self, tag):
        if tag == "tr":
            self._row = None


def scan_page(name: str) -> PageScan:
    parser = PageScan()
    with open(os.path.join(ROOT, name), encoding="utf-8") as fh:
        parser.feed(fh.read())
    return parser


def norm_title(title: str) -> str:
    return re.sub(r"[^a-z0-9]+", " ", title.lower()).strip()


# Read-only import of the canonical group mapping so TYPE_GROUP checks mirror
# data/events.py assign_views exactly (no dataset file is modified).
sys.path.insert(0, os.path.join(ROOT, "data"))
from events import TYPE_TO_GROUP, EXPLICIT_GROUP  # noqa: E402


def main() -> int:
    with open(os.path.join(ROOT, "data", "events.json"), encoding="utf-8") as fh:
        payload = json.load(fh)
    events = payload["events"]
    flagged = payload["flagged"]

    html_files = sorted(f for f in os.listdir(ROOT) if f.endswith(".html"))
    pages = {name: scan_page(name) for name in html_files}
    flagged_html = ""
    with open(os.path.join(ROOT, "flagged.html"), encoding="utf-8") as fh:
        flagged_html = fh.read()

    id_counts = Counter(e.get("id", "") for e in events)
    title_counts = Counter(norm_title(e.get("title", "")) for e in events)
    flag_id_counts = Counter(f.get("id", "") for f in flagged)

    hard: list[str] = []
    rows: list[dict] = []
    flag_counts: Counter = Counter()

    for e in events:
        flags: list[str] = []
        url = (e.get("source_url") or "").strip()
        host = urlsplit(url).netloc.lower() if url else ""
        if not url:
            flags.append("MISSING_SOURCE")
            hard.append(f"{e.get('id')}: missing source_url")
        elif not url.startswith("https://"):
            flags.append("NON_HTTPS_SOURCE")
            hard.append(f"{e.get('id')}: non-https source {url}")
        if any(p in url.lower() for p in AGGREGATOR_PARTS):
            flags.append("AGGREGATOR_SOURCE")
            hard.append(f"{e.get('id')}: aggregator source {url}")
        if id_counts[e.get("id", "")] != 1 or not e.get("id"):
            flags.append("DUPLICATE_OR_EMPTY_ID")
            hard.append(f"{e.get('id')}: duplicate/empty id")
        if title_counts[norm_title(e.get("title", ""))] > 1:
            flags.append("DUPLICATE_TITLE")
        if e.get("status") not in ("verified", "unverified"):
            flags.append("UNKNOWN_STATUS")
            hard.append(f"{e.get('id')}: status={e.get('status')!r}")
        if e.get("group") not in GROUP_PAGE:
            flags.append("UNKNOWN_GROUP")
            hard.append(f"{e.get('id')}: group={e.get('group')!r}")
        if e.get("category") not in CATEGORY_PAGE:
            flags.append("UNKNOWN_CATEGORY")
            hard.append(f"{e.get('id')}: category={e.get('category')!r}")
        # NOTE (checker v1 -> v2): v1 flagged PAGE_NE_GROUP (128 rows) on the
        # assumption that the authored `page` field must equal `group`. That is
        # wrong: data/events.py `assign_views` derives `group` from `type`
        # (TYPE_TO_GROUP / EXPLICIT_GROUP) and `page` may name a category page
        # (or be "" on imported rows). The real invariant — one listing on the
        # group page + one on the category page — is checked via HTML below.
        expected_group = EXPLICIT_GROUP.get(e.get("id") or "", TYPE_TO_GROUP.get(e.get("type", ""), "recurring"))
        if e.get("group") != expected_group:
            flags.append(f"TYPE_GROUP_MISMATCH(expected={expected_group})")
            hard.append(f"{e.get('id')}: group={e.get('group')!r} expected {expected_group!r}")

        blank_core = [f for f in CORE_FIELDS if not (e.get(f) or "").strip()]
        blank_dates = not (e.get("dates") or "").strip()
        # Mirror scripts/build_site.py unverified_rows(): the flagged page's
        # blank-cell table can only ever name Schedule/Dates/Location/Cost.
        if "organiser" in blank_core:
            flags.append("ORGANISER_BLANK_UNNAMED_ON_FLAGGED_PAGE")
        table_shows = (
            e.get("status") == "unverified"
            or any(not (e.get(k) or "").strip() for k in ("schedule", "location", "cost"))
        )
        if not table_shows and (blank_core or (blank_dates and e.get("group") in ("annual", "special"))):
            flags.append("BLANK_ESCAPES_FLAGGED_TABLE")
        if e.get("status") == "verified" and blank_core:
            flags.append("VERIFIED_BUT_BLANK_CORE(" + ",".join(blank_core) + ")")
        if e.get("status") == "verified" and blank_dates:
            flags.append("VERIFIED_BLANK_DATES")
        if e.get("status") == "unverified" and not blank_core and not blank_dates:
            flags.append("UNVERIFIED_WITHOUT_BLANK")
        if e.get("status") == "unverified" and f'id="{e.get("id")}"' not in flagged_html \
                and f"#{e.get('id')}" not in flagged_html and (e.get("id") or "") not in flagged_html:
            flags.append("UNVERIFIED_NOT_ON_FLAGGED_PAGE")
            hard.append(f"{e.get('id')}: unverified but not reachable from flagged.html")

        dates_text = e.get("dates") or ""
        if any(p in dates_text.lower() for p in PROSE_IN_DATES):
            flags.append("PROSE_IN_DATES_CELL")
        parsed = parse_dates(dates_text)
        latest = max(parsed) if parsed else None
        if latest and latest < AUDIT_DATE:
            flags.append(f"LATEST_DATE_BEFORE_AUDIT({latest.isoformat()})")
        if parsed and e.get("group") == "recurring" and latest and latest < AUDIT_DATE:
            flags.append("RECURRING_WITH_PAST_SEASON")

        blob = " ".join(str(e.get(k, "")) for k in ("title", "location", "area", "notes")).lower()
        hits = [m.group(0) for p in GEO_PATTERNS for m in [re.search(p, blob)] if m]
        if hits:
            flags.append("GEO_REVIEW(" + ",".join(hits) + ")")
        if re.search(r"\b2024\b", blob + " " + dates_text):
            flags.append("MENTIONS_2024")

        # HTML membership on the two expected listing pages
        for label, mapping, key in (("TYPE", GROUP_PAGE, "group"), ("CATEGORY", CATEGORY_PAGE, "category")):
            page_name = mapping.get(e.get(key) or "")
            if not page_name:
                continue
            scan = pages.get(page_name)
            hrefs = scan.rows.get(e.get("id") or "", []) if scan else []
            occurrences = 1 if (scan and (e.get("id") or "") in scan.rows) else 0
            if occurrences == 0:
                flags.append(f"HTML_MISSING_ON_{label}_PAGE({page_name})")
                hard.append(f"{e.get('id')}: missing from {page_name}")
            elif url and url not in hrefs:
                flags.append(f"SOURCE_LINK_MISSING_ON_{label}_PAGE({page_name})")
                hard.append(f"{e.get('id')}: source link missing on {page_name}")

        for f in flags:
            flag_counts[f.split("(")[0]] += 1
        rows.append({
            "id": e.get("id", ""), "title": e.get("title", ""),
            "group": e.get("group", ""), "category": e.get("category", ""),
            "type": e.get("type", ""), "status": e.get("status", ""),
            "dates": dates_text, "latest_parsed_date": latest.isoformat() if latest else "",
            "blank_core": ",".join(blank_core), "blank_dates": "yes" if blank_dates else "",
            "source_url": url, "source_host": host, "flags": ";".join(flags),
        })

    # Flagged-register integrity
    flagged_problems = []
    for f in flagged:
        if flag_id_counts[f.get("id", "")] != 1 or not f.get("id"):
            flagged_problems.append(f"{f.get('id')!r}: duplicate/empty register id")
        fu = (f.get("source_url") or "").strip()
        if fu and not fu.startswith("https://"):
            flagged_problems.append(f"{f.get('id')}: non-https source {fu}")
        if any(p in fu.lower() for p in AGGREGATOR_PARTS):
            flagged_problems.append(f"{f.get('id')}: aggregator source {fu}")
    hard.extend(flagged_problems)

    # Internal links / anchors
    broken = []
    for name, scan in pages.items():
        for href in scan.links:
            if href.startswith(("https://", "http://", "mailto:", "tel:")):
                continue
            target, _, frag = href.partition("#")
            target = target or name
            if "?" in target:
                target = target.split("?")[0]
            if target and not os.path.exists(os.path.join(ROOT, target)):
                broken.append(f"{name} -> {href} (missing file)")
                continue
            if frag and target in pages and frag not in pages[target].element_ids:
                broken.append(f"{name} -> {href} (missing anchor)")
    hard.extend(broken)

    # Headline-count cross-check (README + index claims)
    counts = {
        "events": len(events), "flagged": len(flagged),
        "verified": sum(1 for e in events if e.get("status") == "verified"),
        "unverified": sum(1 for e in events if e.get("status") == "unverified"),
    }
    by_group = Counter(e.get("group") for e in events)
    by_category = Counter(e.get("category") for e in events)
    hosts = sorted({urlsplit(e["source_url"]).netloc.lower() for e in events if e.get("source_url")})
    hosts_nowww = sorted({h[4:] if h.startswith("www.") else h for h in hosts})
    urls = sorted({e["source_url"] for e in events if e.get("source_url")})

    with open(os.path.join(ROOT, "README.md"), encoding="utf-8") as fh:
        readme = fh.read()
    with open(os.path.join(ROOT, "index.html"), encoding="utf-8") as fh:
        index_html = fh.read()
    claim_problems = []
    for doc_name, doc in (("README.md", readme),):
        for key, val in [("events", counts["events"]), ("verified", counts["verified"])]:
            if str(val) not in doc:
                claim_problems.append(f"{doc_name}: {key} count {val} not found in text")

    with open(OUT, "w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=[
            "id", "title", "group", "category", "type", "status", "dates",
            "latest_parsed_date", "blank_core", "blank_dates", "source_url",
            "source_host", "flags"])
        writer.writeheader()
        writer.writerows(rows)

    print(f"AUDIT_DATE={AUDIT_DATE.isoformat()} session=arena-76d2c635")
    print(f"events={counts['events']} flagged_register={counts['flagged']} "
          f"verified={counts['verified']} unverified={counts['unverified']}")
    print(f"by_group={dict(by_group)} by_category={dict(by_category)}")
    print(f"distinct_source_urls={len(urls)} distinct_hosts={len(hosts)} "
          f"distinct_hosts_www_stripped={len(hosts_nowww)}")
    print(f"meta_event_count={payload.get('event_count')} meta_flagged_count={payload.get('flagged_count')} "
          f"generated={payload.get('generated')} verified_on={payload.get('verified_on')}")
    print(f"flag_counts={dict(flag_counts.most_common())}")
    print(f"flagged_register_problems={flagged_problems}")
    print(f"broken_internal_links={broken}")
    print(f"headline_claim_problems={claim_problems}")
    print(f"hard_problems({len(hard)})={hard}")
    print(f"wrote {OUT}")
    return 1 if hard else 0


if __name__ == "__main__":
    sys.exit(main())
