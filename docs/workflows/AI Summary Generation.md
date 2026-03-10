---
title: AI Summary Generation
created: 2025-12-21T17:40
updated: 2026-03-04T17:55
tags:
- documentation
version: null
status: in progress
---


## AI Summary Generation Workflow

Generates concise, standardised summaries from Markdown files using a local Python script connected to the OpenAI API.

---

### Prerequisites

- Python 3.9+ installed
    
- `OPENAI_API_KEY` set as an environment variable
    
- Dependencies installed (`pip install -r requirements.txt`)
    
- Source Markdown file located under `docs/`
    
---

### Usage

Run from the repository root:

```
python scripts/chatgpt_summary.py docs/system/architecture.md
```

Optional parameters:

```
--model gpt-4o-mini
--max-tokens 800
--output-dir docs/system/summaries/
```

---

### Process Summary  
Generates a summarized version of the document while preserving metadata for provenance and version tracking.

---

### Inputs

- Markdown file in `docs/`
    
- YAML metadata fields (`title`, `tags`, `status`, `created`, `updated`, `version`)
    
- Script path: `scripts/chatgpt_summary.p`
    

---

### Outputs

- `<filename>.summary.md` created in the same directory as the source file
    
- Original YAML frontmatter is preserved with an additional `generated: true` field
    
- Included in `auto-index.md` on next regeneration
    

---

### Example

Input:  
`docs/system/architecture.md`

Output:  
`docs/system/architecture.summary.md`

---

### Notes
    
- Ensure the OpenAI API key is configured in your environment before execution.
    
- The generated file is committed manually, to maintain transparency in version control.
    

---