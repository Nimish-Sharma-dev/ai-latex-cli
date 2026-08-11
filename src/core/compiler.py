import subprocess
import shutil
from pathlib import Path

def compile_tex_to_pdf(tex_file_path: str | Path, output_dir: str | Path = "outputs") -> Path:
    """
    Compiles a .tex file into a PDF using pdflatex.
    Cleans up auxiliary compilation files automatically.
    """
    tex_path = Path(tex_file_path)
    base_output_path = Path(output_dir)
    pdf_output_dir = base_output_path / "pdfs"
    
    if not tex_path.exists():
        raise FileNotFoundError(f"LaTeX file not found at: {tex_path}")
        
    # Ensure output directories exist
    pdf_output_dir.mkdir(parents=True, exist_ok=True)
    
    # Check if pdflatex is installed on the system
    if not shutil.which("pdflatex"):
        raise RuntimeError(
            "pdflatex command not found. Please ensure a TeX distribution "
            "(MikTeX or TeX Live) is installed and added to your system PATH."
        )

    print(f"Compiling {tex_path.name} to PDF...")
    
    # We run pdflatex pointing its output directory to our base output folder
    # -interaction=nonstopmode stops it from pausing the CLI if there's a syntax error in your LaTeX
    command = [
        "pdflatex",
        "-interaction=nonstopmode",
        f"-output-directory={base_output_path}",
        str(tex_path)
    ]
    
    # Run the compilation process
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    
    if result.returncode != 0:
        print(result.stdout) # Print out the log so you can debug LaTeX formatting issues
        raise RuntimeError(f"LaTeX compilation failed for {tex_path.name}. Check output above for errors.")

    # Paths to the generated files
    generated_pdf = base_output_path / f"{tex_path.stem}.pdf"
    final_pdf_path = pdf_output_dir / f"{tex_path.stem}.pdf"
    
    # Move the PDF into its clean final home: outputs/pdfs/n.pdf
    if generated_pdf.exists():
        shutil.move(str(generated_pdf), str(final_pdf_path))
    
    # --- AUTOMATIC CLEANUP ---
    # pdflatex drops messy logs/aux files in the output directory. Let's sweep them up.
    extensions_to_clean = [".aux", ".log", ".out", ".synctex.gz"]
    for ext in extensions_to_clean:
        aux_file = base_output_path / f"{tex_path.stem}{ext}"
        if aux_file.exists():
            aux_file.unlink()

    print(f"Success! PDF safely compiled to: {final_pdf_path}")
    return final_pdf_path

