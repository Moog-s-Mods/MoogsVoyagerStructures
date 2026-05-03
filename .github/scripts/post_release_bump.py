#!/usr/bin/env python3
"""Insert a stub `## [NEW] - DATE` section at the top of CHANGELOG.md.

Reads NEW_VERSION and RELEASE_DATE from the environment. Inserts the stub
right after the first `# Changelog\n---` header. Falls back to prepending
if that header isn't found.

Called by .github/workflows/release.yml during the post-release bump step.
"""
import os
import re
import sys
from pathlib import Path

new_v = os.environ['NEW_VERSION']
today = os.environ['RELEASE_DATE']

stub = (
    f"## [{new_v}] - {today}\n\n"
    "_Pending. Update this header date and replace this line with the actual changes before tagging._\n\n"
    "---\n\n"
)

p = Path('CHANGELOG.md')
if not p.exists():
    print('CHANGELOG.md not found, skipping stub.', file=sys.stderr)
    sys.exit(0)

content = p.read_text(encoding='utf-8')

# Insert right after the first `# Changelog\n---` separator.
# \r?\n keeps the regex working when CHANGELOG.md is saved with Windows line endings.
match = re.search(r'# Changelog(?:\r?\n)+---(?:\r?\n)+', content)
if match:
    end = match.end()
    new_content = content[:end] + stub + content[end:]
else:
    # No standard header found - just prepend the stub
    new_content = stub + content

p.write_text(new_content, encoding='utf-8')
print(f'✓ stubbed CHANGELOG.md with ## [{new_v}] - {today}')
