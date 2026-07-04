"""
Swap blocks that only exist in newer Minecraft versions out of the structure
NBTs so they validate on 1.20.x.

Unlike the 1.21 line, 1.20.x has NO supported version in which these blocks
exist, so there is nothing to preserve: the swap is applied straight to the
base NBTs in place. No version folders and no versioned pool elements are
created here. (If a 1.20 structure were already versioned, we would follow its
existing pattern -- the affected houses below are plain single_pool_element, so
an in-place swap is all that is needed.)

The swap map below is the single source of truth. For each palette entry whose
Name matches, the Name is rewritten and Properties are rebuilt to keep only the
properties valid on the replacement block (or dropped entirely for the air
replacements). All edits go through nbtlib so the length-prefixed NBT strings
stay valid -- never do raw byte replacement on these files.

Idempotent: re-running finds nothing left to change and reports zero edits.

Run from project root:  python scripts/fix_versioned_blocks.py
"""
import nbtlib as nbt

from _paths import STRUCTURES_DIR


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

# Base structure paths (no extension, relative to structures dir) to fix. Every
# 1.20 file flagged by the structure validator as using a newer-only block.
TARGET_STRUCTURES = [
    "houses/diorite_tower",
    "houses/mud_brick_house_1",
    "houses/diorite_and_deepslate_house",
    "houses/prismarine_house_1",
]


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


def main():
    for base_rel in TARGET_STRUCTURES:
        path = STRUCTURES_DIR / f"{base_rel}.nbt"
        if not path.exists():
            print(f"  {base_rel}: MISSING ({path})")
            continue
        changed = swap_base_nbt(path)
        print(f"  {base_rel}: base_swaps={changed}")

    print("\nDone.")


if __name__ == "__main__":
    main()
