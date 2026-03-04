---
title: System Architecture Overview
created: 2025-12-21T19:05
updated: 2025-12-21T19:05
tags:
  - documentation
version:
status:
---
## 1.?
### 1.1 Purpose of the Document

This document provides a high-level overview of the project, outlining the directory structure, the main categories of documents, and how they relate to the publishing and updating workflow.
It is intended as a non-technical snapshot of the system as it currently stands.

The goal is to support onboarding and future development by clarifying how the different components—Obsidian, Git, MkDocs, GitHub Pages, and GitHub Actions—interact within the larger documentation workflow. By describing these connections explicitly, the document offers a stable reference for maintaining, extending, or modifying the system over time.

#### 1.2 Previous Knowledge Assumptions

Readers do not need a deep technical background to understand this document. References to Git, static site generators, and CI/CD pipelines are kept at a conceptual level, so those new to these tools can still follow the architectural overview.  
For contributors who plan to modify or extend the system, a basic familiarity with Markdown and Git will eventually be required.

#### 1.3 System Overview

Manual documentation approaches become difficult to maintain and share as complexity grows. This system establishes a structured, extensible baseline that supports automation, consistency, and collaborative evolution over time.

At a high level, this project is a doc-as-code documentation system that combines an Obsidian authoring vault, a Git/GitHub repository, MkDocs Material, and a GitHub Actions pipeline.

The same content is used to build and deploy a public documentation site to GitHub Pages on each push to the main branch. For brevity, this branch is referred to as “main” throughout this document.

#### 1.3.1 System at a Glance

Components and Interactions
- Source of truth: GitHub repository mirroring the local Obsidian vault
- Authoring tool: Obsidian vault with structured folders, templates with YAML frontmatter
- Automation scripts: Python-based automations handling indexing, AI-generated summaries, and frontmatter timestamp updates
- CI/CD pipeline: GitHub Actions workflow that builds and deploys the site to GitHub Pages on every push to main.

### 1.4 System Components
    
#### 1.4.1 Obsidian Vault

The local directory of Markdown files used as the primary authoring environment for documentation content. Its role in the system is to support drafting, structuring, and maintaining documentation, before content is processed by version control, automation, and publishing workflows. 

Writers create and edit Markdown files using templates with YAML frontmatter, ensuring that each document carries consistent metadata required by downstream scripts and CI pipelines. 

The vault itself resides locally and corresponds directly to the working directory of the Git repository.

#### 1.4.2 Git and GitHub Repository

The GitHub repository is the remote version-controlled repository that stores the system’s documentation, configuration files, and automation code. It provides the shared remote location from which automation and publishing processes operate.

#### 1.4.3 MkDocs and Site Generation

MkDocs is a static site generator for building documentation websites from Markdown files. In this system, it is defined through configuration and used to generate the documentation site published via GitHub Pages.

#### 1.4.4 GitHub Actions and CI

GitHub Actions is GitHub’s built-in automation and continuous integration service. In this system, it provides the environment in which automated tasks are executed in response to changes in the repository.

#### 1.4.5 Automation Scripts

Automation scripts are custom Python programs maintained as part of the system to perform operations on documentation files and metadata. They encapsulate system-specific logic and are executed either locally or within automated processes.


##  2. Workflows

### 2.1 System-driven documentation maintenance

**Trigger**  
A commit is pushed to the main branch.

**Behavior**  
Commits to the main branch trigger a rebuild and redeployment of the documentation site to GitHub Pages.

**Outcome**  
The published documentation on GitHub Pages reflects the updated repository state.


### 2.2 AI-assisted documentation summarization

**Trigger**

A contributor runs `chatgpt_summary.py` on a Markdown file ready for summarization.

**Process** Steps

1. The script reads the Markdown file and extracts YAML frontmatter and body.
    
2. Content is sent to the OpenAI API for summarization.
    
3. The API response is written as a new `*.summary.md` file.
    
4. Original metadata is propagated to the new file.
    
5. The generated summary enters version control and can be indexed or published via MkDocs.
    

**Inputs**

- Markdown file (`docs/...`)
    
- YAML metadata fields (`title`, `tags`, `updated`)
    
- `scripts/chatgpt_summary.py`
    

**Outputs**

- AI-generated `*.summary.md` file with consistent metadata
    
- Added to `auto-index.md` during the next index generation

    
**Notes**

For detailed usage instructions, see [[.....]]



****