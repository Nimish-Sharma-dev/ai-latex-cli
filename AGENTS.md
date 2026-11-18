# Antigravity Persistent Knowledge & Reporting Rules

## 1. Automatic Memory for Skills, Repositories, and Harnesses
Whenever the user mentions a skill, a repository of skills, or a testing/evaluation harness:
1. **Store Forever**: Immediately register it into the persistent registry (`.latex_ai/registry.json`).
2. **Auto-Invocation**: Whenever coding, auditing, or generating reports, automatically recognize any registered skill or harness and incorporate its capabilities and evaluation into the architecture and report.

## 2. Dynamic LaTeX Formatting Memory
Whenever the user describes or specifies a new LaTeX formatting style (e.g. custom margins, two-column layouts, Springer LNCS, NeurIPS, Nature, Beamer themes, university-specific thesis guidelines):
1. **Store Forever**: Save the new template into `templates/<format_name>.tex` and register its formatting rules in `.latex_ai/registry.json`.
2. **Auto-Selectable**: Make the new format immediately selectable in `latex-ai report --format <name>` and future chat interactions.

## 3. Strict Quality Invariants for Reports
1. **Zero Placeholders**: Never output `[TODO]`, `[insert text here]`, `\lipsum`, or `<placeholder>` in any LaTeX document.
2. **Real Visuals & Screenshots**: Include generated 300 DPI architecture diagrams, benchmark charts, and realistic terminal screenshots in `figures/`.
3. **Verified Citations**: Include real BibTeX entries in `references.bib` matching all `\cite{...}` tags.
