# CONTRIBUTING.md — Contribution Guidelines

Thank you for your interest in contributing to the AI LaTeX CLI project.
This document defines the standards, workflow, and expectations for all contributors.

---

## Table of Contents

1. [Code of Conduct](#code-of-conduct)
2. [Getting Started](#getting-started)
3. [Branching Strategy](#branching-strategy)
4. [Development Workflow](#development-workflow)
5. [Pull Request Rules](#pull-request-rules)
6. [Coding Standards](#coding-standards)
7. [Testing Requirements](#testing-requirements)
8. [Documentation Requirements](#documentation-requirements)
9. [Commit Message Format](#commit-message-format)
10. [Issue Reporting](#issue-reporting)

---

## Code of Conduct
try to learn as much as possible 
use llms to understand the parts that are confusing 
let other contributors know if you face any challenges
---

## Getting Started

### 1. Fork and Clone

```bash
git clone https://github.com/Nimish-Sharma-dev/ai-latex-cli.git
cd ai-latex-cli
```

### 2. Set Up the Development Environment

```bash
# Create a virtual environment
python -m venv venv
source venv/bin/activate       # Linux/macOS
# venv\Scripts\activate        # Windows

# Install in editable mode with all dev dependencies
pip install -e .
pip install -r requirements.txt
```

### 3. Configure Environment

```bash
cp .env.example .env
# Edit .env and add your DEEPSEEK_API_KEY
```

### 4. Verify Setup

```bash
# Run the test suite
pytest tests/

# Verify CLI is working
latex-ai --help
```

---

## Branching Strategy

We use a simplified **Git Flow** model:

```
main              ← Protected. Production-ready only. Requires PR + review.
  └── develop     ← Integration branch. All features merge here first.
        ├── feature/your-feature-name
        ├── fix/issue-description
        └── docs/what-you-are-documenting
```


**Never commit directly to `main` **

---

## Development Workflow

1. **Create a branch** from `develop`:
   ```bash
   git checkout develop
   git pull origin develop
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes** following the coding standards below.

3. **Run quality checks locally** before pushing:
   ```bash
   black src/
   isort src/
   flake8 src/
   mypy src/
   pytest tests/ --cov=src
   ```

4. **Push your branch** and open a Pull Request on github.

---

## Pull Request Rules

Every PR must:

- [ ] Target the `develop` branch (not `main`)
- [ ] Have a descriptive title: `telling about what you have built`
- [ ] Include a description explaining: what was changed, why, and how to test it
- [ ] Pass all CI checks (lint, type check, unit tests, template compilation)
- [ ] Not reduce code coverage below the current threshold

**PR descriptions should answer:**
- What problem does this solve?
- Are there any known limitations or edge cases that are causing troubles?
- anything else that is imp to

---


### Language & Version

- Python 3.10+ required
- All new code must be compatible with Python 3.10, 3.11, and 3.12

### Type Hints

All public functions must have complete type annotations:

```python
# ✅ Correct
def select_template(prompt: str) -> Path:
    ...

# ❌ Wrong — missing types
def select_template(prompt):
    ...
```

### Docstrings

All public functions and classes must have docstrings following this format:

```python
def compile(path: Path) -> CompileResult:
    """
    Compile a LaTeX file to PDF using latexmk or pdflatex.

    Attempts latexmk first; falls back to pdflatex if unavailable.
    On failure, returns a CompileResult with structured error information.

    Args:
        path: Absolute or relative path to the .tex file to compile.

    Returns:
        CompileResult dataclass with success status, PDF path, errors, and raw log.

    Raises:
        FileNotFoundError: If the specified .tex file does not exist.
        CompilerNotFoundError: If neither latexmk nor pdflatex is on PATH.
    """
```


---

## Testing Requirements

### Test Location

All tests live in `tests/`. Mirror the `src/` structure:

```
tests/
├── test_cli.py           # Tests for src/cli/main.py
├── test_deepseek.py      # Tests for src/api/deepseek.py
├── test_fs_manager.py    # Tests for src/core/fs_manager.py
└── test_compiler.py      # Tests for src/core/compiler.py
```


### Mocking Policy
- (very important)
- All tests for `src/api/deepseek.py` must mock the DeepSeek API — no real API calls in unit tests
- All tests for `src/core/compiler.py` must mock `subprocess` — no real `pdflatex` calls in unit tests
- Integration tests (real API calls, real compilation) are tagged `@pytest.mark.integration` and run only on `main` branch merges

### Running Tests

```bash
# All tests
pytest tests/

# Unit tests only (no integration)
pytest tests/ -m "not integration"

# With coverage report
pytest tests/ --cov=src --cov-report=html
open htmlcov/index.html
```

---

## Documentation Requirements

- Any new command added to `src/cli/main.py` must be documented in `docs/COMMAND_REFERENCE.md`
- Any new template added to `templates/` must be documented in `templates/README.md`
- Any significant architectural change must be reflected in `docs/ARCHITECTURE.md`
- All new source files must have a module-level docstring

---

## Commit Message Format

Use the **Conventional Commits** format:

```
<type>(<scope>): <short description>

[optional body]

[optional footer]
```

**Types:**

| Type | Use |
|------|-----|
| `feat` | New feature |
| `fix` | Bug fix |
| `docs` | Documentation only |
| `refactor` | Code change without behavior change |
| `test` | Adding or fixing tests |
| `chore` | Build process, dependency updates |


---

## Issue Reporting

When reporting a bug, please include:

1. **AI LaTeX CLI version:** `latex-ai --version`
2. **Python version:** `python --version`
3. **OS and LaTeX installation:** e.g., "Ubuntu 22.04, TeX Live 2023"
4. **The exact command you ran**
5. **The full error output** (use `--verbose` flag)
6. **The `.tex` file or a minimal reproducing example** (remove any sensitive content)

Use the GitHub Issues tab with the appropriate label:
- `bug` — Something is broken
- `enhancement` — Feature request
- `documentation` — Docs improvement
- `template-request` — Request for a new LaTeX template
