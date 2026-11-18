"""
Main CLI Application: latex-ai
Rich terminal interface supporting free AI providers, repository auditing,
project generation, zero-placeholder LaTeX reports, figures, screenshots, and compilation.
"""

import sys
import os
from pathlib import Path
from typing import Optional
import typer
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.prompt import Prompt

# Import core modules
from ..core.fs_manager import FileSystemManager, select_template
from ..core.compiler import LaTeXCompiler, compile_tex_to_pdf
from ..core.repo_auditor import RepoAuditor
from ..core.report_generator import ReportGenerator
from ..core.project_coder import ProjectCoder
from ..core.registry_manager import RegistryManager
from ..api.llm_client import LLMClient
from ..api import deepseek
from ..api.config import get_settings

# Set console encoding safely on Windows
if sys.platform == "win32":
    try:
        if hasattr(sys.stdout, "reconfigure"):
            sys.stdout.reconfigure(encoding="utf-8")
        if hasattr(sys.stderr, "reconfigure"):
            sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

console = Console(highlight=False)

app = typer.Typer(
    name="latex-ai",
    help="AI CLI-Based LaTeX Generation & Repository Reporting System",
    add_completion=False
)


@app.callback()
def main_callback(
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Show verbose debugging logs"),
    dry_run: bool = typer.Option(False, "--dry-run", help="Simulate actions without writing files"),
    no_backup: bool = typer.Option(False, "--no-backup", help="Skip creating .bak files")
):
    """AI LaTeX CLI: Generate, Audit, Code, and Typeset publication-ready LaTeX documents."""
    pass


@app.command()
def generate(prompt: str):
    """Generate LaTeX documents matching template structures automatically."""
    typer.echo(" Analyzing prompt and selecting matching structural template...")
    template_content = select_template(prompt)
    typer.echo(" Processing workspace requirements with AI Engine...")
    
    try:
        final_latex = deepseek.call_llm(prompt, template=template_content)
        typer.secho("\n LaTeX Document Successfully Constructed:", fg=typer.colors.GREEN, bold=True)
        typer.echo(final_latex)
        
        output_dir = Path("outputs")
        output_dir.mkdir(exist_ok=True)
        
        n = 1
        while (output_dir / f"{n}.tex").exists():
            n += 1
            
        output_file = output_dir / f"{n}.tex"
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


@app.command()
def audit(
    repo_path: str = typer.Argument(".", help="Path to the repository or directory to audit"),
    json_output: bool = typer.Option(False, "--json", help="Output raw JSON analysis")
):
    """Audit a codebase: scans files, AST symbols, dependencies, and architecture."""
    with console.status("[bold green]Auditing repository structure and code metrics..."):
        auditor = RepoAuditor(repo_path)
        data = auditor.audit()

    if json_output:
        import json
        console.print_json(json.dumps(data, indent=2))
        return

    # Visual Audit Report
    console.print(Panel.fit(
        f"[bold cyan][AUDIT] Codebase Audit Report: {data['project_name']}[/bold cyan]\n"
        f"Location: [italic]{data['root_path']}[/italic]",
        border_style="cyan"
    ))

    # Metrics summary table
    table = Table(title="Summary Metrics", border_style="dim")
    table.add_column("Metric", style="bold yellow")
    table.add_column("Value", style="green")

    table.add_row("Primary Language", data["primary_language"])
    table.add_row("Total Files", str(data["total_files"]))
    table.add_row("Total Code Lines (LOC)", f"{data['total_loc']:,}")
    table.add_row("Frameworks Detected", ", ".join(data["frameworks"]) if data["frameworks"] else "None")
    table.add_row("Dependencies", ", ".join(data["dependencies"][:6]) if data["dependencies"] else "None")

    console.print(table)

    # Language breakdown table
    lang_table = Table(title="Language Distribution", border_style="dim")
    lang_table.add_column("Language", style="cyan")
    lang_table.add_column("Files", justify="right")
    lang_table.add_column("Lines of Code", justify="right", style="magenta")

    for lang, count in data["languages"].items():
        loc = data["language_loc"].get(lang, 0)
        lang_table.add_row(lang, str(count), f"{loc:,}")

    console.print(lang_table)

    if data["modules_summary"]:
        console.print("\n[bold]Key Analyzed Modules:[/bold]")
        for mod in data["modules_summary"][:5]:
            cls_str = f"Classes: {', '.join(mod['classes'])}" if mod['classes'] else ""
            fn_str = f"Functions: {', '.join(mod['functions'][:4])}" if mod['functions'] else ""
            details = " | ".join(filter(None, [cls_str, fn_str]))
            console.print(f"  • [blue]{mod['path']}[/blue] ({details})")


@app.command()
def report(
    repo_path: str = typer.Argument(".", help="Path to repository to document"),
    format: Optional[str] = typer.Option(
        None, "--format", "-f",
        help="Report format: ieee, standard, report (thesis), acm, presentation"
    ),
    author: str = typer.Option("Engineering Research Team", "--author", "-a", help="Author name"),
    institution: str = typer.Option("Department of Computer Science & Engineering", "--inst", help="Institution name"),
    email: str = typer.Option("contact@project-research.org", "--email", help="Author email"),
    no_compile: bool = typer.Option(False, "--no-compile", help="Skip compiling to PDF")
):
    """
    Generate a full LaTeX report for a repository with zero placeholders,
    including system architecture diagrams, benchmark charts, screenshots, and citations.
    """
    console.print(Panel.fit("[bold green][START] AI LaTeX Report Generation Engine[/bold green]"))

    selected_format = format
    reg = RegistryManager()
    custom_formats = reg.list_formats()

    if not selected_format:
        console.print("[yellow]Select document format:[/yellow]")
        console.print("  [1] [bold]ieee[/bold]        -- Double-column IEEE Conference/Transactions paper")
        console.print("  [2] [bold]report[/bold]      -- Comprehensive University/Project Report (with Chapters)")
        console.print("  [3] [bold]standard[/bold]    -- Clean standard academic/technical article")
        console.print("  [4] [bold]acm[/bold]         -- ACM Conference proceedings format")
        console.print("  [5] [bold]presentation[/bold]-- Beamer widescreen slide deck")

        mapping = {"1": "ieee", "2": "report", "3": "standard", "4": "acm", "5": "presentation"}
        valid_choices = ["1", "2", "3", "4", "5", "ieee", "report", "standard", "acm", "presentation"]

        for idx, cf in enumerate(custom_formats, start=6):
            console.print(f"  [{idx}] [bold]{cf['name']}[/bold] -- {cf['description']}")
            mapping[str(idx)] = cf["identifier"]
            valid_choices.extend([str(idx), cf["identifier"], cf["name"]])

        choice = Prompt.ask("Choose format", choices=valid_choices, default="1")
        selected_format = mapping.get(choice, choice)

    # Check for matched skills and harnesses
    matched_skills = reg.match_skills(repo_path)
    matched_harnesses = reg.match_harnesses(repo_path)
    if matched_skills:
        console.print(f"[bold cyan][SKILL IN USE][/bold cyan] Active Skills: {', '.join([s['name'] for s in matched_skills])}")
    if matched_harnesses:
        console.print(f"[bold magenta][HARNESS IN USE][/bold magenta] Active Harnesses: {', '.join([h['name'] for h in matched_harnesses])}")

    with console.status(f"[bold cyan]Auditing repository and generating {selected_format.upper()} report...[/bold cyan]"):
        generator = ReportGenerator(output_root="outputs")
        res = generator.generate_report(
            repo_path=repo_path,
            format_type=selected_format,
            author_name=author,
            institution=institution,
            author_email=email
        )

    console.print("\n[bold green][SUCCESS] Report Generation Complete![/bold green]")
    console.print(f"[TEX] LaTeX Source:  [cyan]{res['tex_path']}[/cyan]")
    console.print(f"[BIB] BibTeX File:   [cyan]{res['bibtex_path']}[/cyan]")
    console.print(f"[FIG] Figures & UI:  [cyan]{', '.join(res['figures_generated'])}[/cyan]")

    if res.get("pdf_path"):
        console.print(f"[PDF] Compiled PDF:  [bold green]{res['pdf_path']}[/bold green]")
    elif res.get("compile_status", {}).get("no_compiler"):
        console.print(f"[yellow][NOTICE][/yellow] {res['compile_status']['error']}")
    else:
        console.print(f"[red][ERROR][/red] {res.get('compile_status', {}).get('error')}")


@app.command()
def build(
    prompt: Optional[str] = typer.Argument(None, help="Natural language description of the project to create"),
    format: Optional[str] = typer.Option(None, "--format", "-f", help="Target LaTeX report format"),
    target_dir: Optional[str] = typer.Option(None, "--dir", "-d", help="Target output folder name")
):
    """
    End-to-End Workflow: Code a complete project from prompt,
    audit what was made, prompt for document format, and generate publication-ready LaTeX with diagrams and citations.
    """
    console.print(Panel.fit("[bold magenta][BUILD] Antigravity Autonomous Project Builder & Reporter[/bold magenta]"))

    project_prompt = prompt
    if not project_prompt:
        project_prompt = Prompt.ask("[bold cyan]Enter your project requirements & details[/bold cyan]")

    # 1. Code the project
    with console.status("[bold green]Coding project architecture, source files, and unit tests...[/bold green]"):
        coder = ProjectCoder(output_root=".")
        code_result = coder.code_project(project_prompt, target_dir_name=target_dir)

    console.print(f"\n[bold green][SUCCESS] Codebase successfully generated in:[/bold green] [cyan]{code_result['project_dir']}[/cyan]")
    for f in code_result["files_created"]:
        console.print(f"  + [dim]{f}[/dim]")

    # 2. Audit the project
    with console.status("[bold blue]Auditing created project architecture...[/bold blue]"):
        auditor = RepoAuditor(code_result["project_dir"])
        audit_data = auditor.audit()

    console.print("\n[bold cyan][AUDIT] Project Summary:[/bold cyan]")
    console.print(f"  * Files: {audit_data['total_files']} | Total LOC: {audit_data['total_loc']:,}")
    console.print(f"  * Modules: {', '.join([m['path'] for m in audit_data['modules_summary'][:3]])}")

    # 3. Ask for report format
    selected_format = format
    reg = RegistryManager()
    custom_formats = reg.list_formats()

    if not selected_format:
        console.print("\n[yellow]What format should the LaTeX report be in?[/yellow]")
        console.print("  [1] [bold]ieee[/bold]         -- IEEE Conference format")
        console.print("  [2] [bold]report[/bold]       -- Comprehensive University Project Report / Thesis")
        console.print("  [3] [bold]standard[/bold]     -- Academic Technical Article")
        console.print("  [4] [bold]acm[/bold]          -- ACM Conference format")
        console.print("  [5] [bold]presentation[/bold] -- Beamer Presentation Slides")

        mapping = {"1": "ieee", "2": "report", "3": "standard", "4": "acm", "5": "presentation"}
        valid_choices = ["1", "2", "3", "4", "5", "ieee", "report", "standard", "acm", "presentation"]

        for idx, cf in enumerate(custom_formats, start=6):
            console.print(f"  [{idx}] [bold]{cf['name']}[/bold]       -- {cf['description']}")
            mapping[str(idx)] = cf["identifier"]
            valid_choices.extend([str(idx), cf["identifier"], cf["name"]])

        choice = Prompt.ask("Choose format", choices=valid_choices, default="1")
        selected_format = mapping.get(choice, choice)

    # Check for matched skills and harnesses
    matched_skills = reg.match_skills(project_prompt)
    matched_harnesses = reg.match_harnesses(project_prompt)
    if matched_skills:
        console.print(f"[bold cyan][SKILL IN USE][/bold cyan] Active Skills: {', '.join([s['name'] for s in matched_skills])}")
    if matched_harnesses:
        console.print(f"[bold magenta][HARNESS IN USE][/bold magenta] Active Harnesses: {', '.join([h['name'] for h in matched_harnesses])}")

    # 4. Generate LaTeX Report
    with console.status(f"[bold green]Generating complete {selected_format.upper()} report with figures & citations...[/bold green]"):
        report_gen = ReportGenerator(output_root="outputs")
        report_res = report_gen.generate_report(
            repo_path=code_result["project_dir"],
            format_type=selected_format
        )

    console.print("\n[bold green][COMPLETE] Project and LaTeX Report Finished![/bold green]")
    console.print(f"[CODE] Codebase:    [cyan]{code_result['project_dir']}[/cyan]")
    console.print(f"[TEX]  LaTeX File:  [cyan]{report_res['tex_path']}[/cyan]")
    console.print(f"[BIB]  References:  [cyan]{report_res['bibtex_path']}[/cyan]")
    console.print(f"[FIG]  Figures:     [cyan]{', '.join(report_res['figures_generated'])}[/cyan]")
    if report_res.get("pdf_path"):
        console.print(f"[PDF]  PDF Report:  [bold green]{report_res['pdf_path']}[/bold green]")


@app.command()
def init(
    prompt: str = typer.Argument(..., help="Description of document to create"),
    output: Optional[str] = typer.Option(None, "--output", "-o", help="Output .tex filename"),
    template: Optional[str] = typer.Option(None, "--template", "-t", help="Template file to use"),
    no_compile: bool = typer.Option(False, "--no-compile", help="Skip compilation to PDF")
):
    """Create a new LaTeX document from natural language prompt."""
    fs = FileSystemManager()
    compiler = LaTeXCompiler()

    tpl_name = template or fs.match_template_by_prompt(prompt)
    tpl_content = fs.load_template(tpl_name)

    with console.status("[bold green]Synthesizing LaTeX document..."):
        generated_latex = deepseek.generate(prompt, template_context=tpl_content)

    out_file = output or "document.tex"
    out_path = Path("outputs") / out_file
    fs.write_file(out_path, generated_latex)

    console.print(f"[OK] Created [cyan]{out_path}[/cyan] using template [yellow]{tpl_name}[/yellow]")

    if not no_compile:
        with console.status("[bold cyan]Compiling to PDF..."):
            res = compiler.compile(out_path)
            if res["success"]:
                console.print(f"[PDF] PDF generated at: [bold green]{res['pdf_path']}[/bold green]")
            elif res.get("no_compiler"):
                console.print(f"[yellow][NOTICE][/yellow] {res['error']}")


@app.command()
def edit(
    file: str = typer.Argument(..., help="Path to .tex file"),
    prompt: str = typer.Argument(..., help="Instruction to apply"),
    section: Optional[str] = typer.Option(None, "--section", "-s", help="Restrict edit to named section"),
    append: bool = typer.Option(False, "--append", help="Append content rather than replacing"),
    no_recompile: bool = typer.Option(False, "--no-recompile", help="Skip verification compilation")
):
    """Modify an existing LaTeX document or section using natural language."""
    fs = FileSystemManager()
    compiler = LaTeXCompiler()
    file_path = Path(file)

    if not file_path.exists():
        console.print(f"[red]Error: File not found: {file}[/red]")
        raise typer.Exit(code=2)

    original_text = fs.read_file(file_path)

    with console.status("[bold green]Applying edits..."):
        if append:
            edited_chunk = deepseek.generate(prompt)
            updated_doc = fs.apply_append(original_text, edited_chunk)
        elif section:
            edited_chunk = deepseek.edit(original_text, prompt, section=section)
            updated_doc = fs.apply_section_replace(original_text, section, edited_chunk)
        else:
            updated_doc = deepseek.edit(original_text, prompt)

        fs.write_file(file_path, updated_doc, create_backup=True)

    console.print(f"[OK] Successfully updated [cyan]{file}[/cyan] (backup created)")

    if not no_recompile:
        with console.status("[bold cyan]Verifying compilation..."):
            res = compiler.compile(file_path)
            if res["success"]:
                console.print(f"[PDF] Verification PDF: [bold green]{res['pdf_path']}[/bold green]")
            elif not res.get("no_compiler"):
                console.print(f"[red][WARNING] Compilation warning/error:[/red] {res['error']}")


@app.command()
def table(
    file: str = typer.Argument(..., help="Target .tex file"),
    prompt: str = typer.Argument(..., help="Description of table"),
    position: str = typer.Option("end", "--position", help="Where to insert (end or after-section <name>)"),
    style: str = typer.Option("booktabs", "--style", help="Table style (booktabs, basic, longtable)")
):
    """Generate and insert a LaTeX table into an existing document."""
    fs = FileSystemManager()
    file_path = Path(file)

    if not file_path.exists():
        console.print(f"[red]Error: File not found: {file}[/red]")
        raise typer.Exit(code=2)

    with console.status("[bold green]Generating table..."):
        table_code = deepseek.generate_table(prompt, style=style)
        original_doc = fs.read_file(file_path)
        updated_doc = fs.insert_table(original_doc, table_code, position=position)
        fs.write_file(file_path, updated_doc, create_backup=True)

    console.print(f"[OK] Table inserted into [cyan]{file}[/cyan]")


@app.command()
def compile(
    file: str = typer.Argument(..., help="Path to .tex file to compile"),
    auto_fix: bool = typer.Option(False, "--auto-fix", help="Automatically attempt AI fix on compilation error"),
    compiler: str = typer.Option("pdflatex", "--compiler", help="Compiler engine (latexmk, pdflatex, xelatex)"),
    output_dir: Optional[str] = typer.Option(None, "--output-dir", "-o", help="Output directory for PDF"),
    clean: bool = typer.Option(False, "--clean", help="Remove auxiliary files (.aux, .log, .out)")
):
    """Compile a LaTeX document to PDF with error analysis."""
    c = LaTeXCompiler(preferred_compiler=compiler)
    with console.status(f"[bold cyan]Compiling {file} with {compiler}..."):
        res = c.compile(file, compiler=compiler, output_dir=output_dir, clean=clean)

    if res["success"]:
        console.print(f"[bold green][SUCCESS] Compilation successful in {res['duration']}s[/bold green]")
        console.print(f"[PDF] PDF: [cyan]{res['pdf_path']}[/cyan]")
    elif res.get("no_compiler"):
        console.print(f"[yellow][NOTICE][/yellow] {res['error']}")
    else:
        console.print(f"[red][ERROR] Compilation failed ({res['duration']}s)[/red]")
        console.print(f"Error: {res['error']}")
        if auto_fix:
            console.print("[yellow]Attempting auto-fix...[/yellow]")
            fix(file)


@app.command()
def fix(
    file: str = typer.Argument(..., help="Path to broken .tex file"),
    show_diff: bool = typer.Option(False, "--show-diff", help="Show diff of changes"),
    no_recompile: bool = typer.Option(False, "--no-recompile", help="Skip re-compilation after fix")
):
    """Automatically diagnose and fix LaTeX compilation errors."""
    fs = FileSystemManager()
    c = LaTeXCompiler()
    file_path = Path(file)

    if not file_path.exists():
        console.print(f"[red]Error: File not found: {file}[/red]")
        raise typer.Exit(code=2)

    original_code = fs.read_file(file_path)
    compile_res = c.compile(file_path)
    error_log = compile_res.get("stdout", "") + "\n" + str(compile_res.get("error", ""))

    with console.status("[bold green]Diagnosing error and generating fix..."):
        fixed_code = deepseek.fix(original_code, error_log)
        fs.write_file(file_path, fixed_code, create_backup=True)

    console.print(f"[OK] Fix applied to [cyan]{file}[/cyan] (backup created)")

    if not no_recompile:
        with console.status("[bold cyan]Re-compiling fixed document..."):
            verify_res = c.compile(file_path)
            if verify_res["success"]:
                console.print(f"[PDF] Fixed document compiled: [bold green]{verify_res['pdf_path']}[/bold green]")
            elif not verify_res.get("no_compiler"):
                console.print(f"[yellow][WARNING] Still has errors:[/yellow] {verify_res['error']}")


@app.command(name="list-templates")
def list_templates():
    """List all available LaTeX templates and trigger keywords."""
    fs = FileSystemManager()
    templates = fs.list_available_templates()

    table = Table(title="Available LaTeX Templates", border_style="cyan")
    table.add_column("Template", style="bold green")
    table.add_column("Keywords", style="yellow")
    table.add_column("Description", style="white")

    for t in templates:
        table.add_row(t["name"], t["keywords"], t["description"])

    console.print(table)


@app.command()
def config():
    """View and configure AI providers (Free Gemini, Groq, Ollama, Antigravity, DeepSeek)."""
    settings = get_settings()
    client = LLMClient()
    active = client.get_active_provider()

    console.print(Panel.fit(
        f"[bold cyan]AI Provider Configuration[/bold cyan]\n"
        f"Active Provider: [bold green]{active.upper()}[/bold green] "
        f"({'100% Free / Local' if active in ['antigravity', 'ollama', 'gemini', 'groq'] else 'Custom API'})\n\n"
        f"• Antigravity Engine: [green]Active (Default / Built-in)[/green]\n"
        f"• Google Gemini API:  {'[green]Configured[/green]' if settings.GEMINI_API_KEY else '[dim]Not configured (Set GEMINI_API_KEY)[/dim]'}\n"
        f"• Groq API:           {'[green]Configured[/green]' if settings.GROQ_API_KEY else '[dim]Not configured (Set GROQ_API_KEY)[/dim]'}\n"
        f"• Ollama (Local):     {'[green]Configured[/green]' if settings.OLLAMA_BASE_URL else '[dim]Not configured[/dim]'}\n"
        f"• DeepSeek API:       {'[green]Configured[/green]' if settings.DEEPSEEK_API_KEY else '[dim]Not configured (Legacy)[/dim]'}",
        border_style="cyan"
    ))


# ── Skills, Harnesses & Formats Registry Subcommands ─────────────────────────

skill_app = typer.Typer(help="Manage and store skills and skill repositories permanently")
harness_app = typer.Typer(help="Manage and store evaluation, benchmark, and test harnesses permanently")
format_app = typer.Typer(help="Manage and store custom LaTeX formats and templates permanently")

app.add_typer(skill_app, name="skill")
app.add_typer(harness_app, name="harness")
app.add_typer(format_app, name="format")


@skill_app.command("add")
def add_skill(
    name: str = typer.Argument(..., help="Skill name or identifier"),
    source: str = typer.Argument(..., help="GitHub repo URL, directory path, or description"),
    description: str = typer.Option("", "--desc", "-d", help="Description of what the skill does"),
    keywords: Optional[str] = typer.Option(None, "--keywords", "-k", help="Comma-separated trigger keywords")
):
    """Register and store a skill or skill repository forever."""
    reg = RegistryManager()
    kw = [k.strip() for k in keywords.split(",")] if keywords else None
    res = reg.register_skill(name=name, source_or_repo=source, description=description, keywords=kw)

    console.print(Panel.fit(
        f"[bold green][STORED FOREVER] Skill Registered![/bold green]\n"
        f"• Name:        [bold cyan]{res['name']}[/bold cyan] ({res['identifier']})\n"
        f"• Source:      [yellow]{res['source']}[/yellow]\n"
        f"• Description: {res['description']}\n"
        f"• Keywords:    {', '.join(res['keywords'])}\n\n"
        f"[dim]This skill will now be automatically recognized and incorporated into future project builds and LaTeX reports.[/dim]",
        border_style="green"
    ))


@skill_app.command("list")
def list_skills():
    """List all permanently registered skills and repositories."""
    reg = RegistryManager()
    skills = reg.list_skills()

    if not skills:
        console.print("[yellow]No custom skills registered yet. Use `latex-ai skill add` or `latex-ai learn`.[/yellow]")
        return

    table = Table(title="Permanently Stored Skills & Repositories", border_style="cyan")
    table.add_column("Skill Name", style="bold green")
    table.add_column("Source / Repo", style="yellow")
    table.add_column("Description", style="white")
    table.add_column("Triggers", style="magenta")

    for s in skills:
        table.add_row(s["name"], s["source"], s["description"], ", ".join(s.get("keywords", [])))

    console.print(table)


@harness_app.command("add")
def add_harness(
    name: str = typer.Argument(..., help="Harness name (e.g. swe-bench, unit-eval)"),
    command: str = typer.Argument(..., help="Command or script to execute harness"),
    type: str = typer.Option("evaluation", "--type", "-t", help="Type: evaluation, benchmark, test"),
    description: str = typer.Option("", "--desc", "-d", help="Description of harness purpose")
):
    """Register and store an evaluation, test, or benchmark harness forever."""
    reg = RegistryManager()
    res = reg.register_harness(name=name, command_or_runner=command, description=description, harness_type=type)

    console.print(Panel.fit(
        f"[bold green][STORED FOREVER] Harness Registered![/bold green]\n"
        f"• Name:    [bold cyan]{res['name']}[/bold cyan]\n"
        f"• Type:    [magenta]{res['type']}[/magenta]\n"
        f"• Command: [yellow]{res['command']}[/yellow]\n"
        f"• Desc:    {res['description']}\n\n"
        f"[dim]Whenever this harness or project evaluation is needed, it will be automatically applied.[/dim]",
        border_style="green"
    ))


@harness_app.command("list")
def list_harnesses():
    """List all permanently registered harnesses."""
    reg = RegistryManager()
    harnesses = reg.list_harnesses()

    if not harnesses:
        console.print("[yellow]No custom harnesses registered yet. Use `latex-ai harness add` or `latex-ai learn`.[/yellow]")
        return

    table = Table(title="Permanently Stored Harnesses", border_style="cyan")
    table.add_column("Harness Name", style="bold green")
    table.add_column("Type", style="magenta")
    table.add_column("Command", style="yellow")
    table.add_column("Description", style="white")

    for h in harnesses:
        table.add_row(h["name"], h["type"], h["command"], h["description"])

    console.print(table)


@format_app.command("add")
def add_format(
    name: str = typer.Argument(..., help="Format identifier (e.g. springer, nature, neurips)"),
    description: str = typer.Option("", "--desc", "-d", help="Format description"),
    doc_class: str = typer.Option("article", "--class", "-c", help="LaTeX document class"),
    margin: str = typer.Option("1in", "--margin", "-m", help="Page margin (e.g. 1in, 2cm)"),
    columns: str = typer.Option("onecolumn", "--columns", help="Column mode (onecolumn, twocolumn)"),
    template_file: Optional[str] = typer.Option(None, "--template", "-t", help="Path to custom .tex template file to import")
):
    """Register and store a new LaTeX formatting style forever."""
    reg = RegistryManager()
    tpl_content = None
    if template_file:
        tpl_path = Path(template_file)
        if tpl_path.exists():
            tpl_content = tpl_path.read_text(encoding="utf-8")

    styling_rules = {
        "document_class": doc_class,
        "margin": margin,
        "columns": columns
    }

    res = reg.register_format(
        name=name,
        description=description or f"Custom LaTeX format: {name}",
        template_content=tpl_content,
        styling_rules=styling_rules
    )

    console.print(Panel.fit(
        f"[bold green][STORED FOREVER] Custom LaTeX Format Registered![/bold green]\n"
        f"• Format Name:   [bold cyan]{res['name']}[/bold cyan]\n"
        f"• Template File: [yellow]{res['template_file']}[/yellow]\n"
        f"• Description:   {res['description']}\n\n"
        f"[dim]This format is now permanently selectable in `latex-ai report --format {res['identifier']}` and build prompts.[/dim]",
        border_style="green"
    ))


@format_app.command("list")
def list_formats():
    """List all permanently stored custom LaTeX formats."""
    reg = RegistryManager()
    formats = reg.list_formats()

    if not formats:
        console.print("[yellow]No custom formats registered yet. Built-in templates: ieee, report, standard, acm, presentation.[/yellow]")
        return

    table = Table(title="Permanently Stored Custom LaTeX Formats", border_style="cyan")
    table.add_column("Format Name", style="bold green")
    table.add_column("Template File", style="yellow")
    table.add_column("Description", style="white")

    for f in formats:
        table.add_row(f["name"], f["template_file"], f["description"])

    console.print(table)


@app.command()
def learn(
    instruction: str = typer.Argument(..., help="Natural language description of skill, repo, harness, or LaTeX format")
):
    """
    Intake and permanently store any skill, repo of skills, harness, or LaTeX formatting.
    Just mention it in natural language and the system remembers and applies it forever.
    """
    reg = RegistryManager()
    with console.status("[bold green]Analyzing and persisting knowledge permanently..."):
        res = reg.learn(instruction)

    console.print(Panel.fit("[bold green][KNOWLEDGE PERSISTED FOREVER][/bold green]"))

    if res["skills_added"]:
        for s in res["skills_added"]:
            console.print(f"  • [bold green]+ Skill Stored:[/bold green] [cyan]{s['name']}[/cyan] ({s['source']})")
    if res["harnesses_added"]:
        for h in res["harnesses_added"]:
            console.print(f"  • [bold green]+ Harness Stored:[/bold green] [cyan]{h['name']}[/cyan] -> `{h['command']}`")
    if res["formats_added"]:
        for f in res["formats_added"]:
            console.print(f"  • [bold green]+ LaTeX Format Stored:[/bold green] [cyan]{f['name']}[/cyan] -> `{f['template_file']}`")

    if not (res["skills_added"] or res["harnesses_added"] or res["formats_added"]):
        entry = reg.register_skill(name="custom_entry", source_or_repo=instruction, description=instruction)
        console.print(f"  • [bold green]+ Saved into Knowledge Base:[/bold green] [cyan]{entry['name']}[/cyan]")


if __name__ == "__main__":
    app()
