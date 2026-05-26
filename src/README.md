# src/ — Source Code Root

This directory contains all Python source code for the AI LaTeX CLI system.
It is organized into three sub-packages, each responsible for a distinct layer
of the application pipeline.

---

## Sub-Package Overview

```
src/
├── cli/        ← User-facing command layer (entry point)
├── api/        ← LLM communication layer (DeepSeek API client)
└── core/       ← Business logic layer (file system + LaTeX compiler)
```

---

## Package: `cli/`

**Role:** The outermost layer. Parses terminal commands, validates user input,
displays output, and delegates tasks to the `api` and `core` layers.

**Key file:** `cli/main.py`

This is where the `latex-ai` CLI command is defined. Every command a user types
(e.g., `latex-ai init`, `latex-ai edit`, `latex-ai compile`) is declared here.

→ See [`cli/README.md`](cli/README.md) for details.

---

## Package: `api/`

**Role:** The intelligence layer. Manages the connection to the DeepSeek API,
constructs structured prompts, sends requests, and returns LaTeX code or text
responses.

**Key file:** `api/deepseek.py`

All LLM interactions are centralized here. No other module talks to the API directly.

→ See [`api/README.md`](api/README.md) for details.

---

## Package: `core/`

**Role:** The execution layer. Handles everything that touches the file system
and the local LaTeX installation.

**Key files:**
- `core/fs_manager.py` — Reads templates, writes `.tex` files, applies edits
- `core/compiler.py` — Invokes `pdflatex`/`latexmk`, captures errors, triggers auto-fix

→ See [`core/README.md`](core/README.md) for details.

---

## Data Flow Through `src/`

```
Terminal Input
     │
     ▼
 cli/main.py          ← Parses command, extracts prompt & file args
     │
     ├──► api/deepseek.py     ← Sends prompt to DeepSeek, gets LaTeX back
     │         │
     │         ▼
     └──► core/fs_manager.py  ← Selects template, writes/patches .tex file
               │
               ▼
          core/compiler.py    ← Compiles .tex → .pdf, captures errors
               │
               ▼ (on error)
          api/deepseek.py     ← Sends error log back, gets corrected LaTeX
               │
               ▼
          core/fs_manager.py  ← Applies the fix to the .tex file
               │
               ▼
          core/compiler.py    ← Re-compiles → final PDF
```

---

## Package Initialization

Each sub-package contains an `__init__.py` file to make it importable as a Python module.
These files remain minimal (they do not import all symbols eagerly) to keep startup time fast.

---

## Coding Standards

All code in `src/` must:
- Use **Python type hints** on all function signatures
- Include **docstrings** on all public functions and classes
- Pass `black`, `isort`, `flake8`, and `mypy` checks (enforced by CI)
- Have corresponding unit tests in the `tests/` directory
