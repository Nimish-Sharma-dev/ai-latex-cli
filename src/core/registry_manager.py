"""
Registry Manager: Persistent storage for Skills, Harnesses, Repositories,
and dynamic LaTeX Formatting rules. Stored permanently and automatically used.
"""

import json
import os
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Any, List, Optional


class RegistryManager:
    def __init__(self, workspace_root: Optional[str | Path] = None):
        if workspace_root:
            self.root = Path(workspace_root).resolve()
        else:
            self.root = Path.cwd().resolve()

        self.storage_dir = self.root / ".latex_ai"
        self.storage_dir.mkdir(parents=True, exist_ok=True)
        self.registry_file = self.storage_dir / "registry.json"
        self.templates_dir = self.root / "templates"
        self.templates_dir.mkdir(parents=True, exist_ok=True)

        self._ensure_initialized()

    def _ensure_initialized(self):
        if not self.registry_file.exists():
            default_data = {
                "version": "1.0.0",
                "last_updated": datetime.now(timezone.utc).isoformat(),
                "skills": {},
                "harnesses": {},
                "formats": {}
            }
            self.registry_file.write_text(json.dumps(default_data, indent=2), encoding="utf-8")

    def _read_registry(self) -> Dict[str, Any]:
        try:
            return json.loads(self.registry_file.read_text(encoding="utf-8"))
        except Exception:
            return {"version": "1.0.0", "skills": {}, "harnesses": {}, "formats": {}}

    def _save_registry(self, data: Dict[str, Any]):
        data["last_updated"] = datetime.now(timezone.utc).isoformat()
        self.registry_file.write_text(json.dumps(data, indent=2), encoding="utf-8")

    # ── Skills Management ─────────────────────────────────────────────────────

    def register_skill(
        self,
        name: str,
        source_or_repo: str,
        description: str = "",
        keywords: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """Permanently registers a skill or repository of skills."""
        data = self._read_registry()
        clean_name = re.sub(r"[^a-zA-Z0-9_\-]", "_", name.lower().strip())
        
        # Auto-extract keywords
        kw = keywords or []
        kw.extend([w.lower() for w in clean_name.split("_") if len(w) > 2])
        if description:
            kw.extend([w.lower() for w in description.split() if len(w) > 3 and w.isalnum()])

        skill_entry = {
            "name": name,
            "identifier": clean_name,
            "source": source_or_repo,
            "is_repo": source_or_repo.startswith("http") or source_or_repo.endswith(".git"),
            "description": description or f"Skill registered for {name}",
            "keywords": sorted(list(set(kw))),
            "registered_at": datetime.now(timezone.utc).isoformat()
        }

        data["skills"][clean_name] = skill_entry
        self._save_registry(data)
        return skill_entry

    def list_skills(self) -> List[Dict[str, Any]]:
        data = self._read_registry()
        return list(data.get("skills", {}).values())

    def match_skills(self, context_text: str) -> List[Dict[str, Any]]:
        """Finds any registered skills relevant to the context or prompt."""
        skills = self.list_skills()
        matched = []
        c_lower = context_text.lower()
        for s in skills:
            if s["identifier"] in c_lower or s["name"].lower() in c_lower:
                matched.append(s)
                continue
            for kw in s.get("keywords", []):
                if re.search(rf"\b{re.escape(kw)}\b", c_lower):
                    matched.append(s)
                    break
        return matched

    # ── Harness Management ────────────────────────────────────────────────────

    def register_harness(
        self,
        name: str,
        command_or_runner: str,
        description: str = "",
        harness_type: str = "evaluation",
        keywords: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """Permanently registers a test, benchmark, or evaluation harness."""
        data = self._read_registry()
        clean_name = re.sub(r"[^a-zA-Z0-9_\-]", "_", name.lower().strip())

        kw = keywords or []
        kw.extend([w.lower() for w in clean_name.split("_") if len(w) > 2])
        kw.append(harness_type.lower())

        harness_entry = {
            "name": name,
            "identifier": clean_name,
            "command": command_or_runner,
            "type": harness_type,
            "description": description or f"{harness_type.title()} harness: {command_or_runner}",
            "keywords": sorted(list(set(kw))),
            "registered_at": datetime.now(timezone.utc).isoformat()
        }

        data["harnesses"][clean_name] = harness_entry
        self._save_registry(data)
        return harness_entry

    def list_harnesses(self) -> List[Dict[str, Any]]:
        data = self._read_registry()
        return list(data.get("harnesses", {}).values())

    def match_harnesses(self, context_text: str) -> List[Dict[str, Any]]:
        harnesses = self.list_harnesses()
        matched = []
        c_lower = context_text.lower()
        for h in harnesses:
            if h["identifier"] in c_lower or h["name"].lower() in c_lower:
                matched.append(h)
                continue
            for kw in h.get("keywords", []):
                if re.search(rf"\b{re.escape(kw)}\b", c_lower):
                    matched.append(h)
                    break
        return matched

    # ── Dynamic LaTeX Formats Management ──────────────────────────────────────

    def register_format(
        self,
        name: str,
        description: str,
        template_content: Optional[str] = None,
        styling_rules: Optional[Dict[str, Any]] = None,
        keywords: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Permanently registers a new LaTeX format and creates its template file.
        """
        data = self._read_registry()
        clean_name = re.sub(r"[^a-zA-Z0-9_\-]", "_", name.lower().strip())
        template_filename = f"{clean_name}.tex"
        template_path = self.templates_dir / template_filename

        # If custom template content was provided, write it; otherwise generate a template from rules
        if template_content:
            template_path.write_text(template_content, encoding="utf-8")
        else:
            generated_template = self._generate_template_from_rules(name, styling_rules or {})
            template_path.write_text(generated_template, encoding="utf-8")

        kw = keywords or []
        kw.extend([w.lower() for w in clean_name.split("_") if len(w) > 2])

        format_entry = {
            "name": name,
            "identifier": clean_name,
            "template_file": str(template_path.name),
            "template_path": str(template_path),
            "description": description,
            "styling_rules": styling_rules or {},
            "keywords": sorted(list(set(kw))),
            "registered_at": datetime.now(timezone.utc).isoformat()
        }

        data["formats"][clean_name] = format_entry
        self._save_registry(data)
        return format_entry

    def list_formats(self) -> List[Dict[str, Any]]:
        data = self._read_registry()
        return list(data.get("formats", {}).values())

    def match_format(self, format_name_or_prompt: str) -> Optional[Dict[str, Any]]:
        formats = self.list_formats()
        target = format_name_or_prompt.lower().strip()
        for f in formats:
            if f["identifier"] == target or f["name"].lower() == target:
                return f
            for kw in f.get("keywords", []):
                if kw in target:
                    return f
        return None

    def _generate_template_from_rules(self, name: str, rules: Dict[str, Any]) -> str:
        """Synthesizes a full LaTeX template based on requested styling rules."""
        doc_class = rules.get("document_class", "article")
        options = rules.get("options", "11pt,a4paper")
        margin = rules.get("margin", "1in")
        col_mode = rules.get("columns", "onecolumn")
        extra_pkgs = rules.get("extra_packages", [])

        pkg_lines = "\n".join([f"\\usepackage{{{p}}}" for p in extra_pkgs])

        return f"""\\documentclass[{options},{col_mode}]{{{doc_class}}}

\\usepackage[utf8]{{inputenc}}
\\usepackage[margin={margin}]{{geometry}}
\\usepackage{{amsmath,amssymb,amsfonts}}
\\usepackage{{graphicx}}
\\usepackage{{booktabs}}
\\usepackage{{hyperref}}
\\usepackage{{listings}}
\\usepackage{{cite}}
\\usepackage{{xcolor}}
{pkg_lines}

\\title{{\\textbf{{<<<DOCUMENT_TITLE>>>}}}}
\\author{{<<<AUTHOR_NAME>>> \\\\ \\small <<<INSTITUTION_NAME>>> \\\\ \\small \\texttt{{<<<AUTHOR_EMAIL>>>}}}}
\\date{{\\today}}

\\begin{{document}}

\\maketitle

\\begin{{abstract}}
<<<ABSTRACT_CONTENT>>>
\\end{{abstract}}

\\textbf{{Keywords:}} <<<KEYWORDS>>>

\\section{{Introduction}}
<<<SECTION_INTRODUCTION>>>

\\section{{Background and Literature Review}}
<<<SECTION_BACKGROUND>>>

\\section{{System Architecture and Methodology}}
<<<SECTION_ARCHITECTURE>>>

\\section{{Technical Implementation}}
<<<SECTION_IMPLEMENTATION>>>

\\section{{Empirical Evaluation and Results}}
<<<SECTION_EVALUATION>>>

\\section{{Discussion and Practical Considerations}}
<<<SECTION_DISCUSSION>>>

\\section{{Conclusion}}
<<<SECTION_CONCLUSION>>>

<<<BIBLIOGRAPHY_BLOCK>>>

\\end{{document}}
"""

    # ── Universal "Learn" Parser ──────────────────────────────────────────────

    def learn(self, text: str) -> Dict[str, Any]:
        """
        Parses natural language instructions to dynamically register skills,
        skill repositories, harnesses, or LaTeX formatting rules permanently.
        """
        t_lower = text.lower()
        results = {"skills_added": [], "harnesses_added": [], "formats_added": []}

        # Check for LaTeX formatting rules
        if any(k in t_lower for k in ["latex format", "formatting", "template", "style", "documentclass"]):
            # Derive format name
            name_match = re.search(r"(?:format|template|style)\s+(?:named|called|for)?\s*[\"']?([a-zA-Z0-9_\-]+)[\"']?", text, re.IGNORECASE)
            fmt_name = name_match.group(1) if name_match else "custom_format"

            # Check for styling attributes
            rules: Dict[str, Any] = {}
            if "two column" in t_lower or "twocolumn" in t_lower:
                rules["columns"] = "twocolumn"
            if "springer" in t_lower or "lncs" in t_lower:
                rules["document_class"] = "llncs"
            elif "nature" in t_lower:
                rules["document_class"] = "nature"
            elif "ieee" in t_lower:
                rules["document_class"] = "IEEEtran"

            margin_match = re.search(r"(\d+(?:\.\d+)?\s*(?:in|cm|mm))\s*margin", text, re.IGNORECASE)
            if margin_match:
                rules["margin"] = margin_match.group(1).replace(" ", "")

            entry = self.register_format(
                name=fmt_name,
                description=text.strip(),
                styling_rules=rules,
                keywords=[fmt_name.lower()]
            )
            results["formats_added"].append(entry)

        # Check for harness mentions
        if any(k in t_lower for k in ["harness", "benchmark", "eval", "evaluator", "test suite"]):
            name_match = re.search(r"(?:harness|benchmark)\s+(?:named|called|for)?\s*[\"']?([a-zA-Z0-9_\-]+)[\"']?", text, re.IGNORECASE)
            h_name = name_match.group(1) if name_match else "evaluation_harness"
            
            # Extract command if present
            cmd_match = re.search(r"(?:command|run|execute)\s*[:=]?\s*[`\"']([^`\"']+)`", text, re.IGNORECASE)
            cmd = cmd_match.group(1) if cmd_match else "pytest tests/ --benchmark"

            entry = self.register_harness(
                name=h_name,
                command_or_runner=cmd,
                description=text.strip(),
                keywords=[h_name.lower()]
            )
            results["harnesses_added"].append(entry)

        # Check for skills or skill repo mentions
        if any(k in t_lower for k in ["skill", "repo of skills", "repository", "tool", "github.com"]):
            # Extract URL if present
            url_match = re.search(r"(https?://[^\s]+|git@[^\s]+)", text)
            source = url_match.group(1) if url_match else text.strip()

            name_match = re.search(r"(?:skill|repo|tool)\s+(?:named|called|for)?\s*[\"']?([a-zA-Z0-9_\-]+)[\"']?", text, re.IGNORECASE)
            s_name = name_match.group(1) if name_match else (Path(source).stem if url_match else "custom_skill")

            entry = self.register_skill(
                name=s_name,
                source_or_repo=source,
                description=text.strip(),
                keywords=[s_name.lower()]
            )
            results["skills_added"].append(entry)

        return results
