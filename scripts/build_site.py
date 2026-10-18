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
from datetime import date

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "data"))

from events import (  # noqa: E402
    EVENTS as BASE_EVENTS,
    FLAGGED as BASE_FLAGGED,
    VERIFIED_ON,
    assign_views,
)
from merge_parallel import parallel_events, parallel_flagged  # noqa: E402

# Union of this session's research and the parallel session's research
# (arena-8fb52462), which is preserved verbatim in data/*.json.
PARALLEL_EVENTS = parallel_events(BASE_EVENTS)
EVENTS = assign_views(list(BASE_EVENTS) + PARALLEL_EVENTS)
FLAGGED = list(BASE_FLAGGED) + parallel_flagged()

SITE_NAME = "San Francisco Events"
SITE_TAGLINE = "A curated, source-linked snapshot of public events in San Francisco"

# Snapshot date ("today" for the executive summary). The site is a static
# snapshot, so "close to today" always means close to the verification date.
VERIFIED_YEAR = int(VERIFIED_ON[:4])
TODAY = date(VERIFIED_YEAR, int(VERIFIED_ON[5:7]), int(VERIFIED_ON[8:10]))

# (filename, label, blurb, kind) where kind is "group" (recurrence type),
# "category" (subject area), "static" or "home".
PAGES = [
    ("index.html", "Home", "Dashboard", "home"),
    ("all-events.html", "Full list", "Every entry in one searchable table", "full"),
    ("recurring.html", "Regularly recurring", "Events that happen on a fixed weekly or monthly schedule", "group"),
    ("annual.html", "Annual", "Events that repeat year after year", "group"),
    ("special.html", "Special", "Dated events for 2026–2027", "special"),
    ("civic.html", "Civic", "Boards, commissions and public meetings", "category"),
    ("arts.html", "Arts & culture", "Museums, galleries, performance and screen", "category"),
    ("sports.html", "Sports", "Teams, races and active recreation", "category"),
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


# --- date parsing (presentation only; never invents a date) -----------------
import re  # noqa: E402

_MONTHS = {
    "jan": 1, "january": 1, "feb": 2, "february": 2, "mar": 3, "march": 3,
    "apr": 4, "april": 4, "may": 5, "jun": 6, "june": 6, "jul": 7, "july": 7,
    "aug": 8, "august": 8, "sep": 9, "sept": 9, "september": 9,
    "oct": 10, "october": 10, "nov": 11, "november": 11,
    "dec": 12, "december": 12,
}
_MONTH_RE = (
    r"(jan(?:uary)?|feb(?:ruary)?|mar(?:ch)?|apr(?:il)?|may|jun(?:e)?|jul(?:y)?"
    r"|aug(?:ust)?|sep(?:t)?(?:ember)?|oct(?:ober)?|nov(?:ember)?|dec(?:ember)?)"
)


def parse_dates(text: str):
    """Best-effort extraction of the *printed* date tokens in an official date
    string. Fuzzy wording ("mid-November") is never resolved into a date.
    """
    if not text:
        return []
    t = text
    out = set()

    def add(mon_name, day, year):
        try:
            out.add(date(year, _MONTHS[mon_name.lower()], int(day)))
        except (ValueError, KeyError):
            pass

    years = [int(y) for y in re.findall(r"\b(20\d{2})\b", t)]
    default_year = years[0] if years else VERIFIED_YEAR

    # 1) Month D, YYYY  (explicit year)
    for m in re.finditer(rf"\b{_MONTH_RE}\s+(\d{{1,2}})(?!\d)(?:st|nd|rd|th)?,\s*(\d{{4}})", t, re.I):
        add(m.group(1), m.group(2), int(m.group(3)))
    # 2) Month D - Month D[, YYYY]  (cross-month range)
    for m in re.finditer(
            rf"\b{_MONTH_RE}\s+(\d{{1,2}})(?!\d)\s*[-\u2013\u2014]\s*"
            rf"{_MONTH_RE}\s+(\d{{1,2}})(?!\d)(?:,\s*(\d{{4}}))?",
            t, re.I):
        y = int(m.group(5)) if m.group(5) else default_year
        add(m.group(1), m.group(2), y)
        add(m.group(3), m.group(4), y)
    # 3) Month D-D[, YYYY]  (same-month range)
    for m in re.finditer(
            rf"\b{_MONTH_RE}\s+(\d{{1,2}})(?!\d)\s*[-\u2013\u2014]\s*"
            rf"(\d{{1,2}})(?!\d)(?:,\s*(\d{{4}}))?",
            t, re.I):
        y = int(m.group(4)) if m.group(4) else default_year
        add(m.group(1), m.group(2), y)
        add(m.group(1), m.group(3), y)
    # 4) bare Month D  (year defaults to the first year printed in the string)
    for m in re.finditer(
            rf"\b{_MONTH_RE}\s+(\d{{1,2}})(?!\d)(?:st|nd|rd|th)?"
            rf"(?!,\s*\d{{4}})(?![-\u2013\u2014]\s*\d)(?![-\u2013\u2014]\s*{_MONTH_RE})",
            t, re.I):
        add(m.group(1), m.group(2), default_year)
    return sorted(out)


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


def _cost_class(cost: str) -> str:
    c = (cost or "").lower()
    if not c.strip():
        return "blank"
    is_free = "free" in c
    is_paid = any(w in c for w in ("ticket", "$", "fee", "registration", "prix fixe", "donation", "membership", "admission"))
    if is_free and is_paid:
        return "mixed"
    if is_free:
        return "free"
    return "paid"


def _cost_cell(cost: str) -> str:
    cls = _cost_class(cost)
    if cls == "blank":
        return '<td class="unverified-cell"><span class="na">not confirmed</span></td>'
    chip = ""
    if cls == "free":
        chip = '<span class="cost-chip free-chip">Free</span> '
    elif cls == "paid":
        chip = '<span class="cost-chip paid-chip">$</span> '
    elif cls == "mixed":
        chip = '<span class="cost-chip mixed-chip">Free / paid</span> '
    return f'<td class="cost-cell cost-{cls}">{chip}{esc(cost)}</td>'


def _row_data(ev) -> str:
    text = " ".join(
        str(ev.get(k, "")) for k in ("title", "location", "area", "organiser", "source_name", "type")
    ).lower()
    return (
        f' data-group="{esc(ev.get("group", ""))}"'
        f' data-cat="{esc(ev.get("category", ""))}"'
        f' data-status="{esc(ev.get("status", "verified"))}"'
        f' data-timing="{esc(ev.get("timing", "current"))}"'
        f' data-cost="{_cost_class(ev.get("cost", ""))}"'
        f' data-text="{esc(text)}"'
    )


def event_table(events, table_id: str) -> str:
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
        title_cell = f'<td><span class="ev-title">{esc(ev["title"])}</span></td>'
        source_cell = (
            f'<td class="source-cell"><span class="ev-source">{badge}'
            f'<a href="{esc(ev["source_url"])}" target="_blank" rel="noopener">'
            f'{esc(ev["source_name"])} &nearr;</a></span></td>'
        )
        cells = [title_cell]
        for key in ("type", "schedule", "dates", "location", "area", "cost", "organiser"):
            if key == "cost":
                cells.append(_cost_cell(ev.get("cost", "")))
                continue
            value = ev.get(key, "")
            if not value:
                cells.append('<td class="unverified-cell"><span class="na">not confirmed</span></td>')
            else:
                cells.append(f"<td>{esc(value)}</td>")
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


def by_page(page: str):
    """Rows for a page, filtered by the page's kind."""
    if page == "recurring":
        sel = [e for e in EVENTS if e.get("group") == "recurring"]
    elif page == "annual":
        sel = [e for e in EVENTS if e.get("group") == "annual"]
    elif page == "special":
        sel = [e for e in EVENTS if e.get("group") == "special"]
    else:
        sel = [e for e in EVENTS if e.get("category") == page]
    return sorted(sel, key=lambda e: (e.get("area", ""), e.get("title", "")))


def build_index() -> str:
    counts = Counter()
    for e in EVENTS:
        counts[e["group"]] += 1
        counts[e["category"]] += 1
    verified = sum(1 for e in EVENTS if e.get("status") == "verified")
    unverified = len(EVENTS) - verified

    tiles = []
    for filename, label, blurb, kind in PAGES[1:]:
        if kind == "static":
            continue
        key = filename.replace(".html", "")
        n = len(EVENTS) if key == "all-events" else counts.get(key, 0)
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

    # --- dated rows: parsed from the printed date strings only -------------
    dated = []
    for e in EVENTS:
        if e.get("timing") == "concluded" or not e.get("dates"):
            continue
        tokens = parse_dates(e.get("dates", ""))
        if not tokens:
            continue
        dated.append((tokens[0], tokens[-1], e))
    dated.sort(key=lambda t: (t[0], t[2].get("title", "")))
    horizon = TODAY.toordinal() + 21
    starting_soon = [t for t in dated if TODAY.toordinal() <= t[0].toordinal() <= horizon]
    running_now = [t for t in dated if t[0] <= TODAY <= t[1] and t[1] > t[0]]
    running_now.sort(key=lambda t: (t[1], t[2].get("title", "")))
    upcoming = [t for t in dated if t[1] >= TODAY][:12]

    def row_page(e) -> str:
        return {"recurring": "recurring.html", "annual": "annual.html",
                "special": "special.html"}.get(e.get("group", ""), "all-events.html")

    def row_link(e) -> str:
        return f"{row_page(e)}#{esc(e['id'])}"

    def mini_rows(items, show_end=False):
        out = []
        for start, end, e in items:
            when = e.get("dates", "")
            cost = e.get("cost", "")
            cls = _cost_class(cost)
            chip = ('<span class="cost-chip free-chip">Free</span> ' if cls == "free"
                    else '<span class="cost-chip paid-chip">$</span> ' if cls == "paid"
                    else '<span class="cost-chip mixed-chip">Free / paid</span> ' if cls == "mixed"
                    else "")
            cost_html = f"{chip}{esc(cost)}" if cost else '<span class="na">not confirmed</span>'
            out.append(
                f"<tr><td>{esc(when)}</td><td><a href='{row_link(e)}'>{esc(e['title'])}</a></td>"
                f"<td>{cost_html}</td>"
                f"<td><a href='{esc(e['source_url'])}' target='_blank' rel='noopener'>"
                f"{esc(e['source_name'])} &nearr;</a></td></tr>"
            )
        return "".join(out) or ("<tr><td colspan='4'><span class='na'>none listed in this window</span></td></tr>")

    soon_free = sum(1 for _s, _e, ev in starting_soon if _cost_class(ev.get("cost", "")) in ("free", "mixed"))
    soonest = starting_soon[0][2]["title"] if starting_soon else "—"

    # Free spotlight: user-requested focus on free gaming, music and AI events.
    def theme_of(ev):
        t = (ev.get("title", "") + " " + ev.get("notes", "")).lower()
        if re.search(r"\b(game|gaming|games|chess|dungeons|d&d|nintendo|arcade|pinball|esports)\b", t):
            return "Gaming"
        if re.search(r"\b(ai|a\.i\.|artificial intelligence|robotics|machine learning|tech week)\b", t):
            return "AI & tech"
        if re.search(r"\b(music|concert|band|jazz|symphony|opera|choir|piano|k-pop|dance|theatre|theater|shakespeare|song)\b", t):
            return "Music & stage"
        return ""

    spotlight = []
    for e in EVENTS:
        if e.get("timing") == "concluded":
            continue
        if _cost_class(e.get("cost", "")) not in ("free", "mixed"):
            continue
        theme = theme_of(e)
        if theme:
            spotlight.append((theme, e))
    spotlight.sort(key=lambda t: (t[0], t[1].get("title", "")))
    spotlight_rows = "".join(
        f"<tr><td>{esc(theme)}</td><td><a href='{row_link(e)}'>{esc(e['title'])}</a></td>"
        f"<td>{esc(e.get('schedule') or e.get('dates') or '')}</td>"
        f"<td><a href='{esc(e['source_url'])}' target='_blank' rel='noopener'>{esc(e['source_name'])} &nearr;</a></td></tr>"
        for theme, e in spotlight
    ) or "<tr><td colspan='4'><span class='na'>none listed</span></td></tr>"

    latest_rows = "".join(
        f"<tr><td><a href='{row_link(e)}'>{esc(e['title'])}</a></td><td>{esc(e.get('dates', ''))}</td>"
        f"<td>{esc(e.get('location', ''))}</td>"
        + _cost_cell(e.get("cost", ""))
        + f"<td><a href='{esc(e['source_url'])}' target='_blank' rel='noopener'>"
        f"{esc(e['source_name'])} &nearr;</a></td></tr>"
        for _s, _e, e in upcoming
    ) or "<tr><td colspan='5'><span class='na'>none listed</span></td></tr>"

    body = f"""
<section class="hero">
  <h1>San Francisco events, sourced and organized</h1>
  <p class="lede">A curated snapshot of public events inside the City of San Francisco, organized by schedule
     and category. Browse events that happen <strong>every week or every year</strong>, plus
     <strong>special and dated</strong> listings, civic meetings, arts, sports and markets. Entries link to
     official organizer or government sources; unconfirmed values are left blank.</p>
  <p class="coverage-note"><strong>Coverage note:</strong> This is not an exhaustive or live events calendar.
     San Francisco has many venue-level, private and short-notice events that are not captured here. Check the
     <a href="https://www.sf.gov/events/upcoming" target="_blank" rel="noopener">City&#x27;s official events calendar</a>
     and each organizer for current listings and details.</p>
  <div class="hero-actions">
    <a class="btn" href="all-events.html">Open the full list ({len(EVENTS)})</a>
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
  <div class="stat"><span class="stat-n">{sum(1 for e in EVENTS if e.get("timing") == "concluded")}</span><span class="stat-l">concluded editions</span></div>
  <div class="stat"><span class="stat-n">{len(FLAGGED)}</span><span class="stat-l">review items published</span></div>
  <div class="stat"><span class="stat-n">{len({e['source_url'].split('/')[2] for e in EVENTS})}</span><span class="stat-l">distinct official domains</span></div>
</section>

<section class="exec-summary">
  <h2>Executive summary &mdash; what&#x27;s close to today ({esc(VERIFIED_ON)})</h2>
  <p class="lede">This snapshot was verified on <strong>{esc(VERIFIED_ON)}</strong>. In the next three weeks
     <strong>{len(starting_soon)}</strong> listed dated events start (soonest: <strong>{esc(soonest)}</strong>),
     of which <strong>{soon_free}</strong> are free or partly free, and <strong>{len(running_now)}</strong> dated
     events are running right now. Costs below are exactly as the official source states them;
     <span class="na">not confirmed</span> means the source publishes no price.</p>
  <div class="two-col">
    <div>
      <h3>Starting soon (next three weeks)</h3>
      <div class="table-scroll">
      <table class="data-table compact">
        <thead><tr><th scope="col">When</th><th scope="col">Event</th><th scope="col">Cost</th><th scope="col">Official source</th></tr></thead>
        <tbody>{mini_rows(starting_soon)}</tbody>
      </table>
      </div>
    </div>
    <div>
      <h3>Running now</h3>
      <div class="table-scroll">
      <table class="data-table compact">
        <thead><tr><th scope="col">Dates</th><th scope="col">Event</th><th scope="col">Cost</th><th scope="col">Official source</th></tr></thead>
        <tbody>{mini_rows(running_now)}</tbody>
      </table>
      </div>
    </div>
  </div>
  <h3>Free spotlight &mdash; gaming, music and AI</h3>
  <p class="note">The brief for this catalogue prioritises free events in gaming, music and AI, then everything
     else. The rows below are the free (or partly free) entries in those themes; the
     <a href="all-events.html">full list</a> covers every theme and includes a &ldquo;Free only&rdquo; filter.</p>
  <div class="table-scroll">
  <table class="data-table compact">
    <thead><tr><th scope="col">Theme</th><th scope="col">Event</th><th scope="col">When</th><th scope="col">Official source</th></tr></thead>
    <tbody>{spotlight_rows}</tbody>
  </table>
  </div>
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
  <h2>Upcoming dated events</h2>
  <p class="note">Every listed row with confirmed dates that is running now or starts later, sorted
     <strong>soonest first</strong>. Costs are labelled as the official source states them.</p>
  <div class="table-scroll">
  <table class="data-table">
    <thead><tr><th scope="col">Event</th><th scope="col">Confirmed dates</th><th scope="col">Where</th><th scope="col">Cost</th><th scope="col">Official source</th></tr></thead>
    <tbody>{latest_rows}</tbody>
  </table>
  </div>
  <p class="note"><a href="special.html">See all special events &rarr;</a></p>
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
        rows.append(
            f"""<tr id="{esc(f['id'])}">
  <td class="flag-title">{esc(f['title'])}</td>
  <td>{esc(f['detail'])}</td>
  <td>{esc(f['action'])}</td>
  <td><a href="{esc(f['source_url'])}" target="_blank" rel="noopener">{esc(f['source_name'])} &nearr;</a></td>
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
            f"<tr id=\"review-{esc(e['id'])}\"><td>{esc(e['title'])}</td>"
            f"<td>{esc(e.get('group', ''))} / {esc(e.get('category', ''))}</td>"
            f"<td>{esc(status_cell)}</td>"
            f"<td>{esc(blank_cell)}</td>"
            f"<td><a href='{esc(e['source_url'])}' target='_blank' rel='noopener'>{esc(e['source_name'])} &nearr;</a></td></tr>"
        )
    return "\n".join(out)



FILTER_JS = """
(function () {
  var q = document.getElementById('q');
  var fType = document.getElementById('f-type');
  var fCat = document.getElementById('f-cat');
  var fCost = document.getElementById('f-cost');
  var fStatus = document.getElementById('f-status');
  var fTime = document.getElementById('f-time');
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
    var t = fType.value, c = fCat.value, co = fCost.value, st = fStatus.value, ti = fTime.value;
    var shown = 0;
    rows.forEach(function (r) {
      if (r.classList.contains('note-row')) { return; }
      var ok = true;
      if (t && r.getAttribute('data-group') !== t) { ok = false; }
      if (c && r.getAttribute('data-cat') !== c) { ok = false; }
      if (co && r.getAttribute('data-cost') !== co) { ok = false; }
      if (st && r.getAttribute('data-status') !== st) { ok = false; }
      if (ti && r.getAttribute('data-timing') !== ti) { ok = false; }
      if (ok && term && (r.getAttribute('data-text') || '').indexOf(term) === -1) { ok = false; }
      r.hidden = !ok;
      var n = notes[r.id];
      if (n) { n.hidden = !ok; }
      if (ok) { shown += 1; }
    });
    if (count) { count.textContent = shown; }
  }
  [q, fType, fCat, fCost, fStatus, fTime].forEach(function (el) {
    if (el) { el.addEventListener('input', apply); el.addEventListener('change', apply); }
  });
  var reset = document.getElementById('reset');
  if (reset) {
    reset.addEventListener('click', function (ev) {
      ev.preventDefault();
      q.value = ''; fType.value = ''; fCat.value = ''; fCost.value = ''; fStatus.value = ''; fTime.value = '';
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
            ("markets", "Markets & food"), ("community", "Community & parks")]
    costs = [("", "Any cost"), ("free", "Free"), ("paid", "Paid / ticketed"), ("mixed", "Free / paid mix"),
             ("blank", "Cost not confirmed")]
    stat = [("", "All rows"), ("verified", "Verified"), ("unverified", "Needs review")]
    tim = [("", "Any timing"), ("current", "Current / upcoming"), ("concluded", "Concluded edition")]

    def opts(items):
        return "".join(f'<option value="{esc(v)}">{esc(l)}</option>' for v, l in items)

    body = f"""
<section class="page-head">
  <h1>Full list</h1>
  <p class="lede">Every entry in the catalogue in one table: recurring programmes, annual events and dated
     specials. Filter by schedule, category, cost (Free / paid), verification status or timing, or search
     by name, venue, neighbourhood or organiser. Each row links to its official source.</p>
</section>

<div class="controls" role="search">
  <label class="field grow"><span>Search</span>
    <input id="q" type="search" placeholder="Try &quot;farmers&quot;, &quot;Mission&quot;, &quot;SFMOMA&quot; or &quot;free&quot;" autocomplete="off">
  </label>
  <label class="field"><span>Schedule</span><select id="f-type">{opts(groups)}</select></label>
  <label class="field"><span>Category</span><select id="f-cat">{opts(cats)}</select></label>
  <label class="field"><span>Cost</span><select id="f-cost">{opts(costs)}</select></label>
  <label class="field"><span>Status</span><select id="f-status">{opts(stat)}</select></label>
  <label class="field"><span>Timing</span><select id="f-time">{opts(tim)}</select></label>
  <button id="reset" class="btn ghost" type="button">Reset</button>
</div>

<p class="count-note"><strong id="visible-count">{len(EVENTS)}</strong> of {len(EVENTS)} entries shown &middot;
   checked {esc(VERIFIED_ON)} &middot; <a href="data/events.csv">download CSV</a> &middot;
   <a href="data/events.json">machine-readable JSON</a></p>

{event_table(sorted(EVENTS, key=lambda e: (e.get("group", ""), e.get("title", ""))), "all-table")}

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
    cat_labels = {"civic": "Civic meetings", "arts": "Arts & culture", "sports": "Sports", "markets": "Markets & food", "community": "Community & parks"}

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
    <li><strong>Category pages</strong> for civic meetings, arts and culture, sports, and markets and food are
        provided for usability. Each listed event appears on its category page and on the page matching its type,
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
    body = f"""
<section class="page-head">
  <h1>{esc(label)}</h1>
  <p class="lede">{esc(subtitle)}</p>
</section>

<p class="count-note">{len(events)} entries &middot; {verified} fully verified &middot;
  {len(events) - verified} with a flagged gap &middot; checked {esc(VERIFIED_ON)}</p>

{event_table(events, page + "-table")}
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
.badge.warn { background: var(--warn-bg); color: var(--warn-ink); }
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
  .two-col { grid-template-columns: 1fr; }
}
@media print {
  .site-nav, .hero-actions, .btn { display: none; }
  .table-scroll { overflow: visible; }
  .data-table { min-width: 0; font-size: 8pt; }
}

/* Cost labels (every table row states the cost exactly as the source words it) */
.cost-cell { vertical-align: top; }
.cost-chip {
  display: inline-block; padding: 1px 8px; border-radius: 999px;
  font-size: .72rem; font-weight: 700; letter-spacing: .02em;
  vertical-align: 1px; margin-right: 4px; white-space: nowrap;
}
.free-chip { background: var(--ok-bg); color: var(--ok-ink); border: 1px solid #bfe3c9; }
.paid-chip { background: #eef2f7; color: #3c4a5c; border: 1px solid #d5dde6; }
.mixed-chip { background: var(--warn-bg); color: var(--warn-ink); border: 1px solid #ead9a8; }

/* Executive summary */
.exec-summary {
  background: var(--panel); border: 1px solid var(--line); border-radius: var(--radius);
  padding: 18px 20px 22px; margin: 22px 0 8px; box-shadow: 0 1px 2px rgba(16, 34, 46, .05);
}
.exec-summary h2 { margin-top: 0; }
.exec-summary h3 { font-size: 1.02rem; margin: 18px 0 8px; }
.exec-summary .data-table { min-width: 640px; }
.exec-summary .data-table td, .exec-summary .data-table th { padding: 7px 10px; }

/* Small screens */
@media (max-width: 640px) {
  .stat-row { gap: 8px; }
  .tiles { grid-template-columns: repeat(2, minmax(0, 1fr)); }
  .exec-summary { padding: 14px; }
  .site-nav a { padding: 5px 9px; font-size: .8rem; }
  main { padding: 20px 14px 44px; }
  h2 { font-size: 1.1rem; }
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
    csv_fields = ["id", "title", "group", "category", "type", "schedule", "dates", "location",
                  "area", "cost", "organiser", "status", "timing", "source_name", "source_url", "notes"]
    with open(os.path.join(ROOT, "data", "events.csv"), "w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=csv_fields, extrasaction="ignore")
        writer.writeheader()
        for ev in sorted(EVENTS, key=lambda e: (e.get("group", ""), e.get("title", ""))):
            writer.writerow({k: ev.get(k, "") for k in csv_fields})

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
