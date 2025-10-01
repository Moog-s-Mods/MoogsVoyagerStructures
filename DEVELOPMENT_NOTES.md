## JAR Naming System Changes

### Changes Made
- **gradle.properties**: 
  - Added `minecraft_version_range`
- **build.gradle**: 
  - Set project version to `${rootProject.mod_version}-${rootProject.minecraft_version_range}`
- **fabric/build.gradle & neoforge/build.gradle**: 
  - Reset `archivesBaseName = "${rootProject.archives_base_name}"`
  - Set `archiveClassifier.set("fabric")` in fabric/build.gradle
  - Set `archiveClassifier.set("neoforge")` in neoforge/build.gradle

### Result
JARs are now named: `moogs_structures-<mod_version>-<minecraft_version_range>-<platform>.jar`

### To Apply to Other Branches
1. Add `minecraft_version_range=<start>-<end>` to `gradle.properties`
2. Set `mod_version=<semver>` (without MC version) in `gradle.properties`
3. Update root `build.gradle` version to `${rootProject.mod_version}-${rootProject.minecraft_version_range}`
4. Reset `archivesBaseName` in platform build files to just `${rootProject.archives_base_name}`
5. Set `archiveClassifier.set("fabric")` in fabric/build.gradle
6. Set `archiveClassifier.set("neoforge")` in neoforge/build.gradle

## Publishing Display Name Format

### Desired Format
When publishing to CurseForge/Modrinth, display names should use spaces and follow this pattern:
- `Moog's Structure Lib 1.0.1-1.20-1.20.4 [FABRIC]`
- `Moog's Structure Lib 1.0.1-1.20-1.20.4 [FORGE]`
- `Moog's Structure Lib 1.0.1-1.21.5-1.21.8 [NEOFORGE]`



