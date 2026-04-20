import nbtlib as nbt
from pathlib import Path
import sys

def main():
    script_dir   = Path(__file__).parent
    project_root = script_dir.parent
    structure_dir = project_root / "src" / "main" / "resources" / "data" / "mvs" / "structure"

    if not structure_dir.exists():
        print(f"ERROR: Structure directory not found:\n  {structure_dir}")
        sys.exit(1)

    ok      = []
    corrupt = []

    for nbt_path in sorted(structure_dir.rglob("*.nbt")):
        rel = nbt_path.relative_to(structure_dir)
        try:
            nbt.load(str(nbt_path))
            ok.append(str(rel))
        except Exception as e:
            corrupt.append((str(rel), str(e)))
            print(f"  [CORRUPT] {rel}")
            print(f"            {e}")

    print(f"\n{len(ok)} file(s) OK, {len(corrupt)} corrupt.")

    if corrupt:
        print("\nCorrupt files:")
        for path, err in corrupt:
            print(f"  {path}")
            print(f"    {err}")

    if sys.stdin.isatty():
        input("\nPress Enter to exit...")

if __name__ == "__main__":
    main()
