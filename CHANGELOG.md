# Changelog

---

## [5.0.8] - 2026-07-04

_Pending. Update this header date and replace this line with the actual changes before tagging._

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
