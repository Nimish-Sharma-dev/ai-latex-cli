# `src/core/` — Core Engine & Business Logic

The `src/core/` package provides the document synthesis, static analysis, figure rendering, compilation, and persistent memory engines that power the **AI LaTeX CLI** (`latex-ai`).

---

## 🏗️ Architecture & Modules

```
src/core/
├── fs_manager.py         # File system operations, template selection, and section replacements
├── compiler.py           # LaTeX compiler interface (pdflatex, xelatex) with error parsing
├── repo_auditor.py       # Codebase static analysis, AST symbol extraction, and metrics
├── figure_generator.py   # Publication-quality 300 DPI figures, charts, and terminal screenshots
├── citation_manager.py   # Verified BibTeX synthesis and literature cross-referencing
├── project_coder.py      # Autonomous project scaffolding from natural language prompts
├── report_generator.py   # Dense, zero-placeholder LaTeX academic paper generation
└── registry_manager.py   # Persistent memory for skills, testing harnesses, and LaTeX formats
```

---

## 🧩 Module Breakdown

### 1. `fs_manager.py` (File System Manager)
- Manages template discovery in `templates/` and project directory scaffolding.
- Intelligently maps natural language prompts to matching LaTeX templates (`ieee_paper.tex`, `project_report.tex`, `acm_paper.tex`, `presentation.tex`, `clinical_protocal.tex`, etc.).
- Performs regex-based section replacement (`apply_section_replace`) to safely insert generated sections into existing LaTeX source trees without corrupting preamble or macros.

### 2. `compiler.py` (LaTeX Compiler)
- Wraps local LaTeX distributions (`pdflatex`, `xelatex`, `latexmk`).
- Enforces strict execution timeouts and suppresses interactive prompts with `-interaction=nonstopmode`.
- Parses compiler log files (`.log`) to surface exact line numbers and LaTeX error diagnostics when compilation fails.

### 3. `repo_auditor.py` (Codebase Auditor)
- Recursively audits target repositories, extracting directory hierarchies, file counts, and line metrics.
- Uses Python's `ast` module to extract classes, functions, docstrings, and imports.
- Supports multi-language detection (Python, TypeScript, JavaScript, C/C++, Rust, Go) and produces structured audit dicts for downstream LaTeX paper generation.

### 4. `figure_generator.py` (Scientific Visuals)
- Generates publication-ready 300 DPI diagrams using `matplotlib`:
  - **System Architecture Flowcharts:** Layered component diagrams detailing inputs, processing engines, and outputs.
  - **Empirical Performance Benchmarks:** Latency vs. throughput charts, memory footprints, and classification accuracy curves.
  - **Realistic Terminal Execution Screenshots:** Monospace ANSI-styled terminal snapshots displaying real CLI executions.
- Guarantees zero missing image links during compilation.

### 5. `citation_manager.py` (Citation & Bibliography Synthesis)
- Formats and validates peer-reviewed scientific citations into BibTeX (`references.bib`).
- Automatically resolves domain-specific literature (biomedical engineering, signal processing, machine learning, clinical trials).
- Invariant: Every `\cite{...}` tag in generated LaTeX papers resolves to a verified entry in `references.bib`.

### 6. `project_coder.py` (Autonomous Project Scaffolding)
- Scaffolds complete software projects from natural language requirements.
- Generates clean directory trees, source modules with type hints, test suites, and documentation.
- Automatically invokes `report_generator.py` to produce a matching technical report.

### 7. `report_generator.py` (Dense LaTeX Paper Generator)
- Produces publication-grade papers across IEEE, ACM, Springer LNCS, and Thesis formats.
- **Strict Quality Invariant:** Enforces **zero placeholders** (`[TODO]`, `[insert text here]`, `\lipsum`) — synthesizing dense, domain-accurate technical text, equations, and tables.
- Emits dual versions: a standard build and a self-contained single-file Overleaf-ready edition with inline figures and `filecontents` bibliographies.

### 8. `registry_manager.py` (Persistent Memory)
- Stores skills, skill repositories, testing harnesses, and custom LaTeX templates forever in `.latex_ai/registry.json`.
- Supports dynamic LaTeX template registration, making custom formats immediately selectable via `latex-ai report --format <name>`.
