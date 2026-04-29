"""
Scans all template pool JSONs and injects a new version range entry into any element
whose structure has a versioned NBT in the given version folder.

For elements without a "locations" block, one is created alongside the existing "location".
For elements that already have "locations", the new range is appended.

Usage: python update_template_pools.py
"""

from pathlib import Path
import json
import sys

VERSION_FOLDER = "1_20_6"
VERSION_RANGE  = "1.20-1.20.6"
NAMESPACE      = "mvs"


def collect_versioned_paths(structure_dir: Path, version_folder: str) -> set[str]:
    """Returns a set of base paths that have a versioned NBT, e.g. 'gallows', 'cathedral/base/base'."""
    versioned = set()
    version_dir = structure_dir / version_folder
    if not version_dir.exists():
        print(f"ERROR: Version folder not found: {version_dir}")
        sys.exit(1)
    for nbt in version_dir.rglob("*.nbt"):
        rel = nbt.relative_to(version_dir).with_suffix("")
        versioned.add(str(rel).replace("\\", "/"))
    return versioned


def base_path_from_location(location: str, namespace: str) -> str | None:
    """
    Strips the namespace and any leading version folder from a location string.
    'mvs:gallows'                   -> 'gallows'
    'mvs:1_21_11/small_tower_well'  -> 'small_tower_well'
    'minecraft:empty'               -> None  (not our namespace)
    """
    prefix = namespace + ":"
    if not location.startswith(prefix):
        return None
    path = location[len(prefix):]
    parts = path.split("/")
    if parts[0] and parts[0][0].isdigit():
        path = "/".join(parts[1:])
    return path


def process_pool(json_path: Path, versioned_paths: set[str]) -> bool:
    """Returns True if the file was modified."""
    with open(json_path, encoding="utf-8") as f:
        data = json.load(f)

    modified = False

    for entry in data.get("elements", []):
        element = entry.get("element", {})
        location = element.get("location", "")

        base = base_path_from_location(location, NAMESPACE)
        if base is None or base not in versioned_paths:
            continue

        new_loc = f"{NAMESPACE}:{VERSION_FOLDER}/{base}"

        if "locations" not in element:
            element["locations"] = {}

        if VERSION_RANGE in element["locations"]:
            continue  # already set, skip

        element["locations"][VERSION_RANGE] = new_loc
        modified = True

    if modified:
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
            f.write("\n")

    return modified


def main():
    script_dir   = Path(__file__).parent
    project_root = script_dir.parent
    structure_dir    = project_root / "src" / "main" / "resources" / "data" / "mvs" / "structures"
    template_pool_dir = project_root / "src" / "main" / "resources" / "data" / "mvs" / "worldgen" / "template_pool"

    versioned_paths = collect_versioned_paths(structure_dir, VERSION_FOLDER)
    print(f"Found {len(versioned_paths)} structures with a '{VERSION_FOLDER}' variant.\n")

    updated = []
    skipped = []

    for json_path in sorted(template_pool_dir.rglob("*.json")):
        rel = json_path.relative_to(template_pool_dir)
        if process_pool(json_path, versioned_paths):
            updated.append(str(rel))
            print(f"  [UPDATED] {rel}")
        else:
            skipped.append(str(rel))

    print(f"\nDone! {len(updated)} pool file(s) updated, {len(skipped)} unchanged.")
    if updated:
        print("\nUpdated files:")
        for f in updated:
            print(f"  {f}")

    input("\nPress Enter to exit...")


if __name__ == "__main__":
    main()
