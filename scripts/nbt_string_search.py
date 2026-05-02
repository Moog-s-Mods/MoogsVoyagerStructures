"""
Search for a string inside any NBT file under the structures folder.

Uses a negative-lookahead so 'minecraft:chain' won't match 'minecraft:chainmail'.
Run from project root: python scripts/nbt_string_search.py
"""
import collections.abc
import re
import sys

import nbtlib as nbt

from _paths import STRUCTURES_DIR


def contains_string(node, pattern):
    if isinstance(node, collections.abc.Mapping):
        for entry in node.values():
            if isinstance(entry, (nbt.List, nbt.Compound)):
                if contains_string(entry, pattern):
                    return True
            elif isinstance(entry, nbt.String):
                if pattern.search(str(entry)):
                    return True

    elif isinstance(node, nbt.List):
        for entry in node:
            if isinstance(entry, (nbt.List, nbt.Compound)):
                if contains_string(entry, pattern):
                    return True
            elif isinstance(entry, nbt.String):
                if pattern.search(str(entry)):
                    return True

    return False


def main():
    if not STRUCTURES_DIR.exists():
        print(f"ERROR: Structure directory not found:\n  {STRUCTURES_DIR}")
        sys.exit(1)

    search = input("Search string: ").strip()
    if not search:
        print("No input. Exiting.")
        sys.exit(0)

    pattern = re.compile(re.escape(search) + r'(?![a-zA-Z0-9_])')

    print(f"\nSearching for: '{search}'\n")

    matches = []

    for nbt_path in sorted(STRUCTURES_DIR.rglob("*.nbt")):
        rel = nbt_path.relative_to(STRUCTURES_DIR)

        if rel.parts[0][0].isdigit():
            continue

        try:
            nbtfile = nbt.load(str(nbt_path))
        except Exception as e:
            print(f"  [ERROR] {rel} -- {e}")
            continue

        if contains_string(nbtfile, pattern):
            matches.append(rel)

    if matches:
        print(f"Found in {len(matches)} file(s):\n")
        for rel in matches:
            print(f"  {rel}")
    else:
        print("No matches found.")

    input("\nPress Enter to exit...")


if __name__ == "__main__":
    main()
