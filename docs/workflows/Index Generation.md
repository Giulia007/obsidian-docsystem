---
title: Index Generation
created: 2026-03-04T13:42
updated: 2026-03-04T17:55
tags:
- documentation
- automation
version: null
status:
- in progress
---


## Index Generation Workflow

Generates `auto-index.md` — a navigable index of all documentation files, grouped by section, with metadata displayed for each entry.

---

### Purpose

Manually maintaining index pages is tedious and error-prone. As documentation grows, indexes drift out of sync with actual content. This script generates the index automatically from YAML frontmatter, ensuring navigation always reflects the current state of the documentation.

---

### Usage

Run from the repository root, with the Python virtual environment activated:
```bash
python scripts/metadata_extractor.py
```

---

### What It Does

1. Scans all Markdown files in `docs/` (excluding `auto-index.md` itself)
2. Reads YAML frontmatter from each file (title, status, tags, updated, version)
3. Groups files by section (API, System, Workflows, Templates)
4. Outputs `docs/system/auto-index.md`

---

### Output

The generated `auto-index.md` includes:

- Document title (linked)
- Status, last updated date, version (if present)
- Tags

Example entry:
```
- [System Architecture Overview](system/System Architecture Overview.md) — status: `in progress` · updated: `2025-03-04` · tags: `documentation`
```

---

### When to Run

Run this script before committing when you've:

- Added new documentation files
- Deleted or renamed files
- Changed a document's title or tags

---

### Notes

- The script does not auto-commit — you decide when to commit the regenerated index.
- The output file's status is set to `generated` automatically.