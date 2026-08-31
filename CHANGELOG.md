# Changelog

---

## [5.1.0] - 2026-08-31

### Fixed
- Added back villagers to barn, large_cart_1, large_cart_2

### Added
- Wired MSL config-screen previews via `mod_slug: voyager-structures` — MSL's Structures tab now shows an enabled Preview button for each MVS structure, opening `https://previews.moogsmods.com/voyager-structures/<mc>/<structure>`

---

## [5.0.8] - 2026-07-06

### Fixed
- Fixed crash when generating any of the new houses on 1.20.1 (diorite_and_deepslate_house, mud_brick_house_1, prismarine_house_1) - their sign block entities had bare empty `messages` list entries that the 1.20.1 sign codec parses as null, causing an NPE during chunk feature placement ([#85](https://github.com/Moog-s-Mods/MoogsVoyagerStructures/issues/85))
- Converted written book items in mud_brick_house_1 and lecturn_garden from the 1.20.5+ `components` schema to the legacy `tag` schema so their pages, title, and author actually load on 1.20.x
- Converted entity `attributes` list on strays, guardians, drowned, and the small_ship villager to the legacy `Attributes` schema so their custom health/speed/follow-range no longer silently drop on 1.20.x
- Stripped 1.21.5+ `fall_distance` float from mobs in prismarine_house_2 and ocean_tower (silently ignored pre-1.21.5)
- Fixed horse jump strength attribute id on horse_pen

---

## [5.0.7] - 2026-05-28

### Changed
- Removed mineshaft as it has been moved to MMR, [link](https://www.curseforge.com/minecraft/mc-mods/mmr-moogs-mineshafts-reimagined)
- Removed end scraps and end wells as they have been moved to MES, [link](https://www.curseforge.com/minecraft/mc-mods/moogs-end-structures)
- Removed grass blocks and dirt from lots of structures so they blend more in with various biomes

### Added
- Added houses:
    - diorite_and_deepslate_house
    - diorite_tower
    - mud_brick_house_1
    - prismarine_house_1
    - prismarine_house_2
---

## [5.0.6] - 2026-05-02

### Fixed
- Fixed crash when loading large warped tower or cathedral near spawn on Forge 1.20.1 - sign block entities in those structures were saved in a newer NBT format (DataVersion 4556) incompatible with 1.20.1's sign codec

---

## [5.0.5] - 2026-05-01

### Fixed
- Cherry, crimson, mangrove, and dark oak biome tags now resolve correctly on 1.20
- Fixed mineshaft generation
- Fixed cathedral generation
- Fixed large warped tower generation
- Compressed mod icon, reducing overall jar size
- replaced bogged with skeletons
- Replaced all `#c:` biome tags with custom `#mvs:` tags for correct biome resolution on both Fabric and Forge
- All empty and hardcoded containers now have loot tables assigned
- Added new `pond` and `end_scraps` loot tables

---
