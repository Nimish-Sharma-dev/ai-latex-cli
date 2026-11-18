import pytest
from pathlib import Path
from src.core.compiler import LaTeXCompiler


def test_compiler_init():
    compiler = LaTeXCompiler()
    assert compiler.preferred_compiler == "pdflatex"
    assert compiler.timeout == 120
