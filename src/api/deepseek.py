"""
DeepSeek API interface with automatic fallback to Free Providers (Gemini, Groq, Ollama, Antigravity).
"""

from typing import Optional
from .llm_client import LLMClient


class DeepSeekAPI:
    """
    Unified LLM API wrapper preserving DeepSeek compatibility
    while enabling free AI backends (Gemini, Groq, Ollama, Antigravity).
    """

    def __init__(self):
        self.client = LLMClient()

    def generate(self, prompt: str, template_context: Optional[str] = None) -> str:
        system_prompt = (
            "You are an expert LaTeX typesetter and academic technical writer. "
            "Output ONLY valid LaTeX code without markdown code blocks, backticks, or conversational preamble."
        )
        full_prompt = prompt
        if template_context:
            full_prompt = f"Template Context:\n{template_context}\n\nUser Request:\n{prompt}"
        return self.client.complete(full_prompt, system_prompt=system_prompt)

    def edit(self, original_text: str, instruction: str, section: Optional[str] = None) -> str:
        system_prompt = (
            "You are modifying existing LaTeX content. "
            "Preserve formatting, packages, and syntax integrity. Output ONLY the updated LaTeX code."
        )
        prompt = (
            f"Instruction: {instruction}\n"
            f"Target Section: {section if section else 'Entire document'}\n\n"
            f"Original LaTeX:\n{original_text}"
        )
        return self.client.complete(prompt, system_prompt=system_prompt)

    def fix(self, tex_content: str, error_log: str) -> str:
        system_prompt = (
            "You are a LaTeX debugging specialist. Analyze the error log and fix the LaTeX source code. "
            "Output ONLY the corrected, compilable LaTeX code."
        )
        prompt = (
            f"Compilation Error Log:\n{error_log}\n\n"
            f"Broken LaTeX Source:\n{tex_content}"
        )
        return self.client.complete(prompt, system_prompt=system_prompt)

    def generate_table(self, description: str, style: str = "booktabs") -> str:
        system_prompt = (
            "Generate a professional LaTeX table based on the user description. "
            f"Use the {style} style with \\begin{{table}} and appropriate caption and label. "
            "Output ONLY the LaTeX table code."
        )
        return self.client.complete(description, system_prompt=system_prompt)


# Module-level convenience functions
_default_api = DeepSeekAPI()

def call_llm(message: str, template: str = "") -> str:
    """Legacy helper function delegating to unified LLM client."""
    return _default_api.generate(message, template_context=template)

def generate(prompt: str, template_context: Optional[str] = None) -> str:
    return _default_api.generate(prompt, template_context)

def edit(original_text: str, instruction: str, section: Optional[str] = None) -> str:
    return _default_api.edit(original_text, instruction, section)

def fix(tex_content: str, error_log: str) -> str:
    return _default_api.fix(tex_content, error_log)

def generate_table(description: str, style: str = "booktabs") -> str:
    return _default_api.generate_table(description, style)
