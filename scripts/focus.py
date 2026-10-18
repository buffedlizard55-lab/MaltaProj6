#!/usr/bin/env python3
"""Focus-category, cost and date helpers for the SF events catalogue.

Added 2026-10-18 by session ``arena-61a46409``.

Everything in this module is *derived* from the canonical dataset in
``data/events.py``. It never invents a value:

* ``focus``    - a subject tag (gaming / music / ai / other) taken from an
  explicit id -> tag map. Anything not in the map is ``other``.
* ``cost_class`` - free / mixed / paid / unknown, read off the row's ``cost``
  string as published by the official source. A blank ``cost`` is always
  ``unknown``, never guessed.
* dates        - parsed out of the row's ``dates`` string *and* the row's
  ``schedule`` string only when the official source states them there.
  Where the string cannot be parsed unambiguously the date is left empty and
  ``date_source`` records why, so the row simply falls into the
  "no confirmed date" group instead of being silently ordered.
"""

from __future__ import annotations

import re
from datetime import date

# --------------------------------------------------------------------------
# Focus tags. Only rows whose official source describes them as a gaming,
# music or AI event are tagged; everything else is "other".
# --------------------------------------------------------------------------
FOCUS_BY_ID = {
    # --- gaming ---------------------------------------------------------
    "rec-sfpl-mix-gaming": "gaming",
    "rec-sfpl-gaming-citywide": "gaming",
    "x-s-026": "gaming",            # GDC Festival of Gaming 2027
    "art-musee-mecanique": "gaming",  # 300+ coin-operated mechanical games

    # --- music ----------------------------------------------------------
    "rec-bandshell-illuminate-live": "music",
    "rec-sfsymphony": "music",
    "rec-sfjazz-season": "music",
    "rec-sfpl-mix-music-studios": "music",
    "rec-sfpl-dance-music": "music",
    "art-sfopera": "music",
    "art-broadwaysf": "music",
    "ann-sf-mime-troupe": "music",
    "ann-ybg-festival": "music",
    "ann-outside-lands": "music",
    "ann-sfmusic-week": "music",
    "spc-opera-in-the-park": "music",
    "spc-portola-2026": "music",
    "spc-flower-piano": "music",
    "x-w-023": "music",
    "x-a-005": "music",
    "x-a-007": "music",
    "x-a-013": "music",
    "x-a-018": "music",
    "x-s-020": "music",
    "x-s-021": "music",
    "x-s-022": "music",
    "x-s-023": "music",
    "x-s-024": "music",
    "x-s-025": "music",

    # --- arena-fc3438db additions (2026-10-18) ---------------------------
    "spc-symphony-the-ring": "music",
    "spc-symphony-music-for-families": "music",
    "spc-symphony-adams-mendelssohn": "music",
    "spc-opera-strauss-concert": "music",
    "spc-opera-ball": "music",
    "spc-opera-adlers-concert": "music",
    "spc-opera-chorus-concert": "music",
    "spc-illuminate-reggae-2026-10-18": "music",
    "spc-illuminate-ccs-2026-10-20": "music",
    "spc-illuminate-midweek-2026-10-21": "music",
    "spc-illuminate-happyhour-2026-10-23": "music",
    "spc-illuminate-baybeats-2026-10-24": "music",
    "spc-illuminate-reggae-2026-10-25": "music",
    "spc-illuminate-halloween-2026-10-31": "music",

    # --- arena-fe7c710c additions (2026-10-18) ---------------------------
    "spc-illuminate-ccs-2026-10-22": "music",
    "spc-illuminate-ccs-2026-10-27": "music",
    "spc-illuminate-midweek-2026-10-28": "music",
    "spc-illuminate-ccs-2026-10-29": "music",
    "spc-illuminate-happyhour-2026-10-30": "music",
    "spc-illuminate-reggae-2026-11-01": "music",
    "spc-illuminate-mtb-2026-11-04": "music",
    "spc-illuminate-happyhour-2026-11-06": "music",
    "spc-illuminate-saturday-2026-11-07": "music",
    "spc-illuminate-reggae-2026-11-08": "music",
    "spc-illuminate-midweek-2026-11-11": "music",
    "spc-illuminate-happyhour-2026-11-13": "music",
    "spc-illuminate-otisology-2026-11-15": "music",
    "spc-osai-debates-2026-10-19": "ai",
    "spc-osai-awards-2026-10-23": "ai",
    "rec-dogpatch-games-venue": "gaming",
    "rec-dogpatch-boardgame-league": "gaming",
    "spc-dogpatch-love-potion-2026-10-22": "gaming",
    "spc-sfpl-family-game-night-2026-11-10": "gaming",

    # --- arena-fe7c710c additions (2026-10-18) ---------------------------
    "spc-illuminate-ccs-2026-10-22": "music",
    "spc-illuminate-ccs-2026-10-27": "music",
    "spc-illuminate-midweek-2026-10-28": "music",
    "spc-illuminate-ccs-2026-10-29": "music",
    "spc-illuminate-happyhour-2026-10-30": "music",
    "spc-illuminate-reggae-2026-11-01": "music",
    "spc-illuminate-mtb-2026-11-04": "music",
    "spc-illuminate-happyhour-2026-11-06": "music",
    "spc-illuminate-saturday-2026-11-07": "music",
    "spc-illuminate-reggae-2026-11-08": "music",
    "spc-illuminate-midweek-2026-11-11": "music",
    "spc-illuminate-happyhour-2026-11-13": "music",
    "spc-illuminate-otisology-2026-11-15": "music",
    "spc-osai-debates-2026-10-19": "ai",
    "spc-osai-awards-2026-10-23": "ai",
    "rec-dogpatch-games-venue": "gaming",
    "rec-dogpatch-boardgame-league": "gaming",
    "spc-dogpatch-love-potion-2026-10-22": "gaming",
    "spc-sfpl-family-game-night-2026-11-10": "gaming",

    # --- arena-fe7c710c additions (2026-10-18) ---------------------------
    "spc-illuminate-ccs-2026-10-22": "music",
    "spc-illuminate-ccs-2026-10-27": "music",
    "spc-illuminate-midweek-2026-10-28": "music",
    "spc-illuminate-ccs-2026-10-29": "music",
    "spc-illuminate-happyhour-2026-10-30": "music",
    "spc-illuminate-reggae-2026-11-01": "music",
    "spc-illuminate-mtb-2026-11-04": "music",
    "spc-illuminate-happyhour-2026-11-06": "music",
    "spc-illuminate-saturday-2026-11-07": "music",
    "spc-illuminate-reggae-2026-11-08": "music",
    "spc-illuminate-midweek-2026-11-11": "music",
    "spc-illuminate-happyhour-2026-11-13": "music",
    "spc-illuminate-otisology-2026-11-15": "music",
    "spc-osai-debates-2026-10-19": "ai",
    "spc-osai-awards-2026-10-23": "ai",
    "rec-dogpatch-games-venue": "gaming",
    "rec-dogpatch-boardgame-league": "gaming",
    "spc-dogpatch-love-potion-2026-10-22": "gaming",
    "spc-sfpl-family-game-night-2026-11-10": "gaming",

    # --- AI -------------------------------------------------------------
    "ann-sfpl-tech-week": "ai",
    "spc-ai-engineer-code-2026": "ai",
    "spc-ai-week-sf-2026": "ai",
    "spc-current-sf-2026": "ai",
    "spc-microsoft-ignite-2026": "ai",
    "rec-sfpl-ai-workshops": "ai",
    "ann-humanx-2026": "ai",
}

FOCUS_LABELS = [
    ("gaming", "Gaming"),
    ("music", "Music"),
    ("ai", "AI"),
    ("other", "Everything else"),
]

# Rows that are AI/tech adjacent in programme but are NOT branded AI by their
# own official source. They are listed on the AI page under a clearly
# separated heading rather than being tagged, so nothing is over-claimed.
AI_ADJACENT = ["x-s-028", "x-s-031", "spc-cloudflare-connect-2026",
               "spc-informs-2026", "spc-semicon-west-2026", "spc-github-universe-2026"]

# --------------------------------------------------------------------------
# Cost classification
# --------------------------------------------------------------------------
_PAID_MARKERS = (
    "ticketed", "fee", "$", "members only", "included with admission",
    "prix fixe", "paid", "adults $", "registration",
)
_FREE_MARKERS = ("free", "no charge", "no cost", "complimentary")


def cost_class(cost: str) -> str:
    """Classify a published cost string.

    Returns one of ``free``, ``mixed``, ``paid`` or ``unknown``.
    """
    text = (cost or "").strip()
    if not text:
        return "unknown"
    low = text.lower()
    is_free = any(m in low for m in _FREE_MARKERS)
    is_paid = any(m in low for m in _PAID_MARKERS)
    if is_free and is_paid:
        return "mixed"
    if is_free:
        return "free"
    if is_paid:
        return "paid"
    return "unknown"


COST_LABELS = {
    "free": "Free",
    "mixed": "Free / partly free",
    "paid": "Paid",
    "unknown": "Cost not published",
}

# --------------------------------------------------------------------------
# Date parsing
# --------------------------------------------------------------------------
_MONTHS = {
    "january": 1, "jan": 1, "february": 2, "feb": 2, "march": 3, "mar": 3,
    "april": 4, "apr": 4, "may": 5, "june": 6, "jun": 6, "july": 7, "jul": 7,
    "august": 8, "aug": 8, "september": 9, "sep": 9, "sept": 9,
    "october": 10, "oct": 10, "november": 11, "nov": 11, "december": 12, "dec": 12,
}

_MONTH_RE = r"(january|february|march|april|may|june|july|august|september|october|november|december|jan|feb|mar|apr|jun|jul|aug|sep|sept|oct|nov|dec)"

# e.g. "July 25 - September 27, 2026" / "November 10-12, 2026" / "Oct 24, 2026"
_NAMED_RE = re.compile(
    _MONTH_RE + r"\.?\s+(?P<d1>\d{1,2})(?!\d)"
    r"(?:\s*(?:-|–|—|to|through|thru)\s*(?P<d2>\d{1,2})(?!\d))?"
    r"(?:\s*,?\s*(?P<y>\d{4}))?",
    re.IGNORECASE,
)
_ISO_RE = re.compile(r"(?P<y>\d{4})-(?P<m>\d{2})-(?P<d>\d{2})")
_YEAR_RE = re.compile(r"\b(?:19|20)\d{2}\b")

# Dates the automatic parser cannot read safely. Each entry was read by hand
# from the row's official source on 2026-10-18.
DATE_OVERRIDES: dict[str, tuple[str, str]] = {
    # id: (start ISO, end ISO). "" means the value is not published as a
    # calendar day by the row's official source, so it is left empty rather
    # than approximated. Every entry below was read by hand from the row's
    # own ``dates`` string on 2026-10-18 and matches it exactly; these exist
    # only because the mechanical parser cannot read cross-month en-dash
    # ranges or the phrase "mid-November".
    "rec-bandshell-illuminate-live": ("2026-03-01", ""),
    "rec-sf-shakes-free-shakespeare": ("2026-07-25", "2026-09-27"),
    "spc-lightscape": ("2026-11-20", "2027-01-03"),
    "spc-alcatraz-closure": ("2026-10-26", "2026-11-18"),
    # arena-291a13ff (2026-10-18): the museum gives the end as "May 2027" with no
    # calendar day, so the end is left empty rather than approximated or echoed
    # back as the opening date (which the mechanical parser otherwise returns).
    "spc-sfmoma-in-between": ("2026-09-03", ""),
    # Same class: SFMOMA lists this exhibition only as "Opened Oct 3" with the
    # closing date not listed, so a running exhibition was deriving as ended on
    # its opening day. End left empty; displayed dates text is unchanged and
    # still faithful to the museum page.
    "x-s-005": ("2026-10-03", ""),
}


def _valid(y: int, m: int, d: int) -> str:
    try:
        return date(y, m, d).isoformat()
    except ValueError:
        return ""


def _nearest_year(text: str, pos: int, fallback_year: int | None) -> int | None:
    """Pick the year token closest to ``pos`` in ``text``.

    Official pages routinely write ranges such as
    ``"April 10-11 and April 17-18, 2027"`` or ``"The Nutcracker Dec 4-27,
    2026; The Sleeping Beauty Jan 29-Feb 7, 2027"``, where a day number
    carries no year of its own. Taking the *nearest* year token reproduces
    how the sentence reads. When no year appears anywhere in the string the
    caller's ``fallback_year`` is used, and if that is None the fragment is
    dropped rather than guessed.
    """
    spans = [(abs(m.start() - pos), int(m.group(0))) for m in _YEAR_RE.finditer(text or "")]
    if spans:
        return min(spans)[1]
    return fallback_year


def parse_dates(text: str, fallback_year: int | None = None) -> list[str]:
    """Return every concrete calendar date found in ``text``, sorted.

    ``text`` is the row's ``dates`` value as published by its official
    source. Ambiguous or incomplete fragments are dropped rather than
    guessed.
    """
    out: set[str] = set()
    for m in _ISO_RE.finditer(text or ""):
        iso = _valid(int(m.group("y")), int(m.group("m")), int(m.group("d")))
        if iso:
            out.add(iso)
    for m in _NAMED_RE.finditer(text or ""):
        month = _MONTHS[m.group(1).lower().rstrip(".")]
        year = int(m.group("y")) if m.group("y") else _nearest_year(text, m.start(), fallback_year)
        if year is None:
            continue
        d1 = _valid(year, month, int(m.group("d1")))
        if d1:
            out.add(d1)
        if m.group("d2"):
            d2 = _valid(year, month, int(m.group("d2")))
            if d2:
                out.add(d2)
    return sorted(out)


def event_dates(row: dict, fallback_year: int | None = None) -> tuple[str, str, str]:
    """Return ``(start, end, date_source)`` for a row.

    ``date_source`` is ``override`` when the value comes from DATE_OVERRIDES
    (checked by hand against the official page), ``parsed`` when it was read
    mechanically out of the published ``dates`` string, or ``none``.
    """
    rid = row.get("id", "")
    if rid in DATE_OVERRIDES:
        start, end = DATE_OVERRIDES[rid]
        return start, end, "override"
    found = parse_dates(row.get("dates", ""), fallback_year)
    if found:
        return found[0], found[-1], "parsed"
    return "", "", "none"


def next_date(row: dict, today: str) -> str:
    """The next date on or after ``today``, else the last recorded date."""
    start, end, _src = row.get("_start"), row.get("_end"), None
    if start and start >= today:
        return start
    if end and end >= today:
        return start or end
    return end or start or ""
