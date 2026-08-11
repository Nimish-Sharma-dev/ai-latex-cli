from __future__ import annotations
import json
import os
from pathlib import Path
from openai import OpenAI

MODEL = os.getenv("DEEPSEEK_MODEL", "deepseek-chat")
TEMPERATURE = float(os.getenv("DEEPSEEK_TEMPERATURE", "0.3"))

def call_llm(message: str, template: str = "") -> str:
    """
    Calls the DeepSeek API directly using the OpenAI SDK client.
    """
    client = OpenAI(
        api_key=os.getenv("DEEPSEEK_API_KEY"),
        base_url="https://api.deepseek.com/v1"
    )
    system_prompt = (
        "You are an expert LaTeX compiler and academic assistant. "
        "Generate valid, clean LaTeX markup based on the user's requirements."
    )
    
    if template:
        system_prompt += (
            "\n\nCRITICAL: You must use the following base LaTeX template structure. "
            "Identify the placeholders marked like '%[PLACEHOLDER: ...]' or default sections, "
            "and fill them in appropriately with the requested content. Return the complete, "
            "fully populated LaTeX document.\n\n"
            f"--- BASE TEMPLATE ---\n{template}\n--------------------"
        )
    
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": message}
    ]
    
    response = client.chat.completions.create(
        model=MODEL,
        messages=messages,
        temperature=TEMPERATURE,
    )
    return response.choices[0].message.content.strip()