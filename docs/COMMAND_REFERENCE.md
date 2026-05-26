# COMMAND_REFERENCE.md — CLI Command Documentation

**AI LaTeX CLI** | `docs/COMMAND_REFERENCE.md`

---

## Installation & Setup

```bash
# Clone and install
git clone https://github.com/your-org/ai-latex-cli.git
cd ai-latex-cli
pip install -e .

# Configure API key
echo "DEEPSEEK_API_KEY=your_key_here" > .env

# Verify installation
latex-ai --version
latex-ai --help
```

---

## Global Options

These options are available on every command:

| Option | Short | Description |
|--------|-------|-------------|
| `--verbose` | `-v` | Show detailed output including API response metadata |
| `--dry-run` | | Show what would be done without making changes |
| `--no-backup` | | Skip creating a .bak file before overwriting |
| `--output-dir` | `-o` | Override the output directory for compiled PDFs |
| `--help` | | Show help message for any command |
| `--version` | | Show the installed version |

---

## Commands

---

### `latex-ai init`

**Purpose:** Create a new LaTeX document from a natural language description.

```
latex-ai init [OPTIONS] PROMPT
```

**Arguments:**

| Argument | Required | Description |
|----------|----------|-------------|
| `PROMPT` | ✅ | Natural language description of the document to create |

**Options:**

| Option | Default | Description |
|--------|---------|-------------|
| `--output` / `-o` | Auto-generated from prompt | Output `.tex` filename |
| `--template` / `-t` | Auto-selected | Explicitly specify a template file |
| `--no-compile` | False | Generate `.tex` only; skip compilation to PDF |

**Examples:**

```bash
# Auto-select IEEE template based on prompt
latex-ai init "Start an IEEE paper about ECG-based atrial fibrillation detection"

# Auto-select presentation template
latex-ai init "Create lecture slides on pharmacokinetics for medical students"

# Specify output filename explicitly
latex-ai init "Write a report on prosthetic arm control using EMG signals" --output prosthetics_report.tex

# Use a specific template file
latex-ai init "Document about hospital EHR systems" --template templates/standard_article.tex

# Generate only the .tex file, no PDF compilation
latex-ai init "Draft a systematic review protocol for ICU sedation studies" --no-compile
```

**What Happens:**
1. Keywords in `PROMPT` are matched to a template (see `templates/README.md`)
2. The template is loaded and sent to DeepSeek along with the prompt
3. DeepSeek fills in the document structure, abstract scaffold, and section stubs
4. The populated `.tex` file is saved to disk
5. Unless `--no-compile` is set, `pdflatex` is run to verify compilability
6. Output filename and PDF path are reported

---

### `latex-ai edit`

**Purpose:** Modify an existing `.tex` document using a natural language instruction.

```
latex-ai edit [OPTIONS] FILE PROMPT
```

**Arguments:**

| Argument | Required | Description |
|----------|----------|-------------|
| `FILE` | ✅ | Path to the `.tex` file to modify |
| `PROMPT` | ✅ | Natural language description of the edit to make |

**Options:**

| Option | Default | Description |
|--------|---------|-------------|
| `--section` / `-s` | None | Restrict edit to a specific named section |
| `--append` | False | Append content rather than replacing |
| `--recompile` | True | Re-compile after edit to verify no errors introduced |

**Examples:**

```bash
# Add a new section
latex-ai edit paper.tex "Add a Methods section describing bandpass filtering at 0.5–40 Hz"

# Rewrite a specific section
latex-ai edit paper.tex "Rewrite the Introduction to focus on wearable EEG applications" --section Introduction

# Append a paragraph to the Discussion
latex-ai edit paper.tex "Add a paragraph about the clinical translation pathway" --append

# Edit without recompiling (faster, for iterative drafting)
latex-ai edit paper.tex "Fix the abstract to be under 250 words" --no-recompile
```

**What Happens:**
1. The full content of `FILE` is read
2. If `--section` is specified, only that section's content is sent for replacement
3. The prompt + file content is sent to `deepseek.edit()`
4. The returned content is applied via `fs_manager.apply_section_replace()` or `apply_append()`
5. A `.bak` backup of the original is created before any write
6. If `--recompile` (default), the file is compiled to verify no errors were introduced

---

### `latex-ai table`

**Purpose:** Generate and insert a LaTeX table from a natural language description.

```
latex-ai table [OPTIONS] FILE PROMPT
```

**Arguments:**

| Argument | Required | Description |
|----------|----------|-------------|
| `FILE` | ✅ | Target `.tex` file |
| `PROMPT` | ✅ | Description of the table to generate |

**Options:**

| Option | Default | Description |
|--------|---------|-------------|
| `--position` | `end` | Where to insert: `end`, `after-section <name>`, or line number |
| `--style` | `booktabs` | Table style: `booktabs`, `basic`, `longtable` |

**Examples:**

```bash
# Simple comparison table inserted at end of document
latex-ai table paper.tex "Create a table comparing 5 seizure detection algorithms: sensitivity, specificity, AUC, and dataset"

# Longtable for large datasets
latex-ai table paper.tex "Patient demographics table: ID, age, sex, diagnosis, medication" --style longtable

# Insert after the Results section
latex-ai table paper.tex "Confusion matrix for binary classifier: 2x2 with TP, FP, FN, TN" --position "after-section Results"
```

---

### `latex-ai compile`

**Purpose:** Compile a `.tex` file to PDF using the local LaTeX installation.

```
latex-ai compile [OPTIONS] FILE
```

**Arguments:**

| Argument | Required | Description |
|----------|----------|-------------|
| `FILE` | ✅ | Path to the `.tex` file to compile |

**Options:**

| Option | Default | Description |
|--------|---------|-------------|
| `--auto-fix` | False | Automatically attempt AI-based error correction on failure |
| `--compiler` | `latexmk` | Override: `latexmk` or `pdflatex` |
| `--output-dir` | Same as input | Directory for PDF output |
| `--clean` | False | Remove auxiliary files (`.aux`, `.log`, `.out`) after success |

**Examples:**

```bash
# Standard compile
latex-ai compile paper.tex

# Compile and auto-fix errors
latex-ai compile paper.tex --auto-fix

# Use pdflatex explicitly (e.g., if latexmk is unavailable)
latex-ai compile paper.tex --compiler pdflatex

# Output PDF to a specific directory
latex-ai compile paper.tex --output-dir ./output/

# Clean auxiliary files after successful compilation
latex-ai compile paper.tex --clean
```

**Output on Success:**
```
✅ Compilation successful
   PDF: ./paper.pdf
   Duration: 3.2s
   Warnings: 2 (run with --verbose to see details)
```

**Output on Failure:**
```
❌ Compilation failed
   Error on line 47: Undefined control sequence \sectoin
   Suggestion: Did you mean \section?
   
   Run `latex-ai fix paper.tex` to attempt automatic correction.
```

---

### `latex-ai fix`

**Purpose:** Automatically diagnose and fix LaTeX compilation errors using AI.

```
latex-ai fix [OPTIONS] FILE
```

**Arguments:**

| Argument | Required | Description |
|----------|----------|-------------|
| `FILE` | ✅ | Path to the broken `.tex` file |

**Options:**

| Option | Default | Description |
|--------|---------|-------------|
| `--show-diff` | False | Show a diff of changes made by the fix |
| `--no-recompile` | False | Apply the fix but do not re-compile |

**Examples:**

```bash
# Standard auto-fix (compiles after fixing)
latex-ai fix paper.tex

# Show what was changed
latex-ai fix paper.tex --show-diff

# Apply fix without recompiling (for manual inspection first)
latex-ai fix paper.tex --no-recompile
```

**What Happens:**
1. The `.tex` file content is read
2. `pdflatex` is run to generate a fresh error log
3. The error log + file content is sent to `deepseek.fix()`
4. The corrected content is saved (with `.bak` backup)
5. The file is re-compiled to verify the fix worked
6. If re-compilation succeeds: PDF path is reported
7. If re-compilation fails: full error log is shown; user is advised to inspect manually

---

### `latex-ai preview` *(planned)*

**Purpose:** Open the compiled PDF in the system's default viewer.

```
latex-ai preview FILE
```

---

### `latex-ai list-templates`

**Purpose:** Show all available templates with their trigger keywords.

```
latex-ai list-templates
```

**Output:**
```
Available Templates:
┌──────────────────────────┬──────────────────────────────────────────────┐
│ Template                 │ Trigger Keywords                             │
├──────────────────────────┼──────────────────────────────────────────────┤
│ standard_article.tex     │ article, paper, report (default)            │
│ ieee_paper.tex           │ ieee, conference, embc, tbme, jbhi           │
│ presentation.tex         │ slides, beamer, lecture, talk, presentation  │
└──────────────────────────┴──────────────────────────────────────────────┘
```

---

## Exit Codes

| Code | Meaning |
|------|---------|
| `0` | Success |
| `1` | General error (compilation failure, API error) |
| `2` | Invalid usage (missing required argument, file not found) |
| `3` | API configuration error (missing API key) |

---

## Environment Variables

See `docs/ARCHITECTURE.md` — Section 4 for the full configuration reference.
