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
from copy import deepcopy
from collections import Counter
from datetime import date
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
# Focus pages cut the catalogue by the brief's subject areas (gaming, music,
# AI) rather than by the subject categories, so a row can belong to both.
FOCUS_PAGE = {
    "technology.html": {"ai", "gaming"},
    "music.html": {"music"},
}
EXPECTED_CELLS = 9  # Event, type, schedule, dates, location, area, cost, organiser, source
DATE_STATUS_METADATA = {"confirmed", "partial", "not announced"}
NON_PRIMARY_HOST_PARTS = (
    "eventbrite.", "facebook.com", "instagram.com", "twitter.com", "tiktok.com",
    "wikipedia.org", "funcheap.com", "yelp.com", "tripadvisor.", "timeout.com",
    "google.com/search", "bing.com/search",
)


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

    # Keep the committed JSON mirror reproducible from the authored records and
    # the preserved parallel-session input files.
    try:
        sys.path.insert(0, os.path.join(ROOT, "data"))
        sys.path.insert(0, os.path.join(ROOT, "scripts"))
        from events import EVENTS as BASE_EVENTS, FLAGGED as BASE_FLAGGED, assign_views, cost_review_flags, cost_review_flags
        from merge_parallel import parallel_events, parallel_flagged
        from build_site import _event_date_sort_key, _has_free_access, _next_confirmed_date
        base_events = deepcopy(BASE_EVENTS)
        expected_events = assign_views(base_events + parallel_events(base_events))
        expected_flagged = list(BASE_FLAGGED) + parallel_flagged() + cost_review_flags(expected_events)
        from build_site import (
            _event_date_sort_key,
            _has_free_access,
            _next_confirmed_date,
            attach_focus,
            executive_summary_rows,
        )
        base_events = deepcopy(BASE_EVENTS)
        expected_events = attach_focus(assign_views(base_events + parallel_events(base_events)))
        expected_flagged = list(BASE_FLAGGED) + parallel_flagged() + cost_review_flags(expected_events)
        if events != expected_events:
            errors.append("data/events.json: event rows differ from the reproducible source-data union")
        if flagged != expected_flagged:
            errors.append("data/events.json: review rows differ from the reproducible source-data union")
    except Exception as exc:
        errors.append(f"could not reproduce canonical data union: {exc}")

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
        if any(host in source_url.lower() for host in NON_PRIMARY_HOST_PARTS):
            errors.append(f"{event_id}: source_url uses a blocked non-primary host: {source_url}")
        source_urls = [source_url] + [item.get("url", "") for item in event.get("additional_sources", [])]
        for supporting_url in source_urls[1:]:
            parts = urlsplit(supporting_url)
            if parts.scheme != "https" or not parts.netloc:
                errors.append(f"{event_id}: supporting source is not an absolute HTTPS URL: {supporting_url!r}")
            if any(host in supporting_url.lower() for host in NON_PRIMARY_HOST_PARTS):
                errors.append(f"{event_id}: supporting source uses a blocked non-primary host: {supporting_url}")
        if event.get("status") not in ("verified", "unverified"):
            errors.append(f"{event_id}: invalid status {event.get('status')!r}")
        for field in ("schedule", "dates"):
            field_value = event.get(field, "")
            if isinstance(field_value, str) and field_value.strip().casefold() in DATE_STATUS_METADATA:
                errors.append(
                    f"{event_id}: {field} contains date-status metadata {field_value!r}, not an event value"
                )
        if event.get("group") not in GROUP_PAGE:
            errors.append(f"{event_id}: unknown group {event.get('group')!r}")
        known_categories = set(CATEGORY_PAGE) | {"technology"}
        if event.get("category") not in known_categories:
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
            for supporting_url in source_urls:
                if supporting_url and supporting_url not in row["links"]:
                    errors.append(f"{filename}:{event_id}: official source link missing from its row: {supporting_url}")
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
    for filename, focus_keys in FOCUS_PAGE.items():
        expected = {event["id"] for event in events
                    if event.get("focus") in focus_keys
                    or (filename == "technology.html" and event.get("category") == "technology")}
        actual = {event_id for event_id in audits[filename].rows if event_id in events_by_id}
        if actual != expected:
            errors.append(f"{filename}: focus-page membership differs (expected {len(expected)}, found {len(actual)})")

    # Keep chronological-first presentation reproducible and ensure the dedicated
    # free page only contains rows whose source wording explicitly includes free access.
    ordered_pages = {
        "all-events.html": sorted(events, key=_event_date_sort_key),
        "special.html": sorted((e for e in events if e.get("group") == "special"), key=_event_date_sort_key),
        "technology.html": sorted((e for e in events if e.get("category") == "technology"), key=_event_date_sort_key),
        "free-events.html": sorted((e for e in events if _has_free_access(e)), key=_event_date_sort_key),
        "technology.html": sorted(
            (e for e in events if e.get("focus") in ("ai", "gaming") or e.get("category") == "technology"),
            key=_event_date_sort_key),
        "music.html": sorted((e for e in events if e.get("focus") == "music"), key=_event_date_sort_key),
        "free-events.html": sorted((e for e in events if _has_free_access(e)), key=_event_date_sort_key),
    }
    for filename, expected_rows in ordered_pages.items():
        if filename not in audits:
            errors.append(f"{filename}: ordered catalogue page missing")
            continue
        actual_ids = [row["id"] for row in audits[filename].all_rows if row.get("id") in events_by_id]
        expected_ids = [event["id"] for event in expected_rows]
        if actual_ids != expected_ids:
            errors.append(f"{filename}: event rows are not in the expected date-first order")
        for event in expected_rows:
            row = audits[filename].rows.get(event["id"])
            if row and event.get("source_url") not in row["links"]:
                errors.append(f"{filename}:{event['id']}: official source link missing from its row")

    today = date.today()
    upcoming_summary = executive_summary_rows(events, today)
    if "index.html" in audits:
        summary_ids = [row["id"][len("summary-"):] for row in audits["index.html"].all_rows
                       if (row.get("id") or "").startswith("summary-")]
        if summary_ids != [event["id"] for event in upcoming_summary]:
            errors.append("index.html: near-term executive summary is not ordered by confirmed date")

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
            if any(host in url.lower() for host in NON_PRIMARY_HOST_PARTS):
                errors.append(f"{item_id}: review source_url uses a blocked non-primary host: {url}")
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
