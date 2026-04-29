import nbtlib as nbt
from pathlib import Path
import collections.abc
import sys
import re

# https://github.com/vberlier/nbtlib

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

    version = input("\nVersion folder name (e.g. 1_21_9): ").strip()
    if not version:
        print("Version cannot be empty. Exiting.")
        sys.exit(0)

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
    """Apply all replacements to s. Returns the new string if changed, else None.
    Uses a negative lookahead so 'minecraft:chain' won't match 'minecraft:chainmail'."""
    original = s
    for old, new in replacements.items():
        # (?![a-zA-Z0-9_]) ensures the match isn't immediately followed by another identifier character
        s = re.sub(re.escape(old) + r'(?![a-zA-Z0-9_])', new, s)
    return s if s != original else None


def main():
    script_dir = Path(__file__).parent
    project_root = script_dir.parent
    structure_dir = project_root / "src" / "main" / "resources" / "data" / "mvs" / "structures"

    if not structure_dir.exists():
        print(f"ERROR: Structure directory not found:\n  {structure_dir}")
        sys.exit(1)

    replacements, version = get_user_inputs()
    output_base = structure_dir / version

    print(f"\nScanning: {structure_dir}")
    print(f"Output:   {output_base}\n")

    saved = []
    skipped = []

    for nbt_path in sorted(structure_dir.rglob("*.nbt")):
        rel = nbt_path.relative_to(structure_dir)

        # Skip files already inside a version subfolder (first component starts with a digit)
        if rel.parts[0][0].isdigit():
            continue

        changed = [False]
        try:
            nbtfile = nbt.load(str(nbt_path))
        except Exception as e:
            print(f"  [ERROR]   {rel} — {e}")
            continue
        replace_strings(nbtfile, replacements, changed)

        if changed[0]:
            out_path = output_base / rel
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
