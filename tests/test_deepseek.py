import pytest
from src.api.deepseek import DeepSeekAPI, generate, edit, fix, generate_table


def test_deepseek_api_offline_synthesizer():
    api = DeepSeekAPI()
    table = api.generate_table("comparison table")
    assert "\\begin{table}" in table
    assert "\\end{table}" in table
