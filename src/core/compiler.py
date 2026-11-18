"""
LaTeX Compilation Engine: Multi-engine support (latexmk, pdflatex, xelatex),
multi-pass reference resolution, error log parsing, auxiliary cleanup, and packaging.
"""

import os
import shutil
import subprocess
import time
import re
import zipfile
from pathlib import Path
from typing import Dict, Any, Optional, List


class LaTeXCompiler:
    def __init__(self, preferred_compiler: str = "pdflatex", timeout: int = 120):
        self.preferred_compiler = preferred_compiler
        self.timeout = timeout

    def check_compiler_available(self, compiler_name: Optional[str] = None) -> bool:
        """Checks if the given compiler is installed and available in PATH."""
        comp = compiler_name or self.preferred_compiler
        return shutil.which(comp) is not None

    def compile(
        self,
        tex_path: str | Path,
        compiler: Optional[str] = None,
        output_dir: Optional[str | Path] = None,
        clean: bool = False
    ) -> Dict[str, Any]:
        """Compiles a .tex file to PDF with error parsing and multi-pass resolution."""
        src_path = Path(tex_path).resolve()
        if not src_path.exists():
            return {
                "success": False,
                "error": f"Source file does not exist: {src_path}",
                "pdf_path": None,
                "duration": 0.0,
                "warnings": 0
            }

        work_dir = src_path.parent
        out_directory = Path(output_dir).resolve() if output_dir else work_dir
        out_directory.mkdir(parents=True, exist_ok=True)

        engine = compiler or self.preferred_compiler

        # Fallback if preferred isn't found
        if not self.check_compiler_available(engine):
            for candidate in ["latexmk", "pdflatex", "xelatex"]:
                if self.check_compiler_available(candidate):
                    engine = candidate
                    break

        # If still no compiler is found in PATH
        if not self.check_compiler_available(engine):
            bundle_zip = self.create_overleaf_package(src_path, out_directory)
            return {
                "success": False,
                "no_compiler": True,
                "compiler_missing": engine,
                "error": (
                    f"LaTeX compiler '{engine}' was not found on your system PATH.\n"
                    f"To compile locally, please install MiKTeX (Windows) or TeX Live.\n"
                    f"A complete Overleaf-ready project package has been generated at:\n  {bundle_zip}"
                ),
                "package_path": str(bundle_zip),
                "pdf_path": None,
                "duration": 0.0,
                "warnings": 0
            }

        start_time = time.time()
        
        # Build compilation command
        if engine == "latexmk":
            cmd = [
                "latexmk",
                "-pdf",
                f"-outdir={str(out_directory)}",
                "-interaction=nonstopmode",
                "-synctex=1",
                src_path.name
            ]
        else:
            cmd = [
                engine,
                "-interaction=nonstopmode",
                f"-output-directory={str(out_directory)}",
                src_path.name
            ]

        try:
            # First pass
            proc = subprocess.run(
                cmd,
                cwd=str(work_dir),
                capture_output=True,
                text=True,
                timeout=self.timeout
            )
            
            # Second pass for resolving TOC, references, citations if using pdflatex
            if engine != "latexmk" and proc.returncode == 0:
                subprocess.run(
                    cmd,
                    cwd=str(work_dir),
                    capture_output=True,
                    text=True,
                    timeout=self.timeout
                )

            duration = round(time.time() - start_time, 2)
            pdf_path = out_directory / f"{src_path.stem}.pdf"
            log_path = out_directory / f"{src_path.stem}.log"

            # Parse log file for diagnostics
            diagnostics = self._parse_log_file(log_path if log_path.exists() else None, proc.stdout)

            success = proc.returncode == 0 and pdf_path.exists()

            if clean and success:
                self.clean_auxiliary_files(out_directory, src_path.stem)

            return {
                "success": success,
                "pdf_path": str(pdf_path) if pdf_path.exists() else None,
                "duration": duration,
                "warnings": diagnostics["warnings_count"],
                "error": diagnostics["first_error"] if not success else None,
                "error_details": diagnostics["errors"],
                "stdout": proc.stdout,
                "stderr": proc.stderr
            }

        except subprocess.TimeoutExpired:
            return {
                "success": False,
                "error": f"Compilation timed out after {self.timeout} seconds.",
                "pdf_path": None,
                "duration": self.timeout,
                "warnings": 0
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"Unexpected compilation error: {str(e)}",
                "pdf_path": None,
                "duration": round(time.time() - start_time, 2),
                "warnings": 0
            }

    def _parse_log_file(self, log_path: Optional[Path], raw_stdout: str) -> Dict[str, Any]:
        content = ""
        if log_path and log_path.exists():
            try:
                content = log_path.read_text(encoding="utf-8", errors="ignore")
            except Exception:
                pass
        if not content:
            content = raw_stdout

        errors = []
        warnings = 0
        first_error = None

        lines = content.splitlines()
        for i, line in enumerate(lines):
            if "Warning:" in line or "LaTeX Warning:" in line:
                warnings += 1
            if line.startswith("!"):
                err_msg = line.strip()
                context = "\n".join(lines[max(0, i-1):min(len(lines), i+4)])
                errors.append({"message": err_msg, "context": context})
                if not first_error:
                    first_error = err_msg

        return {
            "errors": errors,
            "first_error": first_error or ("Compilation failed (check output log)" if errors else None),
            "warnings_count": warnings
        }

    def clean_auxiliary_files(self, directory: Path, stem: str):
        """Removes auxiliary files (.aux, .log, .out, .toc, .fls, etc.)."""
        exts = [".aux", ".log", ".out", ".toc", ".lof", ".lot", ".fls", ".fdb_latexmk", ".synctex.gz"]
        for ext in exts:
            aux_file = directory / f"{stem}{ext}"
            if aux_file.exists():
                try:
                    aux_file.unlink()
                except Exception:
                    pass

    def create_overleaf_package(self, tex_path: Path, output_dir: Path) -> Path:
        """Packages the LaTeX project into a standalone zip file for Overleaf / archive."""
        zip_path = output_dir / f"{tex_path.stem}_overleaf_bundle.zip"
        src_dir = tex_path.parent

        with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
            zf.write(tex_path, arcname=tex_path.name)
            figures_dir = src_dir / "figures"
            if figures_dir.exists():
                for fig in figures_dir.glob("*"):
                    if fig.is_file():
                        zf.write(fig, arcname=f"figures/{fig.name}")
            bib_file = src_dir / "references.bib"
            if bib_file.exists():
                zf.write(bib_file, arcname="references.bib")

        return zip_path


# Module-level helper for backwards compatibility
def compile_tex_to_pdf(tex_file_path: str | Path, output_dir: str | Path = "outputs") -> Path:
    """Compiles a .tex file into a PDF using LaTeXCompiler."""
    compiler = LaTeXCompiler()
    res = compiler.compile(tex_file_path, output_dir=output_dir)
    if res.get("pdf_path"):
        return Path(res["pdf_path"])
    if res.get("no_compiler"):
        raise RuntimeError(res["error"])
    raise RuntimeError(res.get("error") or "LaTeX compilation failed.")
