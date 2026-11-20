# Continuous Integration & Automation Workflows

This directory contains GitHub Actions workflow configurations for the **AI LaTeX CLI** project.

---

## 🛠️ Workflows

### `main-ci.yml` — Automated CI Test Suite
Automatically triggered on all pushes and pull requests targeting the `main` branch:

1. **Linting & Code Integrity (`lint`):**
   - Validates Python syntax and checks for critical errors across all modules using `flake8`.

2. **Cross-Platform Matrix Testing (`test`):**
   - Tests across **Ubuntu** and **Windows** runners.
   - Evaluates compatibility on **Python 3.10, 3.11, 3.12, and 3.13**.
   - Validates installation of dependencies and the editable CLI entry point (`pip install -e .`).
   - Verifies the `latex-ai` binary execution and `--help` response.
   - Executes the full test suite using `pytest`.

3. **Package Distribution Verification (`package`):**
   - Builds both source distribution (`sdist`) and binary wheel (`bdist_wheel`).
   - Runs `twine check` to guarantee metadata compliance for PyPI releases.
