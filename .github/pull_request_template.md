# Summary

<!-- One or two sentences describing the change. -->

## Type of change

<!-- Check all that apply. -->

- [ ] Bug fix (non-breaking change which fixes an issue)
- [ ] New structure
- [ ] Loot table change
- [ ] Worldgen / biome / placement tweak
- [ ] Build / CI / tooling change
- [ ] Documentation
- [ ] Other:

## Checklist

- [ ] If I added a structure, the corresponding template pool / structure set / processor list / loot table references are in place.
- [ ] If I changed loot tables, I verified containers in affected structures actually reference the right tables (`python scripts/fix_loot.py` if needed).
- [ ] I added an entry to `CHANGELOG.md` under an unreleased version section.
- [ ] The CI build passed locally (`./gradlew build`).
- [ ] I have NOT redistributed any existing `.nbt` files outside this repo (they're All Rights Reserved; see `COPYING.md`).

## Testing

<!-- Describe how you tested this change. Which Minecraft versions, which loaders, what specific structures or loot tables, what coordinates / seeds, etc. -->

## Screenshots / videos

<!-- Optional but very welcome for new structures or visual changes. -->

## Related issue

<!-- "Closes #123" or "Refs #123" if applicable. -->
