#!/usr/bin/env python3
"""Apply the confirmed corrections from AUDIT-2026-10-18-8e8e24dc.md.

This is the second revision of the script, re-based on `main` after PR #26
(arena-8cb2d3cc's final-integration pass). Rows that PR #26 already repaired
(California Museum removed, Conservatory hours, Battery Spencer scope, the
address de-duplication guard and the concluded-edition badge) are not touched
again. What remains are the defects that were still published on 2026-10-18:

    D-2   Contemporary Jewish Museum shown as open at 364 Ninth Street
    D-3   Presidio Museum and Visitor Center at 104 Montgomery Street
    D-4   SF Symphony listed at the War Memorial Opera House
    D-6   Haight-Ashbury Street Fair scheduled by a stale June rule
    D-8   "Quintana" typo and duplicated address fragment (x-w-011)
    D-10  semicolon ISO dates on six imported annual rows
    D-12  Bouquets to Art 2027 dates that the official page does not publish
    D-13  de Young "Open daily"
    D-14  Legion of Honor hours deferred to another page
    D-15  Exploratorium hours missing the Monday closure

Every replacement asserts that its anchor occurs exactly once, so the script
fails loudly instead of editing the wrong row.

Usage:
    python3 audit/apply_fixes_8e8e24dc.py
    python3 scripts/build_site.py
    python3 tools/validate.py
    python3 audit/check_8e8e24dc.py
"""
from __future__ import annotations

import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EVENTS = os.path.join(ROOT, "data", "events.py")
MERGE = os.path.join(ROOT, "scripts", "merge_parallel.py")


def replace_once(text: str, old: str, new: str, label: str) -> str:
    count = text.count(old)
    if count != 1:
        raise SystemExit(f"anchor for {label!r} occurs {count} times (expected 1)")
    return text.replace(old, new, 1)


def drop_event(text: str, event_id: str) -> str:
    pattern = re.compile(
        r"    dict\(\n        id=\"" + re.escape(event_id) + r"\".*?\n        notes=.*?\),\n",
        re.S,
    )
    matches = pattern.findall(text)
    if len(matches) != 1:
        raise SystemExit(f"expected exactly one block for {event_id}, found {len(matches)}")
    return pattern.sub("", text, count=1)


# --------------------------------------------------------------------------
# dataset corrections
# --------------------------------------------------------------------------

SYMPHONY_OLD = """        dates="", location="War Memorial Opera House, 301 Van Ness Avenue (and Davies Symphony Hall)", area="Civic Center / South of Market",
"""
SYMPHONY_NEW = """        dates="", location="Davies Symphony Hall, 201 Van Ness Avenue (main entrance at 249 Grove Street)", area="Civic Center / South of Market",
"""

SYMPHONY_NOTES_OLD = """        notes="2026-27 season calendar confirmed through August 2027 on the official site."),
"""
SYMPHONY_NOTES_NEW = """        notes="Venue confirmed 2026-10-18 by arena-8e8e24dc on the Symphony's Getting Here page and 2026-27 season calendar: all concerts are at Davies Symphony Hall, 201 Van Ness Avenue (main entrance and box office at 249 Grove Street). The War Memorial Opera House is the home of San Francisco Opera and San Francisco Ballet. Season confirmed through August 2027."),
"""

HAIGHT_OLD = """        schedule="Annual street fair on the second Sunday in June, 11:00 a.m.-5:30 p.m.",
        dates="Sunday, September 20, 2026",
        location="Haight Street (five blocks closed, Masonic to Stanyan)", area="Haight-Ashbury / Upper Haight",
        cost="Free", organiser="Haight-Ashbury Street Fair (501(c)(3) non-profit)",
        source_name="Haight-Ashbury Street Fair — official site",
        source_url="https://www.haightashburystreetfair.org/", status="verified",
        notes=""),
"""
HAIGHT_NEW = """        schedule="Annual street fair; the 2026 edition ran Sunday, September 20, 11:00 a.m.-5:30 p.m. (the organiser's About page still says 'second Sunday in June')",
        dates="Sunday, September 20, 2026",
        location="Haight Street (five blocks closed, Masonic to Stanyan)", area="Haight-Ashbury / Upper Haight",
        cost="Free", organiser="Haight-Ashbury Street Fair (501(c)(3) non-profit)",
        source_name="Haight-Ashbury Street Fair — official site",
        source_url="https://www.haightashburystreetfair.org/", status="verified",
        notes="Re-verified 2026-10-18 by arena-8e8e24dc: the organiser's own 2026 vendor page gives 'Event Date: Sunday, September 20, 2026', and SFMTA's event page confirms Sunday 20 September 2026, 11 a.m.-5:30 p.m., Haight Street between Masonic and Stanyan (https://www.sfmta.com/travel-updates/haight-ashbury-street-fair-sunday-september-20-2026). The About page's 'second Sunday in June' rule is stale copy, recorded on Flagged for Review."),
"""

BOUQUETS_OLD = """        id="spc-bouquets-to-art", title="Bouquets to Art 2027",
        page="special", type="Special - Dated",
        schedule="", dates="March 2-7, 2027",
        location="de Young Museum and Legion of Honor, Golden Gate Park", area="Richmond / Sunset",
        cost="Ticketed", organiser="Fine Arts Museums of San Francisco (FAMSF)",
        source_name="FAMSF — Bouquets to Art 2027",
        source_url="https://www.famsf.org/exhibitions/bouquets-to-art-2027", status="verified",
        notes="Annual floral-design exhibition staged throughout both museums."),
"""
BOUQUETS_NEW = """        id="spc-bouquets-to-art", title="Bouquets to Art 2027",
        page="special", type="Special - Dated",
        schedule="", dates="",
        location="de Young Museum and Legion of Honor, Golden Gate Park", area="Richmond / Sunset",
        cost="Ticketed", organiser="Fine Arts Museums of San Francisco (FAMSF)",
        source_name="FAMSF — Bouquets to Art 2027",
        source_url="https://www.famsf.org/exhibitions/bouquets-to-art-2027", status="unverified",
        notes="The 2027 page confirms the 43rd exhibition and that the Legion of Honor is included, but publishes no dates. The previously listed March 2-7, 2027 could not be confirmed anywhere on the official site and was removed rather than inferred (the page's only dated material is the 2026 opening-night photograph)."),
"""

DEYOUNG_OLD = """        id="art-deyoung", title="de Young Museum",
        page="arts", type="Attraction - Open regularly",
        schedule="Open daily (see official tickets + hours page for current hours and free-admission days)",
        dates="", location="50 Hagiwara Tea Garden Drive, Golden Gate Park, 94118", area="Richmond / Sunset",
        cost="Ticketed; free on designated days (first Tuesday of the month)",
        organiser="Fine Arts Museums of San Francisco (FAMSF)",
        source_name="FAMSF — de Young",
        source_url="https://www.famsf.org/visit/de-young", status="verified",
        notes="Free + reduced admission details: https://www.famsf.org/visit/free-reduced-admission"),
"""
DEYOUNG_NEW = """        id="art-deyoung", title="de Young Museum",
        page="arts", type="Attraction - Open regularly",
        schedule="Tuesday-Sunday 9:30 a.m.-5:15 p.m.; closed Mondays, Presidents' Day, Indigenous Peoples' Day, Thanksgiving and Christmas Day",
        dates="", location="50 Hagiwara Tea Garden Drive, Golden Gate Park, 94118", area="Richmond / Sunset",
        cost="Adults $25; seniors 65+ $22; students $10; youth 17 and under free; free general admission on the first Tuesday of every month (permanent collection) and at 4:30 p.m. daily",
        organiser="Fine Arts Museums of San Francisco (FAMSF)",
        source_name="FAMSF — de Young tickets + hours",
        source_url="https://www.famsf.org/visit/de-young-tickets-hours", status="verified",
        notes="Corrected 2026-10-18 by arena-8e8e24dc: the previous schedule said 'Open daily', but the museum is closed Mondays. Free + reduced admission details: https://www.famsf.org/visit/free-reduced-admission"),
"""

LEGION_OLD = """        id="art-legion-honor", title="Legion of Honor",
        page="arts", type="Attraction - Open regularly",
        schedule="Open regularly (see official tickets + hours page for current hours)",
        dates="", location="100 34th Avenue, Golden Gate Park, 94123", area="Richmond / Sunset",
        cost="Ticketed; free on designated days",
        organiser="Fine Arts Museums of San Francisco (FAMSF)",
        source_name="FAMSF — Legion of Honor",
        source_url="https://www.famsf.org/visit/legion-of-honor", status="verified",
        notes=""),
"""
LEGION_NEW = """        id="art-legion-honor", title="Legion of Honor",
        page="arts", type="Attraction - Open regularly",
        schedule="Tuesday-Sunday 9:30 a.m.-5:15 p.m.; closed Mondays, Martin Luther King Jr. Day, Labor Day, Indigenous Peoples' Day, Thanksgiving and Christmas Day",
        dates="", location="100 34th Avenue, Golden Gate Park, 94123", area="Richmond / Sunset",
        cost="Adults $25; seniors 65+ $22; students $10; youth 17 and under free; free general admission on the first Tuesday of every month (permanent collection) and at 4:30 p.m. daily",
        organiser="Fine Arts Museums of San Francisco (FAMSF)",
        source_name="FAMSF — Legion of Honor tickets + hours",
        source_url="https://www.famsf.org/visit/legion-tickets-hours", status="verified",
        notes="Hours and prices added 2026-10-18 by arena-8e8e24dc from the museum's tickets + hours page; the previous schedule said only 'Open regularly'."),
"""

EXPLO_OLD = """        id="art-explatorium", title="Exploratorium",
        page="arts", type="Attraction - Open regularly",
        schedule="Open regularly; Thursday evenings are After Dark (18+); Sunday mornings are members-only until noon",
        dates="", location="200 Pier 15, San Francisco, CA 94102", area="Embarcadero / South Beach",
        cost="Ticketed", organiser="Exploratorium",
        source_name="Exploratorium — Upcoming Events Calendar",
        source_url="https://www.exploratorium.edu/visit/calendar", status="verified",
        notes=""),
"""
EXPLO_NEW = """        id="art-explatorium", title="Exploratorium",
        page="arts", type="Attraction - Open regularly",
        schedule="Sunday 12:00-5:00 p.m. (members-only 10:00 a.m.-noon); Monday closed; Tuesday-Saturday 10:00 a.m.-5:00 p.m.; Thursday 6:00-10:00 p.m. After Dark (18+)",
        dates="", location="200 Pier 15, San Francisco, CA 94102", area="Embarcadero / South Beach",
        cost="Ticketed", organiser="Exploratorium",
        source_name="Exploratorium — Plan Your Visit",
        source_url="https://www.exploratorium.edu/visit", status="verified",
        notes="Hours added 2026-10-18 by arena-8e8e24dc from the official Plan Your Visit page; the previous schedule did not state the Monday closure or the noon Sunday opening."),
"""

PRESIDIO_OLD = """        id="art-presidio-museum", title="Presidio Museum and Visitor Center",
        page="arts", type="Attraction - Open regularly",
        schedule="Open regularly; free museum admission",
        dates="", location="104 Montgomery Street, Presidio of San Francisco, 94129", area="Presidio",
        cost="Free", organiser="Presidio Trust",
        source_name="Presidio — Things To Do",
        source_url="https://presidio.gov/explore", status="verified",
        notes=""),
"""
PRESIDIO_NEW = """        id="art-presidio-museum", title="Presidio Visitor Center",
        page="arts", type="Attraction - Open regularly",
        schedule="Open daily 10:00 a.m.-5:00 p.m.; closed Thanksgiving, Christmas and New Year's Day",
        dates="", location="210 Lincoln Boulevard, Presidio of San Francisco, CA 94129", area="Presidio",
        cost="Free", organiser="Presidio Trust",
        source_name="Presidio Trust — Presidio Visitor Center",
        source_url="https://presidio.gov/explore/attractions/presidio-visitor-center", status="verified",
        notes="Corrected 2026-10-18 by arena-8e8e24dc: the row previously listed '104 Montgomery Street', which is the separate Walt Disney Family Museum (its own row). The Trust's visitor-center page gives 210 Lincoln Boulevard and daily 10-5 hours."),
"""

DATASET_EDITS = [
    ("rec-sfsymphony venue", SYMPHONY_OLD, SYMPHONY_NEW),
    ("rec-sfsymphony notes", SYMPHONY_NOTES_OLD, SYMPHONY_NOTES_NEW),
    ("ann-haight-ashbury-fair", HAIGHT_OLD, HAIGHT_NEW),
    ("spc-bouquets-to-art", BOUQUETS_OLD, BOUQUETS_NEW),
    ("art-deyoung", DEYOUNG_OLD, DEYOUNG_NEW),
    ("art-legion-honor", LEGION_OLD, LEGION_NEW),
    ("art-explatorium", EXPLO_OLD, EXPLO_NEW),
    ("art-presidio-museum", PRESIDIO_OLD, PRESIDIO_NEW),
]

NEW_FLAGS = [
    {
        "id": "flag-cjm-temporarily-closed",
        "title": "Contemporary Jewish Museum removed — temporarily closed since 15 December 2024 and the published address was wrong",
        "detail": "The museum's own homepage says 'THE CJM IS TEMPORARILY CLOSED'. Its 13 November 2024 notice says the galleries closed on 15 December 2024 for a period of at least one year, described as a strategic pause rather than a permanent closure. The published row described the museum as open regularly and gave '364 Ninth Street'; the museum's contact page gives 736 Mission Street, San Francisco, CA 94103 (415-655-7800). The row was removed from the open-attractions list rather than advertised as a visitable venue.",
        "source_name": "The CJM — A Message to Our Community",
        "source_url": "https://www.thecjm.org/pages/621",
        "action": "Monitor thecjm.org; re-add when the museum announces a reopening date and published hours. Use 736 Mission Street.",
    },
    {
        "id": "flag-presidio-visitor-center-address",
        "title": "Presidio Visitor Center — corrected address (104 Montgomery Street is the Walt Disney Family Museum)",
        "detail": "The row previously read 'Presidio Museum and Visitor Center, 104 Montgomery Street'. The Presidio Trust's own visitor-center page gives 210 Lincoln Boulevard, San Francisco, CA 94129, open daily 10 a.m.-5 p.m. except Thanksgiving, Christmas and New Year's Day, free admission. 104 Montgomery Street is the separate Walt Disney Family Museum, which already has its own row.",
        "source_name": "Presidio Trust — Presidio Visitor Center",
        "source_url": "https://presidio.gov/explore/attractions/presidio-visitor-center",
        "action": "Correction applied to the row; no further action unless the Trust changes the address or hours.",
    },
    {
        "id": "flag-sfsymphony-venue",
        "title": "San Francisco Symphony — wrong venue corrected to Davies Symphony Hall",
        "detail": "The row previously said the Symphony performs at the War Memorial Opera House, 301 Van Ness Avenue (and Davies Symphony Hall). The Symphony's Getting Here page and its 2026-27 season calendar both state that all concerts are at Davies Symphony Hall, 201 Van Ness Avenue; the main entrance and box office are at 249 Grove Street. The War Memorial Opera House is the home of San Francisco Opera and San Francisco Ballet.",
        "source_name": "San Francisco Symphony — Getting Here",
        "source_url": "https://www.sfsymphony.org/YourVisit/Getting-Here",
        "action": "Correction applied to the row.",
    },
    {
        "id": "flag-haight-june-copy",
        "title": "Haight-Ashbury Street Fair — organiser's About page still says 'second Sunday in June' while the 2026 edition ran 20 September",
        "detail": "The organisers' About page says the fair is 'held every second Sunday in June'. Their own 2026 vendor page gives 'Event Date: Sunday, September 20, 2026', and SFMTA's event page confirms Sunday 20 September 2026, 11 a.m.-5:30 p.m., Haight Street between Masonic and Stanyan. The published schedule now records the 2026 date; the About-page copy is kept on record as a discrepancy rather than silently preferred.",
        "source_name": "SFMTA — Haight Ashbury Street Fair: Sunday, September 20, 2026",
        "source_url": "https://www.sfmta.com/travel-updates/haight-ashbury-street-fair-sunday-september-20-2026",
        "action": "Ask the organiser to update the About page. For future editions, use the dated vendor/SFMTA notice rather than the general June rule.",
    },
    {
        "id": "flag-bouquets-2027-dates",
        "title": "Bouquets to Art 2027 — the March 2-7, 2027 dates published earlier could not be confirmed",
        "detail": "The FAMSF page for Bouquets to Art 2027 describes the 43rd exhibition, its opening-night reception and the inclusion of the Legion of Honor, but publishes no dates. The row previously stated 'March 2-7, 2027' with a verified badge; that date is not published anywhere on the official page and has been removed rather than inferred.",
        "source_name": "FAMSF — Bouquets to Art 2027",
        "source_url": "https://www.famsf.org/exhibitions/bouquets-to-art-2027",
        "action": "Watch the FAMSF page or press release for the 2027 dates, then fill them from the official announcement.",
    },
    {
        "id": "flag-secondhand-block",
        "title": "Secondhand Saturdays — two official sources disagree on the 37th Avenue block",
        "detail": "Sunset Mercantile publishes '37th Avenue at Ortega to Quintara' for Secondhand Saturdays; SFMTA's Shared Spaces list publishes '37th Avenue from Ortega to Pacheco streets' for the same permitted closure. The row previously misspelled 'Quintara' as 'Quintana' and repeated a second address fragment. The spelling and the duplicated fragment are corrected; the block conflict is recorded here rather than resolved by inference.",
        "source_name": "SFMTA — Shared Spaces",
        "source_url": "https://www.sfmta.com/projects/shared-spaces",
        "action": "Ask Sunset Mercantile or SFMTA to confirm the southern end of the closure. Until then, both official versions are recorded.",
    },
]

FLAGS_END = """]

# ---------------------------------------------------------------------------
# Two orthogonal views of the same dataset.
"""

MERGE_OVERRIDE_009_OLD = """    "w-009": {
        "_clear_unverified": True,
        "schedule": "Sundays, 9:00 a.m.-2:00 p.m., rain or shine",
"""
MERGE_OVERRIDE_009_NEW = """    "w-009": {
        "_clear_unverified": True,
        "location": "37th Avenue at Ortega to Quintara",
        "schedule": "Sundays, 9:00 a.m.-2:00 p.m., rain or shine",
"""

MERGE_OVERRIDE_011_OLD = """    "w-011": {
        "_clear_unverified": True,
        "schedule": "Third Saturdays, 10:00 a.m.-4:00 p.m. (returning April-November 2026)",
"""
MERGE_OVERRIDE_011_NEW = """    "w-011": {
        "_clear_unverified": True,
        "location": "37th Avenue at Ortega to Quintara",
        "schedule": "Third Saturdays, 10:00 a.m.-4:00 p.m. (returning April-November 2026)",
"""

DATES_OLD = """    dates = row.get("dates") or row.get("display_dates") or ""
"""
DATES_NEW = """    dates = row.get("display_dates") or row.get("dates") or ""
"""


def flag_source(flag: dict) -> str:
    return (
        "    dict(\n"
        f"        id={flag['id']!r}, title={flag['title']!r},\n"
        f"        detail={flag['detail']!r},\n"
        f"        source_name={flag['source_name']!r},\n"
        f"        source_url={flag['source_url']!r},\n"
        f"        action={flag['action']!r}),\n"
    )


def main() -> int:
    src = open(EVENTS, encoding="utf-8").read()

    src = drop_event(src, "art-cjm")
    for label, old, new in DATASET_EDITS:
        src = replace_once(src, old, new, label)

    added = []
    for flag in NEW_FLAGS:
        if f'id="{flag["id"]}"' in src:
            continue
        src = replace_once(src, FLAGS_END, flag_source(flag) + FLAGS_END, flag["id"])
        added.append(flag["id"])
    open(EVENTS, "w", encoding="utf-8").write(src)

    merge = open(MERGE, encoding="utf-8").read()
    merge = replace_once(merge, MERGE_OVERRIDE_009_OLD, MERGE_OVERRIDE_009_NEW, "w-009 location")
    merge = replace_once(merge, MERGE_OVERRIDE_011_OLD, MERGE_OVERRIDE_011_NEW, "w-011 location")
    merge = replace_once(merge, DATES_OLD, DATES_NEW, "human-readable dates")
    open(MERGE, "w", encoding="utf-8").write(merge)

    print(f"removed art-cjm; edited {len(DATASET_EDITS)} rows; added {len(added)} flags")
    print("next: python3 scripts/build_site.py && python3 tools/validate.py && python3 audit/check_8e8e24dc.py")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
