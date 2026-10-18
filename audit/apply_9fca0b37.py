#!/usr/bin/env python3
"""Apply the arena-9fca0b37 corrections to the published dataset and site.

Session: ``arena-9fca0b37`` (2026-10-18), eleventh verification pass.

Every change below was checked against the organiser's or agency's own page
on 2026-10-18. The page that was fetched is named in the note that the
change writes into the row, so a reviewer can re-open the same source.

The script is **idempotent**: running it twice leaves the tree unchanged.
Replacements are exact-string edits, so a file that has already been
patched is detected and skipped.

Run with:  python3 audit/apply_9fca0b37.py
"""
from __future__ import annotations

import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EVENTS_PY = os.path.join(ROOT, "data", "events.py")
MERGE_PY = os.path.join(ROOT, "scripts", "merge_parallel.py")
BUILD_PY = os.path.join(ROOT, "scripts", "build_site.py")

# --------------------------------------------------------------------------
# 1. New rows, each verified on its own official page.
# --------------------------------------------------------------------------

NEW_ROWS = '''    dict(
        id="spc-family-summit-d10-2026-12-05", title="District 10 Bayview Family Summit",
        page="special", type="Special - Dated", category="community",
        schedule="11:00 a.m.–1:30 p.m.", dates="Saturday, December 5, 2026",
        location="Southeast Community Center, 1550 Evans Avenue, San Francisco, CA 94124",
        area="Bayview / Potrero Hill", cost="Free",
        organiser="Our Children Our Families Initiative, City and County of San Francisco",
        source_name="SF.gov — District 10 Bayview Family Summit",
        source_url="https://www.sf.gov/event-20261205-district-10-family-summit-bayview/", status="verified",
        notes="Added by arena-9fca0b37 on 2026-10-18. The official SF.gov event page states Saturday, December 5, 2026, 11:00 a.m. to 1:30 p.m., Cost: Free, Southeast Community Center, 1550 Evans Avenue, San Francisco, CA 94124, with free meals, childcare and interpretation. It is listed on the city's own OCOFI calendar at https://www.sf.gov/department-ocofi/events/upcoming . The August 20, 2026 city press release lists the same summit, date, time and venue. This closes the review item flag-d10-family-summit-page-missing, which had recorded that the event page could not be found."),
    dict(
        id="spc-exploratorium-after-dark-2026-10-22", title="After Dark: Death and Life / La muerte y la vida (Exploratorium)",
        page="special", type="Special - Dated", category="arts",
        schedule="6:00-10:00 p.m.", dates="Thursday, October 22, 2026",
        location="Exploratorium, Pier 15, San Francisco",
        area="Embarcadero / South Beach", cost="Ticketed",
        organiser="Exploratorium",
        source_name="Exploratorium — After Dark: Death and Life / La muerte y la vida",
        source_url="https://www.exploratorium.edu/visit/calendar/after-dark-death-and-life", status="verified",
        notes="Added by arena-9fca0b37 on 2026-10-18. The Exploratorium's own After Dark calendar lists 'After Dark: Death and Life / La muerte y la vida — Thu, Oct 22 2026 • 6 - 10pm' and the event's own page carries the programme. The series page states tickets are required and can be bought in advance; no numeric price is published, so the cost cell is left for the price review."),
    dict(
        id="spc-exploratorium-after-dark-2026-11-05", title="After Dark: Digest This (Exploratorium)",
        page="special", type="Special - Dated", category="arts",
        schedule="6:00-10:00 p.m.", dates="Thursday, November 5, 2026",
        location="Exploratorium, Pier 15, San Francisco",
        area="Embarcadero / South Beach", cost="Ticketed",
        organiser="Exploratorium",
        source_name="Exploratorium — After Dark: Digest This",
        source_url="https://www.exploratorium.edu/visit/calendar/after-dark-digest-this", status="verified",
        notes="Added by arena-9fca0b37 on 2026-10-18. The Exploratorium's own After Dark calendar lists 'After Dark: Digest This — Thu, Nov 5 2026 • 6 - 10pm' and the event's own page carries the programme. No numeric ticket price is published, so the cost cell is left for the price review."),
    dict(
        id="spc-exploratorium-after-dark-2026-11-12", title="After Dark: Unplug and Play (Exploratorium, November)",
        page="special", type="Special - Dated", category="arts",
        schedule="6:00-10:00 p.m.", dates="Thursday, November 12, 2026",
        location="Exploratorium, Pier 15, San Francisco",
        area="Embarcadero / South Beach", cost="Ticketed",
        organiser="Exploratorium",
        source_name="Exploratorium — After Dark: Unplug and Play (November 2026)",
        source_url="https://www.exploratorium.edu/visit/calendar/after-dark-unplug-play-nov2026", status="verified",
        notes="Added by arena-9fca0b37 on 2026-10-18. The Exploratorium's own After Dark calendar lists 'After Dark: Unplug and Play — Thu, Nov 12 2026 • 6 - 10pm' and the event's own page carries the programme. No numeric ticket price is published, so the cost cell is left for the price review."),
    dict(
        id="spc-exploratorium-after-dark-2026-12-03", title="After Dark: Rule Breakers (Exploratorium)",
        page="special", type="Special - Dated", category="arts",
        schedule="6:00-10:00 p.m.", dates="Thursday, December 3, 2026",
        location="Exploratorium, Pier 15, San Francisco",
        area="Embarcadero / South Beach", cost="Ticketed",
        organiser="Exploratorium",
        source_name="Exploratorium — After Dark: Rule Breakers",
        source_url="https://www.exploratorium.edu/visit/calendar/after-dark-rule-breakers", status="verified",
        notes="Added by arena-9fca0b37 on 2026-10-18. The Exploratorium's own After Dark calendar lists 'After Dark: Rule Breakers — Thu, Dec 3 2026 • 6 - 10pm' and the event's own page carries the programme. No numeric ticket price is published, so the cost cell is left for the price review."),
    dict(
        id="spc-exploratorium-after-dark-2026-12-10", title="After Dark: Unplug and Play (Exploratorium, December)",
        page="special", type="Special - Dated", category="arts",
        schedule="6:00-10:00 p.m.", dates="Thursday, December 10, 2026",
        location="Exploratorium, Pier 15, San Francisco",
        area="Embarcadero / South Beach", cost="Ticketed",
        organiser="Exploratorium",
        source_name="Exploratorium — After Dark: Unplug and Play (December 2026)",
        source_url="https://www.exploratorium.edu/visit/calendar/after-dark-unplug-play-dec2026", status="verified",
        notes="Added by arena-9fca0b37 on 2026-10-18. The Exploratorium's own After Dark calendar lists 'After Dark: Unplug and Play — Thu, Dec 10 2026 • 6 - 10pm' and the event's own page carries the programme. No numeric ticket price is published, so the cost cell is left for the price review."),
    dict(
        id="spc-exploratorium-after-dark-2026-12-17", title="After Dark: Solstice (Exploratorium)",
        page="special", type="Special - Dated", category="arts",
        schedule="6:00-10:00 p.m.", dates="Thursday, December 17, 2026",
        location="Exploratorium, Pier 15, San Francisco",
        area="Embarcadero / South Beach", cost="Ticketed",
        organiser="Exploratorium",
        source_name="Exploratorium — After Dark: Solstice",
        source_url="https://www.exploratorium.edu/visit/calendar/after-dark-solstice", status="verified",
        notes="Added by arena-9fca0b37 on 2026-10-18. The Exploratorium's own After Dark calendar lists 'After Dark: Solstice — Thu, Dec 17 2026 • 6 - 10pm' and the event's own page carries the programme. No numeric ticket price is published, so the cost cell is left for the price review."),
'''

# --------------------------------------------------------------------------
# 2. Corrections to existing rows in data/events.py.
#    (old, new) exact-string pairs.
# --------------------------------------------------------------------------

EVENTS_EDITS = [
    # --- SF Opera: the organiser's own pages publish price and start time ---
    (
        '''        schedule="", dates="November 6, 2026",
        location="War Memorial Opera House", area="Civic Center",
        cost="Ticketed", organiser="San Francisco Opera",
        source_name="San Francisco Opera — Strauss In Concert",
        source_url="https://www.sfopera.com/seasons/fall-concert/", status="verified",
        notes="Added by arena-fc3438db from the opera's Upcoming Events list (fetched 2026-10-18): 'NOV 6 ... "
              "Strauss In Concert, War Memorial Opera House' — Music Director Eun Sun Kim leads the SF Opera "
              "Orchestra. Start time is not published on the fetched page."),''',
        '''        schedule="7:30 p.m.", dates="Friday, November 6, 2026",
        location="War Memorial Opera House", area="Civic Center",
        cost="Starting at $30", organiser="San Francisco Opera",
        source_name="San Francisco Opera — Strauss In Concert",
        source_url="https://www.sfopera.com/seasons/fall-concert/", status="verified",
        notes="Added by arena-fc3438db from the opera's Upcoming Events list (fetched 2026-10-18): 'NOV 6 ... "
              "Strauss In Concert, War Memorial Opera House' — Music Director Eun Sun Kim leads the SF Opera "
              "Orchestra. Re-checked 2026-10-18 by arena-9fca0b37 on the same official page, which now states "
              "'Friday, November 6, 2026 at 7:30 PM' and 'Price: Starting at $30'; both values are filled from "
              "that page and the row is verified again."),''',
    ),
    (
        '''        schedule="", dates="November 12, 2026",
        location="City Hall, 1 Dr. Carlton B. Goodlett Place", area="Civic Center",
        cost="Ticketed (fundraiser)", organiser="San Francisco Opera",
        source_name="San Francisco Opera — Opera Ball",
        source_url="https://www.sfopera.com/seasons/opera-ball/", status="verified",
        notes="Added by arena-fc3438db from the opera's Upcoming Events list (fetched 2026-10-18): 'NOV 12 ... "
              "Opera Ball, City Hall' — described on the page as the company's biggest fundraiser of the year. "
              "Ticket prices are not published on the fetched page."),''',
        '''        schedule="6:00 p.m. cocktail reception; 7:00 p.m. dinner; 9:00 p.m. music and dancing; 11:00 p.m. concludes",
        dates="Thursday, November 12, 2026",
        location="City Hall, 1 Dr. Carlton B. Goodlett Place", area="Civic Center",
        cost="Buffet Dinner Soirée $450; Advocate $2,000; Benefactor $3,500; Grand Benefactor $5,000; Great Benefactor $10,000",
        organiser="San Francisco Opera",
        source_name="San Francisco Opera — Opera Ball",
        source_url="https://www.sfopera.com/seasons/opera-ball/", status="verified",
        notes="Added by arena-fc3438db from the opera's Upcoming Events list (fetched 2026-10-18): 'NOV 12 ... "
              "Opera Ball, City Hall' — described on the page as the company's biggest fundraiser of the year. "
              "Re-checked 2026-10-18 by arena-9fca0b37 on the same official page, which states the event was "
              "rescheduled to Thursday, November 12, 2026 because of orchestra labour negotiations, gives the "
              "evening's running order (6:00 p.m. red carpet and cocktail reception, 7:00 p.m. dinner, 9:00 p.m. "
              "music and dancing, 11:00 p.m. conclusion) and lists the published ticket levels: Buffet Dinner "
              "Soirée $450, Advocate $2,000, Benefactor $3,500, Grand Benefactor $5,000, Great Benefactor $10,000. "
              "The earlier 'Ticketed (fundraiser)' wording is replaced by those published amounts."),''',
    ),
    (
        '''        schedule="", dates="November 20, 2026",
        location="Herbst Theatre, 401 Van Ness Avenue", area="Civic Center",
        cost="Ticketed", organiser="San Francisco Opera",
        source_name="San Francisco Opera — The Future Is Now: Adlers in Concert",
        source_url="https://www.sfopera.com/seasons/the-future-is-now-adlers-in-concert/", status="verified",
        notes="Added by arena-fc3438db from the opera's Upcoming Events list (fetched 2026-10-18): 'NOV 20 ... "
              "Herbst Theatre' — the annual Adler Fellows showcase with the SF Opera Orchestra. Start time is "
              "not published on the fetched page."),''',
        '''        schedule="7:30 p.m.", dates="Friday, November 20, 2026",
        location="Herbst Theatre, 401 Van Ness Avenue", area="Civic Center",
        cost="Starting at $34", organiser="San Francisco Opera",
        source_name="San Francisco Opera — The Future Is Now: Adlers in Concert",
        source_url="https://www.sfopera.com/seasons/the-future-is-now-adlers-in-concert/", status="verified",
        notes="Added by arena-fc3438db from the opera's Upcoming Events list (fetched 2026-10-18): 'NOV 20 ... "
              "Herbst Theatre' — the annual Adler Fellows showcase with the SF Opera Orchestra. Re-checked "
              "2026-10-18 by arena-9fca0b37 on the same official page, which states 'Date: Friday, November 20 "
              "at 7:30pm', 'Location: Herbst Theatre' and 'Price: Starting at $34'. Both values are filled from "
              "that page and the row is verified again."),''',
    ),
    (
        '''        schedule="", dates="November 22, 2026",
        location="Multiple venues (as listed by the organiser)", area="Civic Center",
        cost="Ticketed", organiser="San Francisco Opera",
        source_name="San Francisco Opera — San Francisco Opera Chorus in Concert",
        source_url="https://www.sfopera.com/seasons/san-francisco-opera-chorus-in-concert/", status="verified",
        notes="Added by arena-fc3438db from the opera's Upcoming Events list (fetched 2026-10-18): 'NOV 22 ... "
              "Multiple Venues' — Chorus Director John Keene leads the company's full-time chorus. The organiser "
              "lists the venue only as 'Multiple Venues'; the exact hall and start time are not published on the "
              "fetched page, so those cells are left blank."),''',
        '''        schedule="2:00 p.m.", dates="Sunday, November 22, 2026",
        location="Dianne and Tad Taube Atrium Theater", area="Civic Center",
        cost="$49.00", organiser="San Francisco Opera",
        source_name="San Francisco Opera — San Francisco Opera Chorus in Concert",
        source_url="https://www.sfopera.com/seasons/san-francisco-opera-chorus-in-concert/", status="verified",
        notes="Added by arena-fc3438db from the opera's Upcoming Events list (fetched 2026-10-18): 'NOV 22 ... "
              "Multiple Venues' — Chorus Director John Keene leads the company's full-time chorus. Re-checked "
              "2026-10-18 by arena-9fca0b37 on the event's own official page, which states 'Date: Sunday, "
              "November 22', 'Location: Dianne and Tad Taube Atrium Theater', 'at 2pm' and 'Tickets are $49.00'. "
              "The earlier 'Multiple Venues' location, the blank schedule and the generic 'Ticketed' wording are "
              "replaced by those published values."),''',
    ),
    # --- SF Symphony: start times are published on the concert pages ---
    (
        '''        schedule="", dates="October 20, 2026",
        location="Davies Symphony Hall, 201 Van Ness Avenue", area="Civic Center",
        cost="Ticketed", organiser="San Francisco Symphony",
        source_name="San Francisco Symphony — The Ring (film with live orchestra)",
        source_url="https://www.sfsymphony.org/Buy-Tickets/2026-27/The-Ring", status="verified",
        notes="Added by arena-fc3438db. The Symphony homepage (fetched 2026-10-18) lists 'The Ring—Film with "
              "Live Orchestra, Oct 20' under MORE UPCOMING and links this ticket page. Start time is not "
              "published on the fetched page, so the schedule cell is left blank."),''',
        '''        schedule="7:30 p.m.", dates="Tuesday, October 20, 2026",
        location="Davies Symphony Hall, 201 Van Ness Avenue", area="Civic Center",
        cost="Ticketed", organiser="San Francisco Symphony",
        source_name="San Francisco Symphony — The Ring (film with live orchestra)",
        source_url="https://www.sfsymphony.org/Buy-Tickets/2026-27/The-Ring", status="verified",
        notes="Added by arena-fc3438db. The Symphony homepage (fetched 2026-10-18) lists 'The Ring—Film with "
              "Live Orchestra, Oct 20' under MORE UPCOMING and links this ticket page. Re-checked 2026-10-18 by "
              "arena-9fca0b37 on the concert's own official page, which states 'Tuesday, October 20, 2026 — "
              "7:30PM — Davies Symphony Hall' with Hans Zimmer's score performed live by the SF Symphony, "
              "conducted by Jason Seber. The start time is filled from that page. The page itself publishes no "
              "ticket amount, so the cost cell stays with the generic wording and the row stays unverified for "
              "price."),''',
    ),
    (
        '''        schedule="", dates="October 29-31, 2026",
        location="Davies Symphony Hall, 201 Van Ness Avenue", area="Civic Center",
        cost="Ticketed", organiser="San Francisco Symphony",
        source_name="San Francisco Symphony — Doctor Atomic and Mendelssohn",
        source_url="https://www.sfsymphony.org/Buy-Tickets/2026-27/Doctor-Atomic-and-Mendelssohn", status="verified",
        notes="Added by arena-fc3438db. The Symphony homepage (fetched 2026-10-18) lists 'Elim Chan Conducts "
              "Adams and Mendelssohn, Oct 29 - Oct 31' and links this ticket page. Start times are not "
              "published on the fetched page."),''',
        '''        schedule="7:30 p.m. on October 29, 30 and 31, 2026", dates="October 29-31, 2026",
        location="Davies Symphony Hall, 201 Van Ness Avenue", area="Civic Center",
        cost="Ticketed", organiser="San Francisco Symphony",
        source_name="San Francisco Symphony — Doctor Atomic and Mendelssohn",
        source_url="https://www.sfsymphony.org/Buy-Tickets/2026-27/Doctor-Atomic-and-Mendelssohn", status="verified",
        notes="Added by arena-fc3438db. The Symphony homepage (fetched 2026-10-18) lists 'Elim Chan Conducts "
              "Adams and Mendelssohn, Oct 29 - Oct 31' and links this ticket page. Re-checked 2026-10-18 by "
              "arena-9fca0b37 on the concert's own official page, which lists three performances — Thursday "
              "October 29, Friday October 30 and Saturday October 31, 2026, all at 7:30PM at Davies Symphony "
              "Hall — with Renaud Capuçon in Mendelssohn's Violin Concerto and the first SF Symphony "
              "performances of John Adams's Doctor Atomic Symphony. The start times are filled from that page. "
              "The page publishes no ticket amount, so the cost cell keeps the generic wording."),''',
    ),
    (
        '''        schedule="", dates="October 24, 2026",
        location="Davies Symphony Hall, 201 Van Ness Avenue", area="Civic Center",
        cost="Ticketed", organiser="San Francisco Symphony",
        source_name="San Francisco Symphony — Music for Families (October)",
        source_url="https://www.sfsymphony.org/Buy-Tickets/2026-27/Music-for-Families-Oct", status="verified",
        notes="Added by arena-fc3438db. Listed as 'Music for Families, Oct 24' on the Symphony homepage "
              "(fetched 2026-10-18). Start time is not published on the fetched page."),''',
        '''        schedule="2:00 p.m.", dates="Saturday, October 24, 2026",
        location="Davies Symphony Hall, 201 Van Ness Avenue", area="Civic Center",
        cost="Ticketed", organiser="San Francisco Symphony",
        source_name="San Francisco Symphony — Music for Families (October)",
        source_url="https://www.sfsymphony.org/Buy-Tickets/2026-27/Music-for-Families-Oct", status="verified",
        notes="Added by arena-fc3438db. Listed as 'Music for Families, Oct 24' on the Symphony homepage "
              "(fetched 2026-10-18). Re-checked 2026-10-18 by arena-9fca0b37 on the concert's own official page, "
              "which states 'Saturday, October 24, 2026 — 2:00PM — Davies Symphony Hall', recommended for ages "
              "5–12, with kids' tickets half off. The start time is filled from that page. The page publishes no "
              "ticket amount, so the cost cell keeps the generic wording and the row stays unverified for price."),''',
    ),
    # --- Castro Merchants rows: the organiser publishes no admission price ---
    (
        '''        cost="Free", organiser="Castro Merchants Association",
        source_name="Castro Merchants Association — Castro Menorah Lighting",
        source_url="https://castromerchants.com/events/castro-menorah-lighting", status="verified",''',
        '''        cost="", organiser="Castro Merchants Association",
        source_name="Castro Merchants Association — Castro Menorah Lighting",
        source_url="https://castromerchants.com/events/castro-menorah-lighting", status="unverified",''',
    ),
    (
        '''        schedule="6:00-6:30 p.m.", dates="Monday, November 30, 2026",
        location="Bank of America Plaza, 501 Castro Street", area="Castro",
        cost="Free",''',
        '''        schedule="6:00-6:30 p.m.", dates="Monday, November 30, 2026",
        location="Bank of America Plaza, 501 Castro Street", area="Castro",
        cost="",''',
    ),
    (
        '''        source_name="Castro Merchants Association — Castro Holiday Tree Lighting Ceremony 2026",
        source_url="https://castromerchants.com/events/castro-holiday-tree-lighting-ceremony-2023", status="verified",
        notes=""),''',
        '''        source_name="Castro Merchants Association — Castro Holiday Tree Lighting Ceremony 2026",
        source_url="https://castromerchants.com/events/castro-holiday-tree-lighting-ceremony-2023", status="unverified",
        notes="Cost blanked 2026-10-18 by arena-9fca0b37: the organiser's own page publishes the date, time and location but no admission price, so 'Free' was an inference and has been removed."),''',
    ),
    (
        '''        schedule="5:00-8:00 p.m., first Friday of the month",
        dates="Friday, November 6 and Friday, December 4, 2026 (next listed)",
        location="Castro district businesses, San Francisco", area="Castro",
        cost="Free",''',
        '''        schedule="5:00-8:00 p.m., first Friday of the month",
        dates="Friday, November 6 and Friday, December 4, 2026 (next listed)",
        location="Castro district businesses, San Francisco", area="Castro",
        cost="",''',
    ),
    (
        '''        source_name="Castro Merchants Association — Castro Art Walk",
        source_url="https://castromerchants.com/events", status="verified",''',
        '''        source_name="Castro Merchants Association — Castro Art Walk",
        source_url="https://castromerchants.com/events", status="unverified",''',
    ),
    (
        '''        cost="", organiser="Castro Merchants Association with Midnight Sun",
        source_name="Castro Merchants Association — Events in the Hood",
        source_url="https://castromerchants.com/events", status="verified",''',
        '''        cost="", organiser="Castro Merchants Association with Midnight Sun",
        source_name="Castro Merchants Association — Castro Holiday Tree Fundraiser at Midnight Sun",
        source_url="https://castromerchants.com/events/castro-holiday-tree-lighting-ceremony-2023-5edw6", status="unverified",''',
    ),
    (
        '''              "holiday-tree fundraiser hosted by Midnight Sun, Saturday, October 24, 2026, 4:00-7:00 p.m. The "
              "listing states no admission price, so the cost cell is left blank rather than guessed."),''',
        '''              "holiday-tree fundraiser hosted by Midnight Sun, Saturday, October 24, 2026, 4:00-7:00 p.m. The "
              "listing states no admission price, so the cost cell is left blank rather than guessed. "
              "Re-checked 2026-10-18 by arena-9fca0b37: the source link is upgraded from the organiser's "
              "listing index to this event's own page, and because no admission price is published anywhere on "
              "it the row is marked unverified for price."),''',
    ),
]

# The Castro Menorah note records a date conflict that the organiser has now
# fixed on its own page; the structured December 7 date was already correct.
MENORAH_NOTE_OLD = '''        notes="The organiser's own description gives the date as Monday, December 15 while the calendar listing gives December 7, 2026 — see Flagged for Review."),'''
MENORAH_NOTE_NEW = '''        notes="Re-checked 2026-10-18 by arena-9fca0b37 on the organiser's own event page. The page previously "
              "listed a structured date of Monday, December 7, 2026 while its prose said 'on Monday, December 15, "
              "at 6 PM'; the prose has since been corrected and now reads 'on Monday, December 7, at 6 PM', so the "
              "conflict is resolved and the row keeps the December 7, 2026 date. The page publishes no admission "
              "price, so the cost cell is left blank and the row is unverified for price."),'''

# --------------------------------------------------------------------------
# 3. Review-register items.
# --------------------------------------------------------------------------

NEW_FLAGS = '''    dict(
        id="flag-sunday-streets-admission-not-published",
        title="SFMTA Sunday Streets — admission price not published",
        detail="The SFMTA Sunday Streets programme page (fetched 2026-10-18) describes the programme as car-free and states the usual 11:00 a.m.–4:00 p.m. window, but it publishes no admission price. The row rec-sunday-streets therefore leaves the cost cell blank and is marked unverified. The 2026 Excelsior edition has its own dated row.",
        source_name="SFMTA — Sunday Streets",
        source_url="https://www.sfmta.com/getting-around/walk/sunday-streets",
        action="Check the organiser's or SFMTA's page for a stated admission price. Fill in an amount only if a page states it; otherwise keep the cell blank."),
    dict(
        id="flag-bos-lut-next-meeting-not-published",
        title="Board of Supervisors Land Use and Transportation Committee — next meeting date not published",
        detail="The row civ-bos-lut carries the standing Monday 1:30 p.m. time from the Legistar meeting calendar and the SFGovTV permanent schedule, but the committee does not publish its own next-meeting date as a row value, so the dates cell is blank. A separate review item records the 10/19/2026 listing conflict.",
        source_name="SF.gov Legistar Meeting Calendar",
        source_url="https://sfgov.legistar.com/Calendar.aspx",
        action="Read the next posted meeting from the Legistar calendar and fill the dates cell from that record only."),
    dict(
        id="flag-bos-rules-next-meeting-not-published",
        title="Board of Supervisors Rules Committee — next meeting date not published",
        detail="The row civ-bos-rules carries the standing Monday 10:00 a.m. time from the Legistar meeting calendar and the SFGovTV permanent schedule, but the committee does not publish its own next-meeting date as a row value, so the dates cell is blank. A separate review item records the 10/19/2026 listing conflict.",
        source_name="SF.gov Legistar Meeting Calendar",
        source_url="https://sfgov.legistar.com/Calendar.aspx",
        action="Read the next posted meeting from the Legistar calendar and fill the dates cell from that record only."),
    dict(
        id="flag-pickleball-palace-hours-not-published",
        title="Pickleball courts at the Palace of Fine Arts — current court hours not published",
        detail="The row spt-pickleball-palace rests on the SF Recreation and Parks newsflash of 2023 that announced three free indoor courts opening on July 11, 2023, with free 90-minute reservations from 9:30 to 11:00 a.m. Tuesday to Sunday and paid DinkSF bookings from 11:30 a.m. to 5 p.m. That announcement is still the department's own live page but it is a 2023 launch notice, so the current schedule, dates and cost cells are left blank rather than carried forward as if they were confirmed for 2026.",
        source_name="SF Recreation and Parks — Free Pickleball Access Expanded to Palace of Fine Arts",
        source_url="https://sfrecpark.org/m/newsflash/home/detail/1544",
        action="Look for a current Rec and Park page or court booking page that states the 2026 hours and whether the courts are still free, then fill the cells from it."),
    dict(
        id="flag-treasurefest-no-sf-date",
        title="TreasureFest — no confirmed San Francisco date published",
        detail="The row mkt-treasurefest rests on treasurefest.com (fetched 2026-10-18), whose own copy now says 'We're scouting our next location in the Bay Area' and lists no Treasure Island dates. The monthly festival was previously held on Treasure Island — which is inside the City and County of San Francisco — but no 2026 date is published, so the schedule, dates and cost cells are blank.",
        source_name="TreasureFest — official site",
        source_url="https://www.treasurefest.com/",
        action="Watch the organiser's site for a published 2026 San Francisco date. Add it only when the organiser publishes one."),
    dict(
        id="flag-outside-lands-2026-concluded",
        title="Outside Lands Music Festival — 2026 edition concluded, organiser site unavailable",
        detail="The row ann-outside-lands records the 2026 edition, August 7-9, 2026 at Golden Gate Park, from SFMTA's own travel update, and is badged as a concluded edition so nobody plans around a finished event. The organiser's site sfoutsidelands.com returned HTTP 500 on 2026-10-18, so organiser-side ticket and price details could not be read and the cost cell is left blank. The 2027 edition is not published.",
        source_name="SFMTA — Outside Lands: August 7-9, 2026",
        source_url="https://www.sfmta.com/travel-updates/outside-lands-august-7-9-2026",
        action="When the organiser's site is reachable, read the 2027 dates and price and record them then."),
    dict(
        id="flag-current-sf-2026-price-not-published",
        title="Current San Francisco 2026 (Confluent) — admission price not published on the venue listing",
        detail="The row spc-current-sf-2026 takes its dates (November 4-5, 2026) and venue (Moscone West) from the Moscone Center's own event listing, fetched 2026-10-18. The venue listing publishes no admission price and no registration link, so the cost cell is blank and the row is unverified.",
        source_name="Moscone Center — Current San Francisco 2026",
        source_url="https://www.moscone.com/events/current-san-francisco-2026",
        action="Read the price from Confluent's own registration page and fill the cell from that source only."),
    dict(
        id="flag-microsoft-ignite-2026-price-not-published",
        title="Microsoft Ignite 2026 — admission price not published on the venue listing",
        detail="The row spc-microsoft-ignite-2026 takes its dates (November 17-20, 2026) and venue (Moscone Center) from the Moscone Center's own event listing, fetched 2026-10-18. The venue listing publishes no admission price, so the cost cell is blank and the row is unverified.",
        source_name="Moscone Center — Microsoft Ignite 2026",
        source_url="https://www.moscone.com/events/microsoft-ignite-2026",
        action="Read the price from Microsoft's own registration page and fill the cell from that source only."),
    dict(
        id="flag-soulful-sundays-admission-not-published",
        title="Soulful Sundays — admission price not published by SFMTA",
        detail="The row x-w-015 comes from SFMTA's Shared Spaces street-closure listing (fetched 2026-10-18), which publishes the permitted hours (1st and 3rd Fridays, 2 p.m.–midnight) and the permit end date (December 18, 2026) but no admission price, so the cost cell is blank and the row is unverified.",
        source_name="SFMTA — Shared Spaces",
        source_url="https://www.sfmta.com/projects/shared-spaces",
        action="Ask the organiser, Brothers For Change, or find an official page that states the admission, then fill the cell from it."),
    dict(
        id="flag-otsego-shared-space-admission-not-published",
        title="Otsego Avenue Shared Space — admission price not published by SFMTA",
        detail="The row x-w-016 comes from SFMTA's Shared Spaces street-closure listing (fetched 2026-10-18), which publishes the permitted hours (4th Sundays, 12 p.m.–9 p.m.) and the permit end date (October 25, 2026) but no admission price, so the cost cell is blank and the row is unverified.",
        source_name="SFMTA — Shared Spaces",
        source_url="https://www.sfmta.com/projects/shared-spaces",
        action="Ask the organiser, the Excelsior Action Group, or find an official page that states the admission, then fill the cell from it."),
    dict(
        id="flag-larkin-shared-space-admission-not-published",
        title="Larkin Street Tenderloin Shared Space — admission price not published by SFMTA",
        detail="The row x-w-017 comes from SFMTA's Shared Spaces street-closure listing (fetched 2026-10-18), which publishes the permitted hours (2nd Saturdays, 8 a.m.–8 p.m.) and the permit end date (December 12, 2026) but no admission price, so the cost cell is blank and the row is unverified.",
        source_name="SFMTA — Shared Spaces",
        source_url="https://www.sfmta.com/projects/shared-spaces",
        action="Ask the organiser, the Tenderloin Lower Polk Merchant & Property Owners Association, or find an official page that states the admission, then fill the cell from it."),
    dict(
        id="flag-sunset-mercantile-admission-not-published",
        title="Sunset Mercantile Diwali, Día de los Muertos, Holidays on Taraval and Cole Valley Nights — admission price not published",
        detail="Checked 2026-10-18 by arena-9fca0b37 on each organiser page. The Diwali page (sunsetmercantilesf.com/diwali2026/) publishes the date, hours, address and a free-chai mention but no admission price, so the row x-s-015 leaves the cost cell blank. The Día de los Muertos page (sunsetmercantilesf.com/ddlm/) publishes the date, hours and address but no admission price, so the row x-s-016 leaves the cost cell blank. The Holidays on Taraval page (sunsetmercantilesf.com/holidaysontaraval/) publishes the date, hours and address but no admission price, so the row x-s-018 leaves the cost cell blank. The Cole Valley Nights page (sunsetmercantilesf.com/colevalleynights2026/) publishes the date, hours and address but no admission price, so the row x-s-019 leaves the cost cell blank. By contrast the organiser's Sunset Holiday Mercantile page (sunsetmercantilesf.com/sunsetholidaymercantile/) does state 'Admission is free!', so the row x-s-017 keeps its free cost.",
        source_name="Sunset Mercantile — event pages",
        source_url="https://sunsetmercantilesf.com/",
        action="Ask Sunset Mercantile to state the admission on each event page, or find an official statement. Fill in 'Free' only when a page says it."),
    dict(
        id="flag-castro-merchants-admission-not-published",
        title="Castro Art Walk, Castro Holiday Tree Lighting and Castro Menorah Lighting — admission price not published",
        detail="Checked 2026-10-18 by arena-9fca0b37 on the Castro Merchants Association's own event pages. The Castro Art Walk listing (castromerchants.com/events) describes a self-guided tour of local businesses with no admission price, so the row spc-castro-art-walk has a blank cost cell and is marked unverified for price. The Castro Holiday Tree Lighting Ceremony listing (castromerchants.com/events/castro-holiday-tree-lighting-ceremony-2023) publishes the date, the 6:00-6:30 p.m. time and Bank of America Plaza at 501 Castro Street but no admission price, so the row spc-castro-holiday-tree has a blank cost cell and is marked unverified for price (its earlier 'Free' value was an inference from no published price). The Castro Menorah Lighting listing (castromerchants.com/events/castro-menorah-lighting) publishes the date, the 6:00-7:00 p.m. time and Jane Warner Plaza but no admission price, so the row spc-castro-menorah has a blank cost cell and is marked unverified for price (its earlier 'Free' value was an inference from no published price). The same association's own 'Castro Holiday Tree Fundraiser' and 'Halloween in The Castro' listings also publish no price, so the row spc-castro-tree-fundraiser is now marked unverified for price as well.",
        source_name="Castro Merchants Association — Events in the Hood",
        source_url="https://castromerchants.com/events",
        action="Ask the Castro Merchants Association to state the admission on each listing, or find an official statement. Fill in 'Free' only when a page says it."),
    dict(
        id="flag-ocofi-calendar-d3-link-broken",
        title="SF.gov OCOFI calendar — its own District 3 Chinatown Family Summit link returns 404",
        detail="The city's OCOFI upcoming-events calendar (https://www.sf.gov/department-ocofi/events/upcoming, fetched 2026-10-18) links the District 3 Chinatown Family Summit to https://www.sf.gov/event-20261212-district-3-chinatown-family-summit/ , which returns 'We can't find that page'. The same event is published at https://www.sf.gov/event-20261212-district-3-family-summit/ , which loads and states Saturday, December 12, 2026, 11:00 a.m. to 1:30 p.m., Cost: Free, Betty Ann Ong Recreation Center, 1199 Mason Street. The row spc-family-summit-d3-2026-12-12 uses the working URL; the broken calendar link is recorded here so the city can fix it.",
        source_name="SF.gov — Our Children Our Families Initiative, upcoming events",
        source_url="https://www.sf.gov/department-ocofi/events/upcoming",
        action="No catalogue change needed. If you want it confirmed with the city, report the broken calendar link."),
'''

# Flags whose content changed on 2026-10-18.
FLAG_EDITS = [
    (
        '''        id="flag-d10-family-summit-page-missing",
        title="District 10 Bayview Family Summit — individual event page not found",
        detail="The August 20, 2026 SF.gov press release lists Saturday, December 5, 2026, 11:00 a.m.–1:30 p.m., Southeast Community Center, 1550 Evans Avenue. Guessed event-page URLs for that date returned 404 on 2026-10-18. The press release says every Family Summit includes free food and childcare; it does not label admission 'Cost: Free' the way the District 1, 2, 3, 4 and 11 event pages do. No row was added, and free admission was not copied from the sibling pages.",
        source_name="SF.gov — This is Your City: 2026 Family Listening Series",
        source_url="https://www.sf.gov/news-san-francisco-launches-this-is-your-city-2026-family-listening-series",
        action="Add a row only from the District 10 event page once that page is published, and copy Cost: Free only if that page states it."),''',
        '''        id="flag-d10-family-summit-page-missing",
        title="District 10 Bayview Family Summit — event page found on 2026-10-18, row added (resolved)",
        detail="The August 20, 2026 SF.gov press release lists Saturday, December 5, 2026, 11:00 a.m.–1:30 p.m., Southeast Community Center, 1550 Evans Avenue. The earlier guessed event-page URLs for that date returned 404, so no row was added at the time. Re-checked 2026-10-18 by arena-9fca0b37: the city's own OCOFI upcoming-events calendar links the summit to https://www.sf.gov/event-20261205-district-10-family-summit-bayview/ , which loads and states Saturday, December 5, 2026, 11:00 a.m. to 1:30 p.m., Cost: Free, Southeast Community Center, 1550 Evans Avenue, San Francisco, CA 94124. The row spc-family-summit-d10-2026-12-05 has been added from that page, so this item is closed.",
        source_name="SF.gov — District 10 Bayview Family Summit",
        source_url="https://www.sf.gov/event-20261205-district-10-family-summit-bayview/",
        action="Closed on 2026-10-18: the event page was found and the row was added from it. Reopen only if the page changes."),''',
    ),
    (
        '''        id="flag-menorah-date-conflict", title="Castro Menorah Lighting — official page prose and structured date disagree",
        detail="The Castro Merchants' official Menorah Lighting page shows a structured event date of Monday, December 7, 2026, 6:00-7:00 p.m., but its body prose still reads 'on Monday, December 15, at 6 PM' (December 15 was a Monday in 2025, so the prose appears to be stale prior-year copy). The row keeps the structured December 7, 2026 date and this mismatch is published rather than silently resolved.",
        source_name="Castro Merchants — Castro Menorah Lighting",
        source_url="https://castromerchants.com/events/castro-menorah-lighting",
        action="Confirm the 2026 date with Castro Merchants; if the structured date is correct, ask them to update the prose."),''',
        '''        id="flag-menorah-date-conflict", title="Castro Menorah Lighting — official page prose and structured date disagreed, now corrected by the organiser (resolved)",
        detail="The Castro Merchants' official Menorah Lighting page showed a structured event date of Monday, December 7, 2026, 6:00-7:00 p.m., while its body prose read 'on Monday, December 15, at 6 PM' (December 15 was a Monday in 2025, so the prose was stale prior-year copy). Re-checked 2026-10-18 by arena-9fca0b37: the organiser's page has since been corrected and the prose now reads 'on Monday, December 7, at 6 PM'. The row keeps the December 7, 2026 date and the earlier mismatch is published here for the record.",
        source_name="Castro Merchants — Castro Menorah Lighting",
        source_url="https://castromerchants.com/events/castro-menorah-lighting",
        action="Closed on 2026-10-18: the organiser's own page now shows the same date in both places."),''',
    ),
    (
        '''        id="flag-castro-menorah-date",
        title="Castro Menorah Lighting — date conflict on the organiser's own site",
        detail="The Castro Merchants Association events calendar lists the Castro Menorah Lighting on Monday, December 7, 2026, but the event description text says 'on Monday, December 15 at 6 PM'. The row uses the calendar date, December 7, 2026.",
        source_name="Castro Merchants Association — Events in the Hood",
        source_url="https://castromerchants.com/events",
        action="Confirm the date with the Castro Merchants Association."),''',
        '''        id="flag-castro-menorah-date",
        title="Castro Menorah Lighting — date conflict on the organiser's own site (resolved 2026-10-18)",
        detail="The Castro Merchants Association events calendar listed the Castro Menorah Lighting on Monday, December 7, 2026, while the event description text said 'on Monday, December 15 at 6 PM'. Re-checked 2026-10-18 by arena-9fca0b37: the organiser's own event page now reads 'on Monday, December 7, at 6 PM', so the copy has been corrected and the row's December 7, 2026 date stands.",
        source_name="Castro Merchants Association — Events in the Hood",
        source_url="https://castromerchants.com/events",
        action="Closed on 2026-10-18: the organiser's page now shows the same date in both places."),''',
    ),
]

# --------------------------------------------------------------------------
# 4. Corrections applied to the parallel session's imported rows.
#    scripts/merge_parallel.py AUDIT_CORRECTIONS
# --------------------------------------------------------------------------

MERGE_EDITS = [
    (
        '''    "s-020": {
        "dates": "October 15 - November 1, 2026",''',
        '''    "s-015": {
        "cost": "",
        "status": "unverified",
        "_correction_note": (
            "AUDIT CORRECTION (arena-9fca0b37, 2026-10-18): the organiser's own page "
            "https://sunsetmercantilesf.com/diwali2026/ was fetched on 2026-10-18. It states "
            "November 8th, 2026, 9am-2pm, 37th Avenue between Ortega & Quintara, San Francisco, "
            "CA 94116, and mentions free chai, but it publishes no admission price. The "
            "imported 'Free' admission is therefore blanked rather than carried over, and the "
            "row is marked unverified. The parallel session's raw data/special.json is unchanged."
        ),
    },
    "s-016": {
        "cost": "",
        "status": "unverified",
        "source_name": "Sunset Mercantile — Dia de los Muertos Outer Sunset",
        "source_url": "https://sunsetmercantilesf.com/ddlm/",
        "_correction_note": (
            "AUDIT CORRECTION (arena-9fca0b37, 2026-10-18): the organiser's own page "
            "https://sunsetmercantilesf.com/ddlm/ was fetched on 2026-10-18. It states "
            "Sunday, November 1, 2026, 9am-2pm, and gives the location two ways: the page head "
            "says '37th Avenue at Ortega to Pacheco' while its address block says '37th Avenue "
            "between Ortega & Quintara'. It publishes no admission price, so the imported 'Free' "
            "admission is blanked and the row is marked unverified. The parallel session's raw "
            "data/special.json is unchanged."
        ),
    },
    "s-018": {
        "cost": "",
        "status": "unverified",
        "source_name": "Sunset Mercantile — Holidays On Taraval",
        "source_url": "https://sunsetmercantilesf.com/holidaysontaraval/",
        "_correction_note": (
            "AUDIT CORRECTION (arena-9fca0b37, 2026-10-18): the organiser's own page "
            "https://sunsetmercantilesf.com/holidaysontaraval/ was fetched on 2026-10-18. It "
            "states Friday, December 11, 5pm-10pm, and gives the address as 'Taraval Street, "
            "20th-24th Avenue' with the event held at McCoppin Park and Taraval at 22nd. It "
            "publishes no admission price, so the imported 'Free' admission is blanked and the "
            "row is marked unverified. The parallel session's raw data/special.json is unchanged."
        ),
    },
    "s-019": {
        "cost": "",
        "status": "unverified",
        "venue": "Cole Street between Carl and Parnassus Avenue, San Francisco",
        "source_name": "Sunset Mercantile — Cole Valley Nights",
        "source_url": "https://sunsetmercantilesf.com/colevalleynights2026/",
        "_correction_note": (
            "AUDIT CORRECTION (arena-9fca0b37, 2026-10-18): the organiser's own page "
            "https://sunsetmercantilesf.com/colevalleynights2026/ was fetched on 2026-10-18. It "
            "states 'December 10th — Holiday Nights, 4pm - 9pm' and the location 'Cole Street "
            "between Carl and Parnassus, San Francisco, CA' (the imported value said 'Carl "
            "Street at Parnassus Avenue', which is the corner rather than the block), and it "
            "lists the season's market hours as 4/16, 5/21, 8/20, 12/10. It publishes no "
            "admission price, so the imported 'Free' admission is blanked and the row is marked "
            "unverified. The parallel session's raw data/special.json is unchanged."
        ),
    },
    "s-017": {
        "source_name": "Sunset Mercantile — Sunset Holiday Mercantile",
        "source_url": "https://sunsetmercantilesf.com/sunsetholidaymercantile/",
        "_correction_note": (
            "AUDIT CORRECTION (arena-9fca0b37, 2026-10-18): the organiser's own event page "
            "https://sunsetmercantilesf.com/sunsetholidaymercantile/ was fetched on 2026-10-18. "
            "It states 'Saturday, December 5 + Sunday, December 6, 11 am-5 pm' at the San "
            "Francisco County Fair Building in Golden Gate Park and states 'Admission is free!' "
            "and 'Free admission', so the imported 'Free' admission is confirmed and the source "
            "link is upgraded from the organiser's home page to the event page. The parallel "
            "session's raw data/special.json is unchanged."
        ),
    },
    "s-020": {
        "dates": "October 15 - November 1, 2026",''',
    ),
]

# --------------------------------------------------------------------------
# 5. The build writes data/meta.json so its counts cannot drift again.
# --------------------------------------------------------------------------

BUILD_EDITS = [
    (
        '''    print(f"Wrote {len(written)} pages, {len(EVENTS)} events, {len(FLAGGED)} flagged items.")''',
        '''    # Machine-readable site metadata, written from the same data as the pages
    # so the counts can never drift from what is published. (Written here
    # since 2026-10-18 by session arena-9fca0b37; before that the file was
    # hand-maintained and went stale.)
    meta = {
        "site": SITE_NAME,
        "verified_on": VERIFIED_ON,
        "generated_on": str(date.today()),
        "counts": {
            "total": len(EVENTS),
            "recurring": sum(1 for e in EVENTS if e.get("group") == "recurring"),
            "annual": sum(1 for e in EVENTS if e.get("group") == "annual"),
            "special": sum(1 for e in EVENTS if e.get("group") == "special"),
            "flagged_rows": sum(1 for e in EVENTS if e.get("status") != "verified"),
            "unverified_rows": sum(1 for e in EVENTS if e.get("status") != "verified"),
            "concluded_rows": sum(1 for e in EVENTS if e.get("timing") == "concluded"),
            "sources": len({(e.get("source_url") or "").split("/")[2] for e in EVENTS
                            if (e.get("source_url") or "").startswith("https://")}),
            "free_access_rows": sum(1 for e in EVENTS if _has_free_access(e)),
        },
        "focus": {key: sum(1 for e in EVENTS if e.get("focus", "other") == key)
                  for key, _label in FOCUS_LABELS},
        "pages": sorted(written),
        "review_sheet": "data/review.csv",
        "spreadsheet_export": "data/events.csv",
    }
    with open(os.path.join(ROOT, "data", "meta.json"), "w", encoding="utf-8") as fh:
        json.dump(meta, fh, indent=2, ensure_ascii=False)
        fh.write("\\n")

    print(f"Wrote {len(written)} pages, {len(EVENTS)} events, {len(FLAGGED)} flagged items.")''',
    ),
]


def apply_edits(path: str, edits) -> int:
    with open(path, encoding="utf-8") as fh:
        text = fh.read()
    applied = 0
    for old, new in edits:
        if new in text:
            print(f"  = {os.path.basename(path)}: already applied")
            continue
        if old not in text:
            raise SystemExit(
                f"anchor not found in {path}:\n{old[:180]!r}\n"
                "Refusing to guess — re-derive the anchor from the current file."
            )
        if text.count(old) != 1:
            raise SystemExit(f"anchor is not unique in {path}: {old[:120]!r}")
        text = text.replace(old, new, 1)
        applied += 1
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(text)
    return applied


def insert_after(path: str, marker: str, block: str) -> int:
    """Insert ``block`` immediately after the single occurrence of ``marker``."""
    with open(path, encoding="utf-8") as fh:
        text = fh.read()
    if block.strip() in text:
        print(f"  = {os.path.basename(path)}: block already present")
        return 0
    if text.count(marker) != 1:
        raise SystemExit(f"marker is not unique in {path}: {marker[:120]!r}")
    text = text.replace(marker, marker + block, 1)
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(text)
    return 1


def main() -> int:
    print("arena-9fca0b37 corrections")
    n = insert_after(
        EVENTS_PY,
        "that fee is not recorded.\"),\n",
        NEW_ROWS,
    )
    print(f"  + data/events.py: {n} new event rows")
    n = apply_edits(EVENTS_PY, EVENTS_EDITS + [(MENORAH_NOTE_OLD, MENORAH_NOTE_NEW)])
    print(f"  ~ data/events.py: {n} row corrections")
    n = insert_after(
        EVENTS_PY,
        "action=\"Re-open the event page. Add a row only with the hours and cost that page itself states.\"),\n",
        NEW_FLAGS,
    )
    print(f"  + data/events.py: {n} new review items")
    n = apply_edits(EVENTS_PY, FLAG_EDITS)
    print(f"  ~ data/events.py: {n} review-item updates")
    n = apply_edits(MERGE_PY, MERGE_EDITS)
    print(f"  ~ scripts/merge_parallel.py: {n} imported-row corrections")
    n = apply_edits(BUILD_PY, BUILD_EDITS)
    print(f"  ~ scripts/build_site.py: {n} build changes")
    print("done")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
