#!/usr/bin/env python3
"""
Interactive tool to assign loot tables to empty/hardcoded containers.
Run from the project root: python scripts/fix_loot.py

Commands at the prompt:
  <loot_table>   assign this loot table to the current container
  a <loot_table> apply to ALL remaining containers in this file
  s              skip this container
  sf             skip the rest of this file
  q              quit (saves progress already made in this file)
"""
from collections import defaultdict
from pathlib import Path

import nbtlib

PROJECT_ROOT = Path(__file__).parent.parent
STRUCTURES_DIR = PROJECT_ROOT / "src" / "main" / "resources" / "data" / "mvs" / "structure"
LOOT_TABLES_DIR = PROJECT_ROOT / "src" / "main" / "resources" / "data" / "mvs" / "loot_table"

_CONTAINER_BLOCKS = {"minecraft:chest", "minecraft:trapped_chest", "minecraft:barrel"}


def get_loot_tables():
    tables = []
    for p in sorted(LOOT_TABLES_DIR.rglob("*.json")):
        name = p.relative_to(LOOT_TABLES_DIR).with_suffix("").as_posix()
        tables.append(f"mvs:{name}")
    return tables


def scan_containers(structures_dir: Path) -> dict:
    """Scan all NBT files and return {rel_path: [(warn_type, x, y, z, block_id), ...]}"""
    results = defaultdict(list)

    for nbt_path in sorted(structures_dir.rglob("*.nbt")):
        try:
            nbt = nbtlib.load(str(nbt_path))
        except Exception:
            continue

        palette = nbt.get("palette")
        blocks = nbt.get("blocks")
        if palette is None or blocks is None:
            continue

        container_indices = {
            i: str(state.get("Name", ""))
            for i, state in enumerate(palette)
            if str(state.get("Name", "")) in _CONTAINER_BLOCKS
        }
        if not container_indices:
            continue

        rel = nbt_path.relative_to(structures_dir).as_posix()

        for block in blocks:
            state_idx = int(block.get("state", -1))
            if state_idx not in container_indices:
                continue

            block_id = container_indices[state_idx]
            pos = block.get("pos")
            x, y, z = (int(v) for v in pos)

            block_nbt = block.get("nbt")
            if block_nbt is None:
                results[rel].append(("empty container", x, y, z, block_id))
                continue

            has_loot = "LootTable" in block_nbt
            has_items = bool(block_nbt.get("Items"))

            if not has_loot and not has_items:
                results[rel].append(("empty container", x, y, z, block_id))
            elif has_items and not has_loot:
                results[rel].append(("hardcoded items", x, y, z, block_id))

    return dict(results)


def patch_nbt(nbt_path: Path, patches: dict) -> int:
    """Apply {(x,y,z): loot_table} patches to an NBT structure file in place."""
    nbt = nbtlib.load(str(nbt_path))
    palette = nbt.get("palette", [])
    id_by_state = {i: str(state.get("Name", "")) for i, state in enumerate(palette)}

    patched = 0
    for block in nbt["blocks"]:
        pos = block.get("pos")
        if pos is None:
            continue
        key = (int(pos[0]), int(pos[1]), int(pos[2]))
        if key not in patches:
            continue
        loot_table = patches[key]
        block_id = id_by_state.get(int(block.get("state", -1)), "minecraft:chest")
        block["nbt"] = nbtlib.Compound({
            "id": nbtlib.String(block_id),
            "LootTable": nbtlib.String(loot_table),
        })
        patched += 1
    nbt.save(str(nbt_path))
    return patched


def save_and_report(nbt_path, rel_path, patches):
    if patches:
        saved = patch_nbt(nbt_path, patches)
        print(f"  -> saved {saved} patch(es) to {rel_path}\n")
    else:
        print("  -> skipped\n")


def main():
    print("Scanning structures...")
    warnings = scan_containers(STRUCTURES_DIR)

    if not warnings:
        print("No empty or hardcoded containers found!")
        return

    loot_tables = get_loot_tables()
    total_files = len(warnings)
    total_containers = sum(len(v) for v in warnings.values())

    print(f"Found {total_containers} container(s) across {total_files} file(s).\n")
    print("Available loot tables:")
    for t in loot_tables:
        print(f"  {t}")
    print()
    print("  <loot_table>   assign to this container")
    print("  a <loot_table> apply to ALL remaining in this file")
    print("  s              skip this container")
    print("  sf             skip the rest of this file")
    print("  q              quit (saves this file's progress first)")
    print()

    for file_idx, (rel_path, containers) in enumerate(warnings.items(), 1):
        nbt_path = STRUCTURES_DIR / rel_path

        print(f"{'='*60}")
        print(f"[{file_idx}/{total_files}]  {rel_path}  ({len(containers)} container(s))")
        print(f"{'='*60}")

        patches = {}
        skip_file = False
        apply_all = None

        for warn_type, x, y, z, block_id in containers:
            if skip_file:
                break

            if apply_all is not None:
                patches[(x, y, z)] = apply_all
                continue

            label = f"{block_id} @ ({x}, {y}, {z})  [{warn_type}]"

            while True:
                try:
                    response = input(f"  {label}\n  > ").strip()
                except (EOFError, KeyboardInterrupt):
                    print()
                    save_and_report(nbt_path, rel_path, patches)
                    print("Interrupted.")
                    return

                if not response:
                    print("  Enter a loot table or a command.")
                    continue

                if response == "q":
                    save_and_report(nbt_path, rel_path, patches)
                    print("Quitting.")
                    return

                if response == "s":
                    break

                if response == "sf":
                    skip_file = True
                    break

                if response.startswith("a "):
                    loot = response[2:].strip()
                    if not loot:
                        print("  Usage: a <loot_table>")
                        continue
                    apply_all = loot
                    patches[(x, y, z)] = loot
                    remaining = sum(
                        1 for wt, wx, wy, wz, _ in containers
                        if (wx, wy, wz) not in patches and not (wx == x and wy == y and wz == z)
                    )
                    print(f"  Applying '{loot}' to this and {remaining} remaining container(s).")
                    break

                patches[(x, y, z)] = response
                break

        save_and_report(nbt_path, rel_path, patches)

    print("All done! Run validate.bat to verify.")


if __name__ == "__main__":
    main()
