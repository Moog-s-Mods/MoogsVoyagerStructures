import nbtlib as nbt
from pathlib import Path
import collections.abc
import sys
import re

# https://github.com/vberlier/nbtlib

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
    script_dir = Path(__file__).parent
    project_root = script_dir.parent
    structure_dir = project_root / "src" / "main" / "resources" / "data" / "mvs" / "structure"

    if not structure_dir.exists():
        print(f"ERROR: Structure directory not found:\n  {structure_dir}")
        sys.exit(1)

    search = input("Search string: ").strip()
    if not search:
        print("No input. Exiting.")
        sys.exit(0)

    # Same boundary rule as the replacer — won't match if followed by an identifier character
    pattern = re.compile(re.escape(search) + r'(?![a-zA-Z0-9_])')

    print(f"\nSearching for: '{search}'\n")

    matches = []

    for nbt_path in sorted(structure_dir.rglob("*.nbt")):
        rel = nbt_path.relative_to(structure_dir)

        if rel.parts[0][0].isdigit():
            continue

        try:
            nbtfile = nbt.load(str(nbt_path))
        except Exception as e:
            print(f"  [ERROR] {rel} — {e}")
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
