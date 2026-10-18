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
    "s-026": "technology",  # GDC Festival of Gaming 2027
    "s-027": "arts",      # Frameline50 Fall Showcase
    "s-028": "community",  # Dreamforce 2026
    "s-030": "arts",      # SFFILM Doc Stories 2026
    "s-031": "community",  # RSA Conference 2027
    "s-032": "community",  # Brava Block Party
    "s-033": "community",  # No Kings Rally
    "s-034": "sports",    # WNBA Finals: Valkyries vs Atlanta Dream
}


# Corrections applied to imported rows by the 2026-10-18 audit session
# (arena-bdaa17b4). The parallel session's raw JSON files are NOT edited;
# each correction states the official source that overrules the imported
# value, and is also published on the Flagged for Review page.
AUDIT_CORRECTIONS = {
    # Manon: imported as "October 18 - November 1, 2026" from the sfopera.com
    # homepage. SF Opera's official 2026-27 season announcement (fetched
    # 2026-10-18) lists Manon as October 15 - November 1, 2026, matching this
    # dataset's own art-sfopera season row; the other imported opera rows
    # already match that announcement exactly.
    # SFMOMA's current "What's On View" page (fetched 2026-10-18): RM x SFMOMA
    # opened Oct 3, 2026 on Floor 7; Sarah Sze opens Nov 21, 2026 on Floor 1
    # (the free ground-floor galleries). Neither page lists a closing date.
    "s-005": {
        "_clear_unverified": True,
        "dates": "Opened Saturday, October 3, 2026 (closing date not listed by the museum)",
        "cost": "",
        "notes": "Re-verified 2026-10-18 by session arena-8cb2d3cc against SFMOMA's exhibitions page, which places 'RM x SFMOMA: Between You and Me' on Floor 7 and dates it 'Opened Oct 3'. No closing date and no separate ticket price are published, so the closing date and cost cells are left blank rather than inferred from the museum's general admission.",
    },
    "s-007": {
        "_clear_unverified": True,
        "dates": "Opens Saturday, November 21, 2026 (closing date not listed by the museum)",
        "cost": "Free (Floor 1 galleries)",
        "notes": "Re-verified 2026-10-18 by session arena-8cb2d3cc against SFMOMA's exhibitions page, which announces 'Sarah Sze: Forever is Composed of Nows' opening November 21, 2026 on Floor 1 — the museum's free-to-enter ground-floor galleries. The closing date is not published, so it is left blank.",
    },
    "s-020": {
        "dates": "October 15 - November 1, 2026",
        "source_name": "San Francisco Opera - 2026-27 season announcement",
        "source_url": "https://www.sfopera.com/press/press-releases/San-Francisco-Opera-2026-27-season/",
        "_correction_note": (
            "AUDIT CORRECTION (arena-bdaa17b4, 2026-10-18): start date corrected from "
            "October 18 to October 15, 2026 per SF Opera's official season announcement; "
            "source upgraded from the sfopera.com homepage to that announcement. "
            "The parallel session's raw data/special.json is unchanged."
        ),
    },
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


def _join_venue(venue: str, address: str) -> str:
    """Join venue and address without repeating the same text twice.

    The parallel session's raw rows sometimes carry the full address in both
    fields, which previously produced cells like
    "100 Alemany Boulevard, 100 Alemany Boulevard".
    """
    venue = (venue or "").strip().strip(",")
    address = (address or "").strip().strip(",")
    if not address:
        return venue
    if not venue:
        return address
    if _norm(venue) == _norm(address) or _norm(address).startswith(_norm(venue)):
        return address
    if _norm(venue).startswith(_norm(address)):
        return venue
    return f"{venue}, {address}"


def _neighbourhood_to_area(value: str) -> str:
    return value or "Citywide"


_MONTHS = ["January", "February", "March", "April", "May", "June", "July",
           "August", "September", "October", "November", "December"]


def _humanize_dates(value: str) -> str:
    """Render semicolon-separated ISO dates as readable prose.

    The parallel session stored multi-day runs as ``2026-10-02;2026-10-03;
    2026-10-04``. Only the formatting changes here; the dates themselves are
    carried over exactly, and anything that is not a pure ISO list is returned
    untouched.
    """
    value = (value or "").strip()
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}(;\d{4}-\d{2}-\d{2})*", value):
        return value
    parts = []
    for token in value.split(";"):
        year, month, day = (int(part) for part in token.split("-"))
        parts.append((year, month, day))
    parts.sort()
    first, last = parts[0], parts[-1]
    if len(parts) == 1:
        return f"{_MONTHS[first[1] - 1]} {first[2]}, {first[0]}"
    same_month = first[0] == last[0] and first[1] == last[1]
    if same_month:
        return f"{_MONTHS[first[1] - 1]} {first[2]}-{last[2]}, {first[0]}"
    if first[0] == last[0]:
        return (f"{_MONTHS[first[1] - 1]} {first[2]} - "
                f"{_MONTHS[last[1] - 1]} {last[2]}, {first[0]}")
    return (f"{_MONTHS[first[1] - 1]} {first[2]}, {first[0]} - "
            f"{_MONTHS[last[1] - 1]} {last[2]}, {last[0]}")


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

    dates = _humanize_dates(row.get("dates") or row.get("display_dates") or "")
    season = row.get("season") or ""
    if season and season.lower() not in ("year-round", "year round"):
        dates = (dates + " · " + season).strip(" ·")

    location = _join_venue(row.get("venue", ""), row.get("address", ""))

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

    location = _join_venue(row.get("venue", ""), row.get("address", ""))

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
        # date_status is metadata, not a human-readable schedule. A special
        # event's Schedule cell is populated only from an explicit schedule.
        "schedule": row.get("schedule", ""),
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


# Corrections applied to imported rows during the 2026-10-18 line-by-line
# re-verification pass (session arena-23722ef3). The parallel session's raw
# files are left untouched as its record; only the published union row is
# corrected, with the reason appended to its notes.
FIELD_OVERRIDES = {
    # SF Opera "Manon": the official homepage states "Manon opens October 15";
    # the performance list (as of 2026-10-18) shows Oct 18, 21, 24, 27, 30 +
    # Nov 1. The run is October 15 - November 1, 2026.
    # Re-verified 2026-10-18 by session arena-8cb2d3cc against each organiser's
    # own page. Blank where the official page does not state the value.
    "w-003": {
        "_clear_unverified": True,
        "schedule": "Wednesdays and Sundays, 7:00 a.m.-4:00 p.m.",
        "notes": "Re-verified 2026-10-18 by session arena-8cb2d3cc: the market's official homepage states 'Sundays 7am-4pm Wednesdays 7am-4pm' at Fulton and Larkin Streets. Season is not stated on the page and remains blank.",
    },
    "w-007": {
        "_clear_unverified": True,
        "schedule": "Sundays, 9:00 a.m.-2:00 p.m., rain or shine",
        "notes": "Re-verified 2026-10-18 by session arena-8cb2d3cc: the Agricultural Institute of Marin page states every Sunday 9am-2pm at 244 Clement St. Season is not stated on the page and remains blank.",
    },
    "w-008": {
        "_clear_unverified": True,
        "schedule": "Sundays, 9:30 a.m.-1:30 p.m.",
        "notes": "Re-verified 2026-10-18 by session arena-8cb2d3cc: the market association's page states every Sunday 9:30am-1:30pm at Fort Mason Center, Marina Blvd. Season is not stated on the page and remains blank.",
    },
    "w-009": {
        "_clear_unverified": True,
        "location": "37th Avenue at Ortega to Quintara",
        "schedule": "Sundays, 9:00 a.m.-2:00 p.m., rain or shine",
        "notes": "Re-verified 2026-10-18 by session arena-8cb2d3cc: Sunset Mercantile's official site lists the Outer Sunset Farmers Market & Mercantile as Sundays, rain or shine, 9am-2pm, 37th Avenue at Ortega to Quintara. Season is not stated on the page and remains blank.",
    },
    "w-010": {
        "_clear_unverified": True,
        "schedule": "Second Sundays, 10:00 a.m.-4:00 p.m. (returning April-November 2026)",
        "dates": "April-November 2026",
        "notes": "Re-verified 2026-10-18 by session arena-8cb2d3cc: Sunset Mercantile's site states second Sundays, returning April-November 2026, 10am-4pm, Irving Street at 9th-11th Avenues. Admission is not stated on the page and remains blank.",
    },
    "w-011": {
        "_clear_unverified": True,
        "location": "37th Avenue at Ortega to Quintara",
        "schedule": "Third Saturdays, 10:00 a.m.-4:00 p.m. (returning April-November 2026)",
        "dates": "April-November 2026",
        "notes": "Re-verified 2026-10-18 by session arena-8cb2d3cc: Sunset Mercantile's site states third Saturdays, returning April-November 2026, 10am-4pm, 37th Avenue at Ortega to Quintara. Admission is not stated on the page and remains blank.",
    },
    "w-012": {
        "_clear_unverified": True,
        "schedule": "Sundays, 7:00 a.m.-3:00 p.m.",
        "notes": "Re-verified 2026-10-18 by session arena-8cb2d3cc: SF.gov's location page gives Sunday 7:00am-3:00pm at 100 Alemany Boulevard, with free on-site parking. Season and admission are not stated and remain blank.",
    },
    "w-013": {
        "_clear_unverified": True,
        "schedule": "First Thursday of each month, 5:00-10:00 p.m., rain or shine",
        "dates": "January-December 2026 season",
        "source_name": "Downtown First Thursdays — 2026 season announcement",
        "source_url": "https://www.dftsf.com/blog/dft2026renewal",
        "notes": "Re-verified 2026-10-18 by session arena-8cb2d3cc: the organiser's own announcement states a 12-month season from January to December 2026, every first Thursday, 5-10pm, on 2nd Street between Market and Howard Streets.",
    },
    "w-020": {
        "_clear_unverified": True,
        "schedule": "Weekdays (Monday-Friday), 11:00 a.m.-2:00 p.m.",
        "notes": "Re-verified 2026-10-18 by session arena-8cb2d3cc: Off the Grid's site listed Levi's Plaza at 1155 Battery Street, 11am-2pm, on each weekday of the week of October 19, 2026. Admission and season are not stated and remain blank.",
    },
    "w-021": {
        "_clear_unverified": True,
        "schedule": "Weekdays (Monday-Friday), 11:00 a.m.-2:00 p.m.",
        "notes": "Re-verified 2026-10-18 by session arena-8cb2d3cc: Off the Grid's site listed Salesforce Tower at 415 Mission Street, 11am-2pm, on each weekday of the week of October 19, 2026. Admission and season are not stated and remain blank.",
    },
    "w-023": {
        "_clear_unverified": True,
        "schedule": "Sundays at 1:00 p.m., April-September season (plus July 4 and Labor Day)",
        "dates": "April-September 2026 season (144th season)",
        "cost": "Free",
        "notes": "Re-verified 2026-10-18 by session arena-8cb2d3cc: the band's official site states the season runs April through September with free Sunday concerts at 1pm at the Spreckels Temple of Music, plus July 4 and Labor Day.",
    },
    "w-024": {
        "_clear_unverified": True,
        "schedule": "Thursdays, 10:00 a.m.-3:00 p.m., during fall and spring semesters",
        "notes": "Re-verified 2026-10-18 by session arena-8cb2d3cc: asi.sfsu.edu states the market runs every Thursday 10am-3pm; parking is $10. Admission is not stated on the page and remains blank.",
    },
    "w-025": {
        "_clear_unverified": True,
        "schedule": "Saturdays, 9:00 a.m.-2:00 p.m.",
        "notes": "Re-verified 2026-10-18 by session arena-8cb2d3cc: the market's official site states every Saturday 9am-2pm at 725 Greenwich Street, between Columbus and Powell. Season is not stated on the page and remains blank; the SF Environment listing of 659 Columbus Avenue, May-November, remains a recorded conflict.",
    },
    "s-031": {
        "_clear_unverified": True,
        "dates": "April 5-8, 2027",
        "cost": "Ticketed (registration and passes)",
        "source_name": "RSA Conference — official site (RSAC 2027)",
        "source_url": "https://www.rsaconference.com/usa",
        "notes": "Re-verified 2026-10-18 by session arena-8cb2d3cc: the official RSAC 2027 page states April 5-8, 2027, San Francisco, and the FAQ gives the venue as the Moscone Center and Yerba Buena Center for the Arts.",
    },
    "a-007": {
        "_clear_unverified": True,
        "notes": "Re-verified 2026-10-18 by session arena-8cb2d3cc: the official site says 'Thank you for an amazing 2026 season. See you next summer for our 90th season!' No 2027 dates are published, so the dates cell stays blank rather than inferred.",
    },
    "a-018": {
        "_clear_unverified": True,
        "cost": "Ticketed (festival passes from $240, per the organiser)",
        "notes": "Re-verified 2026-10-18 by session arena-8cb2d3cc: the official homepage lists Noise Pop Festival 2027 on February 18, 2027, in San Francisco, with tickets from $240. The end date is not stated on the page, so only the confirmed start date is shown.",
    },
    "s-026": {
        "_clear_unverified": True,
        "cost": "Early-rate passes through Dec 11, 2026: Festival Hall-only $175; Business Hall-only $125; 1-Day Career $125; Indie/Start-Up/Academic $299; Festival pass $549; Game Changer $1,249. Later rates increase.",
        "source_name": "GDC Festival of Gaming — Passes & Pricing",
        "source_url": "https://gdconf.com/passes-pricing/",
        "notes": "Re-verified 2026-10-18 against the organizer's official pricing page. It lists March 1-5, 2027 at Moscone Center, San Francisco, with the current Early Rate prices shown here (registration by Dec 11, 2026); later rates are listed separately and increase. No free admission is advertised on the source page.",
    },
    "s-020": {
        "dates": "October 15 - November 1, 2026 (opens October 15)",
        "_override_note": (
            "Corrected 2026-10-18 by session arena-23722ef3: the run start was "
            "changed to October 15 per the official banner 'Manon opens October 15' "
            "(https://www.sfopera.com/); the parallel record said 'October 18 - "
            "November 1, 2026', which matched only the remaining listed performances."
        ),
    },
    "s-034": {
        "title": "WNBA Finals: Valkyries vs Atlanta Dream (Chase Center games)",
        "dates": "Game 1 Saturday, October 17, 2026 (final: Valkyries 68, Dream 64); Game 2 Monday, October 19, 2026, 5:00 p.m. PT; Games 5 (October 26) and 7 (October 31) would also be at Chase Center if the series runs that long",
        "schedule": "WNBA Finals (best-of-seven); Chase Center hosts Games 1, 2 and, if necessary, 5 and 7 — Games 3 (October 21), 4 (October 24) and 6 (October 29) are at Atlanta",
        "source_name": "Golden State Valkyries — official site (WNBA Finals schedule)",
        "source_url": "https://valkyries.wnba.com/",
        "notes": "Re-verified 2026-10-18 by session arena-91296e94 against the team's official site: Game 1 final (ATL 64 @ GSV 68, Golden State leads 1-0); Game 2 Monday, October 19 at 8:00 p.m. EDT (Atlanta Dream @ Golden State Valkyries); the Finals carousel lists Games 3 and 4 at Atlanta and Games 5 and 7, if necessary, at Chase Center. Replaces the earlier SFMTA traffic-advisory citation.",
    },
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
            clear_from_audit = False
            if orig in AUDIT_CORRECTIONS:
                fix = AUDIT_CORRECTIONS[orig]
                for key, value in fix.items():
                    if not key.startswith("_"):
                        rec[key] = value
                if fix.get("_correction_note"):
                    rec["notes"] = (fix["_correction_note"] + " " + rec["notes"]).strip()
                clear_from_audit = bool(fix.get("_clear_unverified"))
            rec["category"] = CATEGORY_BY_ORIG_ID.get(orig, "community")
            if rec["_unverified"]:
                rec["notes"] = (
                    f"Fields the parallel session could not confirm on the official page: "
                    f"{', '.join(rec['_unverified'])}. " + rec["notes"]
                )
            if clear_from_audit:
                rec["_unverified"] = []
                rec["status"] = "verified"
                rec["notes"] = re.sub(
                    r"^Fields the parallel session could not confirm on the official page: [^.]+\.\s*",
                    "",
                    rec["notes"],
                )
            override = FIELD_OVERRIDES.get(orig)
            if override:
                note = override.get("_override_note", "")
                for key, value in override.items():
                    if key in ("_override_note", "_clear_unverified"):
                        continue
                    rec[key] = value
                if note:
                    rec["notes"] = (rec["notes"] + " " + note).strip()
                if override.get("_clear_unverified"):
                    rec["_unverified"] = []
                    rec["status"] = "verified"
                    rec["notes"] = re.sub(
                        r"^Fields the parallel session could not confirm on the official page: [^.]+\.\s*",
                        "",
                        rec["notes"],
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
        # f-038 duplicates the canonical Assessment Appeals Board timing flag;
        # the canonical item now records the conflicting current department and
        # citywide calendars. Keep the preserved source JSON unchanged.
        if item.get("id") == "f-038":
            continue
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
