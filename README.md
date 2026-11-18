# 🚀 AI LaTeX CLI & Autonomous Project Reporter (`latex-ai`)

Welcome to **AI LaTeX CLI** — a 100% free-to-use, terminal-native document engine and codebase reporting system powered by Antigravity, Google Gemini, Groq, and Ollama.

Eliminate the headache of LaTeX boilerplate, packaging conflicts, manual bibliographies, or missing figure links. With `latex-ai`, you can:
- **Audit your codebase:** Automatically inspect file trees, AST symbols, classes, functions, languages, and dependencies.
- **Generate comprehensive LaTeX reports:** Create publication-ready documents formatted for IEEE, ACM, University Thesis / Technical Reports, or Beamer slides with **absolutely NO placeholders** (dense technical content, real math, and tables).
- **Auto-generate figures & screenshots:** High-resolution system architecture diagrams, empirical performance benchmark charts, and terminal execution screenshots generated directly onto disk without missing image links.
- **Synthesize verified citations:** Integrated BibTeX file (`references.bib`) and embedded bibliographies linking real peer-reviewed scientific literature.
- **Code entire projects from natural language:** Prompt your idea and let the engine scaffold full source code, type annotations, unit tests, and the matching LaTeX report automatically.
- **Zero API Credit Lock-in:** 100% free offline execution via the built-in Antigravity engine, or free-tier APIs (Google Gemini, Groq, Ollama). DeepSeek remains supported as an optional provider.

---

## 📁 Project Structure

```text
ai-latex-cli/
│
├── .github/
│   └── workflows/
│       ├── main-ci.yml
│       └── README.md
│
├── docs/
│   ├── ARCHITECTURE.md
│   ├── COMMAND_REFERENCE.md
│   └── README.md
│
├── src/
│   ├── api/
│   │   ├── config.py
│   │   ├── llm_client.py
│   │   ├── deepseek.py
│   │   └── README.md
│   │
│   ├── cli/
│   │   ├── main.py
│   │   └── README.md
│   │
│   ├── core/
│   │   ├── fs_manager.py
│   │   ├── compiler.py
│   │   ├── repo_auditor.py
│   │   ├── figure_generator.py
│   │   ├── citation_manager.py
│   │   ├── project_coder.py
│   │   ├── report_generator.py
│   │   ├── registry_manager.py
│   │   └── README.md
│   │
│   ├── __init__.py
│   └── README.md
├── tests/
│   ├── test_auditor.py
│   ├── test_cli.py
│   ├── test_figure_generator.py
│   ├── test_fs_manager.py
│   ├── test_registry.py
│   └── test_report_generator.py
│  
├── templates/
│   ├── standard_article.tex
│   ├── ieee_paper.tex
│   ├── project_report.tex
│   ├── acm_paper.tex
│   ├── presentation.tex
│   ├── clinical_protocal.tex
│   └── README.md
│
├── .env.example
├── .gitignore
├── CONTRIBUTING.md
├── FUTURE_SCOPE.md
├── README.md
├── PROJECT_VISION_AND_ROADMAP.md
├── requirements.txt
└── setup.py
```

---

## ⚡ Quick Start & Installation

Before jumping in, make sure you have Python 3.10+ and a local LaTeX distribution installed (MiKTeX, MacTeX, or TeX Live).

### 1. Installation
```bash
# Clone the repository
git clone https://github.com/Nimish-Sharma-dev/ai-latex-cli.git
cd ai-latex-cli

# Install dependencies (or in editable mode)
pip install -r requirements.txt
pip install -e .
```

### 2. Configuration (100% Free)
By default, the tool works immediately using the built-in Antigravity engine with **zero setup and zero API keys required**.

If you wish to use cloud free-tier providers:
```bash
cp .env.example .env
# Edit .env to add your free GEMINI_API_KEY or GROQ_API_KEY
```

Check your active provider anytime:
```bash
latex-ai config
```

---

## 💻 Core Commands

### 🔍 1. Audit Any Codebase (`latex-ai audit`)
Scans any repository, computes lines of code (LOC), language breakdown, frameworks, dependencies, and extracts AST classes and functions:
```bash
# Audit the current repository
latex-ai audit .

# Audit an external project with JSON output
latex-ai audit /path/to/project --json
```

---

### 📄 2. Generate Full LaTeX Report (`latex-ai report`)
Inspects your project, prompts for your target format, renders high-DPI figures/screenshots, compiles real citations, and generates a complete LaTeX document with **zero placeholders**:
```bash
# Interactive mode (prompts for format: IEEE, Report, ACM, Standard, Presentation)
latex-ai report .

# Specify format and metadata directly
latex-ai report . --format ieee --author "Jane Doe" --inst "MIT CSAIL"
latex-ai report . --format report   # University Thesis / Multi-Chapter format
latex-ai report . --format presentation  # Beamer slide deck
```

**Artifacts Generated in `outputs/<project>_report/`:**
1. `<project>_<format>.tex` — Complete, dense technical LaTeX manuscript.
2. `references.bib` — Verified BibTeX citations matching all `\cite{...}` keys.
3. `figures/system_architecture.png` — 300 DPI vector-styled architecture diagram.
4. `figures/performance_benchmark.png` — Empirical latency and throughput plots.
5. `figures/terminal_screenshot.png` — High-fidelity terminal execution screenshot.
6. `<project>_<format>_overleaf_bundle.zip` — Ready for 1-click import into Overleaf.

---

### 🌟 3. Autonomous Project Builder & Reporter (`latex-ai build`)
Builds a complete, working codebase from a prompt, audits what was created, asks for the report format, and typesets the full document:
```bash
latex-ai build "A real-time biomedical ECG arrhythmia classification service with FastAPI"
```
What happens automatically:
1. Scaffolds working project structure with source code, Pydantic schemas, signal processing logic, and PyTest tests.
2. Runs AST auditor to inspect created modules.
3. Generates the formatted LaTeX report with diagrams, screenshots, tables, equations, and citations.

---

### 🧠 4. Persistent Memory for Skills, Harnesses & Custom Formats

Mention any skill, repository of skills, benchmark harness, or custom LaTeX formatting rules in natural language or via CLI, and the system **stores it forever** into `.latex_ai/registry.json`. Whenever that skill or harness is relevant, it is automatically invoked and incorporated into future project builds and LaTeX reports.

#### Universal Natural Language Intake (`latex-ai learn`)
```bash
# Teach the system about a skill repository
latex-ai learn "I want to use the skill repo https://github.com/swe-bench/SWE-bench for software evaluation"

# Teach the system a new LaTeX formatting style
latex-ai learn "Here is a new Springer LNCS two column format with 1.2in margin"
```

#### Dedicated CLI Commands:
```bash
# Register and list skills
latex-ai skill add "biomedical-dsp" "https://github.com/example/biosignal-dsp" --desc "Signal filtering skill"
latex-ai skill list

# Register and list evaluation/test harnesses
latex-ai harness add "ecg-benchmark" "pytest tests/ --benchmark-only" --type benchmark
latex-ai harness list

# Register and list custom LaTeX formats
latex-ai format add "springer-lncs" --class llncs --margin 1.2in --desc "Springer LNCS paper"
latex-ai format list
```

---

### ✍️ 5. Interactive LaTeX Editing & Tables
```bash
# Initialize a new document from prompt
latex-ai init "Conference paper on transformer attention optimizations"

# Edit a specific section in-place (with automated .bak backup)
latex-ai edit paper.tex "Add a paragraph describing our Kalman filter" --section Implementation

# Generate and insert a professional booktabs table
latex-ai table paper.tex "Compare 4 deep learning models on accuracy, latency, and memory"

# Compile to PDF (with auto-fix error diagnostics)
latex-ai compile paper.tex --auto-fix

# Auto-diagnose and repair compilation errors
latex-ai fix broken.tex
```

---

## 🎨 Supported LaTeX Templates

View all templates with:
```bash
latex-ai list-templates
```
| Template | Keywords / Formats | Description |
| :--- | :--- | :--- |
| `ieee_paper.tex` | `ieee`, `conference`, `journal` | Double-column IEEE Transactions / Conference format |
| `project_report.tex` | `report`, `thesis`, `dissertation` | Comprehensive multi-chapter report with title page, TOC, list of figures |
| `standard_article.tex` | `standard`, `article`, `paper` | Clean single-column academic/technical article |
| `acm_paper.tex` | `acm`, `sigconf`, `proceedings` | Official ACM Conference Proceedings format |
| `presentation.tex` | `presentation`, `beamer`, `slides` | Modern 16:9 widescreen Beamer presentation slides |

---

## 🧪 Running Tests
```bash
python -m pytest tests/
```
The test suite validates:
- AST repository parsing & metrics collection
- High-resolution figure & screenshot generation
- Filesystem safety, section substitution, backups
- End-to-end report generation with strict regex verification of zero leftover placeholders
- CLI commands and parameter bindings

---

## 📜 License
MIT License. Free to use, modify, and distribute.
