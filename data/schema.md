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

## Legacy per-session schema and merged-site validation

The JSON files above preserve the earlier research tranche. The published union is `data/events.json`, built from `data/events.py` and converted rows from the preserved per-session files. `tools/validate.py` validates the merged published rows, their source links, table alignment, and local site links. It does not fetch official pages or re-confirm mutable event facts.

### Validation rules enforced by `tools/validate.py`

1. The `data/events.json` union matches the source files and merge transform.
2. Canonical source URLs are HTTPS, avoid the explicit social/search/aggregator blocklist, and are present on rendered event rows.
3. Canonical event IDs are unique; groups, categories, and statuses use the expected values.
4. Each unverified canonical row is directly addressable on `flagged.html`.
5. Every review-register source link appears on the review page; internal links and local HTML anchors resolve.
6. Every listing row has the expected nine table cells.
