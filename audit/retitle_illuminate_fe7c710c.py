#!/usr/bin/env python3
"""Give every dated Illuminate LIVE row a date-qualified title.

The catalogue lists one row per concert date, so a series name on its own
("Civic Center Soundtrack (Illuminate LIVE)") is ambiguous once the series
runs more than once. Every dated row now carries the date it lists, matching
the "Crucial Reggae Sundays, October 25 (Illuminate LIVE)" wording that was
already used in the dataset. No date, time, venue or price is changed here.
"""

from __future__ import annotations

import io
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EVENTS_PY = os.path.join(ROOT, "data", "events.py")

# id -> (new title, new source name)
RETITLE = {
    "spc-illuminate-reggae-2026-10-18": ("Crucial Reggae Sundays, October 18 (Illuminate LIVE)", "Illuminate — Crucial Reggae Sundays, October 18"),
    "spc-illuminate-ccs-2026-10-20": ("Civic Center Soundtrack, October 20 (Illuminate LIVE)", "Illuminate — Civic Center Soundtrack, October 20"),
    "spc-illuminate-midweek-2026-10-21": ("Midweek Melodies, October 21 (Illuminate LIVE)", "Illuminate — Midweek Melodies, October 21"),
    "spc-illuminate-happyhour-2026-10-23": ("Friday Happy Hour, October 23 (Illuminate LIVE)", "Illuminate — Friday Happy Hour, October 23"),
    "spc-illuminate-ccs-2026-10-22": ("Civic Center Soundtrack, October 22 (Illuminate LIVE)", "Illuminate — Civic Center Soundtrack, October 22"),
    "spc-illuminate-ccs-2026-10-27": ("Civic Center Soundtrack, October 27 (Illuminate LIVE)", "Illuminate — Civic Center Soundtrack, October 27"),
    "spc-illuminate-midweek-2026-10-28": ("Midweek Melodies, October 28 (Illuminate LIVE)", "Illuminate — Midweek Melodies, October 28"),
    "spc-illuminate-ccs-2026-10-29": ("Civic Center Soundtrack, October 29 (Illuminate LIVE)", "Illuminate — Civic Center Soundtrack, October 29"),
    "spc-illuminate-happyhour-2026-10-30": ("Friday Happy Hour, October 30 (Illuminate LIVE)", "Illuminate — Friday Happy Hour, October 30"),
    "spc-illuminate-reggae-2026-11-01": ("Crucial Reggae Sundays, November 1 (Illuminate LIVE)", "Illuminate — Crucial Reggae Sundays, November 1"),
    "spc-illuminate-mtb-2026-11-04": ("Market to Bandshell, November 4 (Illuminate LIVE)", "Illuminate — Market to Bandshell, November 4"),
    "spc-illuminate-happyhour-2026-11-06": ("Friday Happy Hour, November 6 (Illuminate LIVE)", "Illuminate — Friday Happy Hour, November 6"),
    "spc-illuminate-saturday-2026-11-07": ("Saturday at the Bandshell, November 7 (Illuminate LIVE)", "Illuminate — Saturday at the Bandshell, November 7"),
    "spc-illuminate-reggae-2026-11-08": ("Crucial Reggae Sundays, November 8 (Illuminate LIVE)", "Illuminate — Crucial Reggae Sundays, November 8"),
    "spc-illuminate-midweek-2026-11-11": ("Midweek Melodies, November 11 (Illuminate LIVE)", "Illuminate — Midweek Melodies, November 11"),
    "spc-illuminate-happyhour-2026-11-13": ("Friday Happy Hour, November 13 (Illuminate LIVE)", "Illuminate — Friday Happy Hour, November 13"),
    "spc-illuminate-otisology-2026-11-15": ("Nick Otis Presents Otisology, November 15 (Illuminate LIVE)", "Illuminate — Nick Otis Presents Otisology, November 15"),
}


def main() -> int:
    src = io.open(EVENTS_PY, encoding="utf-8").read()
    changed = 0
    for rid, (title, source_name) in RETITLE.items():
        marker = f'id="{rid}", title="'
        idx = src.find(marker)
        if idx == -1:
            print(f"skip (not found): {rid}")
            continue
        end = src.find('",\n', idx)
        old_title = src[idx + len(marker):end]
        if old_title == title:
            continue
        src = src[:idx + len(marker)] + title + src[end:]
        # the source_name line follows the title within the same dict
        sn_marker = f'source_name="'
        sn_idx = src.find(sn_marker, idx)
        sn_end = src.find('",\n', sn_idx)
        src = src[:sn_idx + len(sn_marker)] + source_name + src[sn_end:]
        changed += 1
    io.open(EVENTS_PY, "w", encoding="utf-8").write(src)
    print(f"retitled {changed} rows")
    return 0


if __name__ == "__main__":
    sys.exit(main())
