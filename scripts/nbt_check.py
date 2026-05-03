"""
Verify every .nbt file under the structures folder loads cleanly + flag oversized ones.

Files larger than SIZE_BUDGET_KB are reported as warnings (non-fatal). Files that fail
to load are reported as errors and cause a non-zero exit.

Run from project root: python scripts/nbt_check.py
"""
import sys
import nbtlib

from _paths import STRUCTURES_DIR

SIZE_BUDGET_KB = 500  # warn for any single NBT larger than this


def main():
    if not STRUCTURES_DIR.exists():
        print(f"ERROR: Structure directory not found:\n  {STRUCTURES_DIR}")
        sys.exit(1)

    ok, corrupt, oversized = [], [], []

    for nbt_path in sorted(STRUCTURES_DIR.rglob("*.nbt")):
        rel = nbt_path.relative_to(STRUCTURES_DIR)
        size_kb = nbt_path.stat().st_size / 1024
        try:
            nbtlib.load(str(nbt_path))
            ok.append(str(rel))
            if size_kb > SIZE_BUDGET_KB:
                oversized.append((str(rel), size_kb))
                print(f"  [SIZE]    {rel}  ({size_kb:.0f} KB > {SIZE_BUDGET_KB} KB budget)")
        except Exception as e:
            corrupt.append((str(rel), str(e)))
            print(f"  [CORRUPT] {rel}")
            print(f"            {e}")

    print(f"\n{len(ok)} file(s) OK, {len(oversized)} oversized, {len(corrupt)} corrupt.")

    if corrupt:
        print("\nCorrupt files:")
        for path, err in corrupt:
            print(f"  {path}")
            print(f"    {err}")

    if sys.stdin.isatty():
        input("\nPress Enter to exit...")

    # Non-zero exit only on corruption (oversized is a warning, not a fail)
    if corrupt:
        sys.exit(1)


if __name__ == "__main__":
    main()
