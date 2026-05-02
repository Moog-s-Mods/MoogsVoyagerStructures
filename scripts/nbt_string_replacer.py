"""
Find-and-replace string values inside NBT files under the structures folder.

Uses a negative-lookahead so 'minecraft:chain' won't match 'minecraft:chainmail'.
You can either overwrite files in place or write the modified copies into a
version subfolder (e.g. '1_20_6/').

Run from project root: python scripts/nbt_string_replacer.py
"""
import collections.abc
import re
import sys

import nbtlib as nbt

from _paths import STRUCTURES_DIR


def get_user_inputs():
    print("=== NBT String Replacer ===\n")
    print("Enter search->replace pairs, one per line, format:  old_string=new_string")
    print("Press Enter with no input when done.\n")

    replacements = {}
    while True:
        entry = input("Replacement (or Enter to finish): ").strip()
        if not entry:
            break
        if "=" not in entry:
            print("  Invalid format, expected: old_string=new_string")
            continue
        old, new = entry.split("=", 1)
        old, new = old.strip(), new.strip()
        replacements[old] = new
        print(f"  Added: '{old}' -> '{new}'")

    if not replacements:
        print("No replacements entered. Exiting.")
        sys.exit(0)

    version = input("\nVersion folder name (leave blank to overwrite in-place): ").strip()

    return replacements, version


def replace_strings(node, replacements, changed):
    """Recursively walk the NBT tree, replacing strings in-place.
    'changed' is a one-element list used as a mutable flag."""
    if isinstance(node, collections.abc.Mapping):
        for key in list(node.keys()):
            entry = node[key]
            if isinstance(entry, (nbt.List, nbt.Compound)):
                replace_strings(entry, replacements, changed)
            elif isinstance(entry, nbt.String):
                result = _replace(str(entry), replacements)
                if result is not None:
                    node[key] = nbt.String(result)
                    changed[0] = True

    elif isinstance(node, nbt.List):
        for i, entry in enumerate(node):
            if isinstance(entry, (nbt.List, nbt.Compound)):
                replace_strings(entry, replacements, changed)
            elif isinstance(entry, nbt.String):
                result = _replace(str(entry), replacements)
                if result is not None:
                    node[i] = nbt.String(result)
                    changed[0] = True


def _replace(s, replacements):
    """Apply all replacements to s. Returns the new string if changed, else None."""
    original = s
    for old, new in replacements.items():
        s = re.sub(re.escape(old) + r'(?![a-zA-Z0-9_])', new, s)
    return s if s != original else None


def main():
    if not STRUCTURES_DIR.exists():
        print(f"ERROR: Structure directory not found:\n  {STRUCTURES_DIR}")
        sys.exit(1)

    replacements, version = get_user_inputs()
    output_base = STRUCTURES_DIR / version if version else STRUCTURES_DIR

    print(f"\nScanning: {STRUCTURES_DIR}")
    print(f"Output:   {'(in-place)' if not version else output_base}\n")

    saved = []
    skipped = []

    for nbt_path in sorted(STRUCTURES_DIR.rglob("*.nbt")):
        rel = nbt_path.relative_to(STRUCTURES_DIR)

        # Skip files already inside a version subfolder (first component starts with a digit)
        if rel.parts[0][0].isdigit():
            continue

        changed = [False]
        try:
            nbtfile = nbt.load(str(nbt_path))
        except Exception as e:
            print(f"  [ERROR]   {rel} -- {e}")
            continue
        replace_strings(nbtfile, replacements, changed)

        if changed[0]:
            out_path = nbt_path if not version else output_base / rel
            if version:
                out_path.parent.mkdir(parents=True, exist_ok=True)
            nbtfile.save(str(out_path))
            saved.append(str(rel))
            print(f"  [SAVED]   {rel}")
        else:
            skipped.append(str(rel))
            print(f"  [skipped] {rel}")

    print(f"\nDone! {len(saved)} file(s) saved to '{version}/', {len(skipped)} unchanged.")
    if saved:
        print("\nSaved files:")
        for f in saved:
            print(f"  {f}")

    input("\nPress Enter to exit...")


if __name__ == "__main__":
    main()
