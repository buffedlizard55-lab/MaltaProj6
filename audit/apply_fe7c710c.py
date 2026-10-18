#!/usr/bin/env python3
"""Apply the `arena-fe7c710c` verification pass to the canonical dataset.

Every row added here was read by hand from the official source named in the
row on 2026-10-18. Nothing is inferred: where the official page publishes no
price the cost cell stays blank and the row is left ``unverified`` so that it
lands on the Flagged for Review page.

Run from the repository root::

    python3 audit/apply_fe7c710c.py
"""

from __future__ import annotations

import io
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EVENTS_PY = os.path.join(ROOT, "data", "events.py")
FOCUS_PY = os.path.join(ROOT, "scripts", "focus.py")

BAND = "Golden Gate Bandshell, 75 Hagiwara Tea Garden Drive, San Francisco, CA 94118"
FULTON = "Fulton Street Plaza, 147 Fulton Street, San Francisco, CA 94102"
SESSION = "arena-fe7c710c"

# ---------------------------------------------------------------------------
# New Illuminate LIVE free concerts, each read from its own official page.
# (id suffix, series, date text, schedule text, location, area, url slug, note)
# ---------------------------------------------------------------------------
ILLUMINATE = [
    ("ccs-2026-10-22", "Civic Center Soundtrack", "Thursday, October 22, 2026",
     "12:00 p.m.–3:00 p.m.", FULTON, "Civic Center",
     "civic-center-soundtrack-october-22",
     "The official page states 'Free live music in Fulton Plaza between the San Francisco Public Library and the Asian Art Museum' and lists three set times."),
    ("ccs-2026-10-27", "Civic Center Soundtrack", "Tuesday, October 27, 2026",
     "12:00 p.m.–3:00 p.m.", FULTON, "Civic Center",
     "civic-center-soundtrack-october-27",
     "The official page states 'Free live music in Fulton Plaza' and lists three set times."),
    ("midweek-2026-10-28", "Midweek Melodies", "Wednesday, October 28, 2026",
     "4:00 p.m.–7:00 p.m.", BAND, "Richmond / Sunset",
     "midweek-melodies-october-28",
     "The official page states 'enjoy free live music from 3 local artists' and lists three set times."),
    ("ccs-2026-10-29", "Civic Center Soundtrack", "Thursday, October 29, 2026",
     "12:00 p.m.–3:00 p.m.", FULTON, "Civic Center",
     "civic-center-soundtrack-october-29",
     "The official page states 'Free live music in Fulton Plaza' and lists three set times."),
    ("happyhour-2026-10-30", "Friday Happy Hour", "Friday, October 30, 2026",
     "4:30 p.m.–7:30 p.m.", BAND, "Richmond / Sunset",
     "friday-happy-hour-october-30",
     "The official page states 'Kick off the weekend with free live music in Golden Gate Park!'"),
    ("reggae-2026-11-01", "Crucial Reggae Sundays", "Sunday, November 1, 2026",
     "4:30 p.m.–7:30 p.m.", BAND, "Richmond / Sunset",
     "crucial-reggae-sundays-november-1",
     "The official page states 'Close out the weekend dancing in the park at Crucial Reggae Sundays' and names the hosts and special guests."),
    ("mtb-2026-11-04", "Market to Bandshell", "Wednesday, November 4, 2026",
     "4:00 p.m.–7:00 p.m.", BAND, "Richmond / Sunset",
     "market-to-bandshell-november-4",
     "The official page states 'This free live concert features up & coming talent from the Sunset Mercantile Farmers Market, showcased on the Golden Gate Bandshell stage!'"),
    ("happyhour-2026-11-06", "Friday Happy Hour", "Friday, November 6, 2026",
     "4:30 p.m.–7:30 p.m.", BAND, "Richmond / Sunset",
     "friday-happy-hour-november-6",
     "The official page states 'Kick off the weekend with free live music in Golden Gate Park!'"),
    ("saturday-2026-11-07", "Saturday at the Bandshell", "Saturday, November 7, 2026",
     "12:00 p.m.–4:00 p.m.", BAND, "Richmond / Sunset",
     "saturday-at-the-bandshell-november-7",
     "The official page currently carries only 'More details coming soon!' and no named performers; the date, time and venue are published."),
    ("reggae-2026-11-08", "Crucial Reggae Sundays", "Sunday, November 8, 2026",
     "12:00 p.m.–7:30 p.m.", BAND, "Richmond / Sunset",
     "crucial-reggae-sundays-november-8",
     "The official page states 'Close out the weekend dancing in the park at Crucial Reggae Sundays' and names the hosts and special guests."),
    ("midweek-2026-11-11", "Midweek Melodies", "Wednesday, November 11, 2026",
     "4:00 p.m.–7:00 p.m.", BAND, "Richmond / Sunset",
     "midweek-melodies-november-11",
     "The official page states 'enjoy free live music from 3 local artists' and lists three set times."),
    ("happyhour-2026-11-13", "Friday Happy Hour", "Friday, November 13, 2026",
     "4:30 p.m.–7:30 p.m.", BAND, "Richmond / Sunset",
     "friday-happy-hour-november-13",
     "The official page states 'Kick off the weekend with free live music in Golden Gate Park!'"),
    ("otisology-2026-11-15", "Nick Otis Presents Otisology: A Tribute to Shuggie & Johnny Otis",
     "Sunday, November 15, 2026", "12:00 p.m.–4:00 p.m.", BAND, "Richmond / Sunset",
     "nick-otis-presents-otisology-a-tribute-to-shuggie-johnny-otis-november-15",
     "The official page currently carries only 'More details coming soon!' and no named performers beyond Nick Otis; the date, time and venue are published."),
]


def illuminate_rows() -> str:
    out = []
    for suffix, series, date_text, schedule, location, area, slug, note in ILLUMINATE:
        rid = f"spc-illuminate-{suffix}"
        out.append(
            f'    dict(\n'
            f'        id="{rid}", title="{series} (Illuminate LIVE)",\n'
            f'        page="special", type="Special - Dated", category="arts",\n'
            f'        schedule="{schedule}", dates="{date_text}",\n'
            f'        location="{location}",\n'
            f'        area="{area}", cost="Free", organiser="Illuminate",\n'
            f'        source_name="Illuminate — {series}, {date_text.split(", ")[1]}",\n'
            f'        source_url="https://illuminate.org/event/{slug}/", status="verified",\n'
            f'        notes="Added by {SESSION} on 2026-10-18 from the organiser\'s own event page, fetched the same day: {note} '
            f'The listing is classified under Illuminate\'s Free Concert category, which is the basis for the cost cell. '
            f'Distinct from the season-long bandshell row."),\n'
        )
    return "".join(out)


AI_ROWS = '''    dict(
        id="spc-osai-debates-2026-10-19", title="Open Weight Debate Night (Open Source AI Week 2026)",
        page="special", type="Special - Dated", category="technology",
        schedule="5:00 p.m.–9:00 p.m.; registration and networking 5:30 p.m., welcome 6:00 p.m., three debates from 6:15 p.m., closing remarks 8:25 p.m.",
        dates="Monday, October 19, 2026",
        location="GitHub Office, 88 Colin P. Kelly Jr. Street, San Francisco, CA 94107",
        area="Mission / SoMa", cost="", organiser="Open Source AI Week, hosted by GitHub",
        source_name="Open Source AI Week — The Debates",
        source_url="https://opensourceaiweek.com/the-debates/", status="unverified",
        notes="Added by SESSION on 2026-10-18. The official week page states Monday, October 19, 2026, 5:00 p.m.–9:00 p.m., GitHub Office — 88 Colin P. Kelly Jr. Street, San Francisco, CA 94107, capacity limited to 250, with three published motions (frontier-weight release risk, affordable access to intelligence, and open vs closed model capability) and named debaters. The page does not publish an admission price, so the cost cell is left blank and the row is flagged. The official page links to the event's Luma registration page, which shows 'Approval Required' and 'Register to See Address' and also publishes no price." .replace("SESSION", "arena-fe7c710c"),
        additional_sources=[{"name": "Open Source AI Week — Luma registration page for the Open Weight Debate Night", "url": "https://luma.com/592fcwx2"}]),
    dict(
        id="spc-osai-awards-2026-10-23", title="Open Source AI Awards Night (Open Source AI Week 2026)",
        page="special", type="Special - Dated", category="technology",
        schedule="5:00 p.m.–9:00 p.m.; arrivals 5:00 p.m., welcome 6:00 p.m., awards from 6:35 p.m., social hour 8:30 p.m.",
        dates="Friday, October 23, 2026",
        location="Founder's Inc, 2 Marina Blvd B300, San Francisco, CA 94123",
        area="Marina", cost="", organiser="Open Source AI Week, hosted by Founder's Inc",
        source_name="Open Source AI Week — Open Source AI Awards",
        source_url="https://opensourceaiweek.com/open-source-ai-awards/", status="unverified",
        notes="Added by SESSION on 2026-10-18. The official week page states Friday, October 23, 2026 — awards night, 5:00 p.m.–9:00 p.m., Founder's Inc — 2 Marina Blvd B300, San Francisco, CA 94123, with six project awards, four individual awards, named speakers and a closing social hour. The page does not publish an admission price, so the cost cell is left blank and the row is flagged. The official page links to the event's Luma registration page, which shows 'Approval Required' and 'Register to See Address' and also publishes no price." .replace("SESSION", "arena-fe7c710c"),
        additional_sources=[{"name": "Open Source AI Week — Luma registration page for the Open Source AI Awards Night", "url": "https://luma.com/7ebvz0oq"}]),
'''

GAMING_ROWS = '''    dict(
        id="rec-dogpatch-games-venue", title="Dogpatch Games — tabletop and board game community hub",
        page="recurring", type="Attraction - Open regularly", category="community",
        schedule="Open 2:00 p.m.–10:00 p.m. Monday to Friday and 12:00 p.m.–10:00 p.m. Saturday and Sunday",
        dates="",
        location="Dogpatch Games, 1095 Tennessee Street, San Francisco, CA 94107",
        area="Dogpatch / SoMa",
        cost="$5 per hour per person for non-members (parties of six or less); $8 per hour per person for private rooms and large-group table play (seven or more); two hours free daily for Basic Members; unlimited for Premier Members",
        organiser="Dogpatch Games",
        source_name="Dogpatch Games — Table Rates",
        source_url="https://www.dogpatch.games/tablerates", status="verified",
        additional_sources=[{"name": "Dogpatch Games — home page (address and opening hours)", "url": "https://www.dogpatch.games/"}],
        notes="Added by SESSION on 2026-10-18. The venue's own rates page publishes regular table play at $5 per hour per person for non-members (parties of six or less) and $8 per hour per person for private rooms and large-group table play (parties of seven or more), with two hours free daily for Basic Members and unlimited play for Premier Members. Opening hours and the address come from the venue's home page, which states '2pm - 10pm Mon to Fri, 12pm - 10pm Sat to Sun' at 1095 Tennessee St. Guided private events, private D&D and private RPG packages are priced separately and are not repeated here." .replace("SESSION", "arena-fe7c710c")),
    dict(
        id="rec-dogpatch-boardgame-league", title="Recreational Board Game League (Wednesdays) — Dogpatch Games",
        page="recurring", type="Recurring - Weekly", category="community",
        schedule="Wednesdays, 7:00 p.m.–9:00 p.m.; teams of four to six play a different game each week across a nine-week season",
        dates="Wednesdays, September 23 - November 18, 2026 (fall season)",
        location="Dogpatch Games, 1095 Tennessee Street, San Francisco, CA 94107",
        area="Dogpatch / SoMa",
        cost="$200 for the nine-week season; $100 for Basic Members; free for Premier Members",
        organiser="Dogpatch Games",
        source_name="Dogpatch Games — Boardgame League",
        source_url="https://www.dogpatch.games/team-league", status="verified",
        notes="Added by SESSION on 2026-10-18. The league page states 'Fall Recreational League starts Wednesday, September 23, 2026', 'Wednesdays, September 23 - November 18, 2026 7:00pm - 9:00pm', 'Individual Pricing: $200 (Basic Member Pricing $100, Free for Premier Members)' and 'Includes all playtime for 9 weeks of league sessions, prizes and more!'. Individual sign-ups are paired with other teams. A separate solo competitive tournament is priced at $75 per month." .replace("SESSION", "arena-fe7c710c")),
    dict(
        id="spc-dogpatch-love-potion-2026-10-22", title="Game Night at Love Potion Library (hosted by Dogpatch Games)",
        page="special", type="Special - Dated", category="community",
        schedule="6:00 p.m.–8:00 p.m.",
        dates="Thursday, October 22, 2026",
        location="Love Potion Library, 284 Noe Street, San Francisco, CA 94114",
        area="Castro / Mission", cost="",
        organiser="Dogpatch Games with The Love Potion Library",
        source_name="Dogpatch Games — Special Event: Game Night at Love Potion Library",
        source_url="https://www.dogpatch.games/events1/love-potion-library-2026-10-22-gaxsg", status="unverified",
        additional_sources=[{"name": "The Love Potion Library — Game Night with Dogpatch Games (RSVP page)", "url": "https://luma.com/k8ahxhhd"}],
        notes="Added by SESSION on 2026-10-18. The organiser's own event page states Thursday, October 22, 2026, 6:00 p.m.–8:00 p.m., at The Love Potion Library, 284 Noe St, San Francisco, CA 94114, hosted by Dogpatch Games with RSVP on the venue's Luma page. The page does not publish an admission price, so the cost cell is left blank and the row is flagged. The venue's own listing describes it as a bookstore and tea room in the Castro." .replace("SESSION", "arena-fe7c710c")),
'''

NEW_FLAGS = '''    dict(
        id="flag-opensource-ai-week-bay-area-scope",
        title="Open Source AI Week 2026 (Oct 16–25) spans the whole Bay Area — only the San Francisco flagship events are listed",
        detail="The official week site describes Open Source AI Week 2026 as 'October 16-25, 2026 · The Bay Area' with '66 Events across the Bay Area', and its calendar lists events in San Francisco, San Jose, Menlo Park, Sunnyvale, Palo Alto and Santa Clara. This project covers the City of San Francisco only, so the two San Francisco-city flagship events are listed as rows (Open Weight Debate Night at GitHub Office, Oct 19; Open Source AI Awards at Founder's Inc, Oct 23) and the week itself is not listed as a single city-wide entry. The week also publishes a Founders' Coffee on Thursday, October 22, 2026 at 9:00 a.m. whose only cost wording anywhere on the official calendar is the word 'Free'; its venue is published as 'location tbd', so the row was not added because the event could not be confirmed to be inside the city limits. The week also contains a physical-AI and open-source hackathon, several meetups and a demo night that are not listed here.",
        source_name="Open Source AI Week — official site and community calendar",
        source_url="https://opensourceaiweek.com/community-events/",
        action="If the Founders' Coffee publishes a San Francisco venue, add it as a free AI row; otherwise leave it recorded here."),
    dict(
        id="flag-opensource-ai-awards-end-time",
        title="Open Source AI Awards Night — official site and its own registration page give different end times",
        detail="The official Open Source AI Week page for the Awards Night states 'Time: 5:00 PM – 9:00 PM'. The Luma registration page linked from that same official page lists '5:00 PM - 10:00 PM PDT'. The row records the official site's 5:00 p.m.–9:00 p.m. Because the two official pages disagree, the end time is worth confirming with the organiser.",
        source_name="Open Source AI Week — Open Source AI Awards",
        source_url="https://opensourceaiweek.com/open-source-ai-awards/",
        action="Ask the organiser which end time is correct before publishing a programme."),
    dict(
        id="flag-dogpatch-love-potion-cost",
        title="Game Night at Love Potion Library (Oct 22) — admission price not published",
        detail="The organiser's own event page for the Thursday, October 22, 2026 game night at The Love Potion Library publishes the date, time and venue but no admission price, and the venue's RSVP page shows a plain 'Register' button with no amount. The cost cell is therefore blank and the row is marked unverified rather than being presented as free.",
        source_name="Dogpatch Games — Special Event: Game Night at Love Potion Library",
        source_url="https://www.dogpatch.games/events1/love-potion-library-2026-10-22-gaxsg",
        action="Check with the venue on arrival or via the RSVP page; record the price here once it is published."),
    dict(
        id="flag-sfpl-afternoon-board-games-status",
        title="SFPL 'Social: Afternoon Board Games' (Oct 18) — cancellation status could not be confirmed",
        detail="The library's own event page for Sunday, 10/18/2026, 1:00 – 4:00 at the Sunset Children's Area was fetched on 2026-10-18 and renders the event as scheduled, with the 'Gaming' topic tag and the 'sponsored by Friends of the San Francisco Public Library' note, and no cancellation notice anywhere on the page. A search-engine cache of the same page carries the heading 'Canceled: Social: Afternoon Board Games'. The live official page is treated as authoritative and the library's standing gaming-programme row was not changed, but the conflicting cached heading is recorded here for a human to check.",
        source_name="San Francisco Public Library — Social: Afternoon Board Games",
        source_url="https://sfpl.org/events/2026/10/18/social-afternoon-board-games",
        action="Call the Sunset branch (415-355-2808) or re-check the event page to confirm whether the October 18 session is running."),
    dict(
        id="flag-dogpatch-games-not-free",
        title="Dogpatch Games and its league are not free events — listed under their published prices",
        detail="The board-game community hub at 1095 Tennessee Street charges $5 per hour per person for non-members, and the Wednesday Recreational Board Game League is $200 for the nine-week season. Both are listed as gaming rows with the exact published prices so that the cost of gaming in San Francisco is visible, and both are kept out of the free list. The one genuinely free item in this organiser's output that is confirmed by an official page is not a Dogpatch Games event: The Mix at the San Francisco Public Library.",
        source_name="Dogpatch Games — Table Rates",
        source_url="https://www.dogpatch.games/tablerates",
        action="No action needed; this note exists so the gaming rows are not mistaken for free events."),
'''


def insert_after(text: str, anchor: str, payload: str) -> str:
    idx = text.find(anchor)
    if idx == -1:
        raise SystemExit(f"anchor not found: {anchor[:80]!r}")
    # find the end of the dict block that contains the anchor: the next
    # top-level "    dict(" opener, or the closing "]" of the list.
    nxt = text.find("\n    dict(\n", idx)
    if nxt == -1:
        end = text.find("\n]\n", idx)
        if end == -1:
            raise SystemExit(f"block end not found for {anchor[:80]!r}")
        end += 1
    else:
        end = nxt + 1
    return text[:end] + payload + text[end:]


def main() -> int:
    src = io.open(EVENTS_PY, encoding="utf-8").read()
    if "spc-illuminate-ccs-2026-10-22" in src:
        print("already applied")
        return 0

    # 1. Illuminate rows, after the last existing Illuminate row.
    src = insert_after(src, 'id="spc-illuminate-halloween-2026-10-31"', illuminate_rows())

    # 2. AI rows, after the existing Week of AI row.
    src = insert_after(src, 'id="spc-ai-week-sf-2026"', AI_ROWS)

    # 3. Gaming rows, after the library's citywide gaming row.
    src = insert_after(src, 'id="rec-sfpl-gaming-citywide"', GAMING_ROWS)

    # 4. New review items, at the head of the FLAGGED list.
    anchor = "FLAGGED = [\n"
    idx = src.find(anchor)
    if idx == -1:
        raise SystemExit("FLAGGED list not found")
    src = src[: idx + len(anchor)] + NEW_FLAGS + src[idx + len(anchor):]

    io.open(EVENTS_PY, "w", encoding="utf-8").write(src)

    # 5. Focus tags.
    focus = io.open(FOCUS_PY, encoding="utf-8").read()
    music_tags = "".join(
        f'    "spc-illuminate-{suffix}": "music",\n' for suffix, *_ in ILLUMINATE
    )
    focus = focus.replace(
        '    # --- AI -------------------------------------------------------------\n',
        "    # --- arena-fe7c710c additions (2026-10-18) ---------------------------\n"
        + music_tags
        + '    "spc-osai-debates-2026-10-19": "ai",\n'
        + '    "spc-osai-awards-2026-10-23": "ai",\n'
        + '    "rec-dogpatch-games-venue": "gaming",\n'
        + '    "rec-dogpatch-boardgame-league": "gaming",\n'
        + '    "spc-dogpatch-love-potion-2026-10-22": "gaming",\n'
        + "\n"
        + '    # --- AI -------------------------------------------------------------\n',
        1,
    )
    io.open(FOCUS_PY, "w", encoding="utf-8").write(focus)

    print("applied arena-fe7c710c additions")
    return 0


if __name__ == "__main__":
    sys.exit(main())
