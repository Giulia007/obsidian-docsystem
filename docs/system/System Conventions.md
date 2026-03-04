---
title: System Conventions
created: 2025-12-21T18:17
updated: 2026-03-04T17:50
tags:
- documentation
version: null
status:
- draft
---

### File Naming

- Markdown files use **Title Case with spaces** (e.g., `System Architecture Overview.md`) for readability in Obsidian.
- Scripts and configuration files use **snake_case** (e.g., `metadata_extractor.py`) for alignment with coding standards.

---

### Links

- **Internal links:**  
    Use standard Markdown syntax with relative paths:
    
    `[AI Summary Generation](../workflows/AI%20Summary%20Generation)`
    
    Works in MkDocs and on GitHub.  
    `%20` replaces spaces in filenames.  
    Omit `.md` for cleaner URLs in MkDocs.
    
- **Obsidian use:**  
    Wikilinks (`[[AI Summary Generation]]`) work only inside Obsidian and are ignored by MkDocs and GitHub.  
    Replace them with standard Markdown links in any file published to the site.
    
- **External links:**  
    Use full `https://` URLs and descriptive link text.
    

---

### Status Field

Defines the lifecycle stage of each document within the documentation system.

|Value|Meaning|Typical Location|Managed by|
|---|---|---|---|
|**draft**|Temporary state for early or incomplete files not yet pushed to `main`. Drafts may later be promoted to `in progress`.|Local vault or feature branch|Manual|
|**in progress**|Committed to `main` and therefore automatically published, but still being refined.|Repository (`main`)|Manual|
|**generated**|Created automatically by a script (e.g., summaries, index pages).|Repository (`main`)|Automation|

**Usage rules**

- Every Markdown file must include a `status` field in its YAML frontmatter.
    
- Files marked `draft` are local or branch-bound and excluded from deployment until committed.
    
- Files marked `in progress` or `generated` are deployed automatically with each push to `main`.
    
- Status values are not changed automatically by CI; they are updated manually or by scripts when applicable.
- Status values are updated manually by the author. CI does not modify the `status` field (future implementation).

---

### Creating New Documents

New documentation files should be created using the `standard-doc` template located in `templates/standard-doc.md`. This template includes the required YAML frontmatter fields:

- `title`
- `created`
- `updated`
- `tags`
- `status`
- `version`

In Obsidian, use **Alt + T** to insert the template when creating a new file (requires the Templater plugin).