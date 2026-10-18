#!/usr/bin/env python3
"""Integration apply-script for session arena-91296e94 (2026-10-18).

Applies the source-supported corrections and additions from
audit/AUDIT-2026-10-18-91296e94.md + data/gap-candidates-91296e94.json to the
canonical dataset. Idempotent: every step checks whether it already ran.
Run from the repository root:  python3 audit/apply_integration_91296e94.py
Then rebuild:                  python3 scripts/build_site.py
                               python3 tools/validate.py
"""
from __future__ import annotations

import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EVENTS_PY = os.path.join(ROOT, "data", "events.py")
MERGE_PY = os.path.join(ROOT, "scripts", "merge_parallel.py")

NEW_ROWS = '''    dict(
        id="spc-techcrunch-disrupt-2026", title="TechCrunch Disrupt 2026",
        page="special", type="Special - Dated",
        schedule="Three-day startup and AI conference (the 2026 edition ran October 13-15; the organiser's page now invites the 2027 waitlist)",
        dates="October 13-15, 2026 (concluded)",
        location="Moscone West, 800 Howard Street, San Francisco", area="SoMa",
        cost="Standard passes: Attendee $1,049; Founder $1,099; Investor $1,199; Non-Profit $499; Student $399; Expo+ $349 (final-day discounted prices $262/$275/$300/$125/$100/$87 were live on the tickets page)",
        organiser="TechCrunch",
        source_name="TechCrunch — Disrupt 2026 (event and tickets pages)",
        source_url="https://techcrunch.com/events/techcrunch-disrupt/", status="verified",
        notes="Added 2026-10-18 by session arena-91296e94. Dates, Moscone West venue (800 Howard Street) and pass prices are taken from the organiser's own event and tickets pages (the site sits behind a Cloudflare browser check for plain fetches; the content was retrieved and cited from techcrunch.com). 10,000+ attendees with an AI-heavy speaker programme (Hugging Face, Cerebras, Replit, Amazon). Closes the catalogue's AI-conference gap alongside Dreamforce and RSAC. The 2026 edition has concluded."),
    dict(
        id="spc-gamesforum-sf-2026", title="Gamesforum San Francisco 2026",
        page="special", type="Special - Dated",
        schedule="Two-day B2B mobile-gaming conference",
        dates="Monday-Tuesday, October 26-27, 2026",
        location="Hotel Nikko San Francisco", area="Union Square / Downtown",
        cost="Standard conference pass $239 (early-bird $199 before September 26, 2026; super early-bird $149; group of 3 $203 per person, group of 4+ $167 per person); passes are for mobile-games publishers and developers only",
        organiser="Games Forum Ltd (Gamesforum)",
        source_name="Gamesforum — Our Events / San Francisco / Register",
        source_url="https://www.globalgamesforum.com/san-francisco", status="verified",
        notes="Added 2026-10-18 by session arena-91296e94. 'The only dedicated F2P mobile games marketing and monetization event in the US' per the organiser; speaker preview includes Meta, Google, Zynga, EA, Activision Blizzard Media, Scopely and Xbox Media executives. The organiser's pages do not publish the hotel's street address, so the location is recorded as published."),
    dict(
        id="spc-gamesbeat-next-2026", title="GamesBeat NEXT 2026 (7th annual)",
        page="special", type="Special - Dated",
        schedule="Two-day gaming-and-AI executive conference",
        dates="Monday-Tuesday, November 2-3, 2026",
        location="Convene, San Francisco", area="Downtown",
        cost="Conference Pass $899; VIP Pass $1,600 (limited-time $1,200, includes 12 months of GB MAX membership); Indie Pass $499 for freelancers and businesses under 50 employees; complimentary Brand & Agency passes by application",
        organiser="GamesBeat (VentureBeat)",
        source_name="GamesBeat Events — GamesBeat NEXT 2026 / Attend",
        source_url="https://events.gamesbeat.com/next26/", status="verified",
        notes="Added 2026-10-18 by session arena-91296e94. 'The 7th annual GamesBeat NEXT returns to the Bay Area on November 2-3, 2026, taking place at Convene in San Francisco' per the organiser; the programme pairs gaming with AI (Nintendo/PlayStation/Sega legends panel; AI-driven development tracks). The organiser's pages do not publish the venue's street address, so the location is recorded as published."),
    dict(
        id="rec-ferry-board-game-night", title="Board Game Night (Ferry Building Marketplace)",
        page="recurring", type="Recurring - Weekly",
        schedule="Fridays, 5:00-8:00 p.m.",
        dates="", location="Ferry Building Marketplace, public seating area between Book Passage and Cholita Linda, 1 Ferry Building", area="Embarcadero / Financial District",
        cost="", organiser="Ferry Building Marketplace (with Gamescape SF)",
        source_name="Ferry Building Marketplace — Board Game Night",
        source_url="https://www.ferrybuildingmarketplace.com/events/board-game-night-2/", status="verified",
        notes="Added 2026-10-18 by session arena-91296e94. 'Games are provided by the Ferry Building Marketplace' — Scrabble, chess, Monopoly and more, with Gamescape SF; grab food and drinks from the Ferry Building shops. The official page states no admission charge, so the cost cell is left blank rather than inferred."),
    dict(
        id="rec-ferry-mahjong", title="Mahjong Meetup (Ferry Building Marketplace)",
        page="recurring", type="Recurring - Weekly",
        schedule="Wednesdays, 3:00-7:00 p.m.",
        dates="", location="Ferry Building Marketplace, across from Delica, 1 Ferry Building", area="Embarcadero / Financial District",
        cost="", organiser="Ferry Building Marketplace",
        source_name="Ferry Building Marketplace — Mahjong Meetup",
        source_url="https://www.ferrybuildingmarketplace.com/events/mahjong-meetup-1/", status="verified",
        notes="Added 2026-10-18 by session arena-91296e94. 'Join us for an afternoon Mahjong meetup every Wednesday from 3-7 PM. All skill levels are welcome!... Sets will be provided'; Chinese-style quick guide available; seating and sets first come first served. The official page states no admission charge, so the cost cell is left blank."),
    dict(
        id="rec-ferry-music-on-the-plaza", title="Music on the Plaza (Ferry Building)",
        page="recurring", type="Recurring - Weekly",
        schedule="Thursdays, 5:00-7:00 p.m.",
        dates="", location="Ferry Building North Plaza (by Fort Point Beer Garden), 1 Ferry Building", area="Embarcadero / Financial District",
        cost="", organiser="Ferry Building Marketplace",
        source_name="Ferry Building Marketplace — Music on the Plaza",
        source_url="https://www.ferrybuildingmarketplace.com/events/music-on-the-plaza/", status="verified",
        notes="Added 2026-10-18 by session arena-91296e94. 'Kick back and enjoy your Thursday afternoon, accompanied by live performances from our favorite Bay Area musicians.' The official page states no admission charge, so the cost cell is left blank rather than inferred."),
    dict(
        id="rec-ferry-monday-yoga", title="Monday Yoga at the Ferry Building",
        page="recurring", type="Recurring - Weekly",
        schedule="Every Monday, 12:00-1:00 p.m.",
        dates="", location="Ferry Building Back Plaza, 1 Ferry Building", area="Embarcadero / Financial District",
        cost="Free (Vinyasa yoga class, per the official calendar listing)", organiser="Ferry Building Marketplace",
        source_name="Ferry Building Marketplace — Monday Yoga",
        source_url="https://www.ferrybuildingmarketplace.com/events/monday-yoga/", status="verified",
        notes="Added 2026-10-18 by session arena-91296e94. Lunch-hour all-levels vinyasa with headphones provided (bring your own mat); registration link to outdoor-yoga.org on the official page; the venue's official events calendar titles it 'Monday Yoga — Free Vinyasa Yoga Class'."),
'''

CATEGORY_ADDITIONS = '''    "spc-techcrunch-disrupt-2026": "community",
    "spc-gamesforum-sf-2026": "community",
    "spc-gamesbeat-next-2026": "community",
    "rec-ferry-board-game-night": "community",
    "rec-ferry-mahjong": "community",
    "rec-ferry-music-on-the-plaza": "community",
    "rec-ferry-monday-yoga": "community",
'''

NEW_FLAG = '''    dict(
        id="flag-menorah-date-conflict", title="Castro Menorah Lighting — official page prose and structured date disagree",
        detail="The Castro Merchants' official Menorah Lighting page shows a structured event date of Monday, December 7, 2026, 6:00-7:00 p.m., but its body prose still reads 'on Monday, December 15, at 6 PM' (December 15 was a Monday in 2025, so the prose appears to be stale prior-year copy). The row keeps the structured December 7, 2026 date and this mismatch is published rather than silently resolved.",
        source_name="Castro Merchants — Castro Menorah Lighting",
        source_url="https://castromerchants.com/events/castro-menorah-lighting",
        action="Confirm the 2026 date with Castro Merchants; if the structured date is correct, ask them to update the prose."),
'''

def step_new_rows(src: str) -> str:
    if '"spc-techcrunch-disrupt-2026"' in src:
        print("  [skip] new event rows already present")
        return src
    anchor = 'so it is listed as a regular-schedule programme."),\n]'
    assert src.count(anchor) == 1, "EVENTS-list closing anchor not found"
    return src.replace(anchor, 'so it is listed as a regular-schedule programme."),\n' + NEW_ROWS + ']')


def step_mime_troupe(src: str) -> str:
    if '"https://www.sfmt.org/full-schedule"' in src:
        print("  [skip] mime-troupe source already fixed")
        return src
    old = '''        source_name="San Francisco Mime Troupe — official summer calendar (iCal feed)",
        source_url="https://calendar.google.com/calendar/ical/c_49cd818e8b83a687e080ec518030bfdcda142d53de55a32a092ac9a67c50675d%40group.calendar.google.com/public/basic.ics", status="verified",'''
    new = '''        source_name="San Francisco Mime Troupe — full schedule (official site)",
        source_url="https://www.sfmt.org/full-schedule", status="verified",'''
    assert src.count(old) == 1, "mime-troupe source lines not found"
    src = src.replace(old, new)
    old_note = 'notes="Added 2026-10-18 by session arena-8cb2d3cc. The company\'s official calendar feed (linked from sfmt.org/summer-schedule as \'Download iCal Calendar\')'
    new_note = 'notes="Source corrected 2026-10-18 by session arena-91296e94: the row now cites the organiser\'s own schedule page (sfmt.org/full-schedule, linked from sfmt.org/summer-schedule), which links the same official iCal calendar feed previously cited directly. Added 2026-10-18 by session arena-8cb2d3cc. The company\'s official calendar feed'
    assert src.count(old_note) == 1, "mime-troupe note anchor not found"
    return src.replace(old_note, new_note)


def step_category(src: str) -> str:
    if '"spc-gamesforum-sf-2026": "community"' in src:
        print("  [skip] category additions already present")
        return src
    anchor = '    "art-musee-mecanique": "arts",\n}'
    assert src.count(anchor) == 1, "CATEGORY_BY_ID closing anchor not found"
    return src.replace(anchor, '    "art-musee-mecanique": "arts",\n' + CATEGORY_ADDITIONS + '}')


def step_concluded(src: str) -> str:
    if '"spc-techcrunch-disrupt-2026"' in src.split("CONCLUDED_2026")[1][:2000]:
        print("  [skip] concluded addition already present")
        return src
    anchor = '    "ann-sf-mime-troupe",\n}'
    assert src.count(anchor) == 1, "CONCLUDED_2026 closing anchor not found"
    return src.replace(anchor, '    "ann-sf-mime-troupe",\n    "spc-techcrunch-disrupt-2026",\n}')


def step_flag(src: str) -> str:
    if '"flag-menorah-date-conflict"' in src:
        print("  [skip] menorah flag already present")
        return src
    anchor = "        action='Ask Sunset Mercantile or SFMTA to confirm the southern end of the closure. Until then, both official versions are recorded.'),\n]"
    assert src.count(anchor) == 1, "FLAGGED closing anchor not found"
    return src.replace(anchor, "        action='Ask Sunset Mercantile or SFMTA to confirm the southern end of the closure. Until then, both official versions are recorded.'),\n" + NEW_FLAG + "]")


def step_s034(src: str) -> str:
    if '"s-034": {' in src:
        print("  [skip] s-034 override already present")
        return src
    anchor = '''        ),
    },
}


def parallel_events'''
    assert src.count(anchor) == 1, "FIELD_OVERRIDES closing anchor not found"
    return src.replace(anchor, '''        ),
    },
    "s-034": {
        "_clear_unverified": True,
        "title": "WNBA Finals: Valkyries vs Atlanta Dream (Chase Center games)",
        "dates": "Game 1 Saturday, October 17, 2026 (final: Valkyries 68, Dream 64); Game 2 Monday, October 19, 2026, 5:00 p.m. PT; Games 5 (October 26) and 7 (October 31) would also be at Chase Center if the series runs that long",
        "schedule": "WNBA Finals (best-of-seven); Chase Center hosts Games 1, 2 and, if necessary, 5 and 7 — Games 3 (October 21), 4 (October 24) and 6 (October 29) are at Atlanta",
        "source_name": "Golden State Valkyries — official site (WNBA Finals schedule)",
        "source_url": "https://valkyries.wnba.com/",
        "notes": "Re-verified 2026-10-18 by session arena-91296e94 against the team's official site: Game 1 final (ATL 64 @ GSV 68, Golden State leads 1-0); Game 2 Monday, October 19 at 8:00 p.m. EDT (Atlanta Dream @ Golden State Valkyries); the Finals carousel lists Games 3 and 4 at Atlanta and Games 5 and 7, if necessary, at Chase Center. Replaces the earlier SFMTA traffic-advisory citation.",
    },
}


def parallel_events''')


def step_meta() -> None:
    """Refresh data/meta.json counts from the union dataset (canonical build
    does not write it; tools/build_site.py would overwrite it with the old
    supplementary-tranche counts)."""
    import json
    sys.path.insert(0, os.path.join(ROOT, "data"))
    sys.path.insert(0, os.path.join(ROOT, "scripts"))
    import importlib
    events = importlib.import_module("events")
    merge_parallel = importlib.import_module("merge_parallel")
    union = events.assign_views(list(events.EVENTS) + merge_parallel.parallel_events(events.EVENTS))
    flagged = list(events.FLAGGED) + merge_parallel.parallel_flagged()
    from collections import Counter
    groups = Counter(e.get("group", "") for e in union)
    domains = {e["source_url"].split("/")[2] for e in union if e.get("source_url", "").startswith("https://")}
    meta_path = os.path.join(ROOT, "data", "meta.json")
    meta = json.load(open(meta_path, encoding="utf-8"))
    meta["counts"] = {
        "total": len(union),
        "recurring": groups.get("recurring", 0),
        "annual": groups.get("annual", 0),
        "special": groups.get("special", 0),
        "flagged_rows": len(flagged),
        "unverified_rows": sum(1 for e in union if e.get("status") != "verified"),
        "concluded_rows": sum(1 for e in union if e.get("timing") == "concluded"),
        "sources": len(domains),
    }
    json.dump(meta, open(meta_path, "w", encoding="utf-8"), indent=2)
    open(meta_path, "a", encoding="utf-8").write("\n")
    print(f"  meta.json counts refreshed: {meta['counts']}")


def main() -> int:
    src = open(EVENTS_PY, encoding="utf-8").read()
    src = step_new_rows(src)
    src = step_mime_troupe(src)
    src = step_category(src)
    src = step_concluded(src)
    src = step_flag(src)
    open(EVENTS_PY, "w", encoding="utf-8").write(src)

    msrc = open(MERGE_PY, encoding="utf-8").read()
    msrc = step_s034(msrc)
    open(MERGE_PY, "w", encoding="utf-8").write(msrc)

    step_meta()

    # verify the modules still import and the counts move as expected
    sys.path.insert(0, os.path.join(ROOT, "data"))
    sys.path.insert(0, os.path.join(ROOT, "scripts"))
    import importlib
    events = importlib.import_module("events")
    importlib.reload(events)
    rows = events.EVENTS + []
    ids = [e["id"] for e in rows]
    assert len(ids) == len(set(ids)), "duplicate ids after apply"
    n_new = sum(1 for i in ("spc-techcrunch-disrupt-2026", "spc-gamesforum-sf-2026",
                            "spc-gamesbeat-next-2026", "rec-ferry-board-game-night",
                            "rec-ferry-mahjong", "rec-ferry-music-on-the-plaza",
                            "rec-ferry-monday-yoga") if i in ids)
    flagged_ids = [f["id"] for f in events.FLAGGED]
    print(f"  events.py: {len(rows)} rows ({n_new}/7 new present), "
          f"{len(flagged_ids)} flagged items "
          f"({'flag-menorah-date-conflict' in flagged_ids and 'menorah flag present' or 'menorah flag MISSING'})")
    print("OK — apply complete. Now run: python3 scripts/build_site.py && python3 tools/validate.py")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
