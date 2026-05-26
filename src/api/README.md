# src/api/ — LLM API Communication Layer

This package contains all logic for communicating with the **DeepSeek LLM API**.
It acts as the intelligence engine of the system — translating user intent into
structured, compilation-ready LaTeX code.

---

## Files

| File | Description |
|------|-------------|
| `__init__.py` | Package marker |
| `deepseek.py` | DeepSeek API client — all LLM calls originate here |

---

## Why This Layer Exists

Keeping API logic isolated in its own package provides several benefits:

1. **Swappability** — If you want to replace DeepSeek with another model (e.g., GPT-4, Claude, Mistral), you only change this file. The CLI and core layers remain untouched.
2. **Testability** — Unit tests can mock this layer entirely, so CLI and compiler tests don't require a live API key.
3. **Prompt Management** — All system prompts and prompt templates live here, making them easy to tune without touching application logic.

---

## DeepSeek API Configuration

DeepSeek exposes an **OpenAI-compatible REST API**, which means the `openai` Python SDK
can communicate with it by simply overriding the `base_url`:

```
Base URL:  https://api.deepseek.com/v1
Model:     deepseek-chat  (or deepseek-coder for code-heavy tasks)
Auth:      Bearer token via DEEPSEEK_API_KEY environment variable
```

### Environment Variables

All configuration is loaded from a `.env` file (never hardcoded):

| Variable | Required | Description |
|----------|----------|-------------|
| `DEEPSEEK_API_KEY` | ✅ Yes | Your DeepSeek API key |
| `DEEPSEEK_MODEL` | Optional | Model name (default: `deepseek-chat`) |
| `DEEPSEEK_BASE_URL` | Optional | API base URL (default: `https://api.deepseek.com/v1`) |
| `DEEPSEEK_MAX_TOKENS` | Optional | Max tokens per response (default: `4096`) |
| `DEEPSEEK_TEMPERATURE` | Optional | Sampling temperature (default: `0.2` for deterministic LaTeX) |

### Getting Your API Key

1. Visit [https://platform.deepseek.com](https://platform.deepseek.com)
2. Create an account and navigate to API Keys
3. Generate a key and paste it into your `.env` file:
   ```env
   DEEPSEEK_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
   ```

---

## System Prompt Design

The system prompt is the most critical part of this layer. It instructs the model to:

1. **Output only valid LaTeX** — No explanatory prose, no markdown fences, no commentary
2. **Preserve existing structure** — When editing, only modify the requested section
3. **Use correct LaTeX packages** — Based on the document type (article, beamer, IEEE)
4. **Follow biomedical conventions** — Use `\SI{}{}` for units, proper citation formats, etc.
5. **Generate compilable code** — Every output must pass `pdflatex` without errors

### System Prompt Template (conceptual):

```
You are an expert LaTeX typesetting assistant specializing in biomedical 
engineering and healthcare documentation.

Rules:
- Output ONLY raw LaTeX code. No explanations, no markdown, no backticks.
- All code must compile with pdflatex without errors.
- Use standard biomedical conventions: SI units, proper citation styles, 
  structured abstract formats for clinical papers.
- When editing an existing document, preserve all content outside the 
  requested section. Only modify what was asked.
- When fixing compilation errors, output the complete corrected document.
```

---

## API Functions

### `generate(prompt, template_content) → str`

Called by `latex-ai init`. Takes a user prompt and a template's content,
and returns a fully populated `.tex` document body.

**Input:** User prompt + base template LaTeX  
**Output:** Complete `.tex` file content as a string

---

### `edit(prompt, file_content) → str`

Called by `latex-ai edit`. Takes an edit instruction and the current file content,
and returns the modified `.tex` content.

**Input:** Edit instruction + current `.tex` file content  
**Output:** Updated `.tex` file content as a string

---

### `fix(error_log, file_content) → str`

Called by `latex-ai fix`. Takes a LaTeX compilation error log and the faulty file,
and returns a corrected version.

**Input:** `pdflatex` error log + broken `.tex` file content  
**Output:** Corrected `.tex` file content as a string

---

### `generate_table(prompt, context) → str`

Called by `latex-ai table`. Generates a standalone LaTeX `tabular` or `longtable`
environment from a natural language description.

**Input:** Table description prompt + surrounding document context  
**Output:** LaTeX table environment as a string

---

## Token & Cost Management

- Temperature is set low (`0.2`) for LaTeX generation to maximize determinism
- `max_tokens` is capped at `4096` by default to control costs
- The full file content is always sent as context (not just the relevant section),
  so the model can maintain consistency with existing structure and packages
- For very large documents (> ~8000 tokens), a summarization pre-pass may be needed
  before sending to the model — this is noted as a future improvement in `FUTURE_SCOPE.md`

---

