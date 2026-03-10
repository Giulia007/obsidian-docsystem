---
title: Timestamp Maintenance
created: 2026-03-04T13:20
updated: 2026-03-10T12:46
tags:
- documentation
- automation
version: null
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

---

## Working with Automated Commits

The timestamp updater pushes a commit to `main` after your push. This means the remote repository will be one commit ahead of your local copy immediately after you push.

### Why This Matters

If you start a new work session without pulling first, your local branch will be behind the remote. When you try to push later, Git will reject it and ask you to pull. This can lead to merge conflicts — especially if you've deleted or renamed files that the CI modified.

### Best Practice

**Always pull before starting work:**
```bash
git pull origin main
```

Run this at the start of every work session, before making any changes.

### If You Forget to Pull 
If you commit locally and then push fails with "rejected... fetch first":
```bash git pull origin main ``` 

If it opens Vim for a merge message:
- Press `Esc`, type `:wq`, press `Enter`
- Then push: ```bash git push origin main ```

### Resolving Common Conflicts

If you see a conflict like this:
```
Unmerged paths:
  deleted by us:   docs/some-file.md
```

This means:
- You deleted the file locally
- The CI updated its timestamp on the remote before you pulled

To resolve, confirm the deletion:
```bash
git rm "docs/some-file.md"
git commit -m "Merge remote changes, keep local deletions"
git push origin main
```

### Alternative Approaches

In a team context, other approaches can reduce these sync issues:

- **Feature branches** — Work on a branch, merge to `main` when ready. CI only runs on `main`, so your branch stays unaffected.
- **Pre-commit hooks** — Update timestamps locally before committing, removing the need for CI to push back.
- **Pull with rebase** — `git pull --rebase origin main` keeps history linear by placing your commits after CI commits.

***