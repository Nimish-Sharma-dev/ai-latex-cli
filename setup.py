"""
setup.py — AI LaTeX CLI Package Installer
==========================================

This file registers the `latex-ai` command as a globally callable
terminal tool when installed via:

    pip install -e .          (editable/development install)
    pip install .             (production install)

After installation, users can run:

    latex-ai --help
    latex-ai init "Start an IEEE paper about neural prosthetics"
    latex-ai compile paper.tex

The entry point maps the `latex-ai` shell command to the
`app` object defined in `src/cli/main.py` (a Typer application).

Domain Context:
    This package is built for biomedical engineering and healthcare
    documentation workflows, combining LaTeX typesetting with AI-assisted
    content generation via the DeepSeek API.
"""

from setuptools import setup, find_packages

# Read the long description from the project README
with open("README.md", encoding="utf-8") as f:
    long_description = f.read()

# Read runtime dependencies from requirements.txt
# (excludes dev/test-only packages by convention)
with open("requirements.txt", encoding="utf-8") as f:
    # Filter out comment lines and blank lines
    install_requires = [
        line.strip()
        for line in f
        if line.strip() and not line.startswith("#")
    ]

setup(
    # ── Package Identity ──────────────────────────────────────────────────────
    name="ai-latex-cli",
    version="0.1.0",
    author="Your Name / Your Organization",
    author_email="your.email@example.com",
    description=(
        "A terminal-native AI document engine for biomedical and healthcare "
        "LaTeX document generation, powered by DeepSeek LLM."
    ),
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/your-org/ai-latex-cli",
    license="MIT",

    # ── Package Discovery ─────────────────────────────────────────────────────
    packages=find_packages(where="src"),
    package_dir={"": "src"},

    # ── Include Non-Python Files (templates, docs) ────────────────────────────
    include_package_data=True,
    package_data={
        "": [
            "templates/*.tex",      # LaTeX template files
            "docs/*.md",            # Documentation files
        ]
    },

    # ── Python Version Requirement ────────────────────────────────────────────
    python_requires=">=3.10",

    # ── Runtime Dependencies ──────────────────────────────────────────────────
    install_requires=install_requires,

    # ── CLI Entry Point ───────────────────────────────────────────────────────
    # This is the key registration: it creates the `latex-ai` shell command
    # that calls the `app` object from src/cli/main.py
    entry_points={
        "console_scripts": [
            "latex-ai=cli.main:app",
        ],
    },

    # ── PyPI Classifiers (metadata) ───────────────────────────────────────────
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Science/Research",
        "Intended Audience :: Healthcare Industry",
        "Topic :: Scientific/Engineering :: Medical Science Apps.",
        "Topic :: Text Processing :: Markup :: LaTeX",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
        "Environment :: Console",
    ],

    # ── Project URLs ──────────────────────────────────────────────────────────
    project_urls={
        "Documentation": "https://github.com/your-org/ai-latex-cli/tree/main/docs",
        "Bug Tracker": "https://github.com/your-org/ai-latex-cli/issues",
        "Source": "https://github.com/your-org/ai-latex-cli",
    },
)
