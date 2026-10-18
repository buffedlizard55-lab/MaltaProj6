#!/usr/bin/env python3
"""Build the static GitHub Pages site for the San Francisco events project.

Reads the canonical dataset from ``data/events.py``, writes a machine-readable
copy to ``data/events.json`` and renders the HTML pages into the repository
root so that GitHub Pages can publish them from the ``main`` branch.

Usage::

    python3 scripts/build_site.py
"""

from __future__ import annotations

import html
import json
import os
import sys
from collections import Counter, defaultdict
from datetime import date, timedelta
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "data"))

from events import (  # noqa: E402
    EVENTS as BASE_EVENTS,
    FLAGGED as BASE_FLAGGED,
    VERIFIED_ON,
    assign_views,
    cost_review_flags,
)
from merge_parallel import parallel_events, parallel_flagged  # noqa: E402

# Union of this session's research and the parallel session's research
# (arena-8fb52462), which is preserved verbatim in data/*.json.
PARALLEL_EVENTS = parallel_events(BASE_EVENTS)
EVENTS = assign_views(list(BASE_EVENTS) + PARALLEL_EVENTS)
FLAGGED = list(BASE_FLAGGED) + parallel_flagged() + cost_review_flags(EVENTS)

from focus import (  # noqa: E402
    FOCUS_BY_ID,
    FOCUS_LABELS,
    AI_ADJACENT,
    COST_LABELS,
    cost_class,
    event_dates,
)


def attach_focus(rows):
    """Derive the focus tag, cost class and published date span for every row.

    Nothing here is inferred: ``focus`` comes from an explicit id -> tag map,
    ``cost_class`` is read off the row's own published ``cost`` wording, and
    ``date_start`` / ``date_end`` are parsed out of the row's own ``dates``
    string (empty when the official source publishes no calendar day).
    """
    for e in rows:
        e["focus"] = FOCUS_BY_ID.get(e["id"], "other")
        e["cost_class"] = cost_class(e.get("cost", ""))
        start, end, source = event_dates(e)
        e["date_start"] = start
        e["date_end"] = end
        e["date_source"] = source
    return rows


attach_focus(EVENTS)

FOCUS_LABEL_BY_KEY = dict(FOCUS_LABELS)

SITE_NAME = "San Francisco Events"
SITE_TAGLINE = "A curated, source-linked snapshot of public events in San Francisco"

# (filename, label, blurb, kind) where kind is "group" (recurrence type),
# "category" (subject area), "static" or "home".
PAGES = [
    ("index.html", "Home", "Dashboard", "home"),
    ("all-events.html", "Full list", "Every entry in one searchable table", "full"),
    ("free-events.html", "Free events", "Entries whose official source explicitly lists free access", "free"),
    ("paid-events.html", "Paid & unconfirmed", "Paid, mixed, and rows whose official page does not state a price", "paid"),
    ("recurring.html", "Regularly recurring", "Events that happen on a fixed weekly or monthly schedule", "group"),
    ("annual.html", "Annual", "Events that repeat year after year", "group"),
    ("special.html", "Special", "Dated events for 2026–2027", "special"),
    ("civic.html", "Civic", "Boards, commissions and public meetings", "category"),
    ("arts.html", "Arts & culture", "Museums, galleries, performance and screen", "category"),
    ("sports.html", "Sports", "Teams, races and active recreation", "category"),
    ("technology.html", "AI & gaming", "Artificial intelligence, gaming and technology events", "focus-tech"),
    ("music.html", "Music", "Concerts, festivals, opera, jazz and free music programmes", "focus-music"),
    ("markets.html", "Markets & food", "Farmers markets, food halls and street markets", "category"),
    ("community.html", "Community & parks", "Neighbourhood programmes, festivals and free recreation", "category"),
    ("analysis.html", "Analysis", "Counts, coverage and findings", "static"),
    ("flagged.html", "Flagged for review", "Discrepancies, gaps and out-of-scope items", "static"),
    ("methodology.html", "Method", "Scope, sourcing rules and verification process", "static"),
]

COLUMNS = [
    ("Event", "title"),
    ("Type", "type"),
    ("Schedule / when", "schedule"),
    ("Confirmed dates", "dates"),
    ("Where", "location"),
    ("Area", "area"),
    ("Cost", "cost"),
    ("Organiser", "organiser"),
]


def esc(value) -> str:
    if value is None:
        return ""
    return html.escape(str(value), quote=True)


def blank(value: str) -> str:
    """Render an unconfirmed value as an explicit blank cell marker."""
    return "" if value else ""


def nav_html(active: str) -> str:
    items = []
    for filename, label, _blurb, _kind in PAGES:
        css = ' class="active"' if filename == active else ""
        items.append(f'<a href="{filename}"{css}>{esc(label)}</a>')
    return "\n      ".join(items)


def page_shell(filename: str, title: str, subtitle: str, body: str) -> str:
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)} &middot; {esc(SITE_NAME)}</title>
<meta name="description" content="{esc(SITE_TAGLINE)}. {esc(subtitle)}">
<link rel="stylesheet" href="assets/site.css">
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<header class="site-header">
  <div class="wrap">
    <a class="brand" href="index.html">
      <span class="brand-mark">SF</span>
      <span class="brand-text">
        <strong>{esc(SITE_NAME)}</strong>
        <small>City-limits only &middot; entries link to official sources</small>
      </span>
    </a>
    <nav class="site-nav" aria-label="Primary">
      {nav_html(filename)}
    </nav>
  </div>
</header>

<main id="main" class="wrap">
{body}
</main>

<footer class="site-footer">
  <div class="wrap">
    <p><strong>{esc(SITE_NAME)}</strong> &mdash; {esc(SITE_TAGLINE)}.</p>
    <p>Each listed entry links to the organiser, city agency or state source recorded as checked on
       <strong>{esc(VERIFIED_ON)}</strong>. Values that could not be confirmed are left blank and marked for
       review. This is a curated snapshot, not an exhaustive or live events calendar; confirm details with the
       official organiser before attending. No values are inferred.</p>
    <p class="muted">Scope is the City and County of San Francisco only. Events physically located in other Bay
       Area cities are excluded and the exclusions are listed on the Flagged for review page.</p>
  </div>
</footer>
</body>
</html>
"""


def cost_cell(ev) -> str:
    """Render the cost exactly as published, with an explicit class label.

    A blank cost stays blank and is labelled "not confirmed" - the site never
    guesses a price.
    """
    value = (ev.get("cost") or "").strip()
    if not value:
        # A cost is only ever blanked when the official source publishes no
        # amount. Where that source did publish generic wording ("Ticketed",
        # "Free; ticketed grand stand") the wording stays visible here, clearly
        # separated from the price, so the information is not lost.
        published = (ev.get("_price_review") or "").strip()
        if published:
            return (
                '<td class="unverified-cell" data-label="Cost">'
                '<span class="na">exact price not published</span>'
                '<span class="cost-wording">as published: &ldquo;' + esc(published) + '&rdquo;</span></td>'
            )
        return '<td class="unverified-cell" data-label="Cost"><span class="na">not confirmed</span></td>'
    cls = ev.get("cost_class", "unknown")
    return (
        '<td data-label="Cost"><span class="cost cost-' + esc(cls) + '">' + esc(value) + '</span></td>'
    )


def _row_data(ev) -> str:
    text = " ".join(
        str(ev.get(k, "")) for k in ("title", "location", "area", "organiser", "source_name", "type", "schedule", "dates", "cost")
    ).lower()
    cost_filter = "free" if _has_free_access(ev) else ("unknown" if not ev.get("cost") else "paid")
    return (
        f' data-group="{esc(ev.get("group", ""))}"'
        f' data-cost="{cost_filter}"'
        f' data-cat="{esc(ev.get("category", ""))}"'
        f' data-focus="{esc(ev.get("focus", "other"))}"'
        f' data-status="{esc(ev.get("status", "verified"))}"'
        f' data-timing="{esc(ev.get("timing", "current"))}"'
        f' data-text="{esc(text)}"'
    )


def event_table(events, table_id: str, show_focus_badges: bool = True) -> str:
    if not events:
        return '<p class="empty">No entries on this page yet.</p>'

    head = "".join(f"<th scope=\"col\">{esc(c[0])}</th>" for c in COLUMNS)
    rows = []
    for ev in events:
        status = ev.get("status", "verified")
        badge = (
            '<span class="badge ok" title="Checked against the official source">verified</span>'
            if status == "verified"
            else '<span class="badge warn" title="Some values could not be confirmed from the official source">unverified</span>'
        )
        if ev.get("timing") == "concluded":
            badge += '<span class="badge past" title="This edition had already finished when the snapshot was built">concluded</span>'
        focus_key = ev.get("focus", "other")
        if focus_key != "other" and show_focus_badges:
            badge += (f'<span class="badge focus-{esc(focus_key)}" title="Focus area: '
                      f'{esc(FOCUS_LABEL_BY_KEY.get(focus_key, focus_key))}">'
                      f'{esc(FOCUS_LABEL_BY_KEY.get(focus_key, focus_key))}</span>')
        title_cell = f'<td data-label="Event"><span class="ev-title">{esc(ev["title"])}</span>'
        if ev.get("_free_access_confirmed"):
            title_cell += '<span class="badge free">some free access listed</span>'
        title_cell += '</td>'
        source_links = [(ev["source_name"], ev["source_url"])]
        source_links.extend((item.get("name", "Official source"), item.get("url", ""))
                            for item in ev.get("additional_sources", []))
        source_html = " · ".join(
            f'<a href="{esc(url)}" target="_blank" rel="noopener">{esc(name)} &nearr;</a>'
            for name, url in source_links if url
        )
        source_cell = f'<td class="source-cell" data-label="Official source"><span class="ev-source">{badge}{source_html}</span></td>'
        cells = [title_cell]
        for key, label in (("type", "Type"), ("schedule", "Schedule / when"),
                           ("dates", "Confirmed dates"), ("location", "Where"),
                           ("area", "Area"), ("organiser", "Organiser")):
            value = ev.get(key, "")
            if not value:
                cells.append(f'<td class="unverified-cell" data-label="{label}"><span class="na">not confirmed</span></td>')
            else:
                cells.append(f'<td data-label="{label}">{esc(value)}</td>')
        # cost sits between area and organiser in COLUMNS order
        cells.insert(6, cost_cell(ev))
        cells.append(source_cell)
        note = ev.get("notes", "")
        note_html = f'<p class="row-note">{esc(note)}</p>' if note else ""
        rows.append(
            f'<tr id="{esc(ev["id"])}"{_row_data(ev)}>'
            + "".join(cells)
            + f"</tr>"
        )
        if note_html:
            rows.append(
                f'<tr class="note-row" data-for="{esc(ev["id"])}">'
                f'<td colspan="{len(COLUMNS) + 1}">{note_html}</td></tr>'
            )
    return f"""
<div class="table-scroll">
<table class="data-table" id="{table_id}">
  <thead>
    <tr>{head}<th scope="col">Source</th></tr>
  </thead>
  <tbody>
    {chr(10).join(rows)}
  </tbody>
</table>
</div>
"""


_MONTH_PATTERN = (
    r"January|Jan|February|Feb|March|Mar|April|Apr|May|June|Jun|July|Jul|"
    r"August|Aug|September|Sept|Sep|October|Oct|November|Nov|December|Dec"
)
_MONTH_NUMBER = {
    "jan": 1, "january": 1, "feb": 2, "february": 2, "mar": 3, "march": 3,
    "apr": 4, "april": 4, "may": 5, "jun": 6, "june": 6, "jul": 7,
    "july": 7, "aug": 8, "august": 8, "sep": 9, "sept": 9, "september": 9,
    "oct": 10, "october": 10, "nov": 11, "november": 11, "dec": 12, "december": 12,
}
_DATE_TOKEN = re.compile(
    rf"\b(?P<month>{_MONTH_PATTERN})\s+(?P<day>\d{{1,2}})(?:st|nd|rd|th)?"
    rf"(?:,?\s+(?P<year>20\d{{2}}))?", re.IGNORECASE,
)
_RANGE_TOKEN = re.compile(
    rf"\b(?P<m1>{_MONTH_PATTERN})\s+(?P<d1>\d{{1,2}})(?:st|nd|rd|th)?"
    rf"(?:,?\s*(?P<y1>20\d{{2}}))?\s*(?:-|–|—|\bto\b)\s*"
    rf"(?:(?P<m2>{_MONTH_PATTERN})\s+)?(?P<d2>\d{{1,2}})(?:st|nd|rd|th)?"
    rf",?\s*(?P<y2>20\d{{2}})", re.IGNORECASE,
)


def _date_parts(month: str, day: str, year: str):
    """Parse a month/day/year explicitly present in a confirmed-date cell."""
    try:
        return date(int(year), _MONTH_NUMBER[month.lower()], int(day))
    except (ValueError, KeyError):
        return None


def _next_confirmed_date(event, today=None):
    """Return the next date explicit in a row, without inventing missing dates.

    Only a year that appears in the official-source-derived date string is used.
    Textual date ranges that include today are ranked as occurring today; otherwise
    the earliest future date explicitly stated is used.
    """
    today = today or date.today()
    text = (event.get("dates") or "").strip()
    if not text:
        return None

    year_matches = [(m.start(), m.group(0)) for m in re.finditer(r"20\d{2}", text)]
    parsed = []
    ranges = []
    for match in _RANGE_TOKEN.finditer(text):
        y1 = match.group("y1") or match.group("y2")
        y2 = match.group("y2") or y1
        m1 = match.group("m1")
        m2 = match.group("m2") or m1
        start = _date_parts(m1, match.group("d1"), y1)
        end = _date_parts(m2, match.group("d2"), y2)
        if start and end:
            parsed.extend((start, end))
            ranges.append((start, end))

    for match in _DATE_TOKEN.finditer(text):
        year = match.group("year")
        if not year and year_matches:
            year = min(year_matches, key=lambda item: abs(item[0] - match.start()))[1]
        if year:
            value = _date_parts(match.group("month"), match.group("day"), year)
            if value:
                parsed.append(value)

    active_ranges = [(start, end) for start, end in ranges if start <= today <= end]
    if active_ranges:
        # An ongoing run has no new start date; use its officially published
        # end date as its position so forthcoming one-day events aren't buried.
        return min(end for _start, end in active_ranges)
    future = [value for value in parsed if value >= today]
    return min(future) if future else None


def _is_free_cost(value):
    """True only when the source's cost wording explicitly includes free access."""
    text = (value or "").strip().lower()
    return text == "free" or text.startswith("free ") or "free entry" in text or "free admission" in text


def _has_free_access(event):
    """Include exact free-cost wording and separately confirmed mixed-access rows."""
    return _is_free_cost(event.get("cost")) or bool(event.get("_free_access_confirmed"))


def _is_explicitly_free(event):
    """True only when the published cost wording is free and not also paid.

    Mixed wording and a blank cost are not treated as free. ``cost_class`` is
    derived from the row's own cost string; it is never guessed.
    """
    return event.get("cost_class") == "free"


def _event_date_sort_key(event, today=None):
    next_date = _next_confirmed_date(event, today=today)
    if next_date:
        return (0, next_date, 0 if _has_free_access(event) else 1, event.get("title", "").casefold())
    if event.get("timing") == "concluded":
        return (2, date.max, 1, event.get("title", "").casefold())
    return (1, date.max, 1, event.get("title", "").casefold())


def by_page(page: str):
    """Rows for a page, filtered by the page's kind."""
    if page == "free-events":
        sel = [e for e in EVENTS if _has_free_access(e)]
    elif page == "paid-events":
        sel = [e for e in EVENTS if not _is_explicitly_free(e)]
    elif page == "technology":
        # AI & gaming: rows the dataset tags AI or gaming, wherever they also
        # sit in the subject categories (a library gaming club is a gaming
        # entry even though its category is "community").
        sel = [e for e in EVENTS if e.get("focus") in ("ai", "gaming")
               or e.get("category") == "technology"]
    elif page == "music":
        sel = [e for e in EVENTS if e.get("focus") == "music"]
    elif page == "recurring":
        sel = [e for e in EVENTS if e.get("group") == "recurring"]
    elif page == "annual":
        sel = [e for e in EVENTS if e.get("group") == "annual"]
    elif page == "special":
        sel = [e for e in EVENTS if e.get("group") == "special"]
    else:
        sel = [e for e in EVENTS if e.get("category") == page]
    if page in ("special", "technology", "music", "free-events", "paid-events"):
        return sorted(sel, key=_event_date_sort_key)
    return sorted(sel, key=lambda e: (e.get("area", ""), e.get("title", "")))


def _summary_row(e, today: date, id_prefix: str = "summary") -> str:
    """One executive-summary row: event, dates, countdown, cost, where, source."""
    when = _next_confirmed_date(e, today=today)
    span_start, span_end = e.get("date_start", ""), e.get("date_end", "")
    running_now = bool(span_start and span_end and span_start <= today.isoformat() <= span_end)
    badges = ""
    if _has_free_access(e):
        badges += '<span class="badge free">free access</span>'
    if e.get("status") != "verified":
        badges += '<span class="badge warn">unverified</span>'
    focus_key = e.get("focus", "other")
    if focus_key != "other":
        badges += (f'<span class="badge focus-{esc(focus_key)}">'
                   f'{esc(FOCUS_LABEL_BY_KEY.get(focus_key, focus_key))}</span>')
    days = (when - today).days if when else None
    if running_now or days == 0:
        when_html = "<span class='when-now'>today / under way</span>"
    elif days == 1:
        when_html = "<span class='when-soon'>tomorrow</span>"
    else:
        css = "when-soon" if days <= 7 else ("when-mid" if days <= 30 else "when-later")
        when_html = f"<span class='{css}'>in {days} days</span>"
    published_cost = (e.get("_price_review") or "").strip()
    if e.get("cost"):
        cost_html = ('<span class="cost cost-' + esc(e.get("cost_class", "unknown")) + '">'
                     + esc(e["cost"]) + '</span>')
    elif published_cost:
        cost_html = ('<span class="na">exact price not published</span>'
                     '<span class="cost-wording">as published: &ldquo;'
                     + esc(published_cost) + '&rdquo;</span>')
    else:
        cost_html = '<span class="na">not confirmed</span>'
    location_html = esc(e["location"]) if e.get("location") else '<span class="na">not confirmed</span>'
    return (
        f"<tr id='{esc(id_prefix)}-{esc(e['id'])}' class='upcoming-row' data-focus='{esc(focus_key)}'>"
        f"<td data-label='Event'><span class='ev-title'>{esc(e['title'])}</span>{badges}</td>"
        f"<td data-label='Confirmed dates'>{esc(e['dates'])}</td>"
        f"<td data-label='Countdown'>{when_html}</td>"
        f"<td data-label='Cost'>{cost_html}</td>"
        f"<td data-label='Where'>{location_html}</td>"
        f"<td data-label='Official source'><a href='{esc(e['source_url'])}' target='_blank' rel='noopener'>"
        f"{esc(e['source_name'])} &nearr;</a></td></tr>"
    )


def executive_summary_rows(events, today: date, horizon_days: int = 21):
    """Free dated rows close to ``today``, grouped into "when it happens" bands.

    Only rows whose published cost wording is free are included. Paid rows and
    rows with no published price are left out; they belong on the paid page.
    A row already under way stays in the today band. Rows whose next confirmed
    date is further than ``horizon_days`` away are omitted.
    """
    horizon_end = today + timedelta(days=horizon_days)
    candidates = []
    for e in events:
        if not _is_explicitly_free(e) or e.get("timing") == "concluded" or not e.get("dates"):
            continue
        when = _next_confirmed_date(e, today=today)
        if not when:
            continue
        span_start, span_end = e.get("date_start", ""), e.get("date_end", "")
        running = bool(span_start and span_end and span_start <= today.isoformat() <= span_end)
        if not running and when > horizon_end:
            continue
        candidates.append(e)
    candidates.sort(key=lambda e: _event_date_sort_key(e, today=today))

    def band(e) -> int:
        span_start, span_end = e.get("date_start", ""), e.get("date_end", "")
        if span_start and span_end and span_start <= today.isoformat() <= span_end:
            return 0
        when = _next_confirmed_date(e, today=today)
        delta = (when - today).days
        if delta <= 0:
            return 0
        if delta <= 7:
            return 1
        if delta <= 30:
            return 2
        return 3

    grouped: dict[int, list] = {}
    for e in candidates:
        grouped.setdefault(band(e), []).append(e)
    ordered = []
    for key in sorted(grouped):
        ordered.extend(grouped[key])
    return ordered


def _running_or_upcoming(event, today: date) -> bool:
    if event.get("timing") == "concluded":
        return False
    span_start, span_end = event.get("date_start", ""), event.get("date_end", "")
    if span_start and span_end and span_start <= today.isoformat() <= span_end:
        return True
    when = _next_confirmed_date(event, today=today)
    return bool(when and when >= today)


def _focus_grouped_rows(events, today: date, id_prefix: str) -> str:
    """Free upcoming rows, gaming then music then AI then everything else."""
    parts = []
    labels = {"gaming": "Gaming", "music": "Music", "ai": "AI", "other": "Everything else"}
    for key, _label in FOCUS_LABELS:
        group = [e for e in events if e.get("focus", "other") == key]
        group.sort(key=lambda e: _event_date_sort_key(e, today=today))
        if not group:
            parts.append(
                f"<tr class='horizon-row'><td colspan='6'><strong>{esc(labels[key])}</strong>"
                f"<span class='horizon-blurb'> &mdash; no dated free upcoming entry in this focus</span></td></tr>"
            )
            continue
        parts.append(
            f"<tr class='horizon-row'><td colspan='6'><strong>{esc(labels[key])}</strong>"
            f"<span class='horizon-blurb'> &mdash; {len(group)} free upcoming</span></td></tr>"
        )
        parts.extend(_summary_row(e, today, id_prefix=id_prefix) for e in group)
    return "".join(parts)


def build_index() -> str:
    today = date.today()
    counts = Counter()
    for e in EVENTS:
        counts[e["group"]] += 1
        counts[e["category"]] += 1
    verified = sum(1 for e in EVENTS if e.get("status") == "verified")
    unverified = len(EVENTS) - verified
    free_count = sum(1 for e in EVENTS if _has_free_access(e))

    tiles = []
    for filename, label, blurb, kind in PAGES[1:]:
        if kind == "static":
            continue
        key = filename.replace(".html", "")
        n = len(EVENTS) if key == "all-events" else len(by_page(key))
        tiles.append(
            f"""<a class="tile" href="{filename}">
  <span class="tile-n">{n}</span>
  <span class="tile-label">{esc(label)}</span>
  <span class="tile-blurb">{esc(blurb)}</span>
</a>"""
        )

    group_labels = {
        "recurring": "Regularly recurring (fixed weekly / monthly schedule)",
        "annual": "Annual (repeats year after year)",
        "special": "Special (a dated, one-off occurrence)",
    }
    group_counts = Counter(e.get("group", "") for e in EVENTS)
    type_rows = "".join(
        f"<tr><td>{esc(group_labels.get(k, k))}</td><td class='num'>{v}</td></tr>"
        for k, v in sorted(group_counts.items(), key=lambda kv: ["recurring", "annual", "special"].index(kv[0]))
    )
    area_counts = Counter(e.get("area", "") for e in EVENTS)
    area_rows = "".join(
        f"<tr><td>{esc(k)}</td><td class='num'>{v}</td></tr>" for k, v in sorted(area_counts.items())
    )

    upcoming = executive_summary_rows(EVENTS, today)

    horizon_labels = {
        0: ("Today and already running", "Happening today or already under way"),
        1: ("Next 7 days", f"{today.isoformat()} to {(today + timedelta(days=7)).isoformat()}"),
        2: ("Next 8-30 days", f"{(today + timedelta(days=8)).isoformat()} to {(today + timedelta(days=30)).isoformat()}"),
        3: ("Later than 30 days out", "Confirmed, but further away"),
    }
    # Group first, then emit, so each horizon heading appears exactly once and
    # rows inside a horizon stay in confirmed-date order.
    def _band(e) -> int:
        span_start, span_end = e.get("date_start", ""), e.get("date_end", "")
        if span_start and span_end and span_start <= today.isoformat() <= span_end:
            return 0
        delta = (_next_confirmed_date(e, today=today) - today).days
        return 0 if delta <= 0 else (1 if delta <= 7 else (2 if delta <= 30 else 3))

    grouped: dict[int, list] = {}
    for e in upcoming:
        grouped.setdefault(_band(e), []).append(e)

    latest_row_parts = []
    free_upcoming = 0
    for bucket in sorted(grouped):
        label, blurb = horizon_labels[bucket]
        latest_row_parts.append(
            f"<tr class='horizon-row'><td colspan='6'><strong>{esc(label)}</strong>"
            f"<span class='horizon-blurb'> &mdash; {esc(blurb)}</span></td></tr>"
        )
        for e in grouped[bucket]:
            latest_row_parts.append(_summary_row(e, today))
        free_upcoming += sum(1 for e in grouped[bucket] if _is_free_cost(e.get("cost")))
    latest_rows = "".join(latest_row_parts)
    free_dated = [e for e in EVENTS if _is_explicitly_free(e) and _running_or_upcoming(e, today)]
    free_main_rows = _focus_grouped_rows(free_dated, today, "free-main")
    not_free_today = [e for e in EVENTS
                      if not _is_explicitly_free(e) and e.get("timing") != "concluded"
                      and _next_confirmed_date(e, today=today) == today]
    not_free_today.sort(key=lambda e: e.get("title", "").casefold())
    not_free_today_rows = "".join(_summary_row(e, today, id_prefix="today-other") for e in not_free_today)
    paid_preview = [e for e in by_page("paid-events") if _running_or_upcoming(e, today)][:8]
    paid_preview_rows = "".join(_summary_row(e, today, id_prefix="paid-preview") for e in paid_preview)

    focus_blurbs = {
        "gaming": "Video and tabletop gaming, from free library clubs to GDC at Moscone",
        "music": "Concerts, festivals, opera, jazz, bandstands and free music programmes",
        "ai": "Artificial-intelligence conferences, weeks and free library workshops",
        "other": "Everything else in the catalogue: civic, arts, sport, markets, parks",
    }
    focus_links = {"gaming": "technology.html", "music": "music.html", "ai": "technology.html",
                   "other": "all-events.html"}
    focus_counts = Counter(e.get("focus", "other") for e in EVENTS)
    focus_free = Counter(e.get("focus", "other") for e in EVENTS if _is_free_cost(e.get("cost")))
    focus_tiles = []
    for key, label in FOCUS_LABELS:
        focus_tiles.append(
            f"""<a class="tile" href="{focus_links[key]}">
  <span class="tile-n">{focus_counts.get(key, 0)}</span>
  <span class="tile-label">{esc(label)}</span>
  <span class="tile-blurb">{esc(focus_blurbs[key])}</span>
  <span class="tile-meta">{focus_free.get(key, 0)} free</span>
</a>"""
        )

    body = f"""
<section class="hero">
  <h1>Free San Francisco events, soonest first</h1>
  <p class="lede">The main list is <strong>free upcoming events inside the City of San Francisco</strong>,
     with <strong>gaming, then music, then AI, then everything else</strong>. Paid events, and events whose
     official page does not state a price, are in a separate section. Weekly and annual programmes stay on
     their own pages. Every row links to an official source; a price that is not on that page is left blank.</p>
  <p class="coverage-note"><strong>Coverage note:</strong> This is not an exhaustive or live events calendar.
     San Francisco has many venue-level, private and short-notice events that are not captured here. Check the
     <a href="https://www.sf.gov/events/upcoming" target="_blank" rel="noopener">City&#x27;s official events calendar</a>
     and each organizer for current listings and details.</p>
  <div class="hero-actions">
    <a class="btn" href="#executive-summary">Free events near today</a>
    <a class="btn ghost" href="#free-upcoming">Free upcoming list</a>
    <a class="btn ghost" href="paid-events.html">Paid and unconfirmed</a>
    <a class="btn ghost" href="all-events.html">Full list ({len(EVENTS)})</a>
    <a class="btn ghost" href="free-events.html">All free wording ({free_count})</a>
    <a class="btn ghost" href="recurring.html">Recurring</a>
    <a class="btn ghost" href="annual.html">Annual</a>
    <a class="btn ghost" href="special.html">Special</a>
    <a class="btn ghost" href="flagged.html">{len(FLAGGED)} items flagged for review</a>
  </div>
</section>

<section class="stat-row">
  <div class="stat"><span class="stat-n">{len(EVENTS)}</span><span class="stat-l">events listed</span></div>
  <div class="stat"><span class="stat-n">{verified}</span><span class="stat-l">rows marked verified</span></div>
  <div class="stat"><span class="stat-n">{unverified}</span><span class="stat-l">rows needing review</span></div>
  <div class="stat"><span class="stat-n">{free_count}</span><span class="stat-l">entries explicitly listing free access</span></div>
  <div class="stat"><span class="stat-n">{sum(1 for e in EVENTS if e.get("timing") == "concluded")}</span><span class="stat-l">concluded editions</span></div>
  <div class="stat"><span class="stat-n">{len(FLAGGED)}</span><span class="stat-l">review items published</span></div>
  <div class="stat"><span class="stat-n">{len({e['source_url'].split('/')[2] for e in EVENTS})}</span><span class="stat-l">distinct official domains</span></div>
</section>

<section>
  <h2 id="executive-summary">Executive summary &mdash; free events near today</h2>
  <p class="count-note">Free events only, earliest first, as of <strong>{today.isoformat()}</strong>.
     A row is here only when its official source states that admission is free and states a date within
     21 days, or the published run already covers today. Cost is copied from that page, not guessed.
     {len(upcoming)} free entries are in this window. Paid events and rows with no published price are
     not in this summary.</p>
  <div class="table-scroll">
  <table class="data-table summary-table">
    <thead><tr><th scope="col">Event</th><th scope="col">Confirmed dates</th><th scope="col">Countdown</th><th scope="col">Cost</th><th scope="col">Where</th><th scope="col">Official source</th></tr></thead>
    <tbody>{latest_rows}</tbody>
  </table>
  </div>
  <p class="note"><a href="#free-upcoming">Full free upcoming list &rarr;</a> &middot;
     <a href="paid-events.html">Paid and unconfirmed &rarr;</a> &middot;
     <a href="music.html">Music &rarr;</a> &middot;
     <a href="technology.html">AI &amp; gaming &rarr;</a></p>
</section>

<section>
  <h2 id="free-upcoming">Free upcoming events</h2>
  <p class="count-note">This is the main section: {len(free_dated)} free events with a confirmed current or future date,
     grouped gaming, music, AI, then everything else. Within each group the soonest date is first.
     Recurring free programmes that have no single published date, including library gaming and AI workshops,
     stay on the <a href="recurring.html">regularly recurring</a>,
     <a href="technology.html">AI and gaming</a> and <a href="music.html">music</a> pages.</p>
  <div class="table-scroll">
  <table class="data-table summary-table">
    <thead><tr><th scope="col">Event</th><th scope="col">Confirmed dates</th><th scope="col">Countdown</th><th scope="col">Cost</th><th scope="col">Where</th><th scope="col">Official source</th></tr></thead>
    <tbody>{free_main_rows}</tbody>
  </table>
  </div>
</section>

<section>
  <h2 id="paid-section">Paid and cost not confirmed</h2>
  <p class="count-note">Separate from the free list. A blank cost means the official page did not state a price;
     it does not mean the event is free. {len(not_free_today)} of these have a confirmed date of today.</p>
  {"<div class='table-scroll'><table class='data-table summary-table'><thead><tr><th scope='col'>Event</th><th scope='col'>Confirmed dates</th><th scope='col'>Countdown</th><th scope='col'>Cost</th><th scope='col'>Where</th><th scope='col'>Official source</th></tr></thead><tbody>" + not_free_today_rows + "</tbody></table></div>" if not_free_today_rows else "<p class='count-note'>No dated non-free event is confirmed for today.</p>"}
  <h3>Next dated rows that are not free</h3>
  <div class="table-scroll">
  <table class="data-table summary-table">
    <thead><tr><th scope="col">Event</th><th scope="col">Confirmed dates</th><th scope="col">Countdown</th><th scope="col">Cost</th><th scope="col">Where</th><th scope="col">Official source</th></tr></thead>
    <tbody>{paid_preview_rows or "<tr><td colspan='6'>No dated non-free rows.</td></tr>"}</tbody>
  </table>
  </div>
  <p class="note"><a href="paid-events.html">Open the full paid and unconfirmed list &rarr;</a></p>
</section>

<section>
  <h2>Browse by category</h2>
  <div class="tiles">
    {chr(10).join(tiles)}
  </div>
</section>

<section class="two-col">
  <div>
    <h2>How the list is organised</h2>
    <table class="data-table compact">
      <thead><tr><th scope="col">Type</th><th scope="col" class="num">Entries</th></tr></thead>
      <tbody>{type_rows}</tbody>
    </table>
  </div>
  <div>
    <h2>By neighbourhood / area</h2>
    <table class="data-table compact">
      <thead><tr><th scope="col">Area</th><th scope="col" class="num">Entries</th></tr></thead>
      <tbody>{area_rows}</tbody>
    </table>
  </div>
</section>

<section>
  <h2>Focus areas &mdash; gaming, music, AI</h2>
  <p class="count-note">The same catalogue cut the way the brief asks for: gaming first, then music, then AI,
     with everything else after. Every entry keeps its own official source link.</p>
  <div class="tiles">
    {chr(10).join(focus_tiles)}
  </div>
</section>

<section>
  <h2>How to read a row</h2>
  <ul class="plain-list">
    <li><strong>Schedule / when</strong> &mdash; the cadence exactly as the official source words it. A blank cell
        marked <span class="na">not confirmed</span> means the source did not state it, so it has been left empty
        rather than guessed.</li>
    <li><strong>Source</strong> &mdash; a direct link to the organiser's, city agency's or state agency's page
        that was opened and checked on {esc(VERIFIED_ON)}.</li>
    <li><strong>verified</strong> / <strong>unverified</strong> &mdash; the badge shows whether every value on the
        row could be confirmed from the official source. A <span class="badge past">concluded</span> badge means the
        listed edition had already finished when the snapshot was built; it stays in the list as a record.</li>
    <li>Rows in italics beneath a table entry are analyst notes recording a discrepancy, a seasonal caveat or a
        scope decision. They are evidence, not filler.</li>
  </ul>
  <p class="note"><a href="methodology.html">Read the method and sourcing rules &rarr;</a></p>
</section>
"""
    return page_shell("index.html", "Dashboard", "Dashboard", body)


def build_flagged() -> str:
    rows = []
    for f in FLAGGED:
        links = [(f.get("source_name", "Official source"), f.get("source_url", ""))]
        links.extend((item.get("name", "Official source"), item.get("url", ""))
                     for item in f.get("additional_sources", []))
        source_html = " · ".join(
            f'<a href="{esc(url)}" target="_blank" rel="noopener">{esc(name)} &nearr;</a>'
            for name, url in links if url
        )
        rows.append(
            f"""<tr id="{esc(f['id'])}">
  <td class="flag-title" data-label="Item">{esc(f['title'])}</td>
  <td data-label="What was found">{esc(f['detail'])}</td>
  <td data-label="Action / next step">{esc(f['action'])}</td>
  <td data-label="Official source">{source_html}</td>
</tr>"""
        )
    body = f"""
<section class="page-head">
  <h1>Flagged for review</h1>
  <p class="lede">Every discrepancy, gap and out-of-scope decision found while checking the list line by line.
     These do not block publication &mdash; they are published here so that nothing is hidden. Each item links to
     the official source involved.</p>
</section>

<p class="count-note">{len(FLAGGED)} items flagged. Checked {esc(VERIFIED_ON)}.</p>

<div class="table-scroll">
<table class="data-table flag-table">
  <thead><tr>
    <th scope="col">Item</th>
    <th scope="col">What was found</th>
    <th scope="col">Action / next step</th>
    <th scope="col">Official source</th>
  </tr></thead>
  <tbody>
    {chr(10).join(rows)}
  </tbody>
</table>
</div>

<section>
  <h2>Rows carrying a blank cell</h2>
  <p class="lede">These rows are in the main list but have at least one value that the official source did not
     state. The blank is deliberate.</p>
</section>
<div class="table-scroll">
<table class="data-table">
  <thead><tr>
    <th scope="col">Event</th><th scope="col">Page</th><th scope="col">Row status</th><th scope="col">Fields left blank</th>
    <th scope="col">Official source</th>
  </tr></thead>
  <tbody>
    {unverified_rows()}
  </tbody>
</table>
</div>
"""
    return page_shell("flagged.html", "Flagged for review", "Discrepancies and unconfirmed values", body)


def unverified_rows() -> str:
    out = []
    for e in EVENTS:
        value_blanks = [
            label
            for label, key in (
                ("Schedule", "schedule"),
                ("Location", "location"),
                ("Cost", "cost"),
            )
            if not e.get(key)
        ]
        is_unverified = e.get("status") == "unverified"
        if not is_unverified and not value_blanks:
            continue
        if is_unverified:
            blanks = [
                label
                for label, key in (
                    ("Schedule", "schedule"),
                    ("Dates", "dates"),
                    ("Location", "location"),
                    ("Cost", "cost"),
                )
                if not e.get(key)
            ]
            status_cell = "unverified"
            blank_cell = ", ".join(blanks) if blanks else "see note"
        else:
            status_cell = "verified (values shown are confirmed)"
            blank_cell = (
                ", ".join(value_blanks)
                + " — not stated on the official source; left blank, nothing inferred"
            )
        out.append(
            f"""<tr id="review-{esc(e['id'])}">
  <td data-label="Event">{esc(e['title'])}</td>
  <td data-label="Page">{esc(e.get('group', ''))} / {esc(e.get('category', ''))}</td>
  <td data-label="Row status">{esc(status_cell)}</td>
  <td data-label="Fields left blank">{esc(blank_cell)}</td>
  <td data-label="Official source"><a href='{esc(e['source_url'])}' target='_blank' rel='noopener'>{esc(e['source_name'])} &nearr;</a></td>
</tr>"""
        )
    return "\n".join(out)



FILTER_JS = """
(function () {
  var q = document.getElementById('q');
  var fType = document.getElementById('f-type');
  var fCat = document.getElementById('f-cat');
  var fStatus = document.getElementById('f-status');
  var fTime = document.getElementById('f-time');
  var fCost = document.getElementById('f-cost');
  var fFocus = document.getElementById('f-focus');
  var count = document.getElementById('visible-count');
  var table = document.getElementById('all-table');
  if (!table) { return; }
  var rows = Array.prototype.slice.call(table.querySelectorAll('tbody tr'));
  var notes = {};
  rows.forEach(function (r) {
    if (r.classList.contains('note-row')) { notes[r.getAttribute('data-for')] = r; }
  });
  function apply() {
    var term = (q.value || '').trim().toLowerCase();
    var t = fType.value, c = fCat.value, st = fStatus.value, ti = fTime.value, co = fCost.value;
    var fo = fFocus ? fFocus.value : '';
    var shown = 0;
    rows.forEach(function (r) {
      if (r.classList.contains('note-row')) { return; }
      var ok = true;
      if (t && r.getAttribute('data-group') !== t) { ok = false; }
      if (c && r.getAttribute('data-cat') !== c) { ok = false; }
      if (st && r.getAttribute('data-status') !== st) { ok = false; }
      if (ti && r.getAttribute('data-timing') !== ti) { ok = false; }
      if (co && r.getAttribute('data-cost') !== co) { ok = false; }
      if (fo && r.getAttribute('data-focus') !== fo) { ok = false; }
      if (ok && term && (r.getAttribute('data-text') || '').indexOf(term) === -1) { ok = false; }
      r.hidden = !ok;
      var n = notes[r.id];
      if (n) { n.hidden = !ok; }
      if (ok) { shown += 1; }
    });
    if (count) { count.textContent = shown; }
  }
  [q, fType, fCat, fStatus, fTime, fCost, fFocus].forEach(function (el) {
    if (el) { el.addEventListener('input', apply); el.addEventListener('change', apply); }
  });
  var reset = document.getElementById('reset');
  if (reset) {
    reset.addEventListener('click', function (ev) {
      ev.preventDefault();
      q.value = ''; fType.value = ''; fCat.value = ''; fStatus.value = ''; fTime.value = '';
      fCost.value = ''; if (fFocus) { fFocus.value = ''; }
      apply();
      q.focus();
    });
  }
  apply();
})();
"""


def build_full_list() -> str:
    groups = [("", "All schedules"), ("recurring", "Regularly recurring"), ("annual", "Annual"), ("special", "Special / dated")]
    cats = [("", "All categories"), ("civic", "Civic"), ("arts", "Arts & culture"), ("sports", "Sports"),
            ("technology", "AI & gaming"), ("markets", "Markets & food"), ("community", "Community & parks")]
    stat = [("", "All rows"), ("verified", "Verified"), ("unverified", "Needs review")]
    tim = [("", "Any timing"), ("current", "Current / upcoming"), ("concluded", "Concluded edition")]
    costs = [("", "Any cost"), ("free", "Free / includes free access"),
             ("paid", "Published paid / mixed price"), ("unknown", "Cost not confirmed")]
    foci = [("", "All focus areas")] + [(key, label) for key, label in FOCUS_LABELS]

    def opts(items):
        return "".join(f'<option value="{esc(v)}">{esc(l)}</option>' for v, l in items)

    body = f"""
<section class="page-head">
  <h1>Full list</h1>
  <p class="lede">Every entry in the catalogue in one table: recurring programmes, annual events and dated
     specials. Filter by schedule, category, verification status or timing, or search by name, venue,
     neighbourhood or organiser. Each row links to its official source.</p>
</section>

<div class="controls" role="search">
  <label class="field grow"><span>Search</span>
    <input id="q" type="search" placeholder="Try &quot;farmers&quot;, &quot;Mission&quot;, &quot;SFMOMA&quot; or &quot;free&quot;" autocomplete="off">
  </label>
  <label class="field"><span>Schedule</span><select id="f-type">{opts(groups)}</select></label>
  <label class="field"><span>Category</span><select id="f-cat">{opts(cats)}</select></label>
  <label class="field"><span>Status</span><select id="f-status">{opts(stat)}</select></label>
  <label class="field"><span>Timing</span><select id="f-time">{opts(tim)}</select></label>
  <label class="field"><span>Focus</span><select id="f-focus">{opts(foci)}</select></label>
  <label class="field"><span>Cost</span><select id="f-cost">{opts(costs)}</select></label>
  <button id="reset" class="btn ghost" type="button">Reset</button>
</div>

<p class="count-note"><strong id="visible-count">{len(EVENTS)}</strong> of {len(EVENTS)} entries shown &middot;
   checked {esc(VERIFIED_ON)} &middot; <a href="data/events.csv">download CSV</a> &middot;
   <a href="data/events.json">machine-readable JSON</a></p>

{event_table(sorted(EVENTS, key=_event_date_sort_key), "all-table")}

<script>{FILTER_JS}</script>
"""
    return page_shell("all-events.html", "Full list", "Every entry in one searchable table", body)


def _bar(n: int, total: int, width: int = 140) -> str:
    pct = 0 if not total else round(100 * n / total)
    return (
        f'<span class="bar"><span class="bar-fill" style="width:{pct}%"></span></span> '
        f'<span class="bar-num">{n} ({pct}%)</span>'
    )


def build_analysis() -> str:
    total = len(EVENTS)
    verified = sum(1 for e in EVENTS if e.get("status") == "verified")
    unverified = total - verified
    concluded = sum(1 for e in EVENTS if e.get("timing") == "concluded")
    domains = Counter(e["source_url"].split("/")[2] for e in EVENTS)
    blank_counts = Counter()
    for e in EVENTS:
        for label, key in (("schedule", "schedule"), ("dates", "dates"), ("location", "location"),
                           ("cost", "cost"), ("organiser", "organiser")):
            if not e.get(key):
                blank_counts[label] += 1
    all_core = sum(1 for e in EVENTS if all(e.get(k) for k in ("schedule", "location", "organiser", "source_url")))
    group_counts = Counter(e.get("group", "") for e in EVENTS)
    cat_counts = Counter(e.get("category", "") for e in EVENTS)
    area_counts = Counter(e.get("area", "") for e in EVENTS)
    type_counts = Counter(e.get("type", "") for e in EVENTS)

    def rows_for(counter, labels=None, limit=None):
        items = counter.most_common(limit)
        out = []
        for key, n in items:
            label = labels.get(key, key) if labels else key
            out.append(f"<tr><td>{esc(label)}</td><td>{_bar(n, total)}</td></tr>")
        return "".join(out)

    group_labels = {"recurring": "Regularly recurring (weekly / monthly)", "annual": "Annual (year after year)", "special": "Special / dated one-off"}
    cat_labels = {"civic": "Civic meetings", "arts": "Arts & culture", "sports": "Sports", "technology": "AI & gaming", "markets": "Markets & food", "community": "Community & parks"}

    domain_rows = "".join(
        f"<tr><td><a href='https://{esc(d)}' target='_blank' rel='noopener'>{esc(d)} &nearr;</a></td><td class='num'>{n}</td></tr>"
        for d, n in domains.most_common()
    )
    blank_rows = "".join(
        f"<tr><td>{esc(k.capitalize())}</td><td class='num'>{v}</td><td class='num'>{round(100 * v / total)}%</td></tr>"
        for k, v in blank_counts.most_common()
    )

    body = f"""
<section class="page-head">
  <h1>Analysis and findings</h1>
  <p class="lede">What the catalogue contains, how complete each field is, and what this pass changed. Every
     figure on this page is computed from <code>data/events.py</code> at build time, so it cannot drift from
     the published tables.</p>
</section>

<section class="stat-row">
  <div class="stat"><span class="stat-n">{total}</span><span class="stat-l">entries</span></div>
  <div class="stat"><span class="stat-n">{verified}</span><span class="stat-l">values verified</span></div>
  <div class="stat"><span class="stat-n">{unverified}</span><span class="stat-l">needing review</span></div>
  <div class="stat"><span class="stat-n">{concluded}</span><span class="stat-l">concluded editions</span></div>
  <div class="stat"><span class="stat-n">{len(FLAGGED)}</span><span class="stat-l">review items</span></div>
  <div class="stat"><span class="stat-n">{len(domains)}</span><span class="stat-l">official domains</span></div>
</section>

<section class="two-col">
  <div>
    <h2>By schedule</h2>
    <table class="data-table compact"><thead><tr><th scope="col">Type</th><th scope="col">Entries</th></tr></thead>
      <tbody>{rows_for(group_counts, group_labels)}</tbody></table>
  </div>
  <div>
    <h2>By category</h2>
    <table class="data-table compact"><thead><tr><th scope="col">Category</th><th scope="col">Entries</th></tr></thead>
      <tbody>{rows_for(cat_counts, cat_labels)}</tbody></table>
  </div>
</section>

<section>
  <h2>Every record type used</h2>
  <table class="data-table compact"><thead><tr><th scope="col">Record type</th><th scope="col">Entries</th></tr></thead>
    <tbody>{rows_for(type_counts)}</tbody></table>
</section>

<section>
  <h2>Value coverage</h2>
  <p class="lede">A blank cell means the official source did not state the value. It is never filled in from
     another source or from inference.</p>
  <table class="data-table compact"><thead><tr><th scope="col">Field</th><th scope="col">Rows left blank</th><th scope="col">Share</th></tr></thead>
    <tbody>{blank_rows}</tbody></table>
  <p class="note">{all_core} of {total} rows have a schedule, a location, an organiser and an official source link.
     All {total} rows carry an https source link.</p>
</section>

<section>
  <h2>Neighbourhood / area</h2>
  <table class="data-table compact"><thead><tr><th scope="col">Area</th><th scope="col">Entries</th></tr></thead>
    <tbody>{rows_for(area_counts, None, 25)}</tbody></table>
</section>

<section>
  <h2>Official domains used as sources ({len(domains)})</h2>
  <p class="lede">Organiser, city, state and federal sites. Aggregators and tourism listings are never used as
     the evidence for a value.</p>
  <div class="table-scroll"><table class="data-table compact"><thead><tr><th scope="col">Domain</th><th scope="col">Rows</th></tr></thead>
    <tbody>{domain_rows}</tbody></table></div>
</section>

<section>
  <h2>What the 2026-10-18 final pass changed</h2>
  <ul class="plain-list">
    <li><strong>Removed an out-of-scope row.</strong> The California Museum was listed as a San Francisco
        attraction at "1045 Moscone Center". The museum's own pages place it at 1020 O Street, Sacramento, with
        $10 adult admission. The row was deleted; the evidence is on the <a href="flagged.html">Flagged for review</a>
        page.</li>
    <li><strong>Corrected the Conservatory of Flowers.</strong> It is closed Wednesdays, opens 10:00 a.m.-4:30 p.m.
        with last entry at 4:00 p.m., and the first Tuesday of the month is free. The row previously said
        "open daily".</li>
    <li><strong>Removed Battery Spencer.</strong> The National Park Service lists it in the Marin Headlands,
        outside the City and County of San Francisco.</li>
    <li><strong>Filled verified gaps.</strong> SF Music Week (Feb 23-Mar 1, 2026), the Parol Lantern Festival
        (Dec 12, 2026, 24th annual), RSAC 2027 (Apr 5-8, 2027) and Noise Pop 2027 (from Feb 18, 2027) now carry
        dates taken from their organisers' pages.</li>
    <li><strong>Reclassified TreasureFest.</strong> The organiser describes a monthly festival and publishes no
        2026 dates, so it is no longer labelled "Annual" and its dates stay blank.</li>
    <li><strong>Closed four long-standing gaps.</strong> FOG Design+Art (gala Jan 20, fair Jan 21-24, 2027, Fort
        Mason, with the advance and at-door prices), Portola Music Festival (Sep 26-27, 2026, Pier 80, Goldenvoice),
        the Juneteenth Fillmore celebration (Jun 13, 2026, 11 a.m.-6 p.m., free) and the Golden State Valkyries
        (2026 home opener May 10; Finals games Oct 17 and 19) are now sourced to the organiser's own page.</li>
    <li><strong>Added three verified rows.</strong> The San Francisco Mime Troupe's free summer season (dated from
        the company's official calendar feed), the Yerba Buena Gardens Festival (2026 season opener May 9, 100+
        free performances May-November) and the Conservatory of Flowers light show (nightly, 30 minutes after
        sunset, Oct 1, 2026-Jan 30, 2027, free).</li>
    <li><strong>Marked concluded editions.</strong> {concluded} rows describe an edition that had already
        finished on 2026-10-18. They stay in the catalogue as records and carry a "concluded" badge, so the
        list is not mistaken for an upcoming-events feed.</li>
    <li><strong>Reduced the review gap.</strong> Re-checking official pages against the published values took
        the unverified count from 40 to {unverified}. The remaining gaps are listed row by row on the review
        page.</li>
  </ul>
</section>

<section>
  <h2>How to read this</h2>
  <ul class="plain-list">
    <li><strong>"Verified"</strong> means every populated cell on the row matches the official page linked in
        its Source column on the date recorded. A blank cell means the source did not state that value.</li>
    <li><strong>"Needing review"</strong> means at least one populated value could not be confirmed, official
        pages conflict, or the event's current status is uncertain.</li>
    <li><strong>Counts are a snapshot.</strong> San Francisco publishes hundreds of events a week; this
        catalogue is a curated, source-linked inventory, not a live calendar. See
        <a href="methodology.html">Method</a>.</li>
  </ul>
</section>
"""
    return page_shell("analysis.html", "Analysis", "Counts, coverage and findings", body)


def build_methodology() -> str:
    domains = sorted({e["source_url"].split("/")[2] for e in EVENTS})
    domain_rows = "".join(f"<li>{esc(d)}</li>" for d in domains)
    body = f"""
<section class="page-head">
  <h1>Method, scope and verification</h1>
  <p class="lede">How this list was built, what counts as an official source, and what was deliberately left out.</p>
</section>

<section>
  <h2>Scope</h2>
  <ul class="plain-list">
    <li><strong>City of San Francisco only.</strong> Listed events are intended to be physically inside the
        San Francisco city limits. Events in other Bay Area cities are excluded, even when they are called
        "San Francisco" events (for example the San Francisco 49ers, who play every home game at Levi's Stadium
        in Santa Clara).</li>
    <li><strong>Not exhaustive.</strong> This is a curated research snapshot, not a complete calendar of every
        concert, gallery opening, private event or short-notice listing. The inventory is limited to public
        programmes and event pages located during the research pass. Use the
        <a href="https://www.sf.gov/events/upcoming" target="_blank" rel="noopener">City&#x27;s official events calendar</a>
        and organiser sites to find additional or newer listings.</li>
    <li><strong>Two organising groups, as requested:</strong> events that occur on a <em>regular schedule</em>
        (every week / every month) are on the <a href="recurring.html">Regularly recurring</a> page; events that
        recur <em>year after year</em> are on the <a href="annual.html">Annual</a> page; genuinely one-off dated
        events are on the <a href="special.html">Special</a> page.</li>
    <li><strong>Category pages</strong> for civic meetings, arts and culture, sports, AI and gaming, markets and
        food, and community programmes are provided for usability; a separate free-access page is based only on
        explicit source wording. Each listed event appears on its category page and on the page matching its type,
        so the same row is never duplicated or contradicted.</li>
  </ul>
</section>

<section>
  <h2>Sourcing rules</h2>
  <ul class="plain-list">
    <li><strong>Official sources only.</strong> Each listed row links to the organiser's own site, a City and
        County of San Francisco agency page, a state agency page, or a federally operated national-park page.
        The research log records these pages as checked on <strong>{esc(VERIFIED_ON)}</strong>; the build-time
        validator checks links and table consistency but does not re-fetch or independently authenticate page
        contents.</li>
    <li><strong>No inference.</strong> If the official page did not state a value, the cell is left blank and marked
        <span class="na">not confirmed</span>. Nothing has been filled in from prior knowledge, from a news
        article, or from an aggregator site.</li>
    <li><strong>No aggregators.</strong> Event-listing and tourism sites were used only to <em>find</em> the
        official page; they are never cited as the source of a value.</li>
    <li><strong>Disagreements are published, not resolved silently.</strong> Where two official pages disagree
        (for example two different meeting times for the same Board committee), the disagreement is recorded on
        the <a href="flagged.html">Flagged for review</a> page and the affected cell is left blank.</li>
    <li><strong>Ended and cancelled events are shown.</strong> Events that have been discontinued by their
        organiser are listed on the Flagged for review page rather than silently omitted, so the gap is visible.</li>
  </ul>
</section>

<section>
  <h2>How the data is stored and built</h2>
  <ul class="plain-list">
    <li><code>data/events.py</code> holds the canonical dataset; <code>data/events.json</code> is the
        machine-readable copy emitted by the build.</li>
    <li><code>scripts/build_site.py</code> renders the static HTML pages, the machine-readable
        <code>data/events.json</code> and the spreadsheet-friendly <code>data/events.csv</code>.</li>
    <li>The <a href="all-events.html">Full list</a> page adds a small amount of vanilla JavaScript so the table can be
        searched and filtered in the browser. With JavaScript disabled, the page still shows every row; only the
        filter controls stop working. No external scripts, fonts or trackers are loaded.</li>
    <li>Re-running <code>python3 scripts/build_site.py</code> regenerates the site deterministically from the
        dataset, so the tables and the counts can never drift apart.</li>
  </ul>
</section>

<section>
  <h2>Official domains used as sources ({len(domains)})</h2>
  <ul class="domain-list">{domain_rows}</ul>
</section>

<section>
  <h2>Supplementary views (from the parallel session)</h2>
  <p class="lede">A second agent session worked on this repository in parallel and its research was merged into
     <code>main</code> while this pass was still running. Its raw data files are preserved verbatim in
     <code>data/weekly.json</code>, <code>data/annual.json</code>, <code>data/special.json</code>,
     <code>data/flagged.json</code> and <code>data/sources.json</code>, and its own views of the same events are
     still published. The published tables above are the <em>union</em> of both research passes.</p>
  <ul class="plain-list">
    <li><a href="weekly.html">Weekly &amp; monthly view</a> &mdash; the parallel session's recurring-event table, with
        its own source registry.</li>
    <li><a href="analysis.html">Analysis</a> &mdash; counts, field coverage and the findings of the latest pass.</li>
    <li><a href="sources.html">Source registry</a> &mdash; the parallel session's list of the 58 official sources it checked.</li>
    <li><a href="data/review.csv">Review sheet</a> &mdash; the parallel session's line-by-line review CSV.</li>
    <li><a href="data/schema.md">Data schema</a> &mdash; the parallel session's documented JSON schema.</li>
  </ul>
</section>

<section>
  <h2>Known limitations</h2>
  <ul class="plain-list">
    <li><strong>Coverage is not exhaustive.</strong> The site is a snapshot of the public programmes found in
        this research pass. Small venue shows, private events, new listings and short-notice changes may be
        absent; use the linked official City calendar and organiser pages to search beyond this inventory.</li>
    <li>Source pages can change after the recorded verification date. Re-check the linked official page before
        relying on a schedule, date, venue or admission detail.</li>
    <li>Individual performance dates for large seasons (opera, ballet, theatre) change and are sometimes
        revised late; the rows record the date ranges published on the official site at the time of checking.</li>
    <li>Neighbourhood street fairs publish their next edition a few months ahead; the dates shown are the most
        recent confirmed editions, and later editions were not assumed.</li>
    <li>Pool and court schedules change with the season; each row points at the department's own schedule page
        rather than restating a fixed timetable.</li>
    <li>Where a commission does not publish a regular cadence, the frequency is blank rather than guessed from a
        handful of observed dates.</li>
  </ul>
</section>
"""
    return page_shell("methodology.html", "Method", "Method", body)


def build_page(filename: str, label: str, subtitle: str) -> str:
    page = filename.replace(".html", "")
    events = by_page(page)
    verified = sum(1 for e in events if e.get("status") == "verified")
    # The focus pages already state their focus area in the heading, so the
    # badge is suppressed there rather than repeated on every row.
    show_focus = page not in ("technology", "music")
    body = f"""
<section class="page-head">
  <h1>{esc(label)}</h1>
  <p class="lede">{esc(subtitle)}</p>
</section>

<p class="count-note">{len(events)} entries &middot; {verified} fully verified &middot;
  {len(events) - verified} with a flagged gap &middot; checked {esc(VERIFIED_ON)}</p>

{event_table(events, page + "-table", show_focus_badges=show_focus)}
"""
    return page_shell(filename, label, subtitle, body)


CSS = """/* San Francisco Events - static site styles */
:root {
  --bg: #f6f7f9;
  --panel: #ffffff;
  --ink: #16202c;
  --ink-soft: #4a5766;
  --line: #dfe4ea;
  --brand: #0b5f7a;
  --brand-dark: #084254;
  --accent: #b8442b;
  --ok-bg: #e3f3e8;
  --ok-ink: #1d6b34;
  --warn-bg: #fdf0d5;
  --warn-ink: #8a5a05;
  --radius: 10px;
}
* { box-sizing: border-box; }
html { scroll-behavior: smooth; }
body {
  margin: 0;
  background: var(--bg);
  color: var(--ink);
  font: 16px/1.55 -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
}
a { color: var(--brand); }
a:hover { color: var(--brand-dark); }
.wrap { max-width: 1180px; margin: 0 auto; padding: 0 20px; }
.skip { position: absolute; left: -9999px; }
.skip:focus { left: 12px; top: 12px; background: #fff; padding: 8px 12px; z-index: 99; }

/* Header */
.site-header { background: var(--brand); color: #fff; box-shadow: 0 1px 0 rgba(0,0,0,.12); }
.site-header .wrap { display: flex; flex-wrap: wrap; align-items: center; gap: 10px 24px; padding-top: 14px; padding-bottom: 12px; }
.brand { display: flex; align-items: center; gap: 12px; color: #fff; text-decoration: none; }
.brand:hover { color: #fff; }
.brand-mark { display: grid; place-items: center; width: 40px; height: 40px; border-radius: 9px; background: #fff; color: var(--brand); font-weight: 800; letter-spacing: .5px; }
.brand-text { display: flex; flex-direction: column; line-height: 1.2; }
.brand-text strong { font-size: 1.06rem; }
.brand-text small { opacity: .82; font-size: .76rem; }
.site-nav { display: flex; flex-wrap: wrap; gap: 4px 6px; margin-left: auto; }
.site-nav a { color: #e8f3f7; text-decoration: none; padding: 6px 11px; border-radius: 999px; font-size: .86rem; white-space: nowrap; }
.site-nav a:hover { background: rgba(255,255,255,.14); color: #fff; }
.site-nav a.active { background: #fff; color: var(--brand); font-weight: 600; }

/* Main */
main { padding: 28px 20px 56px; }
h1 { font-size: 1.9rem; line-height: 1.2; margin: 0 0 10px; letter-spacing: -.015em; }
h2 { font-size: 1.22rem; margin: 34px 0 12px; letter-spacing: -.01em; }
p { margin: 0 0 12px; }
.lede { font-size: 1.03rem; color: var(--ink-soft); max-width: 78ch; }
.muted { color: var(--ink-soft); }
.page-head { margin-bottom: 18px; }
.count-note { color: var(--ink-soft); font-size: .9rem; margin: 0 0 14px; }
.note { margin-top: 12px; font-size: .92rem; }

/* Hero */
.hero { background: var(--panel); border: 1px solid var(--line); border-left: 5px solid var(--brand); border-radius: var(--radius); padding: 26px 28px; }
.hero h1 { max-width: 22ch; }
.coverage-note { margin: 16px 0 0; padding: 12px 14px; border: 1px solid #ead9a5; border-radius: 8px; background: #fff9e8; color: #53420f; font-size: .92rem; }
.coverage-note a { font-weight: 650; }
.hero-actions { display: flex; flex-wrap: wrap; gap: 10px; margin-top: 18px; }
.btn { display: inline-block; background: var(--brand); color: #fff; text-decoration: none; padding: 9px 16px; border-radius: 8px; font-weight: 600; font-size: .93rem; }
.btn:hover { background: var(--brand-dark); color: #fff; }
.btn.ghost { background: transparent; color: var(--brand); border: 1px solid var(--brand); }
.btn.ghost:hover { background: #e8f3f7; color: var(--brand-dark); }

/* Stats */
.stat-row { display: flex; flex-wrap: wrap; gap: 12px; margin: 20px 0 6px; }
.stat { flex: 1 1 160px; background: var(--panel); border: 1px solid var(--line); border-radius: var(--radius); padding: 14px 16px; }
.stat-n { display: block; font-size: 1.7rem; font-weight: 700; color: var(--brand); line-height: 1.1; }
.stat-l { display: block; font-size: .82rem; color: var(--ink-soft); }

/* Tiles */
.tiles { display: grid; grid-template-columns: repeat(auto-fill, minmax(215px, 1fr)); gap: 12px; }
.tile { display: flex; flex-direction: column; gap: 2px; background: var(--panel); border: 1px solid var(--line); border-radius: var(--radius); padding: 16px 18px; text-decoration: none; color: var(--ink); }
.tile:hover { border-color: var(--brand); box-shadow: 0 2px 10px rgba(11,95,122,.10); color: var(--ink); }
.tile-n { font-size: 1.6rem; font-weight: 700; color: var(--brand); }
.tile-label { font-weight: 650; }
.tile-blurb { font-size: .85rem; color: var(--ink-soft); }

/* Tables */
.two-col { display: grid; grid-template-columns: repeat(auto-fit, minmax(320px, 1fr)); gap: 26px; }
.table-scroll { overflow-x: auto; background: var(--panel); border: 1px solid var(--line); border-radius: var(--radius); }
.data-table { width: 100%; border-collapse: collapse; font-size: .9rem; min-width: 980px; }
.data-table th { text-align: left; background: #eef2f5; color: var(--ink); font-size: .78rem; text-transform: uppercase; letter-spacing: .04em; padding: 10px 12px; border-bottom: 1px solid var(--line); white-space: nowrap; }
.data-table td { padding: 11px 12px; border-bottom: 1px solid var(--line); vertical-align: top; }
.data-table tbody tr:hover td { background: #f7fafb; }
.data-table.compact { min-width: 0; }
.data-table.compact th, .data-table.compact td { padding: 7px 12px; }
.data-table .num { text-align: right; }
.ev-title { display: block; font-weight: 620; }
.ev-source { display: block; margin-top: 3px; font-size: .78rem; }
.badge { display: inline-block; padding: 1px 7px; border-radius: 999px; font-size: .68rem; font-weight: 700; text-transform: uppercase; letter-spacing: .03em; vertical-align: 1px; }
.badge.ok { background: var(--ok-bg); color: var(--ok-ink); }
.badge.free { background: #dff3ed; color: #145c46; margin: 4px 4px 0 0; }
.badge.warn { background: var(--warn-bg); color: var(--warn-ink); }
.upcoming-row td:first-child { border-left: 3px solid #14765a; }
.upcoming-row td:nth-child(2) { font-weight: 650; color: var(--brand-dark); }
.na { color: #8b95a1; font-style: italic; font-size: .84rem; }
.unverified-cell { background: #fffdf5; }
.note-row td { background: #fbfcfd; padding-top: 0; border-bottom: 1px solid var(--line); }
.row-note { font-size: .82rem; color: var(--ink-soft); margin: 0 0 10px; }
.flag-table td { font-size: .88rem; }
/* Controls */
.controls { display: flex; flex-wrap: wrap; gap: 10px 12px; align-items: end; background: var(--panel); border: 1px solid var(--line); border-radius: var(--radius); padding: 14px 16px; margin: 0 0 12px; }
.field { display: flex; flex-direction: column; gap: 4px; font-size: .78rem; color: var(--ink-soft); }
.field.grow { flex: 1 1 260px; }
.field span { font-weight: 650; text-transform: uppercase; letter-spacing: .03em; }
.field input, .field select { font: inherit; font-size: .92rem; color: var(--ink); background: #fff; border: 1px solid var(--line); border-radius: 8px; padding: 8px 10px; min-width: 150px; }
.field input:focus, .field select:focus { outline: 2px solid #9fd3e4; outline-offset: 1px; border-color: var(--brand); }
.field.grow input { min-width: 100%; }
.controls .btn { padding: 9px 14px; }
.badge.past { background: #eceff3; color: #4d5866; }
tr[hidden] { display: none; }
/* Bars */
.bar { display: inline-block; width: 140px; height: 9px; background: #eef2f5; border-radius: 999px; overflow: hidden; vertical-align: middle; margin-right: 8px; }
.bar-fill { display: block; height: 100%; background: var(--brand); }
.bar-num { font-size: .82rem; color: var(--ink-soft); }
@media (max-width: 640px) {
  .controls { padding: 12px; }
  .field, .field input, .field select { width: 100%; min-width: 0; }
}
.flag-title { font-weight: 620; }

/* Lists */
.plain-list { margin: 0; padding-left: 20px; }
.plain-list li { margin-bottom: 8px; }
.domain-list { columns: 3 200px; list-style: none; padding: 0; font-size: .9rem; }
.domain-list li { padding: 3px 0; border-bottom: 1px dotted var(--line); }
code { background: #eef2f5; padding: 1px 5px; border-radius: 4px; font-size: .88em; }

/* Footer */
.site-footer { background: #10222e; color: #c9d6de; font-size: .88rem; padding: 26px 0 34px; }
.site-footer a { color: #8fd0e6; }
.site-footer p { max-width: 90ch; }
.empty { padding: 20px; background: var(--panel); border: 1px solid var(--line); border-radius: var(--radius); }

@media (max-width: 820px) {
  .site-nav { margin-left: 0; width: 100%; }
  h1 { font-size: 1.55rem; }
  .hero { padding: 20px; }
}
/* Cost labelling - the price is quoted exactly as the official source words it */
.cost-wording { display: block; margin-top: 3px; font-size: .78rem; color: var(--ink-soft); font-style: italic; }
.cost { display: inline-block; padding: 2px 8px; border-radius: 999px; font-size: .84rem; font-weight: 650; }
.cost-free { background: var(--ok-bg); color: var(--ok-ink); }
.cost-mixed { background: #eaf2fb; color: #205c8a; }
.cost-paid { background: #f4eef7; color: #5b3b78; }
.cost-unknown { background: #eceff3; color: #4d5866; font-style: italic; font-weight: 500; }

/* Focus badges (gaming / music / AI) */
.badge.focus-gaming { background: #ede7fb; color: #4a2f86; }
.badge.focus-music { background: #fdeaf2; color: #8b2a5c; }
.badge.focus-ai { background: #e2f0f8; color: #14506e; }
.badge + .badge { margin-left: 4px; }

/* Executive summary horizons and countdowns */
.horizon-row td { background: #eef2f5; font-size: .82rem; letter-spacing: .02em; padding: 8px 12px; }
.horizon-blurb { color: var(--ink-soft); font-weight: 400; }
.when-now { font-weight: 700; color: #145c46; }
.when-soon { font-weight: 700; color: var(--accent); }
.when-mid { color: var(--ink-soft); }
.when-later { color: var(--ink-soft); }
.summary-table tbody td { vertical-align: top; }
.tile-meta { margin-top: 4px; font-size: .78rem; font-weight: 700; color: var(--ok-ink); }

/* Mobile: every table becomes a stack of readable cards. The columns are
   still there - each cell repeats its column name - so nothing is hidden
   and no horizontal scrolling is needed on a phone. */
@media (max-width: 760px) {
  .wrap { padding: 0 14px; }
  main { padding: 20px 14px 44px; }
  h1 { font-size: 1.45rem; }
  .table-scroll { overflow: visible; background: transparent; border: 0; border-radius: 0; }
  .data-table:not(.compact) { min-width: 0; display: block; }
  .data-table:not(.compact) thead { position: absolute; left: -9999px; top: auto; }
  .data-table:not(.compact) tbody { display: block; }
  .data-table:not(.compact) tr {
    display: block; background: var(--panel); border: 1px solid var(--line);
    border-radius: var(--radius); padding: 12px 14px; margin: 0 0 12px;
  }
  .data-table:not(.compact) tbody tr:hover td { background: transparent; }
  .data-table:not(.compact) td { display: block; border: 0; padding: 5px 0; }
  .data-table:not(.compact) td[data-label]::before {
    content: attr(data-label); display: block; margin-bottom: 1px;
    font-size: .67rem; font-weight: 700; letter-spacing: .05em;
    text-transform: uppercase; color: var(--ink-soft);
  }
  .data-table:not(.compact) td:first-child::before { display: none; }
  .data-table:not(.compact) .ev-title { font-size: 1.02rem; }
  .data-table:not(.compact) .note-row { padding-top: 0; }
  .data-table:not(.compact) .note-row td { padding-top: 0; }
  .horizon-row td { border-radius: 8px; }
  .stat { flex: 1 1 128px; padding: 12px 14px; }
  .stat-n { font-size: 1.45rem; }
  .tiles { grid-template-columns: 1fr; }
  .domain-list { columns: 1; }
}
@media print {
  .site-nav, .hero-actions, .btn { display: none; }
  .table-scroll { overflow: visible; }
  .data-table { min-width: 0; font-size: 8pt; }
}
"""


def main() -> int:
    os.makedirs(os.path.join(ROOT, "assets"), exist_ok=True)

    # machine-readable copy
    payload = {
        "project": SITE_NAME,
        "tagline": SITE_TAGLINE,
        "generated": str(date.today()),
        "verified_on": VERIFIED_ON,
        "scope": "City and County of San Francisco only",
        "event_count": len(EVENTS),
        "flagged_count": len(FLAGGED),
        "events": EVENTS,
        "flagged": FLAGGED,
    }
    with open(os.path.join(ROOT, "data", "events.json"), "w", encoding="utf-8") as fh:
        json.dump(payload, fh, indent=2, ensure_ascii=False)
        fh.write("\n")

    with open(os.path.join(ROOT, "assets", "site.css"), "w", encoding="utf-8") as fh:
        fh.write(CSS)

    # CSV mirror for spreadsheet users
    import csv
    csv_fields = ["id", "title", "group", "category", "focus", "type", "schedule", "dates",
                  "date_start", "date_end", "location", "area", "cost", "cost_class", "organiser",
                  "status", "timing", "source_name", "source_url", "additional_sources", "notes"]
    with open(os.path.join(ROOT, "data", "events.csv"), "w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=csv_fields, extrasaction="ignore", lineterminator="\n")
        writer.writeheader()
        for ev in sorted(EVENTS, key=_event_date_sort_key):
            row = {k: ev.get(k, "") for k in csv_fields}
            row["additional_sources"] = " | ".join(
                f"{item.get('name', 'Official source')}: {item.get('url', '')}"
                for item in ev.get("additional_sources", []) if item.get("url")
            )
            writer.writerow(row)

    written = ["index.html", "flagged.html", "methodology.html", "analysis.html", "all-events.html"]
    for filename, label, subtitle, _kind in PAGES:
        if filename in written:
            continue
        page = filename.replace(".html", "")
        with open(os.path.join(ROOT, filename), "w", encoding="utf-8") as fh:
            fh.write(build_page(filename, label, subtitle))
        written.append(filename)

    with open(os.path.join(ROOT, "index.html"), "w", encoding="utf-8") as fh:
        fh.write(build_index())
    with open(os.path.join(ROOT, "flagged.html"), "w", encoding="utf-8") as fh:
        fh.write(build_flagged())
    with open(os.path.join(ROOT, "methodology.html"), "w", encoding="utf-8") as fh:
        fh.write(build_methodology())
    with open(os.path.join(ROOT, "analysis.html"), "w", encoding="utf-8") as fh:
        fh.write(build_analysis())
    with open(os.path.join(ROOT, "all-events.html"), "w", encoding="utf-8") as fh:
        fh.write(build_full_list())

    print(f"Wrote {len(written)} pages, {len(EVENTS)} events, {len(FLAGGED)} flagged items.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
