#!/usr/bin/env python3
"""Validate data/*.json and the generated HTML.  Exit code 1 on any error."""
import datetime as dt
import json
import os
import sys
from urllib.parse import urlparse

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VERIFIED_ON = dt.date(2026, 10, 18)

BAD_HOST_PARTS = (
    "wikipedia", "funcheap", "dylanstours", "sftravel", "timeout", "yelp",
    "tripadvisor", "eventbrite", "facebook.com", "instagram.com", "twitter.com",
    "x.com", "tiktok", "reddit", "google.com/search", "bing.com",
)

COMMON_REQUIRED = ["id", "name", "category", "venue", "neighborhood", "organizer",
                   "source_url", "source_title", "source_type", "verified_on", "unverified_fields"]
RECURRING_REQUIRED = ["cadence", "schedule"]
ANNUAL_REQUIRED = ["edition", "dates", "next_edition_status"]
SPECIAL_REQUIRED = ["start_date", "end_date", "date_status", "type"]

OPTIONAL_FIELDS = {"address", "admission", "notes", "season", "edition", "dates",
                   "display_dates", "next_edition_status", "typical_month",
                   "start_date", "end_date", "date_status", "type",
                   "schedule", "cadence"}
# schedule may legitimately be unknown (a festival with no published timetable).
ALLOWED_BLANK = {"address", "admission", "notes", "season", "edition", "dates",
                 "display_dates", "next_edition_status", "typical_month",
                 "start_date", "end_date"}

CATEGORY_FILES = {
    "weekly": ("weekly.json", {"weekly", "monthly"}),
    "annual": ("annual.json", {"annual"}),
    "special": ("special.json", {"special"}),
}


def load(name):
    with open(os.path.join(ROOT, "data", name), encoding="utf-8") as fh:
        return json.load(fh)


def main():
    errors, warnings = [], []
    events, ids = [], set()
    sources = {s["url"]: s for s in load("sources.json")["sources"]}

    for cat, (filename, allowed_cats) in CATEGORY_FILES.items():
        payload = load(filename)
        if payload.get("verified_on") != VERIFIED_ON.isoformat():
            errors.append(f"{filename}: verified_on is {payload.get('verified_on')!r}")
        rows = payload.get("events", [])
        if not rows:
            errors.append(f"{filename}: no events")
        for ev in rows:
            where = f"{filename}:{ev.get('id', '?')}"
            events.append(ev)
            if ev["id"] in ids:
                errors.append(f"{where}: duplicate id")
            ids.add(ev["id"])
            if ev["category"] not in allowed_cats:
                errors.append(f"{where}: category {ev['category']!r} not allowed in this file")
            required = list(COMMON_REQUIRED)
            if cat == "weekly":
                required += RECURRING_REQUIRED
            elif cat == "annual":
                required += ANNUAL_REQUIRED
            else:
                required += SPECIAL_REQUIRED
            for field in required:
                if field not in ev:
                    errors.append(f"{where}: missing field {field!r}")
                    continue
                value = ev[field]
                if field == "unverified_fields":
                    continue
                if value in ("", None, []) and field not in ALLOWED_BLANK \
                        and field not in ev.get("unverified_fields", []):
                    errors.append(f"{where}: empty required field {field!r}")
            if not isinstance(ev.get("unverified_fields"), list):
                errors.append(f"{where}: unverified_fields must be a list")
                continue
            for field in ev["unverified_fields"]:
                root = field.split(".", 1)[0]
                if root not in OPTIONAL_FIELDS:
                    errors.append(f"{where}: unverified field {field!r} is not an optional schema field")
                if "." not in field and ev.get(field):
                    errors.append(f"{where}: field {field!r} is listed unverified but is populated")

            url = ev.get("source_url", "")
            if not url.startswith("https://"):
                errors.append(f"{where}: source_url must be https")
            if any(bad in url for bad in BAD_HOST_PARTS):
                errors.append(f"{where}: source_url points at a non-official host ({url})")
            if url not in sources:
                errors.append(f"{where}: source_url not registered in sources.json ({url})")
            if ev.get("verified_on") != VERIFIED_ON.isoformat():
                errors.append(f"{where}: verified_on mismatch")

            # Date sanity.
            for field in ("start_date", "end_date"):
                value = ev.get(field)
                if not value:
                    continue
                try:
                    d = dt.date.fromisoformat(value)
                except ValueError:
                    errors.append(f"{where}: {field} is not ISO ({value})")
                    continue
                if field == "end_date" and not ev.get("start_date"):
                    warnings.append(f"{where}: end_date without start_date")
                if field == "end_date" and ev.get("start_date"):
                    try:
                        if d < dt.date.fromisoformat(ev["start_date"]):
                            errors.append(f"{where}: end_date before start_date")
                    except ValueError:
                        pass
            if ev.get("dates"):
                for part in ev["dates"].split(";"):
                    try:
                        dt.date.fromisoformat(part.strip())
                    except ValueError:
                        errors.append(f"{where}: dates entry not ISO ({part})")

            if ev["category"] == "special":
                status = ev.get("date_status")
                if status not in ("confirmed", "partial", "not announced"):
                    errors.append(f"{where}: bad date_status {status!r}")
                if status == "confirmed" and not ev.get("start_date"):
                    errors.append(f"{where}: confirmed status without a start_date")
                if status == "not announced" and (ev.get("start_date") or ev.get("end_date")):
                    errors.append(f"{where}: not announced but dates present")
            if ev["category"] == "annual":
                if ev.get("edition") == "2026" and not ev.get("dates"):
                    warnings.append(f"{where}: 2026 edition without recorded dates")
                if ev.get("dates") and not ev.get("edition"):
                    errors.append(f"{where}: dates without edition")

    flagged = load("flagged.json")
    fids = set()
    for item in flagged["items"]:
        for field in ("id", "kind", "item", "issue", "evidence_url", "action"):
            if not item.get(field):
                errors.append(f"flagged:{item.get('id', '?')}: missing {field}")
        if item["id"] in fids:
            errors.append(f"flagged: duplicate id {item['id']}")
        fids.add(item["id"])
        if not item["evidence_url"].startswith("https://"):
            errors.append(f"flagged:{item['id']}: evidence_url must be https")
        for related in [r.strip() for r in (item.get("related_event") or "").split(";") if r.strip()]:
            if related not in ids:
                errors.append(f"flagged:{item['id']}: related_event {related!r} does not exist")

    # Every unverified row must be reachable from flagged.html.
    flagged_html = ""
    path = os.path.join(ROOT, "flagged.html")
    if os.path.exists(path):
        with open(path, encoding="utf-8") as fh:
            flagged_html = fh.read()
        for ev in events:
            if ev.get("unverified_fields") and f"#{ev['id']}" not in flagged_html:
                errors.append(f"flagged.html: unverified row {ev['id']} not listed")

    # Internal links resolve.
    pages = sorted(f for f in os.listdir(ROOT) if f.endswith(".html"))
    for name_ in pages:
        with open(os.path.join(ROOT, name_), encoding="utf-8") as fh:
            text = fh.read()
        for target in {p.split("#")[0] for p in __import__("re").findall(r'href="([^"]+)"', text)}:
            if not target or target.startswith(("http", "#", "mailto:")):
                continue
            if not os.path.exists(os.path.join(ROOT, target)):
                errors.append(f"{name_}: broken internal link {target!r}")

    # Every row's source domain must appear on the sources page.
    sources_html = ""
    if os.path.exists(os.path.join(ROOT, "sources.html")):
        sources_html = open(os.path.join(ROOT, "sources.html"), encoding="utf-8").read()
    for ev in events:
        if ev["source_url"] not in sources_html:
            errors.append(f"sources.html: missing {ev['source_url']}")

    print(f"rows={len(events)} flagged={len(flagged['items'])} sources={len(sources)} pages={len(pages)}")
    for w in warnings:
        print("WARN ", w)
    if errors:
        for e in errors:
            print("ERROR", e)
        print(f"\n{len(errors)} error(s), {len(warnings)} warning(s)")
        return 1
    print(f"\nOK — no errors, {len(warnings)} warning(s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
