"""
Swap blocks that only exist in newer Minecraft versions out of the BASE-path
structure NBTs, so the base variants validate against the oldest supported
target. Newer blocks stay available via the version-folder variants
(structure/1_21_9/...) referenced by versioned template pools.

The swap map below is the single source of truth. For each palette entry whose
Name matches, the Name is rewritten and Properties are rebuilt to keep only the
properties that exist on the replacement block (or dropped entirely for the
air replacements). Everything is done through nbtlib so the length-prefixed NBT
strings stay valid -- never do raw byte replacement on these files.

This script is idempotent: re-running it finds nothing left to change in the
base paths and reports zero edits.

Two kinds of work, driven by the tables at the bottom:
  VERSION_THEN_SWAP -- base NBT still holds the new blocks and has no version
                       copy yet: copy the current NBT verbatim into
                       structure/1_21_9/<path>.nbt (the new-block variant),
                       then swap the base NBT down to old blocks. The matching
                       template pool is converted to a versioned element.
  SWAP_ONLY         -- structure is already versioned (1_21_9 copy + versioned
                       pool exist): only swap the base NBT; leave the version
                       copy and pool untouched.

Run from project root:  python scripts/fix_versioned_blocks.py
"""
import collections.abc
import json
import shutil

import nbtlib as nbt

from _paths import MOD_ID, STRUCTURES_DIR, TEMPLATE_POOL_DIR

# Version folder holding the new-block variants, and the range keys MVS already
# uses on azelea_house / oak_well / ruined_beacon. Kept identical on purpose.
VERSION_FOLDER = "1_21_9"
LOW_RANGE = "1.21-1.21.8"          # base (old-block) variant
NEW_RANGES = ["1.21.9-1.21.11", "26.1-26.1.2"]  # new-block variant


# Swap map: old block -> (new block, list of properties to keep). A keep-list of
# None means drop the block down to plain air (Name=minecraft:air, no Properties).
SWAP_MAP = {
    "minecraft:iron_chain":              ("minecraft:chain",               ["axis", "waterlogged"]),
    "minecraft:oxidized_lightning_rod":  ("minecraft:lightning_rod",       ["facing", "powered"]),
    "minecraft:weathered_lightning_rod": ("minecraft:lightning_rod",       ["facing", "powered"]),
    "minecraft:stripped_pale_oak_wood":  ("minecraft:stripped_birch_wood", ["axis"]),
    "minecraft:leaf_litter":             ("minecraft:air",                 None),
    "minecraft:dried_ghast":             ("minecraft:air",                 None),
}


def iter_palettes(root):
    """Yield every palette list in a structure NBT (single 'palette' or 'palettes')."""
    if "palette" in root:
        yield root["palette"]
    if "palettes" in root:
        for pal in root["palettes"]:
            yield pal


def swap_palette_entry(entry):
    """Rewrite one palette entry in place per SWAP_MAP. Returns True if changed."""
    name = str(entry.get("Name", ""))
    if name not in SWAP_MAP:
        return False

    new_name, keep_props = SWAP_MAP[name]
    entry["Name"] = nbt.String(new_name)

    if keep_props is None:
        # Air replacement: drop all block-state properties.
        if "Properties" in entry:
            del entry["Properties"]
        return True

    old_props = entry.get("Properties")
    if old_props is not None:
        kept = nbt.Compound()
        for key in keep_props:
            if key in old_props:
                kept[key] = old_props[key]
        if kept:
            entry["Properties"] = kept
        else:
            del entry["Properties"]
    return True


def swap_base_nbt(nbt_path):
    """Apply the swap map to a base NBT in place. Returns count of entries changed."""
    root = nbt.load(str(nbt_path))
    changed = 0
    for pal in iter_palettes(root):
        for entry in pal:
            if swap_palette_entry(entry):
                changed += 1
    if changed:
        root.save(str(nbt_path))
    return changed


def make_version_copy(base_rel):
    """Copy structure/<base_rel>.nbt verbatim to structure/<VERSION_FOLDER>/<base_rel>.nbt.

    Skips the copy if the version file already exists (idempotent / never clobbers
    a hand-made new-block variant)."""
    src = STRUCTURES_DIR / f"{base_rel}.nbt"
    dst = STRUCTURES_DIR / VERSION_FOLDER / f"{base_rel}.nbt"
    if dst.exists():
        return False
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dst)
    return True


def versionize_pool(pool_path, base_rel):
    """Convert a plain single_pool_element into a versioned_single_pool_element,
    mirroring the azelea_house / oak_well schema. Idempotent."""
    with open(pool_path, encoding="utf-8") as f:
        data = json.load(f)

    base_loc = f"{MOD_ID}:{base_rel}"
    new_loc = f"{MOD_ID}:{VERSION_FOLDER}/{base_rel}"

    modified = False
    for entry in data.get("elements", []):
        element = entry.get("element", {})
        if element.get("element_type") == "moogs_structures:versioned_single_pool_element":
            continue  # already versioned
        # Default location points at the newest variant.
        element["location"] = new_loc
        element["locations"] = {LOW_RANGE: base_loc}
        for r in NEW_RANGES:
            element["locations"][r] = new_loc
        element["element_type"] = "moogs_structures:versioned_single_pool_element"
        modified = True

    if modified:
        with open(pool_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
            f.write("\n")
    return modified


# base structure path (no extension, relative to structures dir) -> pool json (relative to template_pool dir)
VERSION_THEN_SWAP = {
    "houses/diorite_tower":               "houses/diorite_tower/start_pool.json",
    "houses/mud_brick_house_1":           "houses/mud_brick_house_1/start_pool.json",
    "houses/diorite_and_deepslate_house": "houses/diorite_and_deepslate_house/start_pool.json",
    "houses/prismarine_house_1":          "houses/prismarine_house_1/start_pool.json",
    "houses/prismarine_house_2":          "houses/prismarine_house_2/start_pool.json",
}

# Already versioned upstream: swap the base NBT only, leave version copy + pool alone.
SWAP_ONLY = [
    "ruins/ruined_beacon",
]


def main():
    print("=== Version-then-swap ===")
    for base_rel, pool_rel in VERSION_THEN_SWAP.items():
        copied = make_version_copy(base_rel)
        changed = swap_base_nbt(STRUCTURES_DIR / f"{base_rel}.nbt")
        pooled = versionize_pool(TEMPLATE_POOL_DIR / pool_rel, base_rel)
        print(f"  {base_rel}: copy={'new' if copied else 'exists'} "
              f"base_swaps={changed} pool={'versioned' if pooled else 'already'}")

    print("\n=== Swap-only (already versioned) ===")
    for base_rel in SWAP_ONLY:
        changed = swap_base_nbt(STRUCTURES_DIR / f"{base_rel}.nbt")
        print(f"  {base_rel}: base_swaps={changed}")

    print("\nDone.")


if __name__ == "__main__":
    main()
