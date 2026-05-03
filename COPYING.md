# Licensing

This project is **dual-licensed**. Different parts of the codebase fall under different licenses - please read carefully before redistributing or modifying.

## Code, configuration, and data files - LGPL-3.0

Everything **except `.nbt` structure files** is licensed under the **GNU Lesser General Public License v3.0**. This includes (non-exhaustive):

- All Java source code (if any)
- All JSON data (loot tables, worldgen, recipes, advancements, tags, biome/structure metadata, processor lists, template pools, etc.)
- All language files (`assets/{mod_id}/lang/*.json`)
- All build scripts (`build.gradle`, `settings.gradle`, `gradle.properties`, GitHub Actions workflows)
- All mod manifests (`fabric.mod.json`, `quilt.mod.json`, `META-INF/mods.toml`, `META-INF/neoforge.mods.toml`, `pack.mcmeta`)
- Documentation (`README.md`, `CHANGELOG.md`, this file)
- Python utility scripts under `scripts/`
- The validator config (`validator.json`)

See [`LICENSE`](LICENSE) for the full LGPL-3.0 text.

## Structure NBT files - All Rights Reserved

All `.nbt` files anywhere within this repository - including but not limited to `src/main/resources/data/{mod_id}/structure/` and `src/main/resources/data/{mod_id}/structures/` - are **© FinnDog (Moog)** and are **All Rights Reserved**.

These files **may not be**:

- Redistributed standalone or as part of another mod, modpack, datapack, or asset bundle
- Modified and republished
- Extracted from the compiled jar and reused
- Used in derivative works (including AI training datasets)
- Repackaged with attribution claiming origination

without **explicit written permission** from the copyright holder.

You **may**:

- Use the mod jar (which embeds these files) in any modpack or personal world, provided the jar itself is not modified
- Reference these structures in tutorials, videos, screenshots, or reviews under standard fair-use principles
- Fork this repository for the purpose of submitting pull requests back to the original

## Permission requests

For permission to use the structure files outside the scope above, contact:

- Discord: see `modDiscord` URL in `gradle.properties`
- GitHub: open an issue on this repository

## Why dual-license?

The code and data files are open so that the modding community can learn from them, contribute to them, and integrate with them. The structures themselves are creative works that took significant time to design - keeping them under ARR protects them from being lifted into competing mods or repackaged without attribution while still allowing the mod to be freely distributed and used.
