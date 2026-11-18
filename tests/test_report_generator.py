import pytest
import re
from pathlib import Path
from src.core.report_generator import ReportGenerator


def test_report_generation_zero_placeholders(tmp_path):
    # Setup mock repo
    repo = tmp_path / "mock_project"
    repo.mkdir()
    (repo / "main.py").write_text("def run():\n    print('ok')\n", encoding="utf-8")
    (repo / "requirements.txt").write_text("requests>=2.0\n", encoding="utf-8")

    out_root = tmp_path / "outputs"
    gen = ReportGenerator(output_root=out_root)
    res = gen.generate_report(repo, format_type="ieee")

    assert res["success"] is True
    tex_path = Path(res["tex_path"])
    assert tex_path.exists()

    content = tex_path.read_text(encoding="utf-8")
    # Strictly ensure zero <<<PLACEHOLDERS>>>
    leftover = re.findall(r"<<<[A-Z0-9_]+>>>", content)
    assert len(leftover) == 0, f"Found unresolved placeholders: {leftover}"

    # Verify figures & citations present
    assert "\\includegraphics" in content
    assert "\\cite{" in content
    assert "\\begin{thebibliography}" in content or "\\bibliography" in content
