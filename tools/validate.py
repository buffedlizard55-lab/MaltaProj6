#!/usr/bin/env python3
"""Validate the published San Francisco events dataset and static pages.

This checks structural integrity, source-link presence, HTML table consistency,
category/type membership, and local links. It does not fetch URLs or authenticate
source-page contents; source review and completeness remain human research tasks.
"""
from __future__ import annotations

import json
import os
import sys
from collections import Counter
from html.parser import HTMLParser
from urllib.parse import unquote, urlsplit

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data", "events.json")
GROUP_PAGE = {"recurring": "recurring.html", "annual": "annual.html", "special": "special.html"}
CATEGORY_PAGE = {
    "civic": "civic.html",
    "arts": "arts.html",
    "sports": "sports.html",
    "markets": "markets.html",
    "community": "community.html",
}
EXPECTED_CELLS = 9  # Event, type, schedule, dates, location, area, cost, organiser, source


class PageAudit(HTMLParser):
    """Collect row IDs, table cell counts, anchor links, and element IDs."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.links: list[str] = []
        self.element_ids: set[str] = set()
        self.rows: dict[str, dict] = {}
        self.all_rows: list[dict] = []
        self.current_row: dict | None = None

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        element_id = attrs.get("id")
        if element_id:
            self.element_ids.add(element_id)
        if tag == "a" and attrs.get("href"):
            self.links.append(attrs["href"])
        if tag == "tr":
            self.current_row = {"id": element_id, "cells": 0, "links": [], "text": []}
        elif self.current_row is not None:
            if tag == "td":
                self.current_row["cells"] += 1
            elif tag == "a" and attrs.get("href"):
                self.current_row["links"].append(attrs["href"])

    def handle_data(self, data):
        if self.current_row is not None:
            self.current_row["text"].append(data)

    def handle_endtag(self, tag):
        if tag == "tr" and self.current_row is not None:
            row = self.current_row
            self.all_rows.append(row)
            if row["id"]:
                self.rows[row["id"]] = row
            self.current_row = None


def audit_page(filename: str) -> PageAudit:
    path = os.path.join(ROOT, filename)
    parser = PageAudit()
    with open(path, encoding="utf-8") as fh:
        parser.feed(fh.read())
    return parser


def main() -> int:
    errors: list[str] = []
    with open(DATA, encoding="utf-8") as fh:
        payload = json.load(fh)
    events = payload.get("events", [])
    flagged = payload.get("flagged", [])

    if payload.get("event_count") != len(events):
        errors.append(f"data/events.json: event_count={payload.get('event_count')} but rows={len(events)}")
    if payload.get("flagged_count") != len(flagged):
        errors.append(f"data/events.json: flagged_count={payload.get('flagged_count')} but rows={len(flagged)}")

    event_ids = [event.get("id", "") for event in events]
    duplicate_ids = [event_id for event_id, count in Counter(event_ids).items() if not event_id or count != 1]
    if duplicate_ids:
        errors.append(f"data/events.json: empty or duplicate event IDs: {duplicate_ids}")

    events_by_id = {event["id"]: event for event in events if event.get("id")}
    pages = sorted(name for name in os.listdir(ROOT) if name.endswith(".html"))
    audits: dict[str, PageAudit] = {}
    for filename in pages:
        audits[filename] = audit_page(filename)

    # All event listings must use valid HTTPS source links and appear exactly once
    # on both their recurrence page and their subject page, with the link in-row.
    for event in events:
        event_id = event.get("id", "?")
        source_url = event.get("source_url", "")
        if urlsplit(source_url).scheme != "https" or not urlsplit(source_url).netloc:
            errors.append(f"{event_id}: source_url is not an absolute HTTPS URL: {source_url!r}")
        if event.get("group") not in GROUP_PAGE:
            errors.append(f"{event_id}: unknown group {event.get('group')!r}")
        if event.get("category") not in CATEGORY_PAGE:
            errors.append(f"{event_id}: unknown category {event.get('category')!r}")

        expected_pages = []
        if event.get("group") in GROUP_PAGE:
            expected_pages.append(GROUP_PAGE[event["group"]])
        if event.get("category") in CATEGORY_PAGE:
            expected_pages.append(CATEGORY_PAGE[event["category"]])
        for filename in expected_pages:
            row = audits[filename].rows.get(event_id)
            if row is None:
                errors.append(f"{filename}: missing event row {event_id}")
                continue
            if row["cells"] != EXPECTED_CELLS:
                errors.append(f"{filename}:{event_id}: expected {EXPECTED_CELLS} table cells, found {row['cells']}")
            if source_url not in row["links"]:
                errors.append(f"{filename}:{event_id}: official source link missing from its row")
            if event.get("status") == "unverified" and "unverified" not in " ".join(row["text"]).lower():
                errors.append(f"{filename}:{event_id}: unverified status badge missing")

    # Confirm each group/category page contains exactly the records assigned to it.
    for group, filename in GROUP_PAGE.items():
        expected = {event["id"] for event in events if event.get("group") == group}
        actual = {event_id for event_id in audits[filename].rows if event_id in events_by_id}
        if actual != expected:
            errors.append(f"{filename}: row membership differs (expected {len(expected)}, found {len(actual)})")
    for category, filename in CATEGORY_PAGE.items():
        expected = {event["id"] for event in events if event.get("category") == category}
        actual = {event_id for event_id in audits[filename].rows if event_id in events_by_id}
        if actual != expected:
            errors.append(f"{filename}: row membership differs (expected {len(expected)}, found {len(actual)})")

    # Review entries have dedicated rows with their official evidence link.
    if "flagged.html" not in audits:
        errors.append("flagged.html: page missing")
    else:
        flagged_audit = audits["flagged.html"]
        flagged_ids = [item.get("id", "") for item in flagged]
        for item in flagged:
            item_id = item.get("id", "?")
            url = item.get("source_url", "")
            if urlsplit(url).scheme != "https" or not urlsplit(url).netloc:
                errors.append(f"{item_id}: review source_url is not an absolute HTTPS URL")
            row = flagged_audit.rows.get(item_id)
            if row is None:
                errors.append(f"flagged.html: missing review item {item_id}")
            elif url not in row["links"]:
                errors.append(f"flagged.html:{item_id}: evidence source link missing from row")
        if len(flagged_ids) != len(set(flagged_ids)):
            errors.append("data/events.json: duplicate review item IDs")

        unverified_rows = [event for event in events if event.get("status") == "unverified"]
        review_table_ids = {row["id"] for row in flagged_audit.all_rows if row["id"]}
        # The unverified table has one review-<event-id> row per record, with a source link.
        missing_unverified = [event["id"] for event in unverified_rows if f"review-{event['id']}" not in review_table_ids]
        if missing_unverified:
            errors.append(f"flagged.html: unverified rows absent from the review table: {missing_unverified}")
        for event in unverified_rows:
            row = flagged_audit.rows.get(f"review-{event['id']}")
            if row and event.get("source_url") not in row["links"]:
                errors.append(f"flagged.html:review-{event['id']}: official source link missing from review row")

    # Check all local links and in-page fragments across the published HTML files.
    for filename, audit in audits.items():
        for href in audit.links:
            parts = urlsplit(href)
            if parts.scheme or parts.netloc or href.startswith(("mailto:", "tel:", "javascript:")):
                continue
            target_name = unquote(parts.path)
            target_path = os.path.join(ROOT, target_name) if target_name else os.path.join(ROOT, filename)
            if not os.path.isfile(target_path):
                errors.append(f"{filename}: broken local link {href!r}")
                continue
            if parts.fragment:
                target_page = filename if not target_name else target_name
                target_audit = audits.get(target_page)
                if target_audit and unquote(parts.fragment) not in target_audit.element_ids:
                    errors.append(f"{filename}: missing fragment target {href!r}")

    domains = {urlsplit(event.get("source_url", "")).netloc for event in events if event.get("source_url")}
    verified = sum(event.get("status") == "verified" for event in events)
    unverified = sum(event.get("status") == "unverified" for event in events)
    print(f"events={len(events)} verified={verified} review_gap={unverified} review_items={len(flagged)} domains={len(domains)} pages={len(pages)}")
    if errors:
        for error in errors:
            print("ERROR", error)
        print(f"\n{len(errors)} error(s)")
        return 1
    print("\nOK — published data and page structure are consistent. Source contents were not fetched.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
