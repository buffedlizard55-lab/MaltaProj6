#!/usr/bin/env python3
"""Independent structural audit for the SF events dataset (session arena-8e8e24dc).

Reads the *published* data/events.json plus the generated HTML pages and reports
per-row findings as CSV, then prints a summary of hard problems.

This checker does not fetch any URL. It only checks what is published against
structural rules; live source-text verification is recorded separately in
audit/AUDIT-2026-10-18-8e8e24dc.md.

Usage:
    python3 audit/check_8e8e24dc.py
"""
from __future__ import annotations

import csv
import json
import os
import re
from collections import Counter, defaultdict
from datetime import date, datetime
from html.parser import HTMLParser
from urllib.parse import unquote, urlsplit

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data", "events.json")
OUT = os.path.join(ROOT, "audit", "row-audit-8e8e24dc.csv")
TODAY = date(2026, 10, 18)

GROUP_PAGE = {"recurring": "recurring.html", "annual": "annual.html", "special": "special.html"}
CATEGORY_PAGE = {
    "civic": "civic.html",
    "arts": "arts.html",
    "sports": "sports.html",
    "markets": "markets.html",
    "community": "community.html",
}

AGGREGATOR_HOSTS = (
    "eventbrite.", "facebook.com", "instagram.com", "twitter.com", "x.com",
    "tiktok.", "wikipedia.org", "funcheap.com", "yelp.com", "tripadvisor.",
    "timeout.com", "sfstation.com", "dothebay.com", "festivalnet.com",
    "meetup.com", "reddit.com", "google.com", "bing.com",
)

OUT_OF_CITY_TERMS = (
    "oakland", "berkeley", "emeryville", "sausalito", "mill valley", "marin",
    "sacramento", "san mateo", "palo alto", "san jose", "santa clara", "alameda",
    "cupertino", "redwood city", "foster city", "pleasant hill", "sunnyvale",
    "tiburon", "angel island", "battery spencer", "tahoe", "napa", "sonoma",
)

WEEKDAYS = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
MONTHS = {
    "january": 1, "february": 2, "march": 3, "april": 4, "may": 5, "june": 6,
    "july": 7, "august": 8, "september": 9, "october": 10, "november": 11,
    "december": 12, "jan": 1, "feb": 2, "mar": 3, "apr": 4, "jun": 6,
    "jul": 7, "aug": 8, "sep": 9, "sept": 9, "oct": 10, "nov": 11, "dec": 12,
}

DATE_RE = re.compile(
    r"(?:(monday|tuesday|wednesday|thursday|friday|saturday|sunday),?\s+)?"
    r"(january|february|march|april|may|june|july|august|september|october|november|december|"
    r"jan|feb|mar|apr|jun|jul|aug|sept|sep|oct|nov|dec)\.?\s+"
    r"(\d{1,2})(?:\s*[–-]\s*(?:(\w+)\.?\s+)?(\d{1,2}))?[,]?\s+(\d{4})",
    re.I,
)


class Page(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.row_ids: list[str] = []
        self.links: list[str] = []
        self.ids: set[str] = set()
        self._in_row = False

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if attrs.get("id"):
            self.ids.add(attrs["id"])
            if tag == "tr":
                self.row_ids.append(attrs["id"])
        if tag == "a" and attrs.get("href"):
            self.links.append(attrs["href"])

    def handle_endtag(self, tag):
        pass


def parse_page(name: str) -> Page:
    p = Page()
    with open(os.path.join(ROOT, name), encoding="utf-8") as fh:
        p.feed(fh.read())
    return p


def host_of(url: str) -> str:
    try:
        return (urlsplit(url).hostname or "").lower()
    except ValueError:
        return ""


def date_mentions(text: str):
    """Yield (weekday_or_None, year, month, day) for every full date found.

    A range such as "November 5–8, 2026" yields both endpoints.
    """
    for m in DATE_RE.finditer(text or ""):
        weekday = (m.group(1) or "").lower() or None
        month = MONTHS.get(m.group(2).lower())
        day = int(m.group(3))
        year = int(m.group(6))
        if month is None:
            continue
        yield weekday, year, month, day
        if m.group(4) or m.group(5):
            end_month = MONTHS.get((m.group(4) or m.group(2)).lower().rstrip("."), month)
            end_day = int(m.group(5))
            if end_day >= day or end_month != month:
                yield None, year, end_month, end_day


def main() -> int:
    payload = json.load(open(DATA, encoding="utf-8"))
    events = payload["events"]
    flagged = payload["flagged"]

    pages = {name: parse_page(name) for name in set(GROUP_PAGE.values()) | set(CATEGORY_PAGE.values()) | {"flagged.html", "index.html", "methodology.html"}}
    all_html_ids = set().union(*(p.ids for p in pages.values()))

    rows = []
    hard: list[str] = []
    seen_titles: dict[str, str] = {}
    seen_urls: dict[str, str] = {}

    for e in events:
        issues: list[str] = []
        eid = e.get("id", "")
        title = e.get("title", "")
        url = e.get("source_url", "")
        host = host_of(url)
        status = e.get("status", "")
        group = e.get("group", "")
        category = e.get("category", "")

        if not eid:
            issues.append("missing id")
        if not title:
            issues.append("missing title")
        if not url:
            issues.append("missing source_url")
        elif not url.startswith("https://"):
            issues.append("source_url not https")
        if host and any(h in host for h in AGGREGATOR_HOSTS):
            issues.append(f"non-primary host: {host}")
        if status not in ("verified", "unverified"):
            issues.append(f"invalid status: {status}")
        if group not in GROUP_PAGE:
            issues.append(f"invalid group: {group}")
        if category not in CATEGORY_PAGE:
            issues.append(f"invalid category: {category}")

        blanks = [k for k in ("schedule", "dates", "location", "area", "cost", "organiser") if not e.get(k)]
        core_blanks = [b for b in blanks if b in ("schedule", "location", "cost")]
        if status == "verified" and core_blanks:
            issues.append("verified but core field blank: " + ",".join(core_blanks))
        if status == "unverified" and not blanks and not e.get("notes"):
            issues.append("unverified with no blank and no note")

        norm_title = re.sub(r"[^a-z0-9]+", " ", title.lower()).strip()
        if norm_title in seen_titles:
            issues.append(f"duplicate title with {seen_titles[norm_title]}")
        else:
            seen_titles[norm_title] = eid
        seen_urls.setdefault(url, eid)

        text = " ".join(str(e.get(k, "")) for k in ("location", "area", "title", "notes"))
        for term in OUT_OF_CITY_TERMS:
            if re.search(rf"\b{re.escape(term)}\b", text, re.I):
                issues.append(f"out-of-city term: {term}")

        for field in ("dates", "schedule", "notes"):
            mentions = list(date_mentions(str(e.get(field, ""))))
            # Weekday checks are only meaningful for a single, unambiguous date.
            if len(mentions) == 1:
                weekday, year, month, day = mentions[0]
                try:
                    actual = date(year, month, day).strftime("%A").lower()
                except ValueError:
                    issues.append(f"invalid date {year}-{month}-{day} in {field}")
                    continue
                if weekday and weekday != actual:
                    issues.append(f"weekday mismatch in {field}: {weekday} vs {actual} {year}-{month:02d}-{day:02d}")

        # Past-dated: specials and any row whose only dates are before today.
        dated = list(date_mentions(str(e.get("dates", ""))))
        if dated:
            years = {d[1] for d in dated}
            latest = max(date(y, m, d) for _, y, m, d in dated)
            if latest < TODAY and years and max(years) <= 2026:
                issues.append(f"past-dated edition (latest {latest.isoformat()})")

        loc = str(e.get("location", ""))
        if re.search(r"(\b[\w' .]+(?:Street|St|Avenue|Ave|Boulevard|Blvd)\b[^,;]*),\s*\1", loc, re.I):
            issues.append("duplicated address text in location")

        page = GROUP_PAGE[group]
        if eid and eid not in pages[page].ids:
            issues.append(f"missing from {page}")
        cat_page = CATEGORY_PAGE[category]
        if eid and eid not in pages[cat_page].ids:
            issues.append(f"missing from {cat_page}")

        rows.append({
            "id": eid,
            "title": title,
            "group": group,
            "category": category,
            "status": status,
            "source_url": url,
            "host": host,
            "issues": " | ".join(issues),
        })

    # HTML link integrity (internal only)
    html_files = sorted(f for f in os.listdir(ROOT) if f.endswith(".html"))
    for name in html_files:
        p = parse_page(name)
        for href in p.links:
            if href.startswith(("http://", "https://", "mailto:")):
                continue
            target, _, anchor = href.partition("#")
            target = target or name
            if target not in html_files and not os.path.exists(os.path.join(ROOT, unquote(target))):
                hard.append(f"{name}: broken internal link {href}")
            elif anchor and anchor not in pages.get(target, parse_page(target)).ids:
                hard.append(f"{name}: missing anchor {href}")

    # Review register checks
    for f in flagged:
        if not f.get("source_url", "").startswith("https://"):
            hard.append(f"flagged {f.get('id')}: missing/non-https source_url")
        if f.get("id") and f["id"] not in all_html_ids:
            hard.append(f"flagged {f.get('id')}: not rendered on any page")

    with open(OUT, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=["id", "title", "group", "category", "status", "source_url", "host", "issues"])
        w.writeheader()
        w.writerows(rows)

    flagged_rows = [r for r in rows if r["issues"]]
    print(f"events={len(events)} flagged_items={len(flagged)} pages={len(html_files)}")
    print(f"rows_with_findings={len(flagged_rows)}")
    print(f"hard_problems={len(hard)}")
    for h in hard[:50]:
        print("  HARD:", h)
    by_issue = Counter()
    for r in rows:
        for i in r["issues"].split(" | "):
            if i:
                by_issue[i.split(":")[0]] += 1
    print("issue kinds:")
    for k, v in by_issue.most_common(30):
        print(f"  {v:3}  {k}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
