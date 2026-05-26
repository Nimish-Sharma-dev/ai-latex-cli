# templates/ — Predefined LaTeX Boilerplate Templates

This directory contains the base `.tex` template files that the AI LaTeX CLI
uses as starting points for new documents.

The key design principle here is **template injection over LLM hallucination**:
rather than asking the AI to generate a full IEEE format document structure from
scratch (which risks subtle formatting errors), the system loads a proven,
pre-validated template and uses the LLM only to fill in the scientific content.

---

## Template Trigger Keywords

The `fs_manager.select_template()` function matches these keywords from the user's
prompt to select the appropriate template:

| User Prompt Keywords | Template Selected |
|----------------------|-------------------|
| `ieee`, `conference`, `embc`, `tbme` | `ieee_paper.tex` |
| `slides`, `presentation`, `beamer`, `lecture`, `talk` | `presentation.tex` |
| `clinical`, `trial`, `protocol`, `rct`, `irb` | `clinical_protocol.tex` |
| *(default — no other match)* | `standard_article.tex` |

---

## Template Design Conventions

All templates in this directory follow these conventions:

### 1. Placeholder Markers

Templates use `%[PLACEHOLDER: ...]` comments to mark locations where the AI
should inject content:

```latex
%[PLACEHOLDER: TITLE]
\title{Your Title Here}

%[PLACEHOLDER: ABSTRACT]
\begin{abstract}
  Insert abstract here.
\end{abstract}
```

This allows `fs_manager.py` to perform targeted replacements rather than
relying on the LLM to correctly re-typeset the entire document header.

### 2. Package Completeness

Each template includes all packages likely to be needed for its document class,
rather than a minimal set. This prevents the most common class of compilation
errors: missing packages.

### 3. Section Scaffolding

Templates include empty (but labeled) sections for the expected document
structure. This gives the AI context about what sections exist, preventing
it from duplicating or misplacing content.
---

## Adding a New Template

To add a new template:

1. Create a `.tex` file in this directory following the conventions above
2. Validate that it compiles cleanly: `pdflatex -interaction=nonstopmode yourtemplate.tex`
3. Add it to the keyword trigger map in `src/core/fs_manager.py`
4. Update this README with the new template's entry in the tables above
5. Add a test in `tests/test_fs_manager.py` verifying the keyword triggers select it correctly

---

## Template Validation

The CI pipeline (`.github/workflows/main-ci.yml`) automatically compiles every
template in this directory on every push to `main`. A template that fails to
compile will block the merge.
