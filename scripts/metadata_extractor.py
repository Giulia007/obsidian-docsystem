import os
import yaml
from datetime import date

DOCS_DIR = "docs"
OUTPUT_FILE = os.path.join("docs", "system", "auto-index.md")

def extract_yaml_metadata(path):
    """Extract YAML frontmatter from a Markdown file."""
    with open(path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    if not lines or not lines[0].startswith("---"):
        return {}

    yaml_block = []
    for line in lines[1:]:
        if line.startswith("---"):
            break
        yaml_block.append(line)

    try:
        return yaml.safe_load("".join(yaml_block)) or {}
    except yaml.YAMLError:
        return {}

def collect_documents():
    """Walk through the docs/ folder and collect metadata."""
    documents = []

    for root, _, files in os.walk(DOCS_DIR):
        for file in files:
            if file.endswith(".md") and file != "auto-index.md":
                full_path = os.path.join(root, file)
                meta = extract_yaml_metadata(full_path)

                documents.append({
                    "path": full_path.replace("\\", "/"),
                    "title": meta.get("title", file.replace(".md", "")),
                    "tags": meta.get("tags", []),
                    "status": meta.get("status", "unknown"),
                    "updated": meta.get("updated", "unknown")
                })

    return documents

def generate_index(docs):
    """Generate the Markdown index file."""
    today = str(date.today())

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write("---\n")
        f.write("title: Auto-Generated Index\n")
        f.write(f"updated: {today}\n")
        f.write("status: generated\n")
        f.write("---\n\n")

        f.write("# Documentation Index (auto-generated)\n\n")

        # Group by folder
        section_map = {}

        for doc in docs:
            directory = os.path.dirname(doc["path"]).replace("docs/", "")
            section_map.setdefault(directory, []).append(doc)

        for section, items in section_map.items():
            f.write(f"## {section}\n")
            for item in items:
                link = item["path"].replace("docs/", "../")
                f.write(f"- [{item['title']}]({link})\n")
                f.write(f"  - status: {item['status']}\n")
                f.write(f"  - updated: {item['updated']}\n")
                f.write(f"  - tags: {item['tags']}\n")
            f.write("\n")

def main():
    docs = collect_documents()
    generate_index(docs)
    print("auto-index.md generated successfully!")

if __name__ == "__main__":
    main()
