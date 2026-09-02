# Changelog

---

## [5.1.1] - 2026-09-02

### Fixed
- The Ocean Tower no longer crashes the game as it generates

### Changed
- The Ocean Tower now turns up in any ocean rather than only the deep ocean, and guardians defend it

---

## [5.1.0] - 2026-08-31

### Added
- Proper loot for the Ocean Tower and the Red Tower
- Golden apples, enchanted golden apples and iron blocks to rare chests
- Loot to the small oak pond
- More mobs across various structures
- Preview buttons for every structure in the Moog's Structure Library config screen

### Fixed
- The small ship now generates on water as it should
- The lil house, the second medium igloo and one cathedral corridor now generate
- Spruce dead trees, desert wells and snowy wells now generate
- Villagers are back in the barn, and every cart now carries a wandering trader
- Bees now stay at the bee dome instead of flying off the moment it generates
- Chests and barrels that were handing out the same fixed items now roll random loot again
- The Red Tower is far easier to find
- Books in lecterns are readable again, and mobs no longer throw errors
- The barn's lightning rod now looks right on older versions
- The pack now loads on Minecraft 26.1.2 and newer

### Changed
- Mobs are placed by the jigsaw system now, so they vary from structure to structure instead of being identical every time.
  - Villagers and wandering traders will always have fresh trades
  - Mobs with variants will spawn as a random variant for example, foxes, dogs, sheep etc
- Spawners fill themselves in when a structure generates, making them easily customisable through datapacks and more reliable across mc versions
- Armour stands turn up wearing random armour
- Rare chests hand out at most two diamond tools or armour pieces instead of loads
- The Ocean Tower is mostly prismarine now, with diamond blocks left as the rare highlight
- The Ocean Tower now sits partially buried instead of on top of terrain.
- Now requires Moog's Structure Library 3.0.0 or newer
- Grass blocks under structures swapped for structure voids so they blend into any biome
- Both cherry trees are built from natural blocks only
- Every structure has been rebuilt for each Minecraft version it supports, fixing a range of small visual and loading problems

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
