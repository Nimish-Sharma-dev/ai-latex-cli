import pytest
from pathlib import Path
from src.core.repo_auditor import RepoAuditor


def test_repo_auditor_scan(tmp_path):
    # Setup mock files
    py_file = tmp_path / "sample.py"
    py_file.write_text("""
class DataProcessor:
    def process_records(self, data):
        return [x * 2 for x in data]

def compute_metrics():
    return {"status": "ok"}
""", encoding="utf-8")

    req_file = tmp_path / "requirements.txt"
    req_file.write_text("fastapi>=0.100.0\npydantic>=2.0\n", encoding="utf-8")

    auditor = RepoAuditor(tmp_path)
    data = auditor.audit()

    assert data["primary_language"] == "Python"
    assert data["total_files"] == 2
    assert "fastapi" in data["dependencies"]
    assert "pydantic" in data["dependencies"]
    assert len(data["modules_summary"]) == 1
    mod = data["modules_summary"][0]
    assert "DataProcessor" in mod["classes"]
    assert "compute_metrics" in mod["functions"]
