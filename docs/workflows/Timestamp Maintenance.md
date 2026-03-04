---
title: Timestamp Maintenence
created: 2026-03-04T13:20
updated: 2026-03-04T13:20
tags:
  - documentation
  - automation
version:
status:
  - in progress
---
## Timestamp Maintenance Workflow

Automatically updates the `updated:` field in YAML frontmatter whenever documentation files are changed, ensuring metadata accuracy without relying on contributors to remember.

---

### Trigger

A push to the `main` branch (without `[skip-timestamp]` flag in the commit message).

---

### Process

1. GitHub Actions CI detects changed Markdown files
2. The `update_timestamps.py` script updates the `updated:` field in each changed file's YAML frontmatter
3. CI commits the changes back to the repository with `[skip-timestamp]` flag to prevent infinite loops
4. Site is rebuilt and redeployed to GitHub Pages

---

### Inputs

- Changed Markdown files in `docs/`
- Script path: `scripts/update_timestamps.py`
- GitHub Actions workflow: `.github/workflows/update-timestamps.yml`

---

### Outputs

- Updated `updated:` field in YAML frontmatter of changed files
- Automatic commit with `[skip-timestamp]` flag

---

### Without This

- Writers forget to update timestamps manually
- Dates become inaccurate or misleading
- Reviewers can't tell which docs were recently touched
- Documentation audits become unreliable

---

### Notes

- The `[skip-timestamp]` flag in commit messages prevents the workflow from triggering itself in a loop.
- This workflow runs as part of CI, not locally — contributors don't need to do anything.