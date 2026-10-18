#!/usr/bin/env python3
"""Apply the arena-9fca0b37 corrections to the published dataset and site.

Session: ``arena-9fca0b37`` (2026-10-18), eleventh verification pass —
**version 2, reconciled with PRs #42-#44** (session ``arena-fe7c710c``).

Version 1 of this script was prepared while ``arena-fe7c710c`` held the live
claim on the shared files. That session then merged an overlapping integration
(Castro and Sunset Mercantile price blanking, the Menorah date correction,
``data/meta.json`` written by the build, README refresh). Every change it
already made was removed from this script; what remains is only what its pass
did not cover:

* 7 new rows read from their own official pages (District 10 Bayview Family
  Summit — free; six Exploratorium After Dark editions — ticketed);
* 7 row corrections (4 SF Opera prices/times, 3 SF Symphony start times);
* 13 register items (12 new + 1 coverage group) and updates to the 3 review
  items whose facts changed (District 10 page found; Menorah prose corrected
  by the organiser).

Every value below was checked against the page named in the row's own
``source_url`` on 2026-10-18. The script is idempotent: running it twice
leaves the tree unchanged (replacements are exact-string edits, already-patched
content is skipped, and a missing anchor aborts loudly instead of guessing).

Run with:  python3 audit/apply_9fca0b37.py
"""
from __future__ import annotations

import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EVENTS_PY = os.path.join(ROOT, "data", "events.py")

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

EVENTS_EDITS = [
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
]

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
        id="flag-ocofi-calendar-d3-link-broken",
        title="SF.gov OCOFI calendar — its own District 3 Chinatown Family Summit link returns 404",
        detail="The city's OCOFI upcoming-events calendar (https://www.sf.gov/department-ocofi/events/upcoming, fetched 2026-10-18) links the District 3 Chinatown Family Summit to https://www.sf.gov/event-20261212-district-3-chinatown-family-summit/ , which returns 'We can't find that page'. The same event is published at https://www.sf.gov/event-20261212-district-3-family-summit/ , which loads and states Saturday, December 12, 2026, 11:00 a.m. to 1:30 p.m., Cost: Free, Betty Ann Ong Recreation Center, 1199 Mason Street. The row spc-family-summit-d3-2026-12-12 uses the working URL; the broken calendar link is recorded here so the city can fix it.",
        source_name="SF.gov — Our Children Our Families Initiative, upcoming events",
        source_url="https://www.sf.gov/department-ocofi/events/upcoming",
        action="No catalogue change needed. If you want it confirmed with the city, report the broken calendar link."),
    dict(
        id="flag-unverified-rows-register-coverage",
        title="Unverified rows whose narrative record lives in another review item (or in the row's own note)",
        detail="A group entry so that every unverified row is also addressable in this register by its row id. Each row below is published with its official source in the flagged rows table of this page and is marked unverified because its official page publishes no admission price: rec-ferry-building-marketplace (ferrybuildingmarketplace.com; also narrated by flag-four-more-free-claims-unpublished), spc-castro-art-walk (castromerchants.com; also narrated by flag-castro-merchants-cost-not-published), mkt-sf-chinatown-food (moonfestival.org; also narrated by flag-four-more-free-claims-unpublished), spc-dogpatch-love-potion-2026-10-22 (dogpatch.games; also narrated by flag-dogpatch-love-potion-cost), spc-osai-debates-2026-10-19 and spc-osai-awards-2026-10-23 (opensourceaiweek.com; also narrated by flag-opensource-ai-week-bay-area-scope), x-w-010 (sunsetmercantilesf.com/innersunsetflea/), and x-s-015 (sunsetmercantilesf.com/diwali2026/; also narrated by flag-sunset-mercantile-cost-not-published). Added after the merge of PR #45 (session arena-8eaf6c0a): rec-sfzinefest-zinething and ann-sf-zine-fest (sfzinefest.org), spc-osms-st-francis-relics-2026 (osmsf.org) and spc-somarts-in-the-shadows-2027 (somarts.org), each unverified because its official page publishes no admission price, with the narrative in the row's own note. No value has been changed here; this item only makes the coverage explicit.",
        source_name="San Francisco Events — flagged for review page",
        source_url="https://buffedlizard55-lab.github.io/MaltaProj6/flagged.html",
        action="If a row's situation changes, update its own row first; then split this group entry into a per-row item or close it."),
'''

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
    (
        '''        detail="The catalogue has two separate signals and they do not always agree: a blank cell means the official source does not state that value, while the verified / unverified badge means the row's published values were confirmed against the source. A recurring programme can be fully verified while legitimately having no single confirmed date. As of the 2026-10-18 build, 156 rows are marked verified and 28 of them still have at least one blank among schedule, location and cost. Separately, 111 rows publish no day-level date at all, which is expected for weekly and open-ended programmes. This is recorded rather than silently changed because re-badging those verified rows as unverified would misrepresent them.",''',
        '''        detail="The catalogue has two separate signals and they do not always agree: a blank cell means the official source does not state that value, while the verified / unverified badge means the row's published values were confirmed against the source. A recurring programme can be fully verified while legitimately having no single confirmed date. As of the 2026-10-18 build by session arena-9fca0b37, 174 rows are marked verified and 23 of them still have at least one blank among schedule, location and cost. Separately, 113 rows publish no day-level date at all, which is expected for weekly and open-ended programmes. This is recorded rather than silently changed because re-badging those verified rows as unverified would misrepresent them.",''',
    ),
]


def apply_edits(path: str, edits) -> int:
    with open(path, encoding="utf-8") as fh:
        text = fh.read()
    applied = 0
    for old, new in edits:
        if new in text:
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


def insert_after(path: str, marker: str, block: str, probe: str = "") -> int:
    """Insert ``block`` immediately after the single occurrence of ``marker``.

    Already-applied state is detected by ``probe`` (a stable id inside the
    block) when given, so later edits to the block's wording do not cause a
    duplicate insert; otherwise by the block's exact text.
    """
    with open(path, encoding="utf-8") as fh:
        text = fh.read()
    if (probe or block.strip()) in text:
        return 0
    if text.count(marker) != 1:
        raise SystemExit(f"marker is not unique in {path}: {marker[:120]!r}")
    text = text.replace(marker, marker + block, 1)
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(text)
    return 1


def main() -> int:
    print("arena-9fca0b37 corrections (v2, reconciled with PRs #42-#44)")
    n = insert_after(
        EVENTS_PY,
        "that fee is not recorded.\"),\n",
        NEW_ROWS,
    )
    print(f"  + data/events.py: {n} new event rows")
    n = apply_edits(EVENTS_PY, EVENTS_EDITS)
    print(f"  ~ data/events.py: {n} row corrections")
    n = insert_after(
        EVENTS_PY,
        "action=\"Re-open the event page. Add a row only with the hours and cost that page itself states.\"),\n",
        NEW_FLAGS,
        probe="flag-unverified-rows-register-coverage",
    )
    print(f"  + data/events.py: {n} new review items")
    n = apply_edits(EVENTS_PY, FLAG_EDITS)
    print(f"  ~ data/events.py: {n} review-item updates")
    print("done")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
