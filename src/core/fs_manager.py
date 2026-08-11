import os
from pathlib import Path
from .intent_parser import parse_intent

# Locate the templates directory relative to this file's root directory
TEMPLATES_DIR = Path(__file__).resolve().parents[2] / "templates"

def select_template(prompt: str) -> str:
    """
    Accepts the raw prompt from main.py, gets the parsed intent from
    intent_parser, and returns the contents of the matching LaTeX template.
    """
    # 1. Pass the prompt to the intent parser to get the intent category
    intent = parse_intent(prompt)
    
    # Normalize intent to lowercase for matching
    intent_lower = str(intent).lower()
    
    # 2. Match the template based on the returned intent
    if intent_lower =="ieee":
        template_file = "ieee_paper.tex"
    elif intent_lower == "presentation":
        template_file = "presentation.tex"
    elif intent_lower == "clinical_protocol":
        template_file = "clinical_protocol.tex"
    else:
        template_file = "standard_article.tex"
        
    template_path = TEMPLATES_DIR / template_file
    
    # 3. Read and return the template file text safely
    if template_path.exists():
        template=template_path.read_text(encoding="utf-8")
        return template
    else:
        # Crucial Debug: Print this out to verify where it is looking if it still fails
        print(f"DEBUG ERROR: Could not find template at: {template_path.resolve()}")
        return ""