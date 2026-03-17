---
title: Design Decisions
created: 2026-03-17T12:09
updated: 2026-03-17T12:09
tags:
  - documentation
version:
status: published
---
# Design Decisions

## Why These Tools

This system uses Obsidian as the authoring environment. It's a personal choice — Obsidian is my current knowledge management tool, and using it here reflects a real-world scenario where documentation systems are built around existing workflows. For a team context, tools like Confluence, Notion, or GitBook would likely be more suitable.

MkDocs Material was chosen after a brief comparison of static site generators. It's widely used, well-documented, and commonly seen in professional documentation workflows — which made it a practical choice for a portfolio project.

## Why This Structure

The folder structure — System, Workflows, Templates, API — emerged partly from convention and partly from iteration. Templates and API are standard categories in most documentation systems. System holds the architectural overview. Workflows was added to separate _how things work_ from _what things are_.

The structure groups content by purpose — a logical choice that makes navigation intuitive for different types of readers.

## Why YAML Frontmatter

Every Markdown file includes YAML frontmatter with fields like title, tags, status, and timestamps. This serves several purposes:

- **Search and retrieval** — tags and titles make content findable
- **Automation** — scripts can read and update metadata without parsing the document body
- **Maintainability** — status fields (such as _draft_, _in-progress_, _to-review_, _published_) make it easy to see what's ready, what needs work, and what's outdated. Timestamps show when a document was last updated. Together, these fields support triage and prioritisation without needing to open every file.

Without this kind of consistent metadata, small gaps accumulate and documentation becomes unreliable over time. Frontmatter is a small upfront investment that keeps the system healthy.

## Why Automate

The automation scripts handle indexing, timestamp updates, and summary generation. These tasks are repetitive, easy to forget, and error-prone when done manually.

Automating them reduces risk and keeps the system consistent — without relying on contributors to remember every step.

Not everything is automated, though. Index generation runs locally and requires a manual commit — because changes to the index affect navigation and visibility, and that deserves a human decision. The principle: automate the mechanical, keep control over the editorial.