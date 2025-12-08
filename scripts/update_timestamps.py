#!/usr/bin/env python3
"""
update_timestamps.py

Update the `updated:` field in the YAML frontmatter of Markdown files.

This script is used by GitHub Actions to automatically update timestamps
ONLY for Markdown files that changed in the last commit (Option B).

Usage:
    python update_timestamps.py <file1.md> <file2.md> ...

Notes:
- If a file has no YAML frontmatter, a block will be created.
- If `updated:` exists, it will be overwritten.
- If the file is not a Markdown file, it is ignored silently.
"""

import sys
from datetime import date
from pathlib import Path
import yaml

FRONTMATTER_DELIMITER = "---"


def update_frontmatter(path: Path) -> bool:
    """
    Update or insert the `updated:` field in the YAML frontmatter.
    Returns True if the file was modified, False otherwise.
    """
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()

    today = str(date.today())
    modified = False

    # Case 1 — file already has YAML frontmatter
    if lines and lines[0].strip() == FRONTMATTER_DELIMITER:
        try:
            end_index = lines[1:].index(FRONTMATTER_DELIMITER) + 1
        except ValueError:
            # malformed frontmatter — ignore file
            return False

        yaml_block = "\n".join(lines[1:end_index])
        body = "\n".join(lines[end_index + 1:])

        try:
            meta = yaml.safe_load(yaml_block) or {}
            if not isinstance(meta, dict):
                return False
        except yaml.YAMLError:
            return False

        # Update or insert the updated field
        if meta.get("updated") != today:
            meta["updated"] = today
            modified = True

        # Write the updated file only if needed
        if modified:
            new_yaml = yaml.safe_dump(meta, sort_keys=False).rstrip()
            new_content = (
                FRONTMATTER_DELIMITER + "\n" +
                new_yaml + "\n" +
                FRONTMATTER_DELIMITER + "\n\n" +
                body
            )
            path.write_text(new_content, encoding="utf-8")

        return modified

    # Case 2 — no frontmatter, create a YAML block
    meta = {"updated": today}
    new_yaml = yaml.safe_dump(meta, sort_keys=False).rstrip()
    body = text.strip()

    new_content = (
        FRONTMATTER_DELIMITER + "\n" +
        new_yaml + "\n" +
        FRONTMATTER_DELIMITER + "\n\n" +
        body + "\n"
    )
    path.write_text(new_content, encoding="utf-8")
    return True


def main():
    if len(sys.argv) < 2:
        print("[INFO] No files provided for timestamp update. Exiting.")
        return 0

    changed_files = [Path(p) for p in sys.argv[1:]]

    modified_any = False

    for file in changed_files:
        if file.suffix != ".md":
            continue
        if file.exists():
            if update_frontmatter(file):
                print(f"[INFO] Timestamp updated in {file}")
                modified_any = True

    if not modified_any:
        print("[INFO] No timestamps updated.")

    return 0


if __name__ == "__main__":
    sys.exit(main())
