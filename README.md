# Obsidian Documentation System

A doc-as-code documentation system demonstrating modern technical writing workflows. Built with Obsidian, MkDocs Material, and GitHub Actions.

**Live site:** [https://giulia007.github.io/obsidian-docsystem/](https://giulia007.github.io/obsidian-docsystem/)

---

## What This Is

This is a portfolio project showcasing documentation system thinking — how content types, folder structures, metadata conventions, and automation work together to create something maintainable.

The system documents itself: the documentation you see *is* the portfolio.

---

## Tech Stack

- **Authoring:** Obsidian (Markdown + YAML frontmatter)
- **Publishing:** MkDocs Material
- **Hosting:** GitHub Pages
- **CI/CD:** GitHub Actions
- **Automation:** Python scripts for indexing, timestamps, and AI summaries

---

## Project Structure
```
├── docs/                   # Documentation content (published via MkDocs)
│   ├── system/             # Architecture, conventions, MOC
│   ├── workflows/          # Process documentation
│   └── api/                # API endpoint documentation
├── scripts/                # Python automation tools
│   ├── metadata_extractor.py   # Generates auto-index.md
│   ├── update_timestamps.py    # Updates YAML timestamps (CI)
│   └── chatgpt_summary.py      # AI-generated summaries
├── api/                    # FastAPI metadata endpoint
├── assets/                 # Diagrams and images
├── templates/              # Obsidian document template
└── .github/workflows/      # CI/CD configuration
```

---

## Setup

### Prerequisites

- Python 3.9+
- Git

### Installation

1. Clone the repository:
```bash
   git clone https://github.com/Giulia007/obsidian-docsystem.git
   cd obsidian-docsystem
```

2. Create and activate virtual environment:
   
   **Windows (PowerShell):**
```powershell
   python -m venv venv
   .\venv\Scripts\Activate.ps1
```

   **macOS/Linux:**
```bash
   python -m venv venv
   source venv/bin/activate
```

3. Install dependencies:
```bash
   pip install -r requirements.txt
```

---

## Running the Scripts

All scripts should be run from the repository root with the virtual environment activated.

### Generate Documentation Index
```bash
python scripts/metadata_extractor.py
```

Outputs `docs/system/auto-index.md` — a navigable index of all documentation files.

### Run Metadata API Locally
```bash
uvicorn api.metadata_api:app --reload
```

Access at [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) for interactive Swagger UI.

### Generate AI Summary (requires OpenAI API key)
```bash
export OPENAI_API_KEY="your-key-here"  # macOS/Linux
setx OPENAI_API_KEY "your-key-here"    # Windows (restart terminal)

python scripts/chatgpt_summary.py docs/path/to/file.md
```

---

## Local Development

To preview the documentation site locally:
```bash
pip install mkdocs-material
mkdocs serve
```

View at [http://127.0.0.1:8000](http://127.0.0.1:8000)

---

## CI/CD

On every push to `main`:

1. **Timestamp Updater** — Automatically updates the `updated:` field in changed Markdown files
2. **MkDocs Build** — Rebuilds and deploys the site to GitHub Pages

Note: Always run `git pull origin main` before starting work, as CI pushes commits after your push.

---

## License

This project is for portfolio and demonstration purposes.
