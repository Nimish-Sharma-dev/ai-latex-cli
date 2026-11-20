import pytest
from pathlib import Path
from src.core.fs_manager import FileSystemManager


def test_fs_manager_templates():
    fs = FileSystemManager()
    templates = fs.list_available_templates()
    assert len(templates) >= 4

    ieee = fs.load_template("ieee_paper.tex")
    assert "\\begin{document}" in ieee
    assert "<<<DOCUMENT_TITLE>>>" in ieee


def test_fs_manager_section_replace(tmp_path):
    fs = FileSystemManager()
    initial_latex = """\\documentclass{article}
\\begin{document}
\\section{Introduction}
Old introduction text.
\\section{Conclusion}
Final thoughts.
\\end{document}"""

    updated = fs.apply_section_replace(initial_latex, "Introduction", "New novel research methodology.")
    assert "New novel research methodology." in updated
    assert "Old introduction text." not in updated
    assert "\\section{Conclusion}" in updated


def test_clinical_protocol_template():
    fs = FileSystemManager()
    template_name = fs.match_template_by_prompt("Draft an IRB clinical trial protocol for biosensors")
    assert template_name == "clinical_protocal.tex"
    content = fs.load_template(template_name)
    assert "\\begin{document}" in content
    assert "Clinical Investigation Protocol" in content

