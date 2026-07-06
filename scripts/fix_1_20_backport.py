"""
Fixes for backporting NBTs saved from newer MC versions onto the 1.20-datapack branch
(target range: 1.20 through 1.20.6).

Applies four independent, idempotent passes to every .nbt under STRUCTURES_DIR:

1. Sign block entities: JSON-quote bare empty `messages` strings and drop the
   post-1.20.5 `components` key. Bare `""` in a sign's messages list makes the
   1.20.1 Component codec return null → ImmutableList.Builder NPE → crash.
   (Same fix as scripts/fix_signs.py but without the DV floor so 1.20.1-native
   saves at DV 3465 are covered too.)

2. Written books saved with the 1.20.5+ `components` schema: rewrite into the
   legacy `tag` schema so pages/title/author actually load pre-1.20.5.

3. Entity `attributes` list (1.21+ schema): rewrite into the legacy `Attributes`
   list with `Name`/`Base`/`Modifiers`, adding `generic.` prefixes and
   synthesizing modifier UUIDs.

4. Entity `Attributes` list where a Name is missing the legacy `generic.` prefix
   (post-1.21.2 saves that kept the list format): re-insert the prefix.

5. Delete the 1.21.5+ `fall_distance` float on entities (silently ignored pre-1.21.5).

Also strips fall_distance from any passengers/riders recursively.
"""
import json
import sys
import uuid

import nbtlib
from nbtlib import Byte, Compound, Double, Float, Int, IntArray, List, String

from _paths import STRUCTURES_DIR


# ---------------------------------------------------------------------------
# 1. Signs
# ---------------------------------------------------------------------------

def _to_json_component(s: str) -> String:
    raw = str(s)
    if raw.startswith("{") or (raw.startswith('"') and raw.endswith('"')):
        return String(raw)
    return String(json.dumps(raw))


def _fix_sign_side(text_compound: Compound) -> bool:
    changed = False
    msgs = text_compound.get("messages")
    if msgs is None:
        return False
    for i, m in enumerate(msgs):
        fixed = _to_json_component(m)
        if str(fixed) != str(m):
            msgs[i] = fixed
            changed = True
    return changed


def _fix_signs(nbt) -> int:
    palette = nbt.get("palette", [])
    blocks = nbt.get("blocks", [])
    sign_ids = {
        i for i, b in enumerate(palette)
        if "sign" in str(b.get("Name", "")).lower()
    }
    if not sign_ids:
        return 0
    changed = 0
    for block in blocks:
        if int(block["state"]) not in sign_ids:
            continue
        be = block.get("nbt")
        if be is None:
            continue
        block_changed = False
        if "components" in be:
            del be["components"]
            block_changed = True
        for key in ("front_text", "back_text"):
            t = be.get(key)
            if t is not None and _fix_sign_side(t):
                block_changed = True
        if block_changed:
            changed += 1
    return changed


# ---------------------------------------------------------------------------
# 2. Written books (components -> tag)
# ---------------------------------------------------------------------------

def _pages_component_to_tag(pages_list) -> List:
    out = []
    for p in pages_list:
        if isinstance(p, Compound):
            text = str(p.get("raw", ""))
        else:
            text = str(p)
        out.append(String(json.dumps(text)))
    return List[String](out)


def _title_component_to_tag(title) -> String:
    if isinstance(title, Compound):
        return String(str(title.get("raw", "")))
    return String(str(title))


def _book_components_to_tag(book_item: Compound) -> bool:
    if "components" not in book_item:
        return False
    comps = book_item["components"]
    content = comps.get("minecraft:written_book_content")
    if content is None:
        return False
    tag = Compound()
    if "title" in content:
        tag["title"] = _title_component_to_tag(content["title"])
    if "author" in content:
        tag["author"] = String(str(content["author"]))
    if "pages" in content:
        tag["pages"] = _pages_component_to_tag(content["pages"])
    if "resolved" in content:
        try:
            tag["resolved"] = Byte(int(content["resolved"]))
        except Exception:
            tag["resolved"] = Byte(1)
    else:
        tag["resolved"] = Byte(1)
    book_item["tag"] = tag
    del book_item["components"]
    if "count" in book_item:
        try:
            n = int(book_item["count"])
        except Exception:
            n = 1
        del book_item["count"]
        book_item["Count"] = Byte(n)
    return True


def _walk_items_in_compound(node, callback):
    if isinstance(node, Compound):
        if node.get("id") is not None and (
            "components" in node or "tag" in node or "count" in node or "Count" in node
        ):
            id_str = str(node.get("id", ""))
            if id_str.endswith(":written_book"):
                callback(node)
        for v in list(node.values()):
            _walk_items_in_compound(v, callback)
    elif isinstance(node, list):
        for v in node:
            _walk_items_in_compound(v, callback)


def _fix_books(nbt) -> int:
    count = 0

    def cb(item):
        nonlocal count
        if _book_components_to_tag(item):
            count += 1

    _walk_items_in_compound(nbt, cb)
    return count


# ---------------------------------------------------------------------------
# 3+4. Attributes (list schema -> legacy Attributes list; legacy name prefix fix)
# ---------------------------------------------------------------------------

_OP_MAP = {
    "add_value": 0,
    "add_multiplied_base": 1,
    "add_multiplied_total": 2,
}


def _legacy_attr_name(id_str: str) -> str:
    """Map a modern attribute id ('minecraft:max_health', 'minecraft:horse.jump_strength')
    to the legacy 1.20.x Name form ('minecraft:generic.max_health', etc.)."""
    name = id_str
    if name.startswith("minecraft:"):
        rest = name[len("minecraft:"):]
    else:
        rest = name
    if rest.startswith("generic.") or rest.startswith("zombie.") or rest.startswith("horse.") or rest.startswith("player."):
        # Already legacy-prefixed
        return f"minecraft:{rest}"
    if rest.startswith("spawn_reinforcements"):
        return f"minecraft:zombie.{rest}"
    if rest.startswith("jump_strength"):
        return f"minecraft:horse.{rest}"
    return f"minecraft:generic.{rest}"


def _synth_uuid_int_array() -> IntArray:
    u = uuid.uuid4()
    hi = u.int >> 64
    lo = u.int & ((1 << 64) - 1)

    def split(n):
        h = (n >> 32) & 0xFFFFFFFF
        l = n & 0xFFFFFFFF
        # Convert unsigned 32-bit to signed
        if h >= 0x80000000:
            h -= 0x100000000
        if l >= 0x80000000:
            l -= 0x100000000
        return h, l

    a, b = split(hi)
    c, d = split(lo)
    return IntArray([a, b, c, d])


def _convert_modifier_new_to_legacy(mod: Compound) -> Compound:
    out = Compound()
    if "id" in mod:
        mod_id = str(mod["id"])
        if mod_id.startswith("minecraft:"):
            mod_id = mod_id[len("minecraft:"):]
        out["Name"] = String(mod_id)
    if "amount" in mod:
        out["Amount"] = Double(float(mod["amount"]))
    if "operation" in mod:
        op = str(mod["operation"])
        out["Operation"] = Int(_OP_MAP.get(op, 0))
    out["UUID"] = _synth_uuid_int_array()
    return out


def _convert_new_attributes_to_legacy(new_list) -> List:
    out_items = []
    for a in new_list:
        entry = Compound()
        if "id" in a:
            entry["Name"] = String(_legacy_attr_name(str(a["id"])))
        if "base" in a:
            entry["Base"] = Double(float(a["base"]))
        if "modifiers" in a:
            mods = List[Compound]()
            for m in a["modifiers"]:
                mods.append(_convert_modifier_new_to_legacy(m))
            entry["Modifiers"] = mods
        out_items.append(entry)
    return List[Compound](out_items)


def _fix_entity_attributes(entity_nbt: Compound) -> bool:
    changed = False
    # 3. new-schema list -> legacy list
    if "attributes" in entity_nbt:
        legacy = _convert_new_attributes_to_legacy(entity_nbt["attributes"])
        entity_nbt["Attributes"] = legacy
        del entity_nbt["attributes"]
        changed = True
    # 4. legacy Attributes list but Names missing generic. prefix
    if "Attributes" in entity_nbt:
        for a in entity_nbt["Attributes"]:
            n = str(a.get("Name", ""))
            fixed = _legacy_attr_name(n)
            if fixed != n and n != "":
                a["Name"] = String(fixed)
                changed = True
    # 5. Strip fall_distance
    if "fall_distance" in entity_nbt:
        del entity_nbt["fall_distance"]
        changed = True
    # Recurse into passengers
    passengers = entity_nbt.get("Passengers")
    if passengers is not None:
        for p in passengers:
            if _fix_entity_attributes(p):
                changed = True
    # Recurse into spawner SpawnData / SpawnPotentials
    for k in ("SpawnData", "SpawnPotentials"):
        node = entity_nbt.get(k)
        if node is None:
            continue
        if isinstance(node, Compound):
            inner = node.get("entity")
            if inner is not None and _fix_entity_attributes(inner):
                changed = True
        elif isinstance(node, list):
            for item in node:
                inner = item.get("entity") if isinstance(item, Compound) else None
                if inner is not None and _fix_entity_attributes(inner):
                    changed = True
    return changed


def _fix_entities(nbt) -> int:
    entities = nbt.get("entities", [])
    changed = 0
    for e in entities:
        be = e.get("nbt")
        if be is None:
            continue
        if _fix_entity_attributes(be):
            changed += 1
    # Also scan block entities (spawners) at top level
    blocks = nbt.get("blocks", [])
    for b in blocks:
        be = b.get("nbt")
        if be is None:
            continue
        for k in ("SpawnData", "SpawnPotentials"):
            node = be.get(k)
            if node is None:
                continue
            if isinstance(node, Compound):
                inner = node.get("entity")
                if inner is not None and _fix_entity_attributes(inner):
                    changed += 1
            elif isinstance(node, list):
                for item in node:
                    inner = item.get("entity") if isinstance(item, Compound) else None
                    if inner is not None and _fix_entity_attributes(inner):
                        changed += 1
    return changed


# ---------------------------------------------------------------------------
# Driver
# ---------------------------------------------------------------------------

def main():
    totals = {"signs": 0, "books": 0, "entities": 0, "files": 0}
    for path in sorted(STRUCTURES_DIR.rglob("*.nbt")):
        try:
            nbt = nbtlib.load(str(path))
        except Exception as ex:
            print(f"  [SKIP]  {path.relative_to(STRUCTURES_DIR)}: {ex}")
            continue
        s = _fix_signs(nbt)
        bk = _fix_books(nbt)
        en = _fix_entities(nbt)
        if s or bk or en:
            nbt.save(str(path))
            totals["files"] += 1
            totals["signs"] += s
            totals["books"] += bk
            totals["entities"] += en
            print(f"  [FIX] {path.relative_to(STRUCTURES_DIR)}   signs={s} books={bk} entities={en}")
    print(
        f"\n{totals['files']} file(s) modified. "
        f"signs={totals['signs']} books={totals['books']} entities={totals['entities']}"
    )


if __name__ == "__main__":
    main()
