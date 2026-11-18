import pytest
from pathlib import Path
from src.core.registry_manager import RegistryManager


def test_registry_manager_skills(tmp_path):
    reg = RegistryManager(workspace_root=tmp_path)
    res = reg.register_skill(
        name="audio-dsp",
        source_or_repo="https://github.com/test/audio-dsp",
        description="Audio signal processing skill"
    )

    assert res["identifier"] == "audio-dsp"
    skills = reg.list_skills()
    assert len(skills) == 1
    assert skills[0]["name"] == "audio-dsp"

    matched = reg.match_skills("This project uses audio dsp filtering")
    assert len(matched) == 1


def test_registry_manager_harnesses(tmp_path):
    reg = RegistryManager(workspace_root=tmp_path)
    h = reg.register_harness(
        name="unit-harness",
        command_or_runner="pytest tests/unit",
        harness_type="test"
    )

    assert h["identifier"] == "unit-harness"
    harnesses = reg.list_harnesses()
    assert len(harnesses) == 1


def test_registry_manager_formats(tmp_path):
    reg = RegistryManager(workspace_root=tmp_path)
    f = reg.register_format(
        name="neurips",
        description="NeurIPS conference format",
        styling_rules={"document_class": "article", "margin": "1in", "columns": "onecolumn"}
    )

    assert f["identifier"] == "neurips"
    tpl = tmp_path / "templates" / "neurips.tex"
    assert tpl.exists()
    assert "\\begin{document}" in tpl.read_text(encoding="utf-8")

    matched = reg.match_format("neurips")
    assert matched is not None


def test_registry_manager_learn(tmp_path):
    reg = RegistryManager(workspace_root=tmp_path)
    learned = reg.learn("I want to use the skill repo https://github.com/org/ai-skill with two column latex format for ieee")
    assert len(learned["skills_added"]) >= 1
    assert len(learned["formats_added"]) >= 1
