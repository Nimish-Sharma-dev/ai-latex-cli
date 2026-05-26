# src/cli/ — Command Line Interface Layer

This package is the **user-facing entry point** of the AI LaTeX CLI system.
It defines every terminal command available under the `latex-ai` tool,
handles input parsing, and orchestrates calls to the `api` and `core` layers.

---

## Files

| File | Description |
|------|-------------|
| `__init__.py` | Package marker; keeps imports clean |
| `main.py` | Typer application — all CLI commands are defined here |

---

## Responsibilities

The CLI layer is responsible for **only** the following:

1. **Command registration** — Declaring commands like `init`, `edit`, `compile`, `fix`, `table`
2. **Input parsing** — Extracting the file path, prompt string, and optional flags from the terminal
3. **User output** — Printing status messages, success confirmations, and error summaries using `rich`
4. **Routing** — Calling the appropriate function from `api/` or `core/` based on the command

The CLI layer does **not** contain business logic. It delegates everything to lower layers.

---

## Command Structure

All commands follow this pattern:

```
latex-ai <command> [FILE] [PROMPT] [OPTIONS]
```

### `init`

```
latex-ai init "Start an IEEE paper on cardiac arrhythmia detection using wearable sensors"
```

- Extracts intent keywords (e.g., "IEEE") from the prompt
- Calls `fs_manager.select_template()` to find the best matching `.tex` template
- Passes the template content + user prompt to `deepseek.generate()` to populate it
- Saves the result as a new `.tex` file in the current directory
- Reports the output filename to the user

### `edit`

```
latex-ai edit paper.tex "Add a Results section with a placeholder table for classifier performance"
```

- Reads the existing `.tex` file
- Sends the file content + edit instruction to `deepseek.edit()`
- Applies the returned patch via `fs_manager.apply_edit()`
- Confirms the change with a diff summary

### `table`

```
latex-ai table paper.tex "Create a table comparing 4 prosthetic limb control methods: accuracy, latency, battery life"
```

- Targeted command specifically for generating LaTeX table environments
- Sends a structured table prompt to the API
- Injects the returned table code at the end of the document or at a marked position

### `compile`

```
latex-ai compile paper.tex
```

- Calls `compiler.compile()` on the specified file
- Displays a progress spinner during compilation
- On success: reports the output PDF path
- On failure: displays a formatted error summary and suggests running `latex-ai fix`

### `fix`

```
latex-ai fix paper.tex
```

- Reads the `.tex` file and the most recent compilation error log
- Sends both to `deepseek.fix()` to generate a corrected version
- Applies the fix and re-compiles automatically
- Reports whether the fix was successful

### `preview` *(planned)*

```
latex-ai preview paper.tex
```

- Opens the compiled PDF in the system default PDF viewer

---

## Terminal Output Design

The CLI uses `rich` for all terminal output:

- **Panels** — Used for section headers and command results
- **Spinners** — Shown during API calls and compilation
- **Syntax highlighting** — LaTeX code is highlighted when displayed
- **Tables** — Used to show diffs and section lists
- **Color coding**:
  - 🟢 Green — Success
  - 🟡 Yellow — Warnings (e.g., compilation warnings)
  - 🔴 Red — Errors
  - 🔵 Blue — Informational messages

---

## Error Handling Philosophy

The CLI is the **last line of user-facing error handling**. It must:

- Never crash silently
- Always show the user a human-readable explanation of what went wrong
- Suggest a corrective action (e.g., "Run `latex-ai fix paper.tex` to attempt auto-correction")
- Exit with a non-zero status code on failure (for CI/scripting compatibility)

---

## Adding a New Command

To add a new command to the CLI:

1. Open `main.py`
2. Define a new function decorated with `@app.command()`
3. Add type-annotated parameters for file path and prompt
4. Call the appropriate function from `api/` or `core/`
5. Add the new command to `docs/COMMAND_REFERENCE.md`
6. Write a unit test in `tests/test_cli.py`
