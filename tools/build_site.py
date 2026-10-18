#!/usr/bin/env python3
"""Generate the static GitHub Pages dashboard from data/*.json.

No third-party dependencies. Writes HTML at the repository root so the
existing GitHub Pages source (main branch, /) serves it directly.
"""
import collections
import datetime as dt
import html
import json
import os
import re
from urllib.parse import urlparse

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TODAY = dt.date(2026, 10, 18)
VERIFIED_ON = "2026-10-18"
SITE_NAME = "SF Events Index"
REPO_URL = "https://github.com/buffedlizard55-lab/MaltaProj6"

NAV = [
    ("index.html", "Overview"),
    ("weekly.html", "Recurring"),
    ("annual.html", "Annual"),
    ("special.html", "Special"),
    ("analysis.html", "Analysis"),
    ("sources.html", "Sources"),
    ("flagged.html", "Flagged for Review"),
]


def load(name):
    with open(os.path.join(ROOT, "data", name), encoding="utf-8") as fh:
        return json.load(fh)


def esc(value):
    return html.escape(str(value or ""), quote=True)


def parse_date(value):
    if not value:
        return None
    try:
        return dt.date.fromisoformat(value)
    except ValueError:
        return None


def date_list(value):
    out = []
    for part in str(value or "").split(";"):
        d = parse_date(part.strip())
        if d:
            out.append(d)
    return out


def fmt(d):
    return d.strftime("%b %-d, %Y") if d else ""


def month_num(name):
    names = ["january", "february", "march", "april", "may", "june", "july",
             "august", "september", "october", "november", "december"]
    low = str(name or "").lower()
    for i, m in enumerate(names, 1):
        if m in low:
            return i
    return 13


def source_link(ev, label=None):
    url = ev.get("source_url", "")
    domain = urlparse(url).netloc.replace("www.", "")
    text = label or domain
    return (f'<a href="{esc(url)}" target="_blank" rel="noopener" '
            f'title="{esc(ev.get("source_title"))}">{esc(text)}</a>')


FIELD_LABELS = {
    "schedule.start_time": "start time",
    "display_dates.end": "end date",
    "dates.next_edition": "next edition date",
}


def unverified_badge(ev):
    if ev.get("unverified_fields"):
        fields = ", ".join(FIELD_LABELS.get(f, f.replace("_", " ")) for f in ev["unverified_fields"])
        return f'<span class="badge unverified" title="Unverified: {esc(fields)}">unverified</span>'
    return ""


def special_status(ev):
    start = parse_date(ev.get("start_date"))
    end = parse_date(ev.get("end_date"))
    if start and end:
        if end < TODAY:
            return "past"
        if start > TODAY:
            return "upcoming"
        return "ongoing"
    if start:
        return "upcoming" if start > TODAY else "ongoing"
    if end:
        return "past" if end < TODAY else "ongoing"
    return "unknown"


def annual_next(ev):
    ds = [d for d in date_list(ev.get("dates")) if d >= TODAY]
    return min(ds) if ds else None


def annual_status(ev):
    if annual_next(ev):
        return "upcoming"
    return "past" if date_list(ev.get("dates")) else "unknown"


def next_when(ev):
    """Sortable (date, text) for the combined 'what's next' feed."""
    if ev["category"] == "special":
        start = parse_date(ev.get("start_date"))
        end = parse_date(ev.get("end_date"))
        status = special_status(ev)
        if status == "ongoing":
            return TODAY, "On now"
        if status == "upcoming" and start:
            return start, fmt(start)
    if ev["category"] == "annual":
        nxt = annual_next(ev)
        if nxt:
            return nxt, fmt(nxt)
    return dt.date(2999, 1, 1), "TBA"


def weekday_hits(text):
    low = str(text or "").lower()
    hits = []
    for key, names in {
        "Monday": ["monday", "mon "], "Tuesday": ["tuesday", "tue "],
        "Wednesday": ["wednesday", "wed "], "Thursday": ["thursday", "thu "],
        "Friday": ["friday", "fri "], "Saturday": ["saturday", "sat "],
        "Sunday": ["sunday", "sun "],
    }.items():
        if any(n in low for n in names):
            hits.append(key)
    return hits


def hoods(value):
    parts = re.split(r"[/,&]", str(value or ""))
    return [p.strip() for p in parts if p.strip()]


def page(title, active, description, body):
    nav_links = []
    for href, label in NAV:
        current = ' aria-current="page"' if href == active else ""
        nav_links.append(f'<a href="{href}"{current}>{label}</a>')
    nav = "\n".join(nav_links)
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)} · {SITE_NAME}</title>
<meta name="description" content="{esc(description)}">
<link rel="stylesheet" href="assets/style.css">
</head>
<body>
<a class="skip-link" href="#main">Skip to content</a>
<header class="site">
  <div class="wrap header-inner">
    <a class="brand" href="index.html">
      <span class="brand-mark" aria-hidden="true">SF</span>
      <span class="brand-text"><strong>{SITE_NAME}</strong><span>Verified event catalogue</span></span>
    </a>
    <nav class="site" aria-label="Main navigation">
      {nav}
    </nav>
  </div>
</header>
<main id="main">
  <div class="wrap">
    {body}
  </div>
</main>
<footer class="site">
  <div class="wrap footer-inner">
    <div>
      <strong>{SITE_NAME}</strong> · City and County of San Francisco only · Data verified {VERIFIED_ON}.
      <br>Every row links to the government, organiser or venue page that confirms it.
    </div>
    <div>
      <a href="analysis.html">Method &amp; analysis</a> ·
      <a href="sources.html">Source registry</a> ·
      <a href="flagged.html">Flagged for Review</a> ·
      <a href="{REPO_URL}" target="_blank" rel="noopener">Repository</a>
      <br><a class="back-top" href="#main">Back to top ↑</a>
    </div>
  </div>
</footer>
<script src="assets/app.js" defer></script>
</body>
</html>
"""


def table(tools_id, table_id, caption, headers, rows, select_label=None, select_options=None):
    opts = ""
    if select_options:
        opts = "".join(f'<option value="{esc(v)}">{esc(l)}</option>' for v, l in select_options)
        select = f'<label for="{table_id}-filter">{esc(select_label or "Filter")}</label><select id="{table_id}-filter">{opts}</select>'
    else:
        select = ""
    head = "".join(f'<th scope="col">{h}</th>' for h in headers)
    body = "\n".join(rows)
    return f"""
<div class="table-tools" data-table="{table_id}">
  <label for="{table_id}-search">Search</label>
  <input id="{table_id}-search" type="search" placeholder="Event, place, organiser…" autocomplete="off">
  {select}
  <span class="result" aria-live="polite"></span>
</div>
<div class="table-wrap">
<table class="data" id="{table_id}">
  <caption>{esc(caption)} <span class="small">(<span data-row-count>{len(rows)}</span> rows)</span></caption>
  <thead><tr>{head}</tr></thead>
  <tbody>
{body}
  </tbody>
</table>
</div>
"""


def weekly_row(ev):
    search = " ".join(str(ev.get(k, "")) for k in
                      ("name", "cadence", "schedule", "venue", "neighborhood", "organizer", "notes")).lower()
    bucket = "weekly" if ev.get("category") == "weekly" else "monthly"
    sub = f'<span class="sub">{esc(ev.get("notes"))}</span>' if ev.get("notes") else ""
    return f"""<tr id="{ev['id']}" data-search="{esc(search)}" data-bucket="{bucket}">
  <td class="event"><span class="name">{esc(ev['name'])}</span>{unverified_badge(ev)}{sub}</td>
  <td>{esc(ev.get('cadence'))}</td>
  <td>{esc(ev.get('schedule')) or '<span class="small">—</span>'}</td>
  <td>{esc(ev.get('venue'))}</td>
  <td>{esc(ev.get('neighborhood'))}</td>
  <td>{esc(ev.get('organizer'))}</td>
  <td>{esc(ev.get('admission')) or '<span class="small">—</span>'}</td>
  <td class="src">{source_link(ev)}<span class="type">{esc(ev.get('source_type'))}</span></td>
</tr>"""


def annual_row(ev):
    status = annual_status(ev)
    search = " ".join(str(ev.get(k, "")) for k in
                      ("name", "display_dates", "venue", "neighborhood", "organizer", "notes", "edition")).lower()
    sub = f'<span class="sub">{esc(ev.get("notes"))}</span>' if ev.get("notes") else ""
    dates = esc(ev.get("display_dates")) or '<span class="small">—</span>'
    edition = f'<span class="badge recurring">{esc(ev.get("edition"))}</span> ' if ev.get("edition") else ""
    nexts = esc(ev.get("next_edition_status")) or '<span class="small">—</span>'
    return f"""<tr id="{ev['id']}" data-search="{esc(search)}" data-bucket="{status}">
  <td class="event"><span class="name">{esc(ev['name'])}</span>{unverified_badge(ev)}{sub}</td>
  <td>{edition}{dates}</td>
  <td>{esc(ev.get('venue'))}<span class="sub">{esc(ev.get('neighborhood'))}</span></td>
  <td>{esc(ev.get('organizer'))}</td>
  <td>{esc(ev.get('admission')) or '<span class="small">—</span>'}</td>
  <td>{nexts}</td>
  <td class="src">{source_link(ev)}<span class="type">{esc(ev.get('source_type'))}</span></td>
</tr>"""


def special_row(ev):
    status = special_status(ev)
    label = {"upcoming": "Upcoming", "ongoing": "On now", "past": "Past", "unknown": "Not announced"}[status]
    search = " ".join(str(ev.get(k, "")) for k in
                      ("name", "display_dates", "venue", "neighborhood", "organizer", "type", "notes")).lower()
    sub = f'<span class="sub">{esc(ev.get("notes"))}</span>' if ev.get("notes") else ""
    return f"""<tr id="{ev['id']}" data-search="{esc(search)}" data-bucket="{status}">
  <td class="event"><span class="name">{esc(ev['name'])}</span>{unverified_badge(ev)}{sub}</td>
  <td>{esc(ev.get('display_dates')) or '<span class="small">—</span>'}</td>
  <td><span class="badge {status}">{label}</span></td>
  <td>{esc(ev.get('type'))}</td>
  <td>{esc(ev.get('venue'))}<span class="sub">{esc(ev.get('neighborhood'))}</span></td>
  <td>{esc(ev.get('organizer'))}</td>
  <td class="src">{source_link(ev)}<span class="type">{esc(ev.get('source_type'))}</span></td>
</tr>"""


def build_index(events, sources, flagged):
    n = len(events)
    n_weekly = sum(1 for e in events if e["category"] == "weekly")
    n_monthly = sum(1 for e in events if e["category"] == "monthly")
    n_annual = sum(1 for e in events if e["category"] == "annual")
    n_special = sum(1 for e in events if e["category"] == "special")
    n_unverified = sum(1 for e in events if e.get("unverified_fields"))
    gov = sum(1 for s in sources if s["type"] == "government")

    feed = [e for e in events if e["category"] in ("annual", "special")]
    feed = [(next_when(e), e) for e in feed]
    feed = [(k, e) for k, e in feed if k[0] != dt.date(2999, 1, 1)]
    feed.sort(key=lambda pair: (pair[0][0], pair[1]["name"]))
    feed = feed[:14]

    feed_rows = []
    for (when, when_text), ev in feed:
        cat = "Annual" if ev["category"] == "annual" else "Special"
        href = "annual.html" if ev["category"] == "annual" else "special.html"
        feed_rows.append(
            f"<tr><td>{esc(when_text)}</td>"
            f"<td class=\"event\"><a href=\"{href}#{ev['id']}\">{esc(ev['name'])}</a>"
            f"{unverified_badge(ev)}</td>"
            f"<td>{cat}</td><td>{esc(ev.get('venue'))}</td>"
            f"<td class=\"src\">{source_link(ev)}</td></tr>"
        )
    feed_table = table("feed-tools", "feed", "What's on now and next",
                       ["When", "Event", "Type", "Where", "Source"], feed_rows) if feed_rows else \
        '<p class="small">No dated events found.</p>'

    body = f"""
<section class="hero">
  <p class="eyebrow">San Francisco · verified {VERIFIED_ON}</p>
  <h1>What’s on in San Francisco — checked against the source that runs it</h1>
  <p class="lede">A working catalogue of events inside the <strong>City and County of San Francisco</strong>, split into
  recurring weekly or monthly programmes, annual traditions, and dated special events. Every row links to an official
  government, organiser or venue page. Nothing is inferred: if a value was not on an official page, it is blank and the
  row is marked <span class="badge unverified">unverified</span>.</p>
  <div class="hero-meta">
    <span class="pill"><strong>{n}</strong> events catalogued</span>
    <span class="pill"><strong>{len(sources)}</strong> official sources</span>
    <span class="pill"><strong>{n_unverified}</strong> rows with unverified fields</span>
    <span class="pill"><strong>{len(flagged)}</strong> review notes</span>
  </div>
  <div class="kpis">
    <div class="kpi"><a href="weekly.html"><div class="num">{n_weekly + n_monthly}</div><div class="label">Recurring weekly / monthly</div></a></div>
    <div class="kpi"><a href="annual.html"><div class="num">{n_annual}</div><div class="label">Annual events</div></a></div>
    <div class="kpi"><a href="special.html"><div class="num">{n_special}</div><div class="label">Special / one-time</div></a></div>
    <div class="kpi"><a href="flagged.html"><div class="num">{n_unverified}</div><div class="label">Rows flagged unverified</div></a></div>
    <div class="kpi"><a href="sources.html"><div class="num">{gov}</div><div class="label">Government sources</div></a></div>
  </div>
</section>

<h2>What's on now and next</h2>
<p class="section-note">Ongoing and upcoming dated events from the annual and special tables, ordered by date. Past editions stay in the
category tables for completeness.</p>
{feed_table}

<h2>Browse by category</h2>
<div class="grid-3">
  <a class="card-link card" href="weekly.html">
    <div class="count">{n_weekly + n_monthly}</div>
    <h3>Recurring weekly &amp; monthly</h3>
    <p>Farmers markets, museum late nights, street markets and monthly neighbourhood programmes — {n_weekly} weekly and {n_monthly} monthly entries, each with its confirmed cadence.</p>
  </a>
  <a class="card-link card" href="annual.html">
    <div class="count">{n_annual}</div>
    <h3>Annual events</h3>
    <p>Parades, street fairs, festivals, races, film and music seasons. Where the organiser has already published 2027 dates, those are shown; otherwise the last confirmed edition is shown and flagged.</p>
  </a>
  <a class="card-link card" href="special.html">
    <div class="count">{n_special}</div>
    <h3>Special &amp; one-time events</h3>
    <p>Dated exhibitions, opera and concert runs, conventions, markets and one-off civic events, each with a start and end date where the organiser publishes them.</p>
  </a>
</div>

<h2>How to read this dashboard</h2>
<div class="grid-3">
  <div class="card">
    <h3>Source first</h3>
    <p>Each row's source column names the domain that confirmed it. Government pages are used first, then the event organiser, then the venue. The full registry is on the <a href="sources.html">Sources page</a>.</p>
  </div>
  <div class="card">
    <h3>Blanks are deliberate</h3>
    <p>If an official page did not state a time, date, address or price, the field is empty. It is never filled from memory or from an aggregator. Rows carrying such gaps are labelled and listed on <a href="flagged.html">Flagged for Review</a>.</p>
  </div>
  <div class="card">
    <h3>City boundary enforced</h3>
    <p>Only events in San Francisco are included. Oakland's Black Joy Parade, Daly City's street festival and Levi's Stadium events in Santa Clara are excluded on purpose; the exclusions are documented in the review log.</p>
  </div>
</div>

<div class="callout">
  <strong>Scope:</strong> this is a broad catalogue of public events, not a ticketing feed. Private and members-only events,
  school-only programmes and one-off private venue bookings are out of scope. Venue concert calendars are represented by
  their published seasons and headline runs, not by every individual performance.
  <a href="analysis.html">Read the method and limitations →</a>
</div>
"""
    return page("Overview", "index.html",
                "Verified catalogue of San Francisco events: recurring weekly and monthly programmes, annual events and dated special events, each linked to an official source.",
                body)


def build_weekly(events):
    rows = [weekly_row(e) for e in sorted(events, key=lambda e: e["name"].lower())]
    n_weekly = sum(1 for e in events if e["category"] == "weekly")
    n_monthly = sum(1 for e in events if e["category"] == "monthly")
    body = f"""
<div class="breadcrumb"><a href="index.html">Overview</a> / Recurring events</div>
<p class="eyebrow">Category</p>
<h1>Recurring weekly &amp; monthly events</h1>
<p class="lede">{n_weekly} weekly programmes and {n_monthly} monthly programmes, each confirmed on the organiser's own page or a
government listing. Cadence and season are recorded exactly as published; where a season was not stated it is left blank
and marked unverified.</p>
<div class="callout">
  <strong>Before you go:</strong> recurring schedules change with permits, seasons and holidays. The source link in each row
  is the page that was checked on {VERIFIED_ON}; re-open it for the week you plan to attend.
</div>
{table("weekly-tools", "weekly-table", "All recurring events",
       ["Event", "Cadence", "When", "Where", "Neighborhood", "Organizer", "Admission", "Source"],
       rows, "Cadence", [("all", "All cadences"), ("weekly", "Weekly"), ("monthly", "Monthly")])}
<p class="small">Rows marked <span class="badge unverified">unverified</span> have at least one field that the official page did not state.
Those fields are blank and listed on <a href="flagged.html">Flagged for Review</a>.</p>
"""
    return page("Recurring weekly & monthly events", "weekly.html",
                "San Francisco farmers markets, museum late nights and monthly street markets with confirmed schedules and official source links.",
                body)


def build_annual(events):
    ordered = sorted(events, key=lambda e: (
        0 if annual_next(e) else 1,
        annual_next(e) or dt.date(2999, 1, 1),
        month_num(e.get("typical_month")),
        e["name"].lower(),
    ))
    rows = [annual_row(e) for e in ordered]
    n_2027 = sum(1 for e in events if str(e.get("edition")) == "2027")
    body = f"""
<div class="breadcrumb"><a href="index.html">Overview</a> / Annual events</div>
<p class="eyebrow">Category</p>
<h1>Annual events</h1>
<p class="lede">Traditions that return every year: parades, street fairs, festivals, races and cultural seasons.
{len(events)} entries are catalogued. {n_2027} already have official 2027 dates; the rest show the most recent confirmed
edition and state plainly when the next edition has not been published.</p>
<div class="callout warn">
  <strong>Dates are edition-specific.</strong> An annual event's month can shift with the lunar calendar, the last Sunday rule,
  or the organiser's permits. The Dates column always names the edition the date belongs to. “2027 not published” means the
  organiser had not announced it on the page checked on {VERIFIED_ON}; it does not mean the event is cancelled.
</div>
{table("annual-tools", "annual-table", "Annual events, upcoming editions first",
       ["Event", "Dates (edition)", "Where", "Organizer", "Admission", "Next edition", "Source"],
       rows, "Show", [("all", "All entries"), ("upcoming", "Upcoming editions"), ("past", "Last confirmed edition")])}
"""
    return page("Annual events", "annual.html",
                "San Francisco annual parades, festivals, street fairs and races with edition-specific dates and official source links.",
                body)


def build_special(events):
    order = {"ongoing": 0, "upcoming": 1, "past": 2, "unknown": 3}

    def key(e):
        status = special_status(e)
        start = parse_date(e.get("start_date")) or dt.date(2999, 1, 1)
        end = parse_date(e.get("end_date")) or dt.date(2999, 1, 1)
        if status == "past":
            return (order[status], -end.toordinal(), e["name"].lower())
        return (order[status], start.toordinal(), e["name"].lower())

    rows = [special_row(e) for e in sorted(events, key=key)]
    counts = collections.Counter(special_status(e) for e in events)
    body = f"""
<div class="breadcrumb"><a href="index.html">Overview</a> / Special events</div>
<p class="eyebrow">Category</p>
<h1>Special &amp; one-time events</h1>
<p class="lede">Dated, limited-run events: museum exhibitions, opera and orchestra runs, conventions, one-off markets and civic
gatherings. {counts['upcoming']} are upcoming, {counts['ongoing']} are on now and {counts['past']} have already finished at the
verification date. Finished events stay listed so the catalogue is a complete record.</p>
<div class="callout">
  <strong>Status is calculated against {VERIFIED_ON}.</strong> “On now” means the run spans the verification date.
  “Not announced” means the organiser's page carried no dates at all; those rows are also on
  <a href="flagged.html">Flagged for Review</a>.
</div>
{table("special-tools", "special-table", "Special and one-time events",
       ["Event", "Dates", "Status", "Type", "Where", "Organizer", "Source"],
       rows, "Status", [("all", "All statuses"), ("ongoing", "On now"), ("upcoming", "Upcoming"), ("past", "Past"), ("unknown", "Not announced")])}
"""
    return page("Special & one-time events", "special.html",
                "Dated San Francisco exhibitions, performances, conventions and one-off events with official source links.",
                body)


def build_sources(sources, events):
    by_url = collections.defaultdict(list)
    for e in events:
        by_url[e["source_url"]].append(e)

    rows = []
    for s in sorted(sources, key=lambda s: (s["type"], urlparse(s["url"]).netloc)):
        used = by_url.get(s["url"], [])
        ids = ", ".join(e["id"] for e in used)
        rows.append(f"""<tr>
  <td class="event"><a href="{esc(s['url'])}" target="_blank" rel="noopener">{esc(s['title'])}</a>
    <span class="sub">{esc(s['url'])}</span></td>
  <td>{esc(s['type'])}</td>
  <td>{len(used)}</td>
  <td>{esc(ids) or '<span class="small">registry only</span>'}</td>
  <td>{esc(s['accessed'])}</td>
</tr>""")
    counts = collections.Counter(s["type"] for s in sources)
    body = f"""
<div class="breadcrumb"><a href="index.html">Overview</a> / Sources</div>
<p class="eyebrow">Verification</p>
<h1>Source registry</h1>
<p class="lede">Every page below was opened during this session. Nothing in the catalogue is sourced from Wikipedia, a
ticketing reseller, a social post or a “best events” blog. {len(sources)} official pages are registered:
{counts['government']} government, {counts['official organizer']} organiser and {counts['official venue']} venue pages.</p>
<div class="callout">
  <strong>Official means:</strong> a San Francisco city department or agency (sf.gov, sfmta.com, sfenvironment.org), the
  organisation that produces the event, or the venue that hosts it. A page is only accepted if the specific claim
  (date, cadence, place or price) appears on that page.
</div>
<table class="data" id="source-table">
  <caption>Official sources used, with the event IDs they support</caption>
  <thead><tr><th scope="col">Source page</th><th scope="col">Type</th><th scope="col">Rows</th><th scope="col">Event IDs</th><th scope="col">Accessed</th></tr></thead>
  <tbody>
{''.join(rows)}
  </tbody>
</table>
<p class="small">Pages that failed, redirected to unrelated content or were parked are documented on
<a href="flagged.html">Flagged for Review</a> and are not counted as sources.</p>
<p class="small"><a href="data/review.csv">Download the review sheet (CSV)</a> — one line per row with its dates, venue,
unverified fields and the exact official URL checked. Intended for line-by-line manual review.</p>
"""
    return page("Source registry", "sources.html",
                "Registry of every government, organiser and venue page used to verify the San Francisco events catalogue.",
                body)


def build_flagged(events, flagged):
    unverified = [e for e in events if e.get("unverified_fields")]
    sorted_unverified = sorted(unverified, key=lambda e: (e["category"], e["id"]))
    urows = []
    for e in sorted_unverified:
        page_name = {"weekly": "weekly.html", "monthly": "weekly.html", "annual": "annual.html", "special": "special.html"}[e["category"]]
        fields = ", ".join(f.replace("_", " ") for f in e["unverified_fields"])
        urows.append(f"""<tr>
  <td><a href="{page_name}#{e['id']}">{esc(e['name'])}</a><span class="sub">{e['id']} · {esc(e['category'])}</span></td>
  <td>{esc(fields)}</td>
  <td class="src">{source_link(e)}<span class="type">{esc(e.get('source_type'))}</span></td>
</tr>""")

    frows = []
    for item in flagged:
        frows.append(f"""<tr id="{item['id']}" data-bucket="{esc(item['kind'])}" data-search="{esc((item['item'] + ' ' + item['kind'] + ' ' + item['issue']).lower())}">
  <td>{esc(item['id'])}</td>
  <td>{esc(item['kind'])}</td>
  <td class="event"><span class="name">{esc(item['item'])}</span><span class="sub">{esc(item.get('related_event')) or '—'}</span></td>
  <td>{esc(item['issue'])}</td>
  <td class="src"><a href="{esc(item['evidence_url'])}" target="_blank" rel="noopener">{esc(urlparse(item['evidence_url']).netloc.replace('www.', ''))}</a></td>
  <td>{esc(item['action'])}</td>
</tr>""")

    counts = collections.Counter(i["kind"] for i in flagged)
    body = f"""
<div class="breadcrumb"><a href="index.html">Overview</a> / Flagged for Review</div>
<p class="eyebrow">Quality control</p>
<h1>Flagged for Review</h1>
<p class="lede">This page is deliberately public. It lists every row with a value that could not be confirmed, every source
irregularity found while verifying, and every scope decision that removed an event from the tables. Nothing here blocks
publication; it is the audit trail for a manual review.</p>

<div class="kpis">
  <div class="kpi"><div class="num">{len(unverified)}</div><div class="label">Rows with unverified fields</div></div>
  <div class="kpi"><div class="num">{len(flagged)}</div><div class="label">Review notes</div></div>
  <div class="kpi"><div class="num">{counts['source unavailable'] + counts['domain hijack'] + counts['domain parked'] + counts['broken official page']}</div><div class="label">Broken or hijacked official pages</div></div>
  <div class="kpi"><div class="num">{counts['data conflict'] + counts['date inconsistency'] + counts['date check']}</div><div class="label">Conflicts / date checks</div></div>
</div>

<h2>1. Rows with unverified fields</h2>
<p class="section-note">These rows are published with the affected fields left blank. Open the official source to see what it does
and does not state. Field names are the JSON keys in the underlying data.</p>
<table class="data" id="unverified-table">
  <caption>Published rows carrying at least one blank, unconfirmed field</caption>
  <thead><tr><th scope="col">Event</th><th scope="col">Unverified fields</th><th scope="col">Official source checked</th></tr></thead>
  <tbody>
{''.join(urows) if urows else '<tr><td colspan="3">None.</td></tr>'}
  </tbody>
</table>

<h2>2. Source and data irregularities</h2>
<p class="section-note">Each note names the page that was checked and the action needed. “Source unavailable” entries were
excluded from the tables rather than guessed.</p>
<div class="table-tools" data-table="flag-table">
  <label for="flag-search">Search</label>
  <input id="flag-search" type="search" placeholder="Domain, event, issue…" autocomplete="off">
  <label for="flag-filter">Kind</label>
  <select id="flag-filter">
    <option value="all">All kinds</option>
    {''.join(f'<option value="{esc(k)}">{esc(k)}</option>' for k in sorted(counts))}
  </select>
  <span class="result" aria-live="polite"></span>
</div>
<div class="table-wrap">
<table class="data" id="flag-table">
  <caption>Review register</caption>
  <thead><tr><th scope="col">ID</th><th scope="col">Kind</th><th scope="col">Item</th><th scope="col">Issue</th><th scope="col">Source checked</th><th scope="col">Action</th></tr></thead>
  <tbody>
{''.join(frows)}
  </tbody>
</table>
</div>

<h2>3. What happens next</h2>
<ul class="clean">
  <li><strong>Nothing is hidden.</strong> Unverified rows stay in the category tables with blank values and an amber badge.</li>
  <li><strong>Corrections are cheap.</strong> Each row carries a stable ID (for example <code>w-002</code> or <code>a-010</code>) that can be cited in a review request.</li>
  <li><strong>Re-verification date:</strong> all rows were checked on {VERIFIED_ON}. Seasonal and permit-based programmes should be re-checked before the next season.</li>
</ul>
"""
    return page("Flagged for Review", "flagged.html",
                "Audit trail: unverified fields, broken or hijacked official pages, data conflicts and scope exclusions for the San Francisco events catalogue.",
                body)


def build_analysis(events, sources, flagged):
    cat = collections.Counter(e["category"] for e in events)
    status = collections.Counter(special_status(e) for e in events if e["category"] == "special")
    src_types = collections.Counter(e["source_type"] for e in events)
    unverified = [e for e in events if e.get("unverified_fields")]
    n_2027 = sum(1 for e in events if e["category"] == "annual" and str(e.get("edition")) == "2027")
    n_annual = sum(1 for e in events if e["category"] == "annual")

    day_counts = collections.Counter()
    for e in events:
        if e["category"] in ("weekly", "monthly"):
            for d in weekday_hits(e.get("cadence", "") + " " + e.get("schedule", "")):
                day_counts[d] += 1
    day_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    day_rows = "".join(
        f"<tr><td>{d}</td><td>{day_counts.get(d, 0)}</td><td>{'█' * day_counts.get(d, 0)}</td></tr>"
        for d in day_order
    )

    hood_counts = collections.Counter()
    for e in events:
        for h in hoods(e.get("neighborhood")):
            hood_counts[h] += 1
    top_hoods = hood_counts.most_common(12)
    hood_rows = "".join(
        f"<tr><td>{esc(h)}</td><td>{c}</td><td>{'█' * c}</td></tr>" for h, c in top_hoods
    )

    src_rows = "".join(
        f"<tr><td>{esc(t)}</td><td>{c}</td><td>{dict(src_types)[t] / len(events) * 100:.0f}%</td></tr>"
        for t, c in src_types.most_common()
    )

    top_day, top_day_n = day_counts.most_common(1)[0]
    second_day, second_day_n = day_counts.most_common(2)[1]
    kind_counts = collections.Counter(i["kind"] for i in flagged)
    broken = sum(kind_counts[k] for k in ("source unavailable", "domain hijack", "domain parked", "broken official page"))
    conflicts = sum(kind_counts[k] for k in ("data conflict", "date inconsistency", "date check"))

    body = f"""
<div class="breadcrumb"><a href="index.html">Overview</a> / Analysis</div>
<p class="eyebrow">Method &amp; findings</p>
<h1>How this catalogue was built — and what it shows</h1>
<p class="lede">The goal was a source-linked inventory, not a list of guesses. Every entry was opened, read and matched to a
specific official page on {VERIFIED_ON}. This page records the method, the coverage, the patterns in the data and the limits
that a reader should know about.</p>

<h2>Method</h2>
<ol class="clean">
  <li><strong>Define the boundary.</strong> Only events physically inside the City and County of San Francisco. Daly City, Oakland and Santa Clara events are excluded even when they are marketed as “SF Bay Area”.</li>
  <li><strong>Find the producer.</strong> For each candidate event, locate the page of the organisation that runs it, or the venue that hosts it. Government listings (sf.gov, SFMTA, SF Environment) are used for city-run programmes and street closures.</li>
  <li><strong>Read the claim on the page.</strong> A date, cadence, time, place or price is recorded only if that page states it. Search-result snippets are treated as leads, not evidence.</li>
  <li><strong>Record the edition.</strong> Annual dates are tied to the specific edition (2026 or 2027). A future date is never inferred from “usually the third weekend”.</li>
  <li><strong>Leave gaps visible.</strong> If the official page is silent, the field is blank, the row gets an <span class="badge unverified">unverified</span> badge and the gap appears on <a href="flagged.html">Flagged for Review</a>.</li>
  <li><strong>Publish the audit trail.</strong> Broken domains, stale pages and conflicting hours are logged with the URL checked and the action taken.</li>
</ol>

<h2>Coverage at a glance</h2>
<div class="table-wrap">
<table class="data" id="coverage-table">
  <caption>What the catalogue contains</caption>
  <thead><tr><th scope="col">Measure</th><th scope="col">Count</th><th scope="col">Note</th></tr></thead>
  <tbody>
    <tr><td>Total catalogue entries</td><td>{len(events)}</td><td>All in San Francisco</td></tr>
    <tr><td>Recurring weekly</td><td>{cat['weekly']}</td><td>Markets, late nights, weekly programmes</td></tr>
    <tr><td>Recurring monthly</td><td>{cat['monthly']}</td><td>First/last/third weekday programmes</td></tr>
    <tr><td>Annual</td><td>{cat['annual']}</td><td>Edition-specific dates</td></tr>
    <tr><td>Special / one-time</td><td>{cat['special']}</td><td>Exhibitions, runs, conventions, one-offs</td></tr>
    <tr><td>Annual rows already carrying 2027 dates</td><td>{n_2027} of {n_annual}</td><td>The rest show the last confirmed edition</td></tr>
    <tr><td>Rows with at least one unverified field</td><td>{len(unverified)}</td><td>{len(unverified) / len(events) * 100:.0f}% of entries; all listed on Flagged for Review</td></tr>
    <tr><td>Official pages in the registry</td><td>{len(sources)}</td><td>Government, organiser and venue pages</td></tr>
    <tr><td>Review notes</td><td>{len(flagged)}</td><td>Broken sources, conflicts, scope decisions</td></tr>
  </tbody>
</table>
</div>

<h2>What the data shows</h2>
<ul class="clean">
  <li><strong>Recurring life is concentrated at the weekend.</strong> {top_day} is the most frequently cited day in the recurring set ({top_day_n} rows), followed by {second_day} ({second_day_n} rows). The weekly table shows the full spread.</li>
  <li><strong>Farmers markets are the backbone.</strong> The catalogue records markets on Tuesday, Wednesday, Thursday, Saturday and Sunday; no Monday or Friday farmers market could be verified. Saturday and Sunday carry the most options.</li>
  <li><strong>Annual events cluster from spring to autumn.</strong> Cherry Blossom, Bay to Breakers, Pride, Fillmore Jazz, the Marathon, Pistahan, Nihonmachi, Folsom, Castro and Hardly Strictly span April to October.</li>
  <li><strong>2027 planning is already possible for {n_2027} annual events.</strong> Organisers including the Chinese New Year Parade, Cherry Blossom Festival, Bay to Breakers, SF Pride, Fillmore Jazz and the Castro Street Fair have published next-year dates.</li>
  <li><strong>Special events are mostly runs, not single nights.</strong> {status['ongoing']} are on now and {status['upcoming']} are upcoming at the verification date; the rest are recorded past editions.</li>
  <li><strong>Verification quality is uneven across official sources.</strong> {broken} official pages were unreachable, hijacked, parked or broken; {conflicts} date or data conflicts needed adjudication. These are logged rather than smoothed over.</li>
</ul>

<h2>Recurring events by weekday</h2>
<p class="section-note">A row is counted once for each weekday named in its cadence or schedule. “1st &amp; 3rd Fridays” counts once for Friday.</p>
<div class="table-wrap">
<table class="data" id="weekday-table">
  <caption>Weekday coverage in the recurring tables</caption>
  <thead><tr><th scope="col">Day</th><th scope="col">Rows</th><th scope="col">Relative coverage</th></tr></thead>
  <tbody>{day_rows}</tbody>
</table>
</div>

<h2>Neighbourhood coverage</h2>
<p class="section-note">Neighbourhoods are recorded as published by the organiser. Multi-neighbourhood routes are counted once for each area named.</p>
<div class="table-wrap">
<table class="data" id="hood-table">
  <caption>Most frequently represented neighbourhoods</caption>
  <thead><tr><th scope="col">Neighbourhood</th><th scope="col">Rows</th><th scope="col">Relative coverage</th></tr></thead>
  <tbody>{hood_rows}</tbody>
</table>
</div>

<h2>Source mix</h2>
<div class="table-wrap">
<table class="data" id="source-mix">
  <caption>Which type of official page confirms each row</caption>
  <thead><tr><th scope="col">Source type</th><th scope="col">Rows</th><th scope="col">Share</th></tr></thead>
  <tbody>{src_rows}</tbody>
</table>
</div>

<h2>Limitations</h2>
<ul class="clean">
  <li><strong>Not literally every event.</strong> A city the size of San Francisco has hundreds of venue-level concerts, gallery openings and private ticketed shows each month. This catalogue covers public recurring programmes, the major annual civic calendar, and dated exhibitions, runs and conventions that were verifiable on an official page. It is comprehensive for those classes, not for every individual gig.</li>
  <li><strong>Official pages go stale.</strong> Several official sites still displayed 2025 dates or outdated hours. Where that happened, the date was left blank and the staleness logged.</li>
  <li><strong>Permits expire.</strong> Monthly street closures are permitted through specific dates (see SFMTA notes). A recurring row can stop recurring without the organiser updating the page.</li>
  <li><strong>Status is a snapshot.</strong> “On now”, “upcoming” and “past” are calculated against {VERIFIED_ON} and will drift as time passes. The dates are the durable information.</li>
  <li><strong>Ticketing and capacity are out of scope.</strong> A row marked “Ticketed” only means the official source describes paid admission; it does not guarantee availability.</li>
</ul>

<div class="callout warn">
  <strong>Review workflow:</strong> unverified fields and source irregularities are published on
  <a href="flagged.html">Flagged for Review</a> with stable row IDs and source links. Nothing is silently corrected by
  inference. If you spot a change, cite the row ID and the official URL.
</div>
"""
    return page("Method & analysis", "analysis.html",
                "Method, coverage counts, findings and limitations for the verified San Francisco events catalogue.",
                body)


def main():
    weekly = load("weekly.json")["events"]
    annual = load("annual.json")["events"]
    special = load("special.json")["events"]
    flagged = load("flagged.json")["items"]
    sources = load("sources.json")["sources"]
    events = weekly + annual + special

    pages = {
        "index.html": build_index(events, sources, flagged),
        "weekly.html": build_weekly(weekly),
        "annual.html": build_annual(annual),
        "special.html": build_special(special),
        "sources.html": build_sources(sources, events),
        "flagged.html": build_flagged(events, flagged),
        "analysis.html": build_analysis(events, sources, flagged),
    }
    for name, content in pages.items():
        with open(os.path.join(ROOT, name), "w", encoding="utf-8") as fh:
            fh.write(content)

    meta = {
        "site": SITE_NAME,
        "verified_on": VERIFIED_ON,
        "generated_on": VERIFIED_ON,
        "counts": {
            "total": len(events),
            "weekly": sum(1 for e in events if e["category"] == "weekly"),
            "monthly": sum(1 for e in events if e["category"] == "monthly"),
            "annual": len(annual),
            "special": len(special),
            "flagged_rows": len(flagged),
            "unverified_rows": sum(1 for e in events if e.get("unverified_fields")),
            "sources": len(sources),
        },
        "pages": sorted(pages),
        "review_sheet": "data/review.csv",
    }
    import csv
    with open(os.path.join(ROOT, "data", "review.csv"), "w", encoding="utf-8", newline="") as fh:
        writer = csv.writer(fh)
        writer.writerow(["id", "category", "name", "cadence", "dates", "display_dates", "venue",
                         "neighborhood", "organizer", "admission", "source_url", "source_type",
                         "unverified_fields", "notes"])
        for e in events:
            writer.writerow([e["id"], e["category"], e["name"], e.get("cadence", ""),
                             e.get("dates", "") or e.get("start_date", ""),
                             e.get("display_dates", ""), e.get("venue", ""),
                             e.get("neighborhood", ""), e.get("organizer", ""),
                             e.get("admission", ""), e["source_url"], e["source_type"],
                             ";".join(e.get("unverified_fields", [])), e.get("notes", "")])

    with open(os.path.join(ROOT, "data", "meta.json"), "w", encoding="utf-8") as fh:
        json.dump(meta, fh, indent=2)
        fh.write("\n")
    print("built:", ", ".join(sorted(pages)))
    print(json.dumps(meta["counts"], indent=2))


if __name__ == "__main__":
    main()
