"""
Repository Auditor: Scans local repositories, extracts codebase architecture,
language metrics, AST symbols, dependencies, and git history for report generation.
"""

import os
import ast
import json
import re
from pathlib import Path
from typing import Dict, Any, List, Set, Optional


class RepoAuditor:
    IGNORED_DIRS = {
        ".git", ".svn", ".hg", "node_modules", "venv", ".venv", "env",
        "__pycache__", ".pytest_cache", ".mypy_cache", ".ruff_cache",
        "dist", "build", "target", ".next", ".nuxt", "coverage", ".idea", ".vscode"
    }

    BINARY_EXTENSIONS = {
        ".png", ".jpg", ".jpeg", ".gif", ".ico", ".pdf", ".exe", ".dll",
        ".so", ".dylib", ".bin", ".zip", ".tar", ".gz", ".pyc", ".db", ".sqlite"
    }

    LANGUAGE_MAP = {
        ".py": "Python",
        ".js": "JavaScript",
        ".ts": "TypeScript",
        ".jsx": "React JSX",
        ".tsx": "React TSX",
        ".rs": "Rust",
        ".go": "Go",
        ".cpp": "C++",
        ".c": "C",
        ".h": "C/C++ Header",
        ".java": "Java",
        ".cs": "C#",
        ".html": "HTML",
        ".css": "CSS",
        ".scss": "SCSS",
        ".tex": "LaTeX",
        ".sh": "Shell Script",
        ".ps1": "PowerShell",
        ".sql": "SQL",
        ".json": "JSON",
        ".yaml": "YAML",
        ".yml": "YAML",
        ".md": "Markdown"
    }

    def __init__(self, root_dir: str | Path = "."):
        self.root_dir = Path(root_dir).resolve()

    def audit(self) -> Dict[str, Any]:
        """Performs a comprehensive audit of the repository."""
        file_tree = []
        language_counts: Dict[str, int] = {}
        language_loc: Dict[str, int] = {}
        total_loc = 0
        total_files = 0
        dependencies: Set[str] = set()
        modules_summary: List[Dict[str, Any]] = []
        frameworks_detected: Set[str] = set()

        # Traverse directory
        for dirpath, dirnames, filenames in os.walk(self.root_dir):
            # Prune ignored directories in place
            dirnames[:] = [d for d in dirnames if d not in self.IGNORED_DIRS and not d.startswith(".")]

            rel_dir = Path(dirpath).relative_to(self.root_dir)

            for fname in filenames:
                ext = Path(fname).suffix.lower()
                if ext in self.BINARY_EXTENSIONS:
                    continue

                full_path = Path(dirpath) / fname
                rel_path = full_path.relative_to(self.root_dir)
                total_files += 1

                lang = self.LANGUAGE_MAP.get(ext, "Other")
                language_counts[lang] = language_counts.get(lang, 0) + 1

                loc = 0
                file_text = ""
                try:
                    file_text = full_path.read_text(encoding="utf-8", errors="ignore")
                    lines = file_text.splitlines()
                    loc = len([l for l in lines if l.strip()])
                except Exception:
                    pass

                total_loc += loc
                language_loc[lang] = language_loc.get(lang, 0) + loc
                file_tree.append(str(rel_path))

                # Check for dependencies manifests
                if fname.lower() == "requirements.txt":
                    dependencies.update(self._parse_requirements(file_text))
                elif fname.lower() == "package.json":
                    dependencies.update(self._parse_package_json(file_text))
                elif fname.lower() == "cargo.toml":
                    dependencies.update(self._parse_cargo_toml(file_text))

                # Analyze python source symbols
                if ext == ".py" and loc > 0:
                    mod_info = self._analyze_python_file(rel_path, file_text)
                    if mod_info["classes"] or mod_info["functions"]:
                        modules_summary.append(mod_info)
                    
                    # Detect common frameworks from imports
                    for imp in mod_info.get("imports", []):
                        for fw in ["fastapi", "flask", "django", "typer", "click", "torch", "tensorflow", "sklearn", "streamlit", "pydantic"]:
                            if fw in imp.lower():
                                frameworks_detected.add(fw.capitalize())

        # Read README if present
        readme_summary = self._extract_readme_summary()

        # Calculate primary language
        primary_language = "Python"
        if language_loc:
            primary_language = max(language_loc.items(), key=lambda x: x[1])[0]

        # Git metadata
        git_info = self._extract_git_info()

        return {
            "project_name": self.root_dir.name,
            "root_path": str(self.root_dir),
            "primary_language": primary_language,
            "total_files": total_files,
            "total_loc": total_loc,
            "languages": language_counts,
            "language_loc": language_loc,
            "frameworks": sorted(list(frameworks_detected)),
            "dependencies": sorted(list(dependencies)),
            "file_tree": sorted(file_tree)[:80],
            "modules_summary": modules_summary[:15],
            "readme_summary": readme_summary,
            "git_info": git_info
        }

    def _parse_requirements(self, text: str) -> List[str]:
        deps = []
        for line in text.splitlines():
            line = line.strip()
            if line and not line.startswith("#"):
                pkg = re.split(r"[><=~;]", line)[0].strip()
                if pkg:
                    deps.append(pkg)
        return deps

    def _parse_package_json(self, text: str) -> List[str]:
        deps = []
        try:
            data = json.loads(text)
            for k in ["dependencies", "devDependencies"]:
                if k in data and isinstance(data[k], dict):
                    deps.extend(data[k].keys())
        except Exception:
            pass
        return deps

    def _parse_cargo_toml(self, text: str) -> List[str]:
        deps = []
        in_deps = False
        for line in text.splitlines():
            line = line.strip()
            if line.startswith("[dependencies]") or line.startswith("[dev-dependencies]"):
                in_deps = True
                continue
            elif line.startswith("["):
                in_deps = False
            if in_deps and "=" in line and not line.startswith("#"):
                pkg = line.split("=")[0].strip()
                if pkg:
                    deps.append(pkg)
        return deps

    def _analyze_python_file(self, rel_path: Path, code_text: str) -> Dict[str, Any]:
        classes = []
        functions = []
        imports = []
        try:
            tree = ast.parse(code_text)
            for node in ast.walk(tree):
                if isinstance(node, ast.ClassDef):
                    classes.append(node.name)
                elif isinstance(node, ast.FunctionDef) or isinstance(node, getattr(ast, "AsyncFunctionDef", ast.FunctionDef)):
                    if not node.name.startswith("_"):
                        functions.append(node.name)
                elif isinstance(node, ast.Import):
                    for alias in node.names:
                        imports.append(alias.name)
                elif isinstance(node, ast.ImportFrom):
                    if node.module:
                        imports.append(node.module)
        except Exception:
            pass

        return {
            "path": str(rel_path),
            "classes": classes[:5],
            "functions": functions[:8],
            "imports": list(set(imports))[:8]
        }

    def _extract_readme_summary(self) -> str:
        for r_name in ["README.md", "readme.md", "README.txt", "readme.txt"]:
            r_path = self.root_dir / r_name
            if r_path.exists():
                try:
                    text = r_path.read_text(encoding="utf-8", errors="ignore")
                    lines = [l.strip() for l in text.splitlines() if l.strip() and not l.startswith("#")]
                    return " ".join(lines[:6])
                except Exception:
                    pass
        return "Comprehensive codebase architecture and software pipeline."

    def _extract_git_info(self) -> Dict[str, Any]:
        git_dir = self.root_dir / ".git"
        if not git_dir.exists():
            return {"is_git": False, "recent_commits": [], "commit_count": 0}

        try:
            import subprocess
            res = subprocess.run(
                ["git", "log", "-n", "5", "--pretty=format:%h - %s (%an)"],
                cwd=str(self.root_dir),
                capture_output=True,
                text=True,
                timeout=5
            )
            commits = res.stdout.strip().splitlines() if res.returncode == 0 else []
            return {
                "is_git": True,
                "recent_commits": commits,
                "commit_count": len(commits)
            }
        except Exception:
            return {"is_git": True, "recent_commits": [], "commit_count": 0}
