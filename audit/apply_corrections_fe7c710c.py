#!/usr/bin/env python3
"""Corrections found by the `arena-fe7c710c` line-by-line verification pass.

Every change here was made after fetching the row's own official source on
2026-10-18 and reading the published text.

1. **Cost cells that the official page does not publish are blanked.**
   The Castro Merchants Association pages and most Sunset Mercantile event
   pages publish no admission price at all, yet the rows carried a bare
   "Free" (inherited from an earlier integration). Under this project's rule
   -- leave a value blank and flag it as unverified rather than infer it --
   those cells are blanked and the rows are marked ``unverified``.

2. **Source links are sharpened to the event's own page.**
   The Sunset Mercantile rows pointed at the organisation's home page. Each
   now points at the page for that specific event, which is the page that
   carries the date and time.

3. **The Castro Menorah date conflict is resolved.**
   The organiser's page body used to say "Monday, December 15" while its
   calendar listing said December 7, 2026. The body now reads "Monday,
   December 7", matching the listing, so the row's structured date is
   correct and the review item is updated rather than left open.

Rows that live in ``data/events.py`` are edited there. Rows that came from the
preserved parallel tranche (``data/weekly.json`` / ``data/special.json``) are
edited through ``scripts/merge_parallel.py``'s override table, so the
preserved research files stay exactly as they were recorded.

Run from the repository root::

    python3 audit/apply_corrections_fe7c710c.py
"""

from __future__ import annotations

import io
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EVENTS_PY = os.path.join(ROOT, "data", "events.py")
MERGE_PY = os.path.join(ROOT, "scripts", "merge_parallel.py")

# ---------------------------------------------------------------------------
# Rows in data/events.py: id -> {field: new value}
# ---------------------------------------------------------------------------
EVENTS_FIXES = {
    "spc-castro-holiday-tree": {
        "cost": "",
        "status": "unverified",
        "notes": (
            "Re-checked 2026-10-18 by session arena-fe7c710c. The organiser's event page "
            "confirms 'Castro Holiday Tree Lighting Ceremony 2026', Monday, November 30, "
            "2026, 6:00 PM - 6:30 PM PDT, Bank of America Plaza at 501 Castro Street. The "
            "page publishes no admission price, so the cost cell has been blanked and the "
            "row marked unverified rather than presented as free. The page URL slug still "
            "reads '2023' although the page is the 2026 edition. See Flagged for Review."
        ),
    },
    "spc-castro-art-walk": {
        "source_url": (
            "https://castromerchants.com/events/event-two-bmpss-x9twa-cchrg-k7z72-f4j9e-2lpxg-"
            "dspen-dfb7l-jpma9-8zzy5-sl46a-dlk63-sdb58-yhyke-bry5g-shj4l-5ls3k"
        ),
        "cost": "",
        "status": "unverified",
        "notes": (
            "Re-checked 2026-10-18 by session arena-fe7c710c. The organiser's own 'Castro "
            "Art Walk November' page confirms Friday, November 6, 2026, 5:00 PM - 8:00 PM, "
            "and the events index also lists 'Castro Art Walk December' on Friday, "
            "December 4, 2026, 5:00 PM - 8:00 PM, both described as 'a self-guided tour and "
            "community-driven event where local businesses host special events'. Neither "
            "page publishes an admission price, so the cost cell has been blanked and the "
            "row marked unverified rather than presented as free. See Flagged for Review."
        ),
    },
    "spc-castro-menorah": {
        "cost": "",
        "status": "unverified",
        "notes": (
            "Re-checked 2026-10-18 by session arena-fe7c710c. The organiser's event page now "
            "reads 'at Jane Warner Plaza on Monday, December 7, at 6 PM', which agrees with "
            "the calendar listing of Monday, December 7, 2026, 6:00 PM - 7:00 PM; the "
            "earlier 'December 15' wording in the body text no longer appears, so the row's "
            "date of Monday, December 7, 2026 is correct. The page publishes no admission "
            "price, so the cost cell has been blanked and the row marked unverified rather "
            "than presented as free. See Flagged for Review."
        ),
    },
}

# ---------------------------------------------------------------------------
# Rows carried over from the preserved parallel tranche:
# orig id -> (source_url, cost, extra fields, note)
# ---------------------------------------------------------------------------
PARALLEL_FIXES = {
    "w-009": (
        "https://sunsetmercantilesf.com/osfmm/", "", {},
        "Re-checked 2026-10-18 by session arena-fe7c710c: the event's own page confirms "
        "'SUNDAYS', 9 am - 2 pm, 37th Avenue at Ortega to Quintara, 'Year-round RAIN or "
        "SHINE', presented by Sunset Mercantile with OEWD and the People of Parkside Sunset. "
        "The page describes a 'Free library at the Artship' and free yoga but does not state "
        "an admission price for the market itself, so the cost cell has been blanked and the "
        "row marked unverified rather than presented as free. See Flagged for Review.",
        True,
    ),
    "w-010": (
        "https://sunsetmercantilesf.com/innersunsetflea/", "", {},
        "Re-checked 2026-10-18 by session arena-fe7c710c: the event's own page confirms "
        "'SECOND SUNDAYS', 10 am - 4 pm, Irving Street at 9th-11th Avenues, April-November, "
        "and publishes the 2026 season schedule (April 12 'Spring Fling Market' - marked "
        "cancelled on the page - May 10, June 14, July 12, August 9, September 13, October "
        "11, November 8). The page states no admission price, so the cost cell stays blank "
        "and the row is marked unverified.",
        True,
    ),
    "w-011": (
        "https://sunsetmercantilesf.com/secondhand/", "", {},
        "Re-checked 2026-10-18 by session arena-fe7c710c: the event's own page confirms "
        "'THIRD SATURDAY MONTHLY', 10 am - 4 pm, 37th Avenue at Ortega to Quintara, "
        "April-November, with 60+ vintage vendors, and publishes the 2026 season schedule "
        "(April 18, May 16, June 20, July 18, August 15, September 19, October 17, "
        "November 21). The page states no admission price, so the cost cell stays blank and "
        "the row is marked unverified.",
        True,
    ),
    "s-015": (
        "https://sunsetmercantilesf.com/diwali2026/", "", {},
        "Re-checked 2026-10-18 by session arena-fe7c710c: the event's own page confirms "
        "'November 8th, 2026', 9am-2pm, 37th Avenue at Ortega to Quintara, the fourth annual "
        "Diwali Festival. The page mentions free chai and a separate paid raffle ($5 per "
        "ticket, five for $20) but does not state an admission price for the festival, so "
        "the cost cell has been blanked and the row marked unverified rather than presented "
        "as free. See Flagged for Review.",
        True,
    ),
    "s-016": (
        "https://sunsetmercantilesf.com/ddlm/", "", {},
        "Re-checked 2026-10-18 by session arena-fe7c710c: the event's own page confirms "
        "'Sunday, November 1, 2026', 9am to 2pm, 37th Avenue at Ortega to Pacheco, Sunset "
        "Mercantile's fifth annual Dia de los Muertos. The page does not state an admission "
        "price, so the cost cell has been blanked and the row marked unverified rather than "
        "presented as free. See Flagged for Review.",
        True,
    ),
    "s-017": (
        "https://sunsetmercantilesf.com/sunsetholidaymercantile/", "Free", {},
        "Re-checked 2026-10-18 by session arena-fe7c710c: the event's own page confirms "
        "'SATURDAY, DEC. 5 + SUNDAY DEC. 6', 11 am - 5 pm, San Francisco County Fair "
        "Building, Golden Gate Park, and states 'Admission is free! Come to the County Fair "
        "Building in Golden Gate Park, December 5th and 6th from 11 AM to 5 PM' and 'Free "
        "admission'. The free cost cell is therefore confirmed by the official source.",
        False,
    ),
    "s-018": (
        "https://sunsetmercantilesf.com/holidaysontaraval/", "", {},
        "Re-checked 2026-10-18 by session arena-fe7c710c: the event's own page confirms "
        "'FRIDAY, DECEMBER 11', 5pm - 10pm, McCoppin Park and Taraval at 22nd, with the "
        "annual tree lighting, performances, art and games along Taraval Street from 20th to "
        "24th Avenue. The page does not state an admission price, so the cost cell has been "
        "blanked and the row marked unverified rather than presented as free. See Flagged "
        "for Review.",
        True,
    ),
    "s-019": (
        "https://sunsetmercantilesf.com/colevalleynights2026/", "", {},
        "Re-checked 2026-10-18 by session arena-fe7c710c: the event's own page confirms "
        "'December 10th - Holiday Nights', 4pm - 9pm, Cole Street between Carl and Parnassus "
        "Avenue, and publishes its market dates as 4/16, 5/21, 8/20 and 12/10. The page does "
        "not state an admission price, so the cost cell has been blanked and the row marked "
        "unverified rather than presented as free. See Flagged for Review.",
        True,
    ),
}

NEW_FLAGS = '''    dict(
        id="flag-castro-merchants-cost-not-published",
        title="Castro Merchants Association listings publish no admission price — three 'Free' cost cells blanked",
        detail="The organiser's own event pages for the Castro Holiday Tree Lighting Ceremony (November 30, 2026), the Castro Art Walk (first Friday of every month) and the Castro Menorah Lighting (December 7, 2026) were fetched on 2026-10-18. Each one publishes its date, time, venue and description, and none of them states an admission price. The rows previously carried a bare 'Free', which is an inference rather than a published fact, so the cost cells have been blanked and the rows marked unverified. The Art Walk source link now points at the November event page rather than the events index, and the Menorah date conflict is resolved because the organiser's body text now reads 'Monday, December 7' instead of the earlier 'December 15'.",
        source_name="Castro Merchants Association — events",
        source_url="https://castromerchants.com/events",
        action="Ask the Castro Merchants Association whether these ceremonies and the Art Walk charge admission, and record the answer here."),
    dict(
        id="flag-sunset-mercantile-cost-not-published",
        title="Sunset Mercantile event pages publish no admission price — five 'Free' cost cells blanked",
        detail="The event pages for the Outer Sunset Farmers Market & Mercantile, Diwali 2026 at the Outer Sunset Farmers Market, Dia de los Muertos Outer Sunset, Holidays on Taraval and Cole Valley Nights were each fetched on 2026-10-18. Every one of them publishes its date, hours and address but no admission price, so the 'Free' cost cells have been blanked and the rows marked unverified. The Sunset Holiday Mercantile row is the exception: its own page states 'Admission is free!' and 'Free admission', so that row keeps its free cost cell. Each of these rows now links to the page for that specific event instead of the organisation's home page.",
        source_name="Sunset Mercantile — official site",
        source_url="https://sunsetmercantilesf.com/",
        action="Ask Sunset Mercantile whether admission is charged at the Outer Sunset Farmers Market, Diwali, Dia de los Muertos, Holidays on Taraval and Cole Valley Nights, and record the answer here."),
    dict(
        id="flag-castro-holiday-tree-url-slug",
        title="Castro Holiday Tree Lighting Ceremony — official page URL slug still reads '2023'",
        detail="The organiser's event page for the 2026 ceremony is published at a URL whose slug ends in '2023' (https://castromerchants.com/events/castro-holiday-tree-lighting-ceremony-2023). The page's own title, heading and body all say 'Castro Holiday Tree Lighting Ceremony 2026' and give Monday, November 30, 2026, 6:00 PM - 6:30 PM PDT, Bank of America Plaza at 501 Castro Street. The date and time in the row are therefore taken from the live page, not from the slug, but the mismatched slug is worth confirming with the organiser in case a 2023 page is later restored at that address.",
        source_name="Castro Merchants Association — Castro Holiday Tree Lighting Ceremony 2026",
        source_url="https://castromerchants.com/events/castro-holiday-tree-lighting-ceremony-2023",
        action="Confirm with the organiser that this URL continues to point at the 2026 ceremony, and re-check the page before the next rebuild."),
'''

ROW_START = "\n    dict(\n"


def row_bounds(src: str, rid: str) -> tuple[int, int]:
    """Return the (start, end) character span of the ``dict(...)`` for ``rid``."""
    marker = f'id="{rid}"'
    idx = src.find(marker)
    if idx == -1:
        raise SystemExit(f"row not found: {rid}")
    start = src.rfind(ROW_START, 0, idx)
    if start == -1:
        raise SystemExit(f"row start not found: {rid}")
    nxt = src.find(ROW_START, idx)
    close = src.find("\n]\n", idx)
    end = nxt + 1 if nxt != -1 and (close == -1 or nxt < close) else close + 1
    return start, end


def patch_row(src: str, rid: str, updates: dict) -> str:
    """Set each field inside the row's own ``dict(...)`` block."""
    for _ in range(len(updates)):
        start, end = row_bounds(src, rid)
        block = src[start:end]
        missing = [f for f in updates if not re.search(rf'\b{re.escape(f)}="', block)]
        if not missing:
            break
        # add the missing field just before the block's closing paren
        close = block.rfind("),")
        field = missing[0]
        insertion = f'{field}="{updates[field]}", '
        block = block[:close] + insertion + block[close:]
        src = src[:start] + block + src[end:]
    start, end = row_bounds(src, rid)
    block = src[start:end]
    for field, value in updates.items():
        pattern = re.compile(rf'(\b{re.escape(field)}=")([^"]*)(")')
        if not pattern.search(block):
            raise SystemExit(f"field {field} still missing in {rid}")
        block = pattern.sub(lambda m: m.group(1) + value + m.group(3), block, count=1)
    return src[:start] + block + src[end:]


def apply_events_fixes(src: str) -> str:
    for rid, updates in EVENTS_FIXES.items():
        src = patch_row(src, rid, updates)
    anchor = "FLAGGED = [\n"
    idx = src.find(anchor)
    if idx == -1:
        raise SystemExit("FLAGGED list not found")
    return src[: idx + len(anchor)] + NEW_FLAGS + src[idx + len(anchor):]


def build_override_block(orig: str, source_url: str, cost: str,
                         extra: dict, note: str, force_unverified: bool) -> str:
    body = [
        f'        "source_url": "{source_url}",',
        f'        "cost": "{cost}",',
    ]
    if force_unverified:
        body.append('        "_force_unverified": True,')
    for key, value in extra.items():
        body.append(f'        "{key}": "{value}",')
    body.append(f'        "_override_note": "{note}",')
    return f'    "{orig}": {{\n' + "\n".join(body) + "\n    },\n"


def apply_merge_fixes(src: str) -> str:
    anchor = """                if override.get("_clear_unverified"):
                    rec["_unverified"] = []
                    rec["status"] = "verified"
"""
    if "_force_unverified" not in src:
        if anchor not in src:
            raise SystemExit("merge anchor not found")
        src = src.replace(anchor, anchor + """                if override.get("_force_unverified"):
                    rec["_unverified"] = ["admission"]
                    rec["status"] = "unverified"
""", 1)

    for orig, (source_url, cost, extra, note, force) in PARALLEL_FIXES.items():
        block = build_override_block(orig, source_url, cost, extra, note, force)
        key = f'    "{orig}": {{\n'
        idx = src.find(key)
        if idx == -1:
            start = src.find("FIELD_OVERRIDES = {")
            if start == -1:
                raise SystemExit("FIELD_OVERRIDES not found")
            end = src.find("\n}\n", start)
            if end == -1:
                raise SystemExit("FIELD_OVERRIDES end not found")
            src = src[:end + 1] + block + src[end + 1:]
            continue
        end = src.find("\n    },\n", idx)
        if end == -1:
            raise SystemExit(f"override block end not found for {orig}")
        src = src[:idx] + block + src[end + len("\n    },\n"):]
    return src


def main() -> int:
    ev = io.open(EVENTS_PY, encoding="utf-8").read()
    if "flag-castro-merchants-cost-not-published" in ev:
        print("already applied")
        return 0
    io.open(EVENTS_PY, "w", encoding="utf-8").write(apply_events_fixes(ev))

    mg = io.open(MERGE_PY, encoding="utf-8").read()
    io.open(MERGE_PY, "w", encoding="utf-8").write(apply_merge_fixes(mg))

    print(f"applied {len(EVENTS_FIXES)} canonical corrections, "
          f"{len(PARALLEL_FIXES)} parallel-tranche overrides and 3 new review items")
    return 0


if __name__ == "__main__":
    sys.exit(main())
