#!/usr/bin/env python3
"""
metadata_extractor.py

Scan all Markdown files under the docs/ folder, extract YAML frontmatter,
and generate an auto-index page grouped by top-level section.

Part of the technical documentation system portfolio.

Features:
- Reads YAML frontmatter from Markdown files
- Groups docs by top-level section
- Produces auto-index.md with metadata overview
- Built for doc-as-code workflows (Obsidian + MkDocs)
- Easily extendable for CI-based updates

Requirements:
    pip install pyyaml
"""

import os
import yaml
from datetime import date

DOCS_DIR = "docs"
OUTPUT_FILE = os.path.join("docs", "system", "auto-index.md")

SECTION_NAMES = {
    "api": "API Documentation",
    "system": "System Documentation",
    "workflows": "Workflow Documentation",
    "templates": "Templates",
    "": "General"
}

def extract_yaml_metadata(path):
    """Extract YAML frontmatter from a Markdown file."""
    with open(path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    if not lines or not lines[0].strip() == "---":
        return {}

    yaml_block = []
    for line in lines[1:]:
        if line.strip() == "---":
            break
        yaml_block.append(line)

    try:
        data = yaml.safe_load("".join(yaml_block)) or {}
        return data if isinstance(data, dict) else {}
    except yaml.YAMLError:
        return {}

def collect_documents():
    """Walk through docs/ and collect metadata from Markdown files."""
    documents = []

    for root, _, files in os.walk(DOCS_DIR):
        for file in files:
            if file.endswith(".md") and file not in ["auto-index.md"]:
                full_path = os.path.join(root, file)
                meta = extract_yaml_metadata(full_path)
                rel_path = full_path.replace("\\", "/").replace(f"{DOCS_DIR}/", "")

                documents.append({
                    "path": rel_path,  # relative within docs/
                    "title": meta.get("title") or file.replace(".md", "").replace("-", " ").title(),
                    "status": meta.get("status", "draft"),
                    "updated": meta.get("updated", "n/a"),
                    "version": meta.get("version", ""),
                    "tags": meta.get("tags") if meta.get("tags") else [],
                    "section": rel_path.split("/")[0] if "/" in rel_path else ""
                })

    return documents

def generate_index(docs):
    """Generate the Markdown auto-index file, grouped by sections."""
    today = str(date.today())

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        # --- Frontmatter ---
        f.write("---\n")
        f.write("title: Auto-Generated Index\n")
        f.write(f"updated: {today}\n")
        f.write("status: generated\n")
        f.write("type: index\n")
        f.write("---\n\n")

        f.write("# Documentation Index\n\n")
        f.write("> This page is generated automatically from YAML metadata.\n\n")

        # --- Group documents ---
        section_map = {}

        for doc in docs:
            section_map.setdefault(doc["section"], []).append(doc)

        # Sort sections alphabetically
        for section in section_map:
            section_map[section] = sorted(
                section_map[section], key=lambda x: x["title"].lower()
            )
        # --- Write sections ---
        for section, items in sorted(section_map.items(), key=lambda x: x[0]):
            section_title = SECTION_NAMES.get(section, section.replace("-", " ").title())

            f.write(f"## {section_title}\n\n")

            for item in items:
                url = item["path"]
                tags = ", ".join(f"`{t}`" for t in item["tags"]) if item["tags"] else "`none`"

                meta_summary = (
                    f"status: `{item['status']}` · "
                    f"updated: `{item['updated']}`"
                )

                if item["version"]:
                    meta_summary += f" · version: `{item['version']}`"

                meta_summary += f" · tags: {tags}"

                f.write(f"- [{item['title']}]({url}) — {meta_summary}\n")
            f.write("\n")

def main():
    docs = collect_documents()
    generate_index(docs)
    print("auto-index.md generated successfully!")

if __name__ == "__main__":
    main()
