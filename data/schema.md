# Data schema

All data files are UTF-8 JSON with a top-level `category`, `verified_on` and `events` array.

## Common fields (every row)

| Field | Required | Notes |
|-------|----------|-------|
| `id` | yes | Stable slug, e.g. `w-001`, `a-014`, `s-003` |
| `name` | yes | Event name as used by the source |
| `category` | yes | `weekly`, `monthly`, `annual`, `special` |
| `cadence` | yes | Human-readable cadence confirmed by source |
| `schedule` | yes for recurring | Day/time pattern confirmed by source; may be blank only when `schedule` (or a sub-attribute) is listed in `unverified_fields` |
| `venue` | yes | Venue or public space |
| `neighborhood` | yes | SF neighbourhood / district |
| `address` | no | Leave blank if not confirmed |
| `organizer` | yes | Producing organisation |
| `admission` | no | Leave blank if not confirmed; otherwise `Free`, `Free entry`, `Ticketed`, `Free / ticketed` |
| `source_url` | yes | Official government / organiser / venue page actually opened during this session |
| `source_title` | yes | Page title |
| `source_type` | yes | `government`, `official organizer`, `official venue` |
| `verified_on` | yes | `YYYY-MM-DD` |
| `unverified_fields` | yes | Array of field names deliberately left blank; empty array = fully verified. A sub-attribute may be named with dot notation, e.g. `schedule.start_time` or `dates.next_edition`; the root field must still be a schema field |
| `notes` | no | Short factual note; no inference |

## Recurring rows (`weekly.json`, `annual.json`)

| Field | Notes |
|-------|-------|
| `season` | e.g. `Year-round`, `May–October`, `2026 edition` |
| `edition` | For annual: the edition the dates belong to (`2026`), else blank |
| `dates` | For annual: confirmed dates of that edition, semicolon-separated ISO dates, e.g. `2026-02-21`; blank if not published |
| `next_edition_status` | Factual status observed on the official page, e.g. `2027 date not published as of 2026-10-18`; blank otherwise |

## Special rows (`special.json`)

| Field | Notes |
|-------|-------|
| `start_date`, `end_date` | ISO dates only when confirmed on the official page; blank otherwise |
| `date_status` | `confirmed` or `not announced` (verified negative) |
| `type` | `exhibition`, `performance`, `convention`, `festival`, `civic`, `sports` |

## Validation rules enforced by `tools/validate.py`

1. Required fields present and non-empty (except fields listed in `unverified_fields`).
2. `source_url` uses `https://` and belongs to the official-source allowlist in `data/sources.json`.
3. `source_url` is not a search, social, aggregator, ticketing or Wikipedia URL.
4. `unverified_fields` only names optional fields from the schema (`field` or `field.subfield`).
5. IDs unique; categories match the file.
6. Every event with `unverified_fields` appears on `flagged.html` (build checks this).
7. Internal links in generated HTML resolve to a generated file.
