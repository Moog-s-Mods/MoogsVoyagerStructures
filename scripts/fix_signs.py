"""
Fix sign block entity NBT in structures saved with DataVersion > 3465 (post-1.20.1).

Two problems with the newer format that crash 1.20.1:
  1. messages list contains bare empty strings '' - 1.20.1 parses each entry as a
     JSON Component; an empty string is not valid JSON so the codec returns null,
     which is then added to a Guava ImmutableList.Builder → NullPointerException.
  2. A 'components' key is present - introduced in 1.20.5, unknown to 1.20.1.

Fix: for every sign block entity with inline NBT in an affected file, replace
empty messages with '""' (JSON empty string) and remove 'components'.
"""
import sys
import nbtlib
from nbtlib import String, List, Compound
from _paths import STRUCTURES_DIR

TARGET_DV_MIN = 3466  # anything newer than 1.20.1

import json as _json


def _to_json_component(s: str) -> String:
    """Convert a bare string to a JSON-encoded component string that 1.20.1 can parse."""
    raw = str(s)
    # Already a valid JSON component (object or quoted string) - leave it alone
    if raw.startswith("{") or (raw.startswith('"') and raw.endswith('"')):
        return String(raw)
    return String(_json.dumps(raw))


def fix_sign_text(text_compound: Compound) -> bool:
    changed = False
    msgs = text_compound.get("messages")
    if msgs is not None:
        for i, m in enumerate(msgs):
            fixed = _to_json_component(m)
            if str(fixed) != str(m):
                msgs[i] = fixed
                changed = True
    return changed


def fix_nbt_file(path) -> bool:
    nbt = nbtlib.load(str(path))
    dv = int(nbt.get("DataVersion", 0))
    if dv < TARGET_DV_MIN:
        return False

    palette = nbt.get("palette", [])
    blocks = nbt.get("blocks", [])

    sign_indices = {
        i for i, b in enumerate(palette)
        if "sign" in str(b.get("Name", "")).lower()
    }
    if not sign_indices:
        return False

    changed = False
    for block in blocks:
        if int(block["state"]) not in sign_indices:
            continue
        be_nbt = block.get("nbt")
        if be_nbt is None:
            continue

        # Remove 'components' key (1.20.5+ only)
        if "components" in be_nbt:
            del be_nbt["components"]
            changed = True

        for key in ("front_text", "back_text"):
            text = be_nbt.get(key)
            if text is not None and fix_sign_text(text):
                changed = True

    if changed:
        nbt.save(str(path))

    return changed


def main():
    fixed, skipped = [], []
    for path in sorted(STRUCTURES_DIR.rglob("*.nbt")):
        rel = str(path.relative_to(STRUCTURES_DIR))
        if fix_nbt_file(path):
            fixed.append(rel)
            print(f"  [FIXED]   {rel}")
        else:
            skipped.append(rel)

    print(f"\n{len(fixed)} file(s) fixed, {len(skipped)} skipped (already OK or no signs).")

    if sys.stdin.isatty():
        input("\nPress Enter to exit...")


if __name__ == "__main__":
    main()
