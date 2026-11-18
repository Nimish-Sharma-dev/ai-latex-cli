"""
File system and LaTeX document manipulation manager.
Handles safe read/write, backups, section replacement, and template resolution.
"""

import os
import shutil
import re
from pathlib import Path
from typing import Optional, List, Dict, Tuple


class FileSystemManager:
    def __init__(self, template_dir: Optional[str] = None, backup_enabled: bool = True):
        if template_dir:
            self.template_dir = Path(template_dir)
        else:
            self.template_dir = Path(__file__).parent.parent.parent / "templates"
        self.backup_enabled = backup_enabled

    def read_file(self, file_path: str | Path) -> str:
        """Reads file content safely across different encodings."""
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"File not found: {path}")

        try:
            return path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            return path.read_text(encoding="latin-1")

    def write_file(self, file_path: str | Path, content: str, create_backup: Optional[bool] = None) -> Path:
        """Writes content to file, creating parent directories and optional backups."""
        path = Path(file_path)
        path.parent.mkdir(parents=True, exist_ok=True)

        should_backup = self.backup_enabled if create_backup is None else create_backup
        if should_backup and path.exists():
            backup_path = path.with_suffix(path.suffix + ".bak")
            shutil.copy2(path, backup_path)

        path.write_text(content, encoding="utf-8")
        return path

    def load_template(self, template_name_or_path: str) -> str:
        """Loads a template file either by filename in template_dir or direct path."""
        direct_path = Path(template_name_or_path)
        if direct_path.exists():
            return self.read_file(direct_path)

        # Check inside template_dir
        candidate = self.template_dir / template_name_or_path
        if candidate.exists():
            return self.read_file(candidate)

        # Try with .tex suffix
        candidate_tex = self.template_dir / f"{template_name_or_path}.tex"
        if candidate_tex.exists():
            return self.read_file(candidate_tex)

        raise FileNotFoundError(
            f"Template '{template_name_or_path}' not found in {self.template_dir}"
        )

    def list_available_templates(self) -> List[Dict[str, str]]:
        """Returns list of available templates with trigger descriptions."""
        templates = [
            {
                "name": "standard_article.tex",
                "keywords": "article, paper, report, technical, document (default)",
                "description": "Clean, single-column standard academic article format"
            },
            {
                "name": "ieee_paper.tex",
                "keywords": "ieee, conference, journal, embc, tbme, jbhi, transactions",
                "description": "Double-column standard IEEE Conference / Journal format"
            },
            {
                "name": "project_report.tex",
                "keywords": "thesis, project, dissertation, university, comprehensive report",
                "description": "Multi-chapter technical report with title page, TOC, list of figures"
            },
            {
                "name": "acm_paper.tex",
                "keywords": "acm, sigconf, proceedings, computing",
                "description": "ACM Conference and Proceedings publication format"
            },
            {
                "name": "presentation.tex",
                "keywords": "slides, beamer, lecture, talk, presentation, pitch",
                "description": "Modern 16:9 widescreen Beamer presentation slides"
            }
        ]
        return templates

    def match_template_by_prompt(self, prompt: str) -> str:
        """Selects the best template based on prompt keywords."""
        p_lower = prompt.lower()
        if any(k in p_lower for k in ["beamer", "slide", "slides", "presentation", "deck"]):
            return "presentation.tex"
        if any(k in p_lower for k in ["ieee", "embc", "tbme", "transactions"]):
            return "ieee_paper.tex"
        if any(k in p_lower for k in ["acm", "sigconf"]):
            return "acm_paper.tex"
        if any(k in p_lower for k in ["project report", "thesis", "dissertation", "capstone", "audit report"]):
            return "project_report.tex"
        if any(k in p_lower for k in ["clinical", "protocol"]):
            candidate = self.template_dir / "clinical_protocal.tex"
            if candidate.exists():
                return "clinical_protocal.tex"
        return "standard_article.tex"

    def apply_section_replace(self, doc_text: str, section_name: str, new_content: str) -> str:
        """Replaces the content of a specific section in the document."""
        escaped_name = re.escape(section_name)
        pattern = rf"(\\section\*?\{{{escaped_name}\}})(.*?)(?=(\\(?:chapter|section|subsection|bibliography|end\{{document\}})|$))"
        
        match = re.search(pattern, doc_text, re.DOTALL | re.IGNORECASE)
        if match:
            head = match.group(1)
            replacement = f"{head}\n{new_content}\n\n"
            return doc_text[:match.start()] + replacement + doc_text[match.end():]

        chap_pattern = rf"(\\chapter\*?\{{{escaped_name}\}})(.*?)(?=(\\(?:chapter|section|subsection|bibliography|end\{{document\}})|$))"
        chap_match = re.search(chap_pattern, doc_text, re.DOTALL | re.IGNORECASE)
        if chap_match:
            head = chap_match.group(1)
            replacement = f"{head}\n{new_content}\n\n"
            return doc_text[:chap_match.start()] + replacement + doc_text[chap_match.end():]

        return self.apply_append(doc_text, f"\n\\section{{{section_name}}}\n{new_content}\n")

    def apply_append(self, doc_text: str, content_to_append: str) -> str:
        """Appends content right before \\end{document}."""
        end_doc_tag = r"\end{document}"
        if end_doc_tag in doc_text:
            idx = doc_text.rfind(end_doc_tag)
            return doc_text[:idx] + f"\n{content_to_append}\n" + doc_text[idx:]
        return doc_text + f"\n{content_to_append}\n"

    def insert_table(self, doc_text: str, table_latex: str, position: str = "end") -> str:
        """Inserts a table at the specified position (end, or after a section)."""
        if position.startswith("after-section"):
            sec_name = position.replace("after-section", "").strip()
            return self.apply_section_replace(
                doc_text, sec_name, f"\n{table_latex}\n"
            )
        return self.apply_append(doc_text, table_latex)


# Module-level helper for backwards compatibility
def select_template(prompt: str) -> str:
    """Accepts raw prompt and returns contents of matching template."""
    fs = FileSystemManager()
    tpl_name = fs.match_template_by_prompt(prompt)
    try:
        return fs.load_template(tpl_name)
    except Exception:
        return ""
