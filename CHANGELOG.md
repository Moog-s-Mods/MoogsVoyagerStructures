# Changelog

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
