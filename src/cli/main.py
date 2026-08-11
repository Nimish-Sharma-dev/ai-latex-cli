import typer
from pathlib import Path  
from src.core.fs_manager import select_template
from src.api.deepseek import call_llm
from dotenv import load_dotenv
from src.core.compiler import compile_tex_to_pdf

load_dotenv()

app = typer.Typer(help="AI LaTeX CLI System")

@app.command()
def generate(prompt: str):
    """
    Generate LaTeX documents matching template structures automatically.
    """
    typer.echo(" Analyzing prompt and selecting matching structural template...")
    
    template_content = select_template(prompt)
    
    typer.echo(" Processing workspace requirements with DeepSeek...")
    
    try:
        final_latex = call_llm(prompt, template=template_content)
        
        typer.secho("\n LaTeX Document Successfully Constructed:", fg=typer.colors.GREEN, bold=True)
        typer.echo(final_latex)
        
        # 1. Ensure the outputs directory exists
        output_dir = Path("outputs")
        output_dir.mkdir(exist_ok=True)
        
        # 2. Find the next available sequential number (n)
        n = 1
        while (output_dir / f"{n}.tex").exists():
            n += 1
            
        output_file = output_dir / f"{n}.tex"
        
        # 3. Write the content to the file
        output_file.write_text(final_latex, encoding="utf-8")
        typer.secho(f" Document saved successfully to: {output_file}", fg=typer.colors.CYAN, bold=True)

        try:
            typer.echo(" Compiling generated LaTeX code into a PDF format...")
            pdf_path = compile_tex_to_pdf(output_file)
            typer.secho(f" PDF Successfully generated: {pdf_path}", fg=typer.colors.GREEN, bold=True)
        except Exception as compile_err:
            typer.secho(f" LaTeX saved, but PDF compilation failed: {compile_err}", fg=typer.colors.YELLOW)
        
    except Exception as e:
        typer.secho(f"\n Error processing pipeline: {e}", fg=typer.colors.RED, err=True)

if __name__ == "__main__":
    app()