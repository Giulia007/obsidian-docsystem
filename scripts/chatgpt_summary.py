#!/usr/bin/env python3

"""
chatgpt_summary.py

Generate an AI-written summary for a Markdown document.

This script:
- Reads YAML frontmatter and body from a Markdown file
- Sends the body to the OpenAI API
- Produces <filename>.summary.md next to the input file
- Preserves metadata and adds summary-specific fields

Usage:
    python scripts/chatgpt_summary.py <input_markdown_file>

API key:
    Store your OpenAI key as an environment variable named OPENAI_API_KEY.
    Windows (PowerShell):
        setx OPENAI_API_KEY "your-key-here"   # restart terminal
    macOS/Linux:
        export OPENAI_API_KEY="your-key-here"

Requirements:
    pip install openai pyyaml
"""

import os
import sys
import yaml
import argparse
from pathlib import Path
from openai import OpenAI
from dotenv import load_dotenv


print("[DEBUG] Script loaded")


# Load environment variables from .env file if present
load_dotenv()

API_KEY = os.getenv("OPENAI_API_KEY")

if not API_KEY:
    print("Error: OPENAI_API_KEY environment variable is not set.")
    sys.exit(1)

client = OpenAI(api_key=API_KEY)

# ------------------------------------------------------------
# Helpers
# ------------------------------------------------------------

def extract_frontmatter(path: Path):
    """Return (metadata_dict, body_text)."""
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()

    if not lines or not lines[0].strip() == "---":
        return {}, text

    # find closing delimiter
    try:
        end = lines[1:].index("---") + 1
    except ValueError:
        return {}, text

    yaml_block = "\n".join(lines[1:end])
    body = "\n".join(lines[end+1:])

    try:
        meta = yaml.safe_load(yaml_block) or {}
        return (meta if isinstance(meta, dict) else {}), body
    except yaml.YAMLError:
        return {}, body


def build_system_prompt():
    """Return a high-quality summarization prompt."""
    return (
        "You are a documentation engineer. Summarize the content of the "
        "Markdown document into a clean, structured technical summary. "
        "Your output MUST be Markdown. Avoid opinions. Keep it concise, "
        "informative, and suitable for a doc-as-code environment.\n\n"
        "Structure your output like this:\n\n"
        "## Overview\n"
        "- What the document covers\n\n"
        "## Key Points\n"
        "- Bullet list of essential concepts\n\n"
        "## Recommended Uses\n"
        "- Where this summary is useful\n"
    )


def call_model(body_text: str, model: str, max_tokens: int, temperature: float):
    """Send the content to OpenAI and return the summary text."""
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": build_system_prompt()},
            {"role": "user", "content": body_text},
        ],
        max_tokens=600,
        temperature=0.2,
    )
    return response.choices[0].message.content.strip()


def write_summary(output_path: Path, metadata: dict, summary_text: str, source_file: Path):
    """Write the summary Markdown file with YAML frontmatter."""
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # Build new frontmatter
    new_meta = metadata.copy()
    new_meta["generated"] = True
    new_meta["source"] = str(source_file.name)
    new_meta["type"] = "summary"

    yaml_block = yaml.safe_dump(new_meta, sort_keys=False).strip()

    with open(output_path, "w", encoding="utf-8") as f:
        f.write("---\n")
        f.write(yaml_block)
        f.write("\n---\n\n")
        f.write(summary_text)

    print(f"[INFO] Summary written to {output_path}")


# ------------------------------------------------------------
# Main
# ------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="Generate an AI summary for a Markdown document.")
    parser.add_argument("input_file", help="Path to the Markdown file to summarize.")
    parser.add_argument("--model", default="gpt-4o-mini", help="OpenAI model to use.")
    parser.add_argument("--max-tokens", type=int, default=600, help="Maximum tokens for the summary.")
    parser.add_argument("--temperature", type=float, default=0.2, help="Sampling temperature (0.0–1.0).")

    args = parser.parse_args()

    target_file = Path(args.input_file)
    if not target_file.exists():
        print(f"[ERROR] File not found: {target_file}")
        sys.exit(1)

    metadata, body = extract_frontmatter(target_file)

    # The model call now uses CLI parameters
    summary_text = call_model(body, args.model, args.max_tokens, args.temperature)

    output_path = target_file.with_suffix(".summary.md")
    write_summary(output_path, metadata, summary_text, target_file)

if __name__ == "__main__":
    main()
