import pytest
from pathlib import Path
from src.core.figure_generator import FigureGenerator


def test_figure_generation(tmp_path):
    fig_gen = FigureGenerator(tmp_path)
    figures = fig_gen.generate_all_figures("TestProject", {"project_name": "TestProject"})

    assert len(figures) == 3
    for fig in figures:
        full_fig_path = tmp_path / fig["path"]
        assert full_fig_path.exists(), f"Figure file does not exist: {full_fig_path}"
        assert full_fig_path.stat().st_size > 1000
