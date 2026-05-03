"""
Scans all template pool JSONs and injects a new version range entry into any element
whose structure has a versioned NBT in the given version folder.

For elements without a "locations" block, one is created alongside the existing "location".
For elements that already have "locations", the new range is appended.

Edit VERSION_FOLDER and VERSION_RANGE below for the version you're publishing.
Run from project root: python scripts/update_template_pools.py
"""
import json
import sys

from _paths import MOD_ID, STRUCTURES_DIR, TEMPLATE_POOL_DIR


# === EDIT THESE FOR THE VERSION YOU'RE TARGETING ===
VERSION_FOLDER = "1_20_6"          # subfolder under structures/ that has the version-specific NBTs
VERSION_RANGE  = "1.20-1.20.6"     # the version range key written into the pool JSON
# ====================================================


def collect_versioned_paths(structure_dir, version_folder):
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


def base_path_from_location(location, namespace):
    """
    Strips the namespace and any leading version folder from a location string.
    '<ns>:gallows'                   -> 'gallows'
    '<ns>:1_21_11/small_tower_well'  -> 'small_tower_well'
    'minecraft:empty'                -> None  (not our namespace)
    """
    prefix = namespace + ":"
    if not location.startswith(prefix):
        return None
    path = location[len(prefix):]
    parts = path.split("/")
    if parts[0] and parts[0][0].isdigit():
        path = "/".join(parts[1:])
    return path


def process_pool(json_path, versioned_paths):
    """Returns True if the file was modified."""
    with open(json_path, encoding="utf-8") as f:
        data = json.load(f)

    modified = False

    for entry in data.get("elements", []):
        element = entry.get("element", {})
        location = element.get("location", "")

        base = base_path_from_location(location, MOD_ID)
        if base is None or base not in versioned_paths:
            continue

        new_loc = f"{MOD_ID}:{VERSION_FOLDER}/{base}"

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
    versioned_paths = collect_versioned_paths(STRUCTURES_DIR, VERSION_FOLDER)
    print(f"Found {len(versioned_paths)} structures with a '{VERSION_FOLDER}' variant.\n")

    updated = []
    skipped = []

    for json_path in sorted(TEMPLATE_POOL_DIR.rglob("*.json")):
        rel = json_path.relative_to(TEMPLATE_POOL_DIR)
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
