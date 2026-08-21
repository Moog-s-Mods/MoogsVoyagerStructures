# Changelog

---

## [5.0.15] - 2026-07-04

_Pending. Update this header date and replace this line with the actual changes before tagging._

### Fixed
- Added back villagers to barn, large_cart_1, large_cart_2
- Split books and entity equipment at the 1.21.5 encoding boundary via `versioned_single_pool_element` for sunzi_gate, mud_brick_house_1, lecturn_garden, prismarine_house_2, and ocean_tower — book pages/title (JSON-string vs SNBT compound) and entity gear (`ArmorItems`/`HandItems` vs `equipment`) now use format-correct variants on either side of 1.21.5

### Changed
- Version-gated barn's `oxidized_lightning_rod` (added in 1.21.9) via `versioned_single_pool_element`; pre-1.21.9 versions get the unoxidized `lightning_rod` variant

### Added
- Wired MSL config-screen previews via `mod_slug: voyager-structures` — MSL's Structures tab now shows an enabled Preview button for each MVS structure, opening `https://previews.moogsmods.com/voyager-structures/<mc>/<structure>`
- `supported_formats: [48, 107]` in `pack.mcmeta` so the pack loads under the strict schema on MC 26.1.2+

---

## [5.0.14] - 2026-06-21

### Changed
- mc 26.2 support
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

## [5.0.12] - 2026-05-22

_Pending. Update this header date and replace this line with the actual changes before tagging._

---

## [5.0.11] - 2026-05-22

### Changed
- Versioned structures now have a defined path for Minecraft 26.1–26.1.2, so the game stops logging "no version mapping matched" warnings and no longer falls back to an older structure template.

---

## [5.0.10] - 2026-05-11

### Changed
removed spawn overrides from mineshaft structure

---

## [5.0.9] - 2026-05-01

### Fixed
- `minecraft:iron_chain` replaced with `minecraft:chain` in pre-1.21.9 structure variants for azelea house, large floating island, large warped tower, big oak tree, small ship, and nether well

### Changed
- All empty and hardcoded containers now have loot tables assigned
- Added new `pond` and `end_scraps` loot tables

---

## [5.0.8] - 2026-04-20

### Fixed
- Cherry, crimson, mangrove, and dark oak biome tags now resolve correctly on 1.21.3-1.21.4

---

## [5.0.7] - 2026-04-20

### Fixed
- Mineshaft now generates properly

### Changed
- Mineshaft is now half as rare

---

## [5.0.6] - 2026-04-20

### Fixed
- Fixed chain renamed issues for 1.21.9+
- Fixed template pool elements using wrong type field (element_type)
- Repaired a few cathedral NBTs
- Repaired various structures
- Fixed mod icon not displaying in Mod Menu

### Changed
- Added description and links to mod metadata

---
