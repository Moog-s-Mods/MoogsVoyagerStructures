#!/usr/bin/env python3
"""
Batch-patches loot tables onto all empty/hardcoded containers.

NOTE: This script's `classify()` function contains MVS-specific business logic
(cathedral -> cathedral_common, mineshaft -> mineshaft/common, etc.). If you copy
this to another mod, you'll need to rewrite `classify()` for that mod's
structure naming conventions.

Run from project root: python scripts/batch_patch_loot.py
"""
from pathlib import Path

from _paths import MOD_ID, STRUCTURES_DIR
from fix_loot import scan_containers, patch_nbt


def classify(rel: str, containers: list) -> dict:
    """Return {(x,y,z): loot_table} for every container in the file."""
    patches = {}

    def is_path(*parts):
        return all(p in rel for p in parts)

    def block_type(x, y, z):
        for wt, cx, cy, cz, bid in containers:
            if (cx, cy, cz) == (x, y, z):
                return bid
        return ""

    # ── wells ─────────────────────────────────────────────────────────────
    if "small_tower_well" in rel:
        for _, x, y, z, _ in containers:
            patches[(x, y, z)] = f"{MOD_ID}:empty"
        return patches

    # ── horse pen ─────────────────────────────────────────────────────────
    if rel == "horse_pen.nbt":
        for _, x, y, z, _ in containers:
            patches[(x, y, z)] = f"{MOD_ID}:empty"
        return patches

    # ── windmill ──────────────────────────────────────────────────────────
    if "small_windmill" in rel:
        for _, x, y, z, _ in containers:
            patches[(x, y, z)] = f"{MOD_ID}:empty"
        return patches

    # ── cathedral ─────────────────────────────────────────────────────────
    if "cathedral" in rel:
        for _, x, y, z, _ in containers:
            patches[(x, y, z)] = f"{MOD_ID}:cathedral_common"
        return patches

    # ── large warped tower ────────────────────────────────────────────────
    if "large_warped_tower" in rel:
        for _, x, y, z, _ in containers:
            patches[(x, y, z)] = f"{MOD_ID}:houses_uncommon"
        return patches

    # ── red tower ─────────────────────────────────────────────────────────
    if "red_tower" in rel:
        for _, x, y, z, _ in containers:
            patches[(x, y, z)] = f"{MOD_ID}:empty"
        return patches

    # ── desert house ──────────────────────────────────────────────────────
    if "desert_house" in rel:
        for _, x, y, z, _ in containers:
            patches[(x, y, z)] = f"{MOD_ID}:houses_desert"
        return patches

    # ── outhouse ──────────────────────────────────────────────────────────
    if "out_house" in rel:
        for _, x, y, z, _ in containers:
            patches[(x, y, z)] = f"{MOD_ID}:houses_common"
        return patches

    # ── houses ────────────────────────────────────────────────────────────
    HOUSE_FILES = {"barn", "house", "medium_igloo_1", "tall_house", "deepslate_house"}
    stem = Path(rel).stem
    if stem in HOUSE_FILES or (rel.startswith("houses/") and stem in HOUSE_FILES):
        for _, x, y, z, _ in containers:
            patches[(x, y, z)] = f"{MOD_ID}:houses_common"
        return patches

    # warped_house not in the explicit list → default (barrels=empty, chests=general)
    if "warped_house" in rel:
        for _, x, y, z, bid in containers:
            if bid == "minecraft:chest":
                patches[(x, y, z)] = f"{MOD_ID}:general"
            else:
                patches[(x, y, z)] = f"{MOD_ID}:empty"
        return patches

    # ── large carts ───────────────────────────────────────────────────────
    if rel.startswith("carts/") or "large_cart" in rel:
        for _, x, y, z, _ in containers:
            patches[(x, y, z)] = f"{MOD_ID}:large_carts"
        return patches

    # ── mineshaft ─────────────────────────────────────────────────────────
    if "mineshaft" in rel:
        barrels = [(x, y, z) for _, x, y, z, bid in containers if bid == "minecraft:barrel"]
        barrels_sorted = sorted(barrels)
        barrel_loot = {
            pos: (f"{MOD_ID}:mineshaft/common" if i % 10 == 0 else f"{MOD_ID}:empty")
            for i, pos in enumerate(barrels_sorted)
        }

        dead_end = "dead_end" in rel

        for _, x, y, z, bid in containers:
            if bid == "minecraft:barrel":
                patches[(x, y, z)] = barrel_loot[(x, y, z)]
            elif bid == "minecraft:trapped_chest":
                patches[(x, y, z)] = f"{MOD_ID}:mineshaft/rare"
            elif bid == "minecraft:chest":
                patches[(x, y, z)] = f"{MOD_ID}:mineshaft/uncommon" if dead_end else f"{MOD_ID}:mineshaft/common"
        return patches

    # ── oak pond ──────────────────────────────────────────────────────────
    if "small_oak_pond" in rel:
        for _, x, y, z, _ in containers:
            patches[(x, y, z)] = f"{MOD_ID}:pond"
        return patches

    # ── end scraps ────────────────────────────────────────────────────────
    if "end_scraps" in rel:
        for _, x, y, z, _ in containers:
            patches[(x, y, z)] = f"{MOD_ID}:end_scraps"
        return patches

    # ── campsites / mine campsites / statue ruins ─────────────────────────
    ABANDONED = {"campsite", "mine_with_campsite", "mine_with_campsite_lower",
                 "small_horse_campsite", "statue_ruins"}
    if stem in ABANDONED:
        for _, x, y, z, _ in containers:
            patches[(x, y, z)] = f"{MOD_ID}:abandoned"
        return patches

    # ── default ───────────────────────────────────────────────────────────
    for _, x, y, z, bid in containers:
        if bid == "minecraft:chest":
            patches[(x, y, z)] = f"{MOD_ID}:general"
        else:
            patches[(x, y, z)] = f"{MOD_ID}:empty"
    print(f"  [WARN] {rel} fell through to default - verify assignment")
    return patches


def main():
    print("Scanning structures...")
    warnings = scan_containers(STRUCTURES_DIR)

    if not warnings:
        print("No empty or hardcoded containers found!")
        return

    total_files = len(warnings)
    total_containers = sum(len(v) for v in warnings.values())
    print(f"Found {total_containers} container(s) across {total_files} file(s). Patching...\n")

    for rel, containers in sorted(warnings.items()):
        nbt_path = STRUCTURES_DIR / rel
        patches = classify(rel, containers)

        if len(patches) != len(containers):
            print(f"  [WARN] {rel}: {len(containers)} containers but {len(patches)} patches - some skipped?")

        saved = patch_nbt(nbt_path, patches)
        assignments = {}
        for pos, lt in patches.items():
            assignments.setdefault(lt, 0)
            assignments[lt] += 1
        summary = ", ".join(f"{c}x {lt}" for lt, c in sorted(assignments.items()))
        print(f"  {rel}: {saved} patched  [{summary}]")

    print("\nDone. Run the validator to confirm.")


if __name__ == "__main__":
    main()
