"""Core modules package."""
from .fs_manager import FileSystemManager
from .compiler import LaTeXCompiler
from .repo_auditor import RepoAuditor
from .figure_generator import FigureGenerator
from .citation_manager import CitationManager
from .project_coder import ProjectCoder
from .report_generator import ReportGenerator
from .registry_manager import RegistryManager

__all__ = [
    "FileSystemManager",
    "LaTeXCompiler",
    "RepoAuditor",
    "FigureGenerator",
    "CitationManager",
    "ProjectCoder",
    "ReportGenerator",
    "RegistryManager",
]
