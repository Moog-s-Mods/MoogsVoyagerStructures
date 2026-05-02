"""
Shared path/mod-id detection for the scripts in this folder.

Auto-detects the mod's namespace from gradle.properties and the data folder
names (singular `structure`/`loot_table` for 1.21, plural for 1.20). Every
script in this folder imports from here so the same code works in every Moog's
mod repo without modification.

Usage:
    from _paths import MOD_ID, PROJECT_ROOT, STRUCTURES_DIR, LOOT_TABLES_DIR, TEMPLATE_POOL_DIR
"""
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent


def _read_mod_id() -> str:
    props = PROJECT_ROOT / "gradle.properties"
    if not props.exists():
        raise RuntimeError(f"gradle.properties not found at {props}")
    for raw in props.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if line.startswith("modId="):
            return line.split("=", 1)[1].strip()
    raise RuntimeError("modId= not found in gradle.properties")


MOD_ID = _read_mod_id()
DATA_ROOT = PROJECT_ROOT / "src" / "main" / "resources" / "data" / MOD_ID


def _pick(*names: str) -> Path:
    """Return the first existing folder under DATA_ROOT, else fall back to the first name."""
    for n in names:
        p = DATA_ROOT / n
        if p.exists():
            return p
    return DATA_ROOT / names[0]


# 1.21 uses singular folders ("structure", "loot_table"); 1.20 uses plural.
STRUCTURES_DIR = _pick("structure", "structures")
LOOT_TABLES_DIR = _pick("loot_table", "loot_tables")
TEMPLATE_POOL_DIR = DATA_ROOT / "worldgen" / "template_pool"
