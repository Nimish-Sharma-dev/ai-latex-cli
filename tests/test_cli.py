import pytest
from typer.testing import CliRunner
from src.cli.main import app

runner = CliRunner()


def test_cli_list_templates():
    result = runner.invoke(app, ["list-templates"])
    assert result.exit_code == 0
    assert "ieee_paper.tex" in result.stdout
    assert "project_report.tex" in result.stdout


def test_cli_config():
    result = runner.invoke(app, ["config"])
    assert result.exit_code == 0
    assert "AI Provider Configuration" in result.stdout
    assert "Antigravity Engine" in result.stdout


def test_cli_audit(tmp_path):
    (tmp_path / "test.py").write_text("print('test')\n", encoding="utf-8")
    result = runner.invoke(app, ["audit", str(tmp_path)])
    assert result.exit_code == 0
    assert "Summary Metrics" in result.stdout
    assert "Python" in result.stdout
