#!/usr/bin/env python3
"""Merge the parallel session's dataset into this project's canonical schema.

A second agent session (``arena-8fb52462``, branch ``arena/8fb52462-maltaproj6``)
worked on the same repository in parallel and its research was merged into
``main``. Its raw data files are preserved verbatim in the repository at
``data/weekly.json``, ``data/annual.json``, ``data/special.json`` and
``data/flagged.json``.

This module converts those rows into the schema used by ``data/events.py`` so
that the union of both research passes is published as one list, without
discarding either session's work. Rows that describe the same event in both
datasets are de-duplicated (the row with the richer, directly-verified data
wins); every other row is carried over with its own official source link and a
note recording where it came from.
"""

from __future__ import annotations

import json
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data")

PARALLEL_SESSION = "arena-8fb52462"

# Rows in the parallel dataset that describe the same event as a row that is
# already in data/events.py. They are not imported a second time, but the
# parallel session's files stay in the repository as the record of its work.
SKIP_DUPLICATES = {
    # regularly recurring
    "w-001",  # Ferry Plaza Farmers Market          -> rec-ferry-plaza-farmers-market
    "w-002",  # Alemany Farmers Market              -> mkt-alemany
    "w-004",  # Mission Community Market            -> mkt-mission-community
    "w-018",  # California Academy of Sciences NightLife -> rec-calacademy-nightlife
    "w-019",  # Exploratorium After Dark            -> rec-explatorium-after-dark
    "w-022",  # Off the Grid: Treasure Island       -> rec-off-the-grid-treasure-island
    "w-026",  # TreasureFest                        -> mkt-treasurefest
    # annual
    "a-001",  # Chinese New Year Parade             -> ann-cny-parade
    "a-002",  # Northern California Cherry Blossom  -> ann-cherry-blossom
    "a-003",  # Bay to Breakers                     -> ann-bay-to-breakers
    "a-004",  # San Francisco Pride                 -> ann-sf-pride
    "a-006",  # The San Francisco Marathon          -> ann-sf-marathon
    "a-009",  # Nihonmachi Street Fair              -> ann-nihonmachi
    "a-010",  # Folsom Street Fair                  -> ann-folsom-fair
    "a-011",  # Up Your Alley                       -> ann-up-your-alley
    "a-012",  # Castro Street Fair                  -> ann-castro-street-fair
    "a-014",  # San Francisco Fleet Week            -> ann-fleet-week
    "a-015",  # Italian Heritage Parade             -> ann-italian-heritage
    "a-016",  # Litquake                            -> ann-litquake
    "a-021",  # Sunday Streets                      -> rec-sunday-streets
    "a-022",  # Chinatown Autumn Moon Festival      -> ann-autumn-moon
    "a-026",  # Haight-Ashbury Street Fair          -> ann-haight-ashbury-fair
    # special
    "s-008",  # Treasures of the Pharaohs           -> spc-famssf-exhibitions
    "s-009",  # Eternal Paris                       -> spc-famssf-exhibitions
    "s-010",  # Miro: Proof Against All             -> spc-famssf-exhibitions
    "s-011",  # Bouquets to Art 2027                -> spc-bouquets-to-art
    "s-012",  # SuperNatural                        -> spc-supernatural
    "s-014",  # Castro Night Market: Halloween      -> spc-castro-halloween
}

# Category for each imported row, keyed by the parallel session's own id.
CATEGORY_BY_ORIG_ID = {
    "w-003": "markets",   # Heart of the City Farmers Market
    "w-005": "markets",   # Fillmore Farmers' Market
    "w-006": "markets",   # Noe Valley Farmers Market
    "w-007": "markets",   # Clement Street Farmers Market
    "w-008": "markets",   # Fort Mason Center Farmers' Market
    "w-009": "markets",   # Outer Sunset Farmers Market & Mercantile
    "w-010": "markets",   # Inner Sunset Flea Market
    "w-009": "markets",   # Outer Sunset Farmers Market & Mercantile
    "w-010": "markets",   # Inner Sunset Flea Market
    "w-011": "markets",   # Secondhand Saturdays
    "w-012": "markets",   # Alemany Flea Market
    "w-013": "markets",   # Downtown First Thursdays
    "w-014": "arts",      # Castro Art Mart
    "w-015": "community",  # Soulful Sundays
    "w-016": "community",  # Otsego Avenue Shared Space
    "w-017": "community",  # Larkin Street Tenderloin Shared Space
    "w-020": "markets",   # Off the Grid: Levi's Plaza
    "w-021": "markets",   # Off the Grid: Salesforce Tower
    "w-023": "arts",      # Golden Gate Park Band concerts
    "w-024": "markets",   # SF State Associated Students Farmers Market
    "w-025": "markets",   # North Beach Farmers Market
    "a-005": "arts",      # Fillmore Jazz Festival
    "a-007": "arts",      # Stern Grove Festival
    "a-008": "community",  # Pistahan Parade & Festival
    "a-013": "community",  # Hardly Strictly Bluegrass
    "a-017": "arts",      # SF Sketchfest
    "a-018": "arts",      # Noise Pop Festival
    "a-019": "markets",   # SF Beer Week
    "a-020": "markets",   # San Francisco Restaurant Week
    "a-023": "markets",   # San Francisco Greek Food Festival
    "a-024": "arts",      # Frameline
    "a-025": "community",  # Potrero Hill Festival
    "a-027": "community",  # Bearrison Street Fair
    "a-028": "community",  # Day of the Dead Festival of Altars
    "s-001": "arts", "s-002": "arts", "s-003": "arts", "s-004": "arts",
    "s-005": "arts", "s-006": "arts", "s-007": "arts",  # SFMOMA exhibitions
    "s-013": "arts",      # Glow: opening night (Exploratorium After Dark)
    "s-015": "markets",   # Diwali at the Outer Sunset Farmers Market
    "s-015": "markets",   # Diwali at the Outer Sunset Farmers Market
    "s-016": "community",  # Dia de los Muertos Outer Sunset
    "s-017": "markets",   # Sunset Holiday Mercantile
    "s-018": "community",  # Holidays on Taraval
    "s-019": "community",  # Cole Valley Nights
    "s-020": "arts", "s-021": "arts", "s-022": "arts", "s-023": "arts",  # Opera productions
    "s-020b": "arts",
    "s-024": "arts", "s-025": "arts",   # Symphony performances
    "s-026": "community",  # GDC Festival of Gaming 2027
    "s-027": "arts",      # Frameline50 Fall Showcase
    "s-028": "community",  # Dreamforce 2026
    "s-030": "arts",      # SFFILM Doc Stories 2026
    "s-031": "community",  # RSA Conference 2027
    "s-032": "community",  # Brava Block Party
    "s-033": "community",  # No Kings Rally
    "s-034": "sports",    # WNBA Finals: Valkyries vs Atlanta Dream
}


def _slug(text: str) -> str:
    text = re.sub(r"[^a-z0-9]+", "-", (text or "").lower()).strip("-")
    return text or "row"


def _norm(text: str) -> str:
    return re.sub(r"\s+", " ", (text or "").lower().strip())


def _tokens(text: str) -> set:
    return {t for t in re.findall(r"[a-z0-9]+", (text or "").lower()) if len(t) > 2}


def _similar(a: str, b: str) -> bool:
    ta, tb = _tokens(a), _tokens(b)
    if not ta or not tb:
        return False
    inter = len(ta & tb)
    return inter / min(len(ta), len(tb)) >= 0.72


def _load(name: str):
    path = os.path.join(DATA, name)
    if not os.path.exists(path):
        return None
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


def _neighbourhood_to_area(value: str) -> str:
    return value or "Citywide"


def _convert_weekly_or_annual(row: dict) -> dict:
    cadence = row.get("cadence", "")
    schedule = row.get("schedule", "")
    if schedule and cadence and cadence.lower() not in schedule.lower():
        schedule = f"{cadence} — {schedule}" if schedule else cadence
    elif not schedule:
        schedule = cadence

    if row.get("category") == "monthly":
        etype = "Recurring - Monthly"
        group = "recurring"
    elif row.get("category") == "annual":
        etype = "Annual"
        group = "annual"
    else:
        etype = "Recurring - Weekly"
        group = "recurring"

    dates = row.get("dates") or row.get("display_dates") or ""
    season = row.get("season") or ""
    if season and season.lower() not in ("year-round", "year round"):
        dates = (dates + " · " + season).strip(" ·")

    venue = row.get("venue", "")
    address = row.get("address", "")
    location = venue if not address else f"{venue}, {address}"

    unverified = row.get("unverified_fields") or []
    note = row.get("notes", "")
    note = (
        f"{note} ".strip()
        + f" Integrated from the parallel session {PARALLEL_SESSION} "
        "(branch arena/8fb52462-maltaproj6) during the final integration pass."
    ).strip()

    return {
        "id": "",
        "title": row.get("name", ""),
        "page": "",
        "type": etype,
        "group": group,
        "schedule": schedule,
        "dates": dates,
        "location": location,
        "area": _neighbourhood_to_area(row.get("neighborhood", "")),
        "cost": row.get("admission", ""),
        "organiser": row.get("organizer", ""),
        "source_name": row.get("source_title", "") or row.get("source_url", ""),
        "source_url": row.get("source_url", ""),
        "status": "verified" if not unverified else "unverified",
        "notes": note,
        "_unverified": unverified,
        "_orig_id": row.get("id", ""),
    }


def _convert_special(row: dict) -> dict:
    dates = row.get("display_dates") or ""
    if not dates and row.get("start_date"):
        dates = row["start_date"]
        if row.get("end_date") and row["end_date"] != row["start_date"]:
            dates = f"{row['start_date']} to {row['end_date']}"

    venue = row.get("venue", "")
    address = row.get("address", "")
    location = venue if not address else f"{venue}, {address}"

    unverified = row.get("unverified_fields") or []
    note = row.get("notes", "")
    note = (
        f"{note} ".strip()
        + f" Integrated from the parallel session {PARALLEL_SESSION} "
        "(branch arena/8fb52462-maltaproj6) during the final integration pass."
    ).strip()

    return {
        "id": "",
        "title": row.get("name", ""),
        "page": "",
        "type": "Special - Dated",
        "group": "special",
        "schedule": row.get("date_status", ""),
        "dates": dates,
        "location": location,
        "area": _neighbourhood_to_area(row.get("neighborhood", "")),
        "cost": row.get("admission", ""),
        "organiser": row.get("organizer", ""),
        "source_name": row.get("source_title", "") or row.get("source_url", ""),
        "source_url": row.get("source_url", ""),
        "status": "verified" if not unverified else "unverified",
        "notes": note,
        "_unverified": unverified,
        "_orig_id": row.get("id", ""),
    }


def parallel_events(existing) -> list:
    """Return the parallel session's rows that are not already in ``existing``."""
    existing_titles = [e.get("title", "") for e in existing]
    existing_ids = {e.get("id", "") for e in existing}
    out = []
    seen = set()

    for fname, converter in (("weekly.json", _convert_weekly_or_annual),
                              ("annual.json", _convert_weekly_or_annual),
                              ("special.json", _convert_special)):
        payload = _load(fname)
        if not payload:
            continue
        for row in payload.get("events", []):
            orig = row.get("id", "")
            if orig in SKIP_DUPLICATES:
                continue  # already covered by a row in data/events.py
            if orig in seen:
                continue
            seen.add(orig)

            title = row.get("name", "")
            if _norm(title) in {_norm(t) for t in existing_titles}:
                continue  # same event, identical title
            if _norm(title) in {_norm(e.get("title", "")) for e in out}:
                continue

            rec = converter(row)
            if not rec["source_url"].startswith("https://"):
                continue
            rec["id"] = f"x-{_slug(orig or rec['title'])}"
            if rec["id"] in existing_ids:
                continue
            rec["category"] = CATEGORY_BY_ORIG_ID.get(orig, "community")
            if rec["_unverified"]:
                rec["notes"] = (
                    f"Fields the parallel session could not confirm on the official page: "
                    f"{', '.join(rec['_unverified'])}. " + rec["notes"]
                )
            out.append(rec)
    return out


def parallel_flagged() -> list:
    """Return the parallel session's flagged items in this project's schema."""
    payload = _load("flagged.json")
    if not payload:
        return []
    out = []
    for item in payload.get("items", []):
        out.append(
            {
                "id": f"xflag-{_slug(item.get('id', ''))}",
                "title": f"{item.get('item', '')} — {item.get('kind', '')}",
                "detail": item.get("issue", ""),
                "source_name": f"Parallel session {PARALLEL_SESSION} · {item.get('kind', '')}",
                "source_url": item.get("evidence_url", ""),
                "action": item.get("action", ""),
            }
        )
    return out
