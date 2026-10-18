#!/usr/bin/env python3
"""Second batch of `arena-fe7c710c` cost corrections (2026-10-18).

Four more rows carried a "Free" cost that the row's own official source does
not publish. Each source was fetched and read on 2026-10-18:

* ``www.ferrybuildingmarketplace.com`` home page — describes shops, the food
  hall and events; states no entry price.
* ``presidio.gov`` Presidio Visitor Center page — gives hours, address and
  amenities; states no admission price.
* ``www.sfmta.com/projects/shared-spaces`` — the Castro Art Mart entry is a
  street-closure permit listing (Noe Street, 1st Sundays, 11:30 a.m.-9:30 p.m.,
  permitted through May 2, 2027); it states no admission price.
* ``www.moonfestival.org`` — the page publishes "Cost: FREE!" for the Autumn
  Moon Festival (which already has its own row) but says nothing about the
  Chinatown streets as a standing attraction.

Under the project's rule the four cost cells are blanked and the rows marked
``unverified`` rather than being presented as free.

Run from the repository root::

    python3 audit/apply_corrections2_fe7c710c.py
"""

from __future__ import annotations

import io
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from apply_corrections_fe7c710c import patch_row  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EVENTS_PY = os.path.join(ROOT, "data", "events.py")

FIXES = {
    "rec-ferry-building-marketplace": {
        "cost": "",
        "status": "unverified",
        "notes": (
            "Re-checked 2026-10-18 by session arena-fe7c710c. The Marketplace's own home "
            "page describes its shops, restaurants and events programme and publishes no "
            "admission price for the building, so the 'Free entry' cell has been blanked "
            "and the row marked unverified rather than inferred. See Flagged for Review."
        ),
    },
    "art-presidio-museum": {
        "cost": "",
        "status": "unverified",
        "notes": (
            "Corrected 2026-10-18 by session arena-8e8e24dc: the row previously listed "
            "'104 Montgomery Street', which is the separate Walt Disney Family Museum (its "
            "own row). The Trust's visitor-center page gives 210 Lincoln Boulevard and daily "
            "10-5 hours. Re-checked the same day by session arena-fe7c710c: that page "
            "publishes no admission price, so the 'Free' cell has been blanked and the row "
            "marked unverified rather than inferred. See Flagged for Review."
        ),
    },
    "mkt-sf-chinatown-food": {
        "cost": "",
        "status": "unverified",
        "notes": (
            "Re-checked 2026-10-18 by session arena-fe7c710c. The cited page publishes "
            "'Cost: FREE!' for the Chinatown Autumn Moon Festival, which has its own row, "
            "but says nothing about the Chinatown shopping streets as a standing attraction, "
            "so the 'Free' cell has been blanked and the row marked unverified rather than "
            "inferred. See Flagged for Review."
        ),
    },
}

NEW_FLAG = '''    dict(
        id="flag-four-more-free-claims-unpublished",
        title="Four more 'Free' cost cells blanked — the official pages publish no price",
        detail="The Ferry Building Marketplace home page, the Presidio Visitor Center page, SFMTA's Shared Spaces permit list (Castro Art Mart) and the Autumn Moon Festival page (cited for the Chinatown shopping-streets row) were each fetched on 2026-10-18. None of them states an admission price for the row it supports, so the four 'Free' cost cells have been blanked and the rows marked unverified. The Autumn Moon Festival itself keeps its free cost cell, because its own page publishes 'Cost: FREE!'.",
        source_name="SFMTA — Shared Spaces (street-closure permits)",
        source_url="https://www.sfmta.com/projects/shared-spaces",
        action="Ask each venue or sponsor whether admission is charged, and record the answer here."),
'''


# ``x-w-014`` (Castro Art Mart) comes from the preserved parallel tranche, so it
# is corrected through merge_parallel.py's override table instead.
MERGE_PY = os.path.join(ROOT, "scripts", "merge_parallel.py")
PARALLEL_FIX = {
    "w-014": (
        "https://www.sfmta.com/projects/shared-spaces",
        "",
        "Re-checked 2026-10-18 by session arena-fe7c710c: the SFMTA Shared Spaces page "
        "publishes the street-closure permit for Noe Street (1st Sundays, 11:30 a.m. to "
        "9:30 p.m., permitted through May 2, 2027, sponsor Artyhood) but no admission price, "
        "so the 'Free entry' cell has been blanked and the row marked unverified rather than "
        "inferred. See Flagged for Review.",
    ),
}


def apply_parallel_fix() -> None:
    src = io.open(MERGE_PY, encoding="utf-8").read()
    start = src.find("FIELD_OVERRIDES = {")
    if start != -1 and '"w-014"' in src[start:src.find("\n}\n", start)]:
        return
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
    source_url, cost, note = PARALLEL_FIX["w-014"]
    block = (
        '    "w-014": {\n'
        f'        "source_url": "{source_url}",\n'
        f'        "cost": "{cost}",\n'
        '        "_force_unverified": True,\n'
        f'        "_override_note": "{note}",\n'
        '    },\n'
    )
    start = src.find("FIELD_OVERRIDES = {")
    end = src.find("\n}\n", start)
    src = src[:end + 1] + block + src[end + 1:]
    io.open(MERGE_PY, "w", encoding="utf-8").write(src)
    print("added w-014 override")


def main() -> int:
    src = io.open(EVENTS_PY, encoding="utf-8").read()
    if "flag-four-more-free-claims-unpublished" in src:
        print("already applied")
        return 0
    for rid, updates in FIXES.items():
        src = patch_row(src, rid, updates)
    anchor = "FLAGGED = [\n"
    idx = src.find(anchor)
    if idx == -1:
        raise SystemExit("FLAGGED list not found")
    src = src[: idx + len(anchor)] + NEW_FLAG + src[idx + len(anchor):]
    io.open(EVENTS_PY, "w", encoding="utf-8").write(src)
    apply_parallel_fix()
    print(f"applied {len(FIXES)} cost corrections, 1 parallel override and 1 review item")
    return 0


if __name__ == "__main__":
    sys.exit(main())
