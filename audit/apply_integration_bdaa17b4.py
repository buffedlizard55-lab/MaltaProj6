#!/usr/bin/env python3
"""One-off integration edits for session arena-bdaa17b4 (task A7).

Applies the audit findings to data/events.py and scripts/merge_parallel.py
with exact-match assertions, so every change either lands exactly once or the
script stops without a partial write of that edit. Kept in the repo as the
record of what changed and why; see audit/AUDIT-2026-10-18-bdaa17b4.md.

Run once: python3 audit/apply_integration_bdaa17b4.py
"""
import re
import sys

EVENTS = "data/events.py"
MERGE = "scripts/merge_parallel.py"


def replace_once(text, old, new, label):
    assert text.count(old) == 1, f"{label}: expected 1 occurrence, found {text.count(old)}"
    return text.replace(old, new)


def remove_event_block(text, event_id):
    pattern = re.compile(
        r"    dict\(\n        id=\"" + re.escape(event_id) + r"\",.*?\n.*?\),\n",
        re.S)
    new, n = pattern.subn("", text, count=1)
    assert n == 1, f"remove {event_id}: {n} blocks removed"
    return new


def main():
    with open(EVENTS, encoding="utf-8") as fh:
        t = fh.read()

    # --- 1. Remove duplicate / out-of-scope rows -------------------------
    for eid in ("ann-illuminate-live", "spc-sf-pride-trans-march-2026", "art-angel-island"):
        t = remove_event_block(t, eid)
    t = replace_once(t, '    "ann-illuminate-live": "community",\n', "", "cat illuminate")
    t = replace_once(t, '    "spc-sf-pride-trans-march-2026": "community",\n', "", "cat transmarch")

    # --- 2. Corroboration notes on the rows kept ---------------------------
    t = replace_once(
        t,
        'notes="Named weekly blocks: Midweek Melodies (Wednesdays), Friday Happy Hour (Fridays), Crucial Reggae Sundays (Sundays)."),',
        'notes="Named weekly blocks: Midweek Melodies (Wednesdays), Friday Happy Hour (Fridays), Crucial Reggae Sundays (Sundays). The 2026 sixth season was also announced by the Mayor\'s Office (https://www.sf.gov/news-mayor-lurie-announces-new-season-of-free-live-music-in-golden-gate-park); a former duplicate annual-season row sourced to that release was removed in the 2026-10-18 audit by arena-bdaa17b4 - see Flagged for Review."),',
        "bandshell note")
    t = replace_once(
        t,
        '        source_url="https://transmarch.org/", status="verified",\n        notes=""),',
        '        source_url="https://transmarch.org/", status="verified",\n        notes="The 2026 edition (Friday, June 26, 2026, 6:00-7:30 p.m. march) is also documented by SFMTA (https://www.sfmta.com/travel-updates/sf-pride-trans-march-friday-june-26-2026); a former duplicate 2026-edition row sourced to SFMTA was removed in the 2026-10-18 audit by arena-bdaa17b4 - see Flagged for Review."),',
        "transmarch note")

    # --- 3. Blank-cell / stale-label corrections -----------------------------
    t = replace_once(
        t,
        'dates="Saturday, December 13, 2025 (23rd annual — 2026 date not yet published, left blank)",',
        'dates="",',
        "parol dates blanked")
    t = replace_once(
        t,
        'notes="2026 date not published on the organiser\'s site as at 18 October 2026, so the date field is left blank rather than inferred."),',
        'notes="2026 date not published on the organiser\'s site as at 18 October 2026, so the date field is left blank rather than inferred. Re-checked 2026-10-18 by arena-bdaa17b4: the organiser homepage still showed the December 13, 2025 (23rd annual) edition; an earlier version of this row wrongly carried that 2025 date as prose in the confirmed-dates cell, now blanked - see Flagged for Review."),',
        "parol note")

    opera_old = '''    dict(
        id="spc-opera-in-the-park", title="Opera in the Park (free concert by San Francisco Opera)",
        page="special", type="Special - Dated",
        schedule="1:30 p.m.", dates="Sunday, September 13, 2026",
        location="San Francisco — venue published with the Opera's season announcement", area="Citywide",
        cost="Free", organiser="San Francisco Opera (presented by the San Francisco Chronicle)",
        source_name="San Francisco Opera — 2026-27 season announcement",
        source_url="https://www.sfopera.com/press/press-releases/San-Francisco-Opera-2026-27-season/", status="unverified",
        notes="The date and time are confirmed in the Opera's official press release; the specific park venue for 2026 was not stated on that page and is left blank."),'''
    opera_new = '''    dict(
        id="spc-opera-in-the-park", title="Opera in the Park (free concert by San Francisco Opera)",
        page="annual", type="Annual",
        schedule="", dates="Sunday, September 13, 2026 (2026 edition)",
        location="Robin Williams Meadow, Golden Gate Park", area="Golden Gate Park",
        cost="Free", organiser="San Francisco Opera",
        source_name="San Francisco Opera — 2026-27 season announcement",
        source_url="https://www.sfopera.com/press/press-releases/San-Francisco-Opera-2026-27-season/", status="verified",
        notes="Corrected 2026-10-18 by arena-bdaa17b4: the cited release describes a 'free, annual OPERA IN THE PARK concert (Sunday, September 13)' at 'Robin Williams Meadow in San Francisco's Golden Gate Park', so the row is now Annual with the venue filled in. The previously published 1:30 p.m. start time and Chronicle presenter credit could not be confirmed in the fetched release text and were removed rather than kept unverified - see Flagged for Review."),'''
    t = replace_once(t, opera_old, opera_new, "opera row")
    t = replace_once(t, '    "spc-opera-in-the-park": "arts",\n', "", "opera cat del")
    t = replace_once(
        t, '    "ann-sfmusic-week": "arts",\n',
        '    "ann-sfmusic-week": "arts",\n    "spc-opera-in-the-park": "arts",  # annual since the 2026-10-18 audit (id kept for stable anchors)\n',
        "opera cat annual")

    t = replace_once(
        t,
        '        schedule="Monthly, 2:00 p.m.", dates="October 1, 2026 (next listed)",',
        '        schedule="", dates="October 1, 2026 (meeting shown on the cited calendar entry; now in the past)",',
        "recpark ops fields")
    t = replace_once(
        t,
        'notes="CADENCE NOT STATED in full on the official calendar entry; left blank pending confirmation of the recurring rule."),',
        'notes="CADENCE NOT STATED in full on the official calendar entry; left blank pending confirmation of the recurring rule. Corrected 2026-10-18 by arena-bdaa17b4: the schedule cell previously said \'Monthly, 2:00 p.m.\', contradicting this note, and fetching the cited calendar entry now redirected to a CivicPlus sign-in page, so the entry could not be re-verified - see Flagged for Review."),',
        "recpark ops note")

    t = replace_once(
        t,
        '        schedule="", dates="October 8, 2026, 5:00 p.m. (next listed meeting)",',
        '        schedule="", dates="October 8, 2026, 5:00 p.m. (meeting listed when checked; now in the past)",',
        "hrc dates")

    t = replace_once(
        t,
        "has no confirmed San Francisco date. All fields left blank rather than inferred.",
        "has no confirmed San Francisco date. Schedule, dates and cost left blank rather than inferred.",
        "treasurefest wording")

    # --- 4. New verified gap rows (data/gap-candidates-bdaa17b4.json) -------
    new_rows = '''
    # ------------------------------------------------------------------
    # ADDED 2026-10-18 by audit session arena-bdaa17b4 (gap research A4/A7).
    # Verification trail: data/gap-candidates-bdaa17b4.json.
    # ------------------------------------------------------------------
    dict(
        id="rec-sf-city-guides", title="San Francisco City Guides — free walking tours",
        page="recurring", type="Recurring - Regular schedule",
        schedule="Free historical and architectural walking tours of 1.5-2 hours; 70+ different tours, with day and meeting time varying by tour (see Find Your Tour on the official site)",
        dates="", location="Meeting points across San Francisco (varies by tour)", area="Citywide",
        cost="Free (donations welcomed)", organiser="San Francisco City Guides (a program of the San Francisco Public Library)",
        source_name="San Francisco City Guides — Free Walking Tours (official site)",
        source_url="https://sfcityguides.org/", status="verified",
        notes="Homepage states the non-profit was founded in 1978 and that more than 300 trained volunteers lead free tours for over 35,000 locals and visitors each year. Added in the 2026-10-18 gap pass by arena-bdaa17b4."),
    dict(
        id="art-walt-disney-family-museum", title="The Walt Disney Family Museum",
        page="arts", type="Attraction - Open regularly",
        schedule="Thu-Sun 10:00 a.m.-5:30 p.m. (last entry 4:30 p.m.); closed Thanksgiving Day, December 25 and January 1; on December 24 and 31 closes at 4:00 p.m. (last entry 3:00 p.m.)",
        dates="", location="104 Montgomery Street, Presidio of San Francisco", area="Presidio",
        cost="Adults $30; Seniors (65+) $20; Students (with valid ID) $20; Youth (ages 6-17) $15; Children (5 and under) free",
        organiser="The Walt Disney Family Museum",
        source_name="The Walt Disney Family Museum — General Admission Information",
        source_url="https://www.waltdisney.org/visit/admission", status="verified",
        notes="Hours and prices from the admission page; the 104 Montgomery Street Presidio address is stated in the Transportation section of the museum's Visit page (https://www.waltdisney.org/visit), fetched the same day. Added in the 2026-10-18 gap pass by arena-bdaa17b4."),
    dict(
        id="ann-outside-lands", title="Outside Lands Music Festival",
        page="annual", type="Annual",
        schedule="Annual music festival (3-day weekend)",
        dates="August 7-9, 2026 (2026 edition)",
        location="Golden Gate Park", area="Golden Gate Park",
        cost="", organiser="",
        source_name="SFMTA — Outside Lands: August 7-9, 2026",
        source_url="https://www.sfmta.com/travel-updates/outside-lands-august-7-9-2026", status="unverified",
        notes="SFMTA calls it 'The annual Outside Lands Music Festival' in Golden Gate Park, August 7-9, expected around 75,000 people each day. The organiser's official site (sfoutsidelands.com) returned HTTP 500 to this session on 2026-10-18 (also logged as HTTP 500 by session arena-8fb52462), so organiser and ticket cost are left blank rather than sourced to press or resale pages. Added in the 2026-10-18 gap pass by arena-bdaa17b4."),
    dict(
        id="ann-juneteenth-fillmore", title="JuneteenthSF Freedom Celebration (Fillmore)",
        page="annual", type="Annual",
        schedule="Annual eight-block celebration down historic Fillmore Street",
        dates="Saturday, June 13, 2026 (2026 edition)",
        location="Fillmore Street, Fillmore District", area="Fillmore",
        cost="Free (listed by SF.gov among no-cost citywide Juneteenth celebrations)", organiser="",
        source_name="SF.gov (Human Rights Commission) — San Francisco Celebrates Juneteenth 2026",
        source_url="https://www.sf.gov/san-francisco-celebrates-juneteenth-2026", status="unverified",
        notes="SF.gov links the organiser site juneteenth-sf.org, which showed a hosting error page when fetched by this session on 2026-10-18; the organiser's formal name and the day's hours are therefore left blank. The same SF.gov page lists separate 2026 Juneteenth events (Market Street parade; Bayview festival) that were not separately verified this session. Added in the 2026-10-18 gap pass by arena-bdaa17b4."),
    dict(
        id="ann-caamfest", title="CAAMFest (Center for Asian American Media)",
        page="annual", type="Annual",
        schedule="Annual film festival (44th year in 2026)",
        dates="May 7-10, 2026 (2026 edition)",
        location="San Francisco Japantown venues (2026: AMC Kabuki, Asian Art Museum, KOHO Creative Hub, Koret Auditorium, New People Cinema)",
        area="Japantown / Western Addition",
        cost="Regular screenings $15 general; Closing Night / Centerpieces / Showcases $20 general; Opening Night screening + gala $90; Film Fan Pass $350 (2026 official box office)",
        organiser="Center for Asian American Media (CAAM)",
        source_name="Center for Asian American Media — CAAMFest",
        source_url="https://caamedia.org/caamfest/", status="verified",
        notes="Dates and Japantown return from caamedia.org; venues and prices from the official festival site's 2026 schedule and box-office pages (caamfest.com/2026/schedule, caamfest.com/2026/box-office), fetched the same day. Organiser copy says 'five days of films' against a four-day May 7-10 range; the row records the dates only. Added in the 2026-10-18 gap pass by arena-bdaa17b4."),
    dict(
        id="ann-escape-from-alcatraz-triathlon", title="Escape From Alcatraz Triathlon",
        page="annual", type="Annual",
        schedule="Annual triathlon, entering its 47th year in 2027: 1.5-mile swim from the waters near Alcatraz Island, 18-mile bike through the Presidio, 8-mile run including the Sand Ladder, finish at Marina Green; two-day Fitness Festival at Marina Green",
        dates="June 5-6, 2027 (2027 Sokin Escape)",
        location="Finish and Fitness Festival at Marina Green; swim from waters near Alcatraz Island, bike through the Presidio",
        area="Presidio / Marina",
        cost="Fitness Festival free and open to the public; race entry by Random Drawing (entry fee not stated on the official overview page)",
        organiser="Escape From Alcatraz Triathlon",
        source_name="Escape From Alcatraz Triathlon — Overview (official site)",
        source_url="https://www.escapealcatraztri.com/event-information/overview", status="verified",
        notes="The official homepage headline reads '2027 Sokin Escape: June 5 - June 6, 2027' with the Random Drawing open. Added in the 2026-10-18 gap pass by arena-bdaa17b4."),
    dict(
        id="ann-lets-glow-sf", title="Let's Glow SF (holiday projection arts festival)",
        page="annual", type="Annual",
        schedule="Annual, ten winter nights (sixth year in 2026)",
        dates="December 4-13, 2026",
        location="Downtown San Francisco buildings, including the Ferry Building (1 Ferry Building), 101 California St, Pacific Exchange (301 Pine St), Hobart Building (582 Market St), Yerba Buena Lane at Market St and Salesforce Tower (415 Mission St)",
        area="Financial District / SoMa",
        cost="Free", organiser="Downtown SF Partnership",
        source_name="Downtown SF Partnership — Let's Glow SF",
        source_url="https://downtownsf.org/things-to-do/lets-glow-sf", status="verified",
        notes="The organiser page bills it as the nation's largest holiday projection arts festival, hosted by the Downtown SF Partnership. Nightly projection hours are not stated on that page and are not recorded here. Added in the 2026-10-18 gap pass by arena-bdaa17b4."),
    dict(
        id="spc-portola-2026", title="Portola Music Festival 2026",
        page="special", type="Special - Dated",
        schedule="Concerts on four stages from 2:00 to 11:00 p.m. each day (per SFMTA)",
        dates="Saturday, September 26 and Sunday, September 27, 2026",
        location="Pier 80", area="Portola Hill",
        cost="", organiser="",
        source_name="SFMTA — Portola Music Festival: September 26 & 27, 2026",
        source_url="https://www.sfmta.com/travel-updates/portola-music-festival-september-26-27-2026", status="unverified",
        notes="Dates, venue and concert hours from SFMTA. The official festival site (portolamusicfestival.com) showed a post-event thank-you page on 2026-10-18 and names Goldenvoice only in newsletter marketing consent, so organiser and ticket cost are left blank rather than inferred. Classified as a dated 2026 edition because neither fetched official page states an annual cadence in words. Added in the 2026-10-18 gap pass by arena-bdaa17b4."),
    dict(
        id="spc-fog-design-art-2027", title="FOG Design+Art 2027",
        page="special", type="Special - Dated",
        schedule="",
        dates="Preview Gala Wednesday, January 20, 2027; Fair Thursday, January 21 - Sunday, January 24, 2027",
        location="Fort Mason Center for Arts & Culture", area="Marina",
        cost="", organiser="FOG Design+Art (the Preview Gala supports SFMOMA's education initiatives)",
        source_name="SFMOMA — FOG Design+Art 2027",
        source_url="https://www.sfmoma.org/event/series/fog-design-and-art-fair/", status="unverified",
        notes="Fair hours and admission prices are not stated on the SFMOMA series page fetched 2026-10-18 (the older SFMOMA event URL returned 404 and fogfair.com's homepage carried no dates, hours or prices), so cost and schedule are left blank. Added in the 2026-10-18 gap pass by arena-bdaa17b4."),
'''
    t = replace_once(t, "\n]\n\n# ---------------------------------------------------------------------------\n# Irregularities",
                     new_rows + "]\n\n# ---------------------------------------------------------------------------\n# Irregularities",
                     "insert new rows")

    cat_add = '''    "rec-sf-city-guides": "community",
    "ann-outside-lands": "community",
    "ann-juneteenth-fillmore": "community",
    "ann-caamfest": "arts",
    "ann-escape-from-alcatraz-triathlon": "sports",
    "ann-lets-glow-sf": "community",
    "spc-portola-2026": "arts",
    "spc-fog-design-art-2027": "arts",
    "spc-alcatraz-closure": "community",'''
    t = replace_once(t, '    "spc-alcatraz-closure": "community",', cat_add, "cat additions")

    # --- 5. New flagged items -------------------------------------------------
    new_flagged = '''    dict(
        id="flag-angel-island-scope",
        title="Angel Island State Park — removed as outside the SF city-limits scope (audit by arena-bdaa17b4)",
        detail="The former row's note claimed 'the island and its ferry landing are part of the City of San Francisco'. The official California State Parks boating-facilities listing for Angel Island State Park (Ayala Cove Marina) gives the facility address as 'Angel Island, Tiburon, CA 94920' and 'County: Marin'. On that official evidence the park is a Tiburon / Marin County destination reached by ferry, not an event inside the City of San Francisco, so the row was removed from the event list on 2026-10-18 and published here instead (the same treatment earlier sessions gave Levi's Stadium and other out-of-scope items).",
        source_name="California State Parks, Division of Boating and Waterways — Angel Island State Park (Ayala Cove Marina)",
        source_url="https://dbw.parks.ca.gov/BoatingFacilities/f/420",
        action="Decide whether ferry-served out-of-city attractions should ever be listed; until then the row stays off the SF-only list. Park page used by the former row: https://www.parks.ca.gov/?page_id=468"),
    dict(
        id="flag-illuminate-duplicate",
        title="Illuminate LIVE Bandshell concerts — duplicate rows merged (audit by arena-bdaa17b4)",
        detail="The 2026 Illuminate LIVE season (125+ free performances, most Wednesdays/Fridays/Sundays, March 1 to mid-November, Golden Gate Park Bandshell) was listed twice: once as a weekly recurring row sourced to SF Rec & Park and once as an annual row sourced to the Mayor's Office season announcement, double-counting one event in the 205 total. The weekly row was kept and now cites the Mayor's announcement in its notes.",
        source_name="SF.gov — Mayor Lurie Announces New Season of Free Live Music in Golden Gate Park",
        source_url="https://www.sf.gov/news-mayor-lurie-announces-new-season-of-free-live-music-in-golden-gate-park",
        action="Closed by the 2026-10-18 audit; no action unless the season should be split into season + weekly-series rows deliberately."),
    dict(
        id="flag-trans-march-duplicate",
        title="Trans March — duplicate 2026-edition row merged (audit by arena-bdaa17b4)",
        detail="The Friday June 26, 2026 Trans March appeared twice: as the annual row (official organiser site, PRIDE-weekend Friday, Dolores Park 3-6 p.m., march 6 p.m.) and as a special dated row sourced to SFMTA's reroute notice for the same march (6:00-7:30 p.m., Market Street to Turk/Taylor). The annual row already carried the 2026 date, so the special row was removed and the SFMTA page is cited in the annual row's notes.",
        source_name="Trans March — official site (SFMTA notice cited in the event row)",
        source_url="https://transmarch.org/",
        action="Closed by the 2026-10-18 audit."),
    dict(
        id="flag-opera-park-venue",
        title="Opera in the Park — venue was in the cited source all along (audit by arena-bdaa17b4)",
        detail="The row said the park venue 'was not stated' in SF Opera's season announcement. Re-fetching that release on 2026-10-18 shows it names 'Robin Williams Meadow in San Francisco's Golden Gate Park' for the 'free, annual OPERA IN THE PARK concert (Sunday, September 13)'. The row is now Annual with the venue filled; the earlier 1:30 p.m. time and Chronicle presenter credit could not be confirmed in the fetched release text and were removed.",
        source_name="San Francisco Opera — 2026-27 season announcement",
        source_url="https://www.sfopera.com/press/press-releases/San-Francisco-Opera-2026-27-season/",
        action="Closed by the 2026-10-18 audit; confirm the concert start time from the Opera's event page if a time is to be published."),
    dict(
        id="flag-parol-dates-cell",
        title="Parol Lantern Festival — stale 2025 prose removed from the confirmed-dates cell (audit by arena-bdaa17b4)",
        detail="The row's confirmed-dates cell read 'Saturday, December 13, 2025 (23rd annual - 2026 date not yet published, left blank)' while its own note said the date was left blank, contradicting this project's blank-means-unconfirmed rule. Re-checking the organiser homepage on 2026-10-18 confirmed it still shows only the December 13, 2025 edition. The cell is now blank.",
        source_name="Parol Lantern Festival — official site",
        source_url="https://www.parollanternfestival.com/",
        action="Add the 2026 date when the organiser publishes it."),
    dict(
        id="flag-Manon-date",
        title="Manon (SF Opera) — imported start date conflicts with the Opera's season announcement (audit by arena-bdaa17b4)",
        detail="The parallel session's imported Manon row (x-s-020, sourced only to the sfopera.com homepage) gave October 18 - November 1, 2026, while SF Opera's official 2026-27 season announcement and this dataset's own season row both give Manon as October 15 - November 1, 2026 (the other three imported opera rows match the announcement exactly). The published union row now follows the season announcement via a documented correction in scripts/merge_parallel.py; the parallel session's raw JSON is unchanged.",
        source_name="San Francisco Opera — 2026-27 season announcement",
        source_url="https://www.sfopera.com/press/press-releases/San-Francisco-Opera-2026-27-season/",
        action="If the Opera's production page shows a first performance on a different date, publish that page as the source instead."),
    dict(
        id="flag-recpark-ops-source",
        title="Rec & Park Operations Committee — schedule contradicted its own note; source now behind login (audit by arena-bdaa17b4)",
        detail="The row published 'Monthly, 2:00 p.m.' while its note said the cadence was not stated and was left blank; its 'next listed' date (October 1, 2026) is also now in the past. On 2026-10-18 the cited calendar entry redirected this session's fetcher to a CivicPlus sign-in page, so the entry could not be re-verified. The schedule cell is now blank, matching the note.",
        source_name="SF Recreation and Parks — Operations Committee calendar entry (EID=9056)",
        source_url="https://sfrecpark.org/Calendar.aspx?EID=9056",
        action="Confirm the committee's recurring rule and next meeting on the department's Meeting Info & Calendar page and complete the row."),
    dict(
        id="flag-outside-lands-source",
        title="Outside Lands — added from SFMTA; organiser site unreachable (audit by arena-bdaa17b4)",
        detail="The city's largest annual music festival had no row, because the organiser's official site (sfoutsidelands.com) returned HTTP 500 both to session arena-8fb52462 and to this session on 2026-10-18. A row was added from SFMTA's official event page (annual; August 7-9, 2026; Golden Gate Park) with organiser and ticket cost left blank and the row marked unverified.",
        source_name="SFMTA — Outside Lands: August 7-9, 2026",
        source_url="https://www.sfmta.com/travel-updates/outside-lands-august-7-9-2026",
        action="Complete organiser and cost from sfoutsidelands.com when it is reachable again."),
    dict(
        id="flag-juneteenth-organiser",
        title="JuneteenthSF Freedom Celebration — organiser site down (audit by arena-bdaa17b4)",
        detail="Added from the SF.gov Human Rights Commission Juneteenth 2026 page (annual eight-block Fillmore celebration; Saturday, June 13, 2026; listed among no-cost events). The organiser site it links (juneteenth-sf.org) showed a hosting error page on 2026-10-18, so the organiser's formal name and event hours are blank and the row is unverified.",
        source_name="SF.gov (Human Rights Commission) — San Francisco Celebrates Juneteenth 2026",
        source_url="https://www.sf.gov/san-francisco-celebrates-juneteenth-2026",
        action="Complete organiser and hours from juneteenth-sf.org when it is back; separately verify the Market Street Juneteenth Parade and Bayview festival named on the same SF.gov page."),
    dict(
        id="flag-portola-organiser",
        title="Portola Music Festival 2026 — organiser and cost unconfirmed (audit by arena-bdaa17b4)",
        detail="Added from SFMTA (Pier 80; September 26-27, 2026; concerts 2-11 p.m.). The official festival site showed only a post-event thank-you page on 2026-10-18 and names Goldenvoice solely in newsletter consent text, which does not establish the organiser field to this project's standard; organiser and cost are blank and the row is unverified and classified as a dated edition.",
        source_name="SFMTA — Portola Music Festival: September 26 & 27, 2026",
        source_url="https://www.sfmta.com/travel-updates/portola-music-festival-september-26-27-2026",
        action="Confirm presenter, ticket prices and annual cadence from portolamusicfestival.com for the next edition."),
    dict(
        id="flag-fog-cost",
        title="FOG Design+Art 2027 — fair hours and prices not on the fetched official page (audit by arena-bdaa17b4)",
        detail="Added from SFMOMA's series page (Preview Gala January 20, 2027; Fair January 21-24, 2027; Fort Mason Center for Arts & Culture). That page states no fair hours or admission prices; the older SFMOMA event URL returned 404 and fogfair.com's homepage carried no dates, hours or prices on 2026-10-18. Schedule and cost are blank and the row is unverified.",
        source_name="SFMOMA — FOG Design+Art 2027",
        source_url="https://www.sfmoma.org/event/series/fog-design-and-art-fair/",
        action="Complete hours and prices from fogfair.com or SFMOMA ticketing when published."),
'''
    t = replace_once(
        t,
        '        action="Verify the 2026-27 home schedule against the WNBA site and complete the row."),\n]',
        '        action="Verify the 2026-27 home schedule against the WNBA site and complete the row."),\n' + new_flagged + ']',
        "flagged additions")

    with open(EVENTS, "w", encoding="utf-8") as fh:
        fh.write(t)

    # --- 6. Manon correction in the parallel-data merge -----------------------
    with open(MERGE, encoding="utf-8") as fh:
        m = fh.read()
    m = replace_once(
        m,
        'def _slug(text: str) -> str:',
        '''# Corrections applied to imported rows by the 2026-10-18 audit session
# (arena-bdaa17b4). The parallel session's raw JSON files are NOT edited;
# each correction states the official source that overrules the imported
# value, and is also published on the Flagged for Review page.
AUDIT_CORRECTIONS = {
    # Manon: imported as "October 18 - November 1, 2026" from the sfopera.com
    # homepage. SF Opera's official 2026-27 season announcement (fetched
    # 2026-10-18) lists Manon as October 15 - November 1, 2026, matching this
    # dataset's own art-sfopera season row; the other imported opera rows
    # already match that announcement exactly.
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


def _slug(text: str) -> str:''',
        "corrections dict")
    m = replace_once(
        m,
        '''            rec["category"] = CATEGORY_BY_ORIG_ID.get(orig, "community")''',
        '''            if orig in AUDIT_CORRECTIONS:
                fix = AUDIT_CORRECTIONS[orig]
                for key, value in fix.items():
                    if not key.startswith("_"):
                        rec[key] = value
                rec["notes"] = (fix.get("_correction_note", "") + " " + rec["notes"]).strip()
            rec["category"] = CATEGORY_BY_ORIG_ID.get(orig, "community")''',
        "corrections apply")
    with open(MERGE, "w", encoding="utf-8") as fh:
        fh.write(m)

    print("integration edits applied OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
