# 🗺️ ARCHITECTURE.md — AI LaTeX CLI System Design

## Project Overview

AI LaTeX CLI is a terminal-based tool that converts natural language prompts into real LaTeX documents and compiled PDFs.

The user interacts with the system entirely through terminal commands. The CLI sends prompts to the LLM, receives generated LaTeX code, edits actual files in the workspace, and compiles them into PDFs.

The system supports:
- generating documents
- editing existing files
- mixing AI-generated and manually written content
- compiling LaTeX projects
- fixing compile issues
- creating structured project files

---

# Core System Flow

## 1. User Interaction Layer (`src/cli/main.py`)

This is the terminal interface of the project.

It:
- accepts commands from the user
- reads prompts
- validates input
- routes actions to other modules
- displays terminal output and errors

Example responsibilities:
- `init`
- `edit`
- `compile`
- `fix`
- `table`
- `rewrite`

This layer does not generate LaTeX itself. It only manages command flow.

---

# 2. AI Generation Layer (`src/api/deepseek.py`)

This module connects the project to DeepSeek APIs.

Its job is to:
- send prompts to the model
- provide context from existing files
- receive generated LaTeX
- return structured output back to the CLI

The model is instructed to:
- output only raw LaTeX
- avoid markdown formatting
- preserve document structure
- follow formatting consistency

When editing files, the existing `.tex` content is also sent as context so the AI understands the current document before modifying it.

This allows:
- partial rewrites
- section editing
- formatting preservation
- hybrid AI/manual workflows

---

# 3. File Management Layer (`src/core/fs_manager.py`)

This module manages all local workspace files.

It is responsible for:
- reading `.tex` files
- writing generated content
- updating sections
- creating project files
- managing templates
- handling backups

The system edits real files directly inside the repository so users can immediately see changes in their editor.

The file manager supports:
- replacing sections
- appending content
- rewriting paragraphs
- inserting tables
- inserting equations
- generating new files

---

# 4. Compilation Layer (`src/core/compiler.py`)

This module handles LaTeX compilation.

It:
- runs `latexmk` or `pdflatex`
- captures terminal logs
- detects compile failures
- returns generated PDFs

If compilation fails:
- logs are parsed
- errors are extracted
- the logs can be sent back to the LLM
- corrected LaTeX is written back to the file
- compilation is attempted again

Compiled PDFs are stored in the `outputs/` directory.

---

# Template System

The project includes predefined LaTeX templates stored inside `templates/`.

These templates reduce generation overhead and maintain consistent formatting.

Examples:
- standard article
- IEEE paper
- presentation

The CLI can automatically choose templates based on keywords inside prompts.

---

# Hybrid Workflow

One of the main goals of the project is supporting both:
- AI-generated content
- raw user-written content

Users are not forced into fully AI-generated documents.

They can:
- manually write LaTeX
- partially edit files using prompts
- rewrite only specific sections
- combine manual and AI workflows together

The system behaves more like an intelligent editor instead of a one-click generator.

---

# File Editing Philosophy

The project focuses heavily on controlled editing instead of blindly overwriting files.

Edits should:
- preserve formatting
- avoid deleting unrelated sections
- maintain package consistency
- avoid breaking structure

The system should modify only the relevant portions of a file whenever possible.

---

# Error Handling

Compilation errors are treated as structured feedback.

The compiler module:
- captures logs
- identifies failing lines
- extracts error messages
- exposes them to the CLI

These logs can also be passed back into the AI generation layer to help repair broken LaTeX automatically.

---

# Outputs

Generated outputs include:
- `.tex` files
- project folders
- compiled PDFs
- logs
- temporary build files

Final PDFs are stored in:

```text
outputs/
```

---

# Design Goals

The project is built around these principles:

- terminal-first workflow
- real editable files
- structured LaTeX generation
- beginner-friendly automation
- hybrid AI/manual editing
- fast document iteration
- minimal manual formatting work

The overall goal is to make professional LaTeX document creation easier through prompting while still keeping the workflow transparent and editable.