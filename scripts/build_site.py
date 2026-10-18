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
SITE_TAGLINE = "Every event in the City of San Francisco — recurring, annual and special"

# (filename, label, blurb, kind) where kind is "group" (recurrence type),
# "category" (subject area), "static" or "home".
PAGES = [
    ("index.html", "Home", "Dashboard", "home"),
    ("recurring.html", "Regularly recurring", "Events that happen on a fixed weekly or monthly schedule", "group"),
    ("annual.html", "Annual", "Events that repeat year after year", "group"),
    ("special.html", "Special", "Dated events for 2026–2027", "special"),
    ("civic.html", "Civic", "Boards, commissions and public meetings", "category"),
    ("arts.html", "Arts & culture", "Museums, galleries, performance and screen", "category"),
    ("sports.html", "Sports", "Teams, races and active recreation", "category"),
    ("markets.html", "Markets & food", "Farmers markets, food halls and street markets", "category"),
    ("community.html", "Community & parks", "Neighbourhood programmes, festivals and free recreation", "category"),
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
        <small>City-limits only &middot; every row sourced to an official site</small>
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
    <p>Every row on this site carries a link to the official organiser, city agency or state source that was
       checked on <strong>{esc(VERIFIED_ON)}</strong>. Values that could not be confirmed from an official source
       are left blank and listed on the
       <a href="flagged.html">Flagged for review</a> page. Nothing on this site is inferred.</p>
    <p class="muted">Scope is the City and County of San Francisco only. Events physically located in other Bay
       Area cities are excluded and the exclusions are listed on the Flagged for review page.</p>
  </div>
</footer>
</body>
</html>
"""


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
        title_cell = (
            f'<span class="ev-title">{esc(ev["title"])}</span>'
            f'<span class="ev-source">{badge}'
            f'<a href="{esc(ev["source_url"])}" target="_blank" rel="noopener">'
            f'{esc(ev["source_name"])} &nearr;</a></span>'
        )
        cells = [title_cell]
        for key in ("type", "schedule", "dates", "location", "area", "cost", "organiser"):
            value = ev.get(key, "")
            if not value:
                cells.append('<td class="unverified-cell"><span class="na">not confirmed</span></td>')
            else:
                cells.append(f"<td>{esc(value)}</td>")
        note = ev.get("notes", "")
        note_html = f'<p class="row-note">{esc(note)}</p>' if note else ""
        rows.append(
            f'<tr id="{esc(ev["id"])}">'
            + "".join(cells)
            + f"</tr>"
        )
        if note_html:
            rows.append(f'<tr class="note-row"><td colspan="{len(COLUMNS)}">{note_html}</td></tr>')
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
        n = counts.get(filename.replace(".html", ""), 0)
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

    latest = [
        e for e in EVENTS if e.get("group") == "special" and e.get("dates")
    ][:6]
    latest_rows = "".join(
        f"<tr><td>{esc(e['title'])}</td><td>{esc(e['dates'])}</td>"
        f"<td>{esc(e['location'])}</td>"
        f"<td><a href='{esc(e['source_url'])}' target='_blank' rel='noopener'>{esc(e['source_name'])} &nearr;</a></td></tr>"
        for e in latest
    )

    body = f"""
<section class="hero">
  <h1>Every event happening inside the City of San Francisco</h1>
  <p class="lede">A verified, source-linked directory of what is on in San Francisco &mdash; split into events that
     happen <strong>every week or every year</strong> and events that are <strong>special and dated</strong>,
     plus civic meetings, arts, sports and markets. Every row links to the official organiser or government
     source that was checked; nothing is filled in from memory.</p>
  <div class="hero-actions">
    <a class="btn" href="recurring.html">Browse recurring events</a>
    <a class="btn ghost" href="annual.html">Browse annual events</a>
    <a class="btn ghost" href="flagged.html">{len(FLAGGED)} items flagged for review</a>
  </div>
</section>

<section class="stat-row">
  <div class="stat"><span class="stat-n">{len(EVENTS)}</span><span class="stat-l">events listed</span></div>
  <div class="stat"><span class="stat-n">{verified}</span><span class="stat-l">fully verified rows</span></div>
  <div class="stat"><span class="stat-n">{unverified}</span><span class="stat-l">rows with a flagged gap</span></div>
  <div class="stat"><span class="stat-n">{len(FLAGGED)}</span><span class="stat-l">discrepancies published</span></div>
  <div class="stat"><span class="stat-n">{len({e['source_url'].split('/')[2] for e in EVENTS})}</span><span class="stat-l">distinct official domains</span></div>
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
  <h2>Recently confirmed dated events</h2>
  <div class="table-scroll">
  <table class="data-table">
    <thead><tr><th scope="col">Event</th><th scope="col">Confirmed dates</th><th scope="col">Where</th><th scope="col">Official source</th></tr></thead>
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
        row could be confirmed from the official source.</li>
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
    <th scope="col">Event</th><th scope="col">Page</th><th scope="col">Fields left blank</th>
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
        if e.get("status") != "unverified":
            continue
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
        out.append(
            f"<tr><td>{esc(e['title'])}</td>"
            f"<td>{esc(e.get('group', ''))} / {esc(e.get('category', ''))}</td>"
            f"<td>{esc(', '.join(blanks) if blanks else 'see note')}</td>"
            f"<td><a href='{esc(e['source_url'])}' target='_blank' rel='noopener'>{esc(e['source_name'])} &nearr;</a></td></tr>"
        )
    return "\n".join(out)


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
    <li><strong>City of San Francisco only.</strong> Events physically inside the San Francisco city limits are
        included. Events in other Bay Area cities are excluded, even when they are called "San Francisco" events
        (for example the San Francisco 49ers, who play every home game at Levi's Stadium in Santa Clara).</li>
    <li><strong>Two organising groups, as requested:</strong> events that occur on a <em>regular schedule</em>
        (every week / every month) are on the <a href="recurring.html">Regularly recurring</a> page; events that
        recur <em>year after year</em> are on the <a href="annual.html">Annual</a> page; genuinely one-off dated
        events are on the <a href="special.html">Special</a> page.</li>
    <li><strong>Category pages</strong> for civic meetings, arts and culture, sports, and markets and food are
        provided for usability. Every event appears on its category page and on the page matching its type, so the
        same row is never duplicated or contradicted.</li>
  </ul>
</section>

<section>
  <h2>Sourcing rules</h2>
  <ul class="plain-list">
    <li><strong>Official sources only.</strong> Every row links to the organiser's own site, a City and County of
        San Francisco agency page, a state agency page, or a federally operated national-park page. Each link was
        opened and read on <strong>{esc(VERIFIED_ON)}</strong>.</li>
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
    <li><code>scripts/build_site.py</code> renders the static HTML pages. There is no client-side JavaScript: every
        page is plain HTML that GitHub Pages can serve directly.</li>
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
    <li><a href="analysis.html">Analysis</a> &mdash; the parallel session's category and neighbourhood analysis.</li>
    <li><a href="sources.html">Source registry</a> &mdash; the parallel session's list of the 58 official sources it checked.</li>
    <li><a href="data/review.csv">Review sheet</a> &mdash; the parallel session's line-by-line review CSV.</li>
    <li><a href="data/schema.md">Data schema</a> &mdash; the parallel session's documented JSON schema.</li>
  </ul>
</section>

<section>
  <h2>Known limitations</h2>
  <ul class="plain-list">
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

    written = ["index.html", "flagged.html", "methodology.html"]
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

    print(f"Wrote {len(written) + 1} pages, {len(EVENTS)} events, {len(FLAGGED)} flagged items.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
