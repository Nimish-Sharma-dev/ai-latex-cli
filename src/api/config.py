"""
Configuration settings for AI LaTeX CLI.
Supports free-tier LLMs (Gemini, Groq, Ollama), DeepSeek, and Antigravity/local offline modes.
"""

import os
from pathlib import Path
from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # LLM Provider: 'antigravity', 'gemini', 'groq', 'ollama', 'deepseek', 'custom'
    LLM_PROVIDER: str = "antigravity"

    # DeepSeek configuration (legacy / optional)
    DEEPSEEK_API_KEY: Optional[str] = None
    DEEPSEEK_MODEL: str = "deepseek-chat"
    DEEPSEEK_BASE_URL: str = "https://api.deepseek.com/v1"

    # Google Gemini configuration (free tier available)
    GEMINI_API_KEY: Optional[str] = None
    GEMINI_MODEL: str = "gemini-2.0-flash"

    # Groq configuration (free tier available)
    GROQ_API_KEY: Optional[str] = None
    GROQ_MODEL: str = "llama-3.3-70b-versatile"

    # Ollama configuration (100% free local)
    OLLAMA_BASE_URL: str = "http://localhost:11434"
    OLLAMA_MODEL: str = "llama3.2"

    # General Generation Parameters
    TEMPERATURE: float = 0.2
    MAX_TOKENS: int = 4096

    # LaTeX Engine Settings
    LATEX_COMPILER: str = "pdflatex"
    LATEX_COMPILE_TIMEOUT: int = 120
    TEMPLATE_DIR: str = str(Path(__file__).parent.parent.parent / "templates")
    OUTPUT_DIR: str = "outputs"
    BACKUP_ENABLED: bool = True

    model_config = SettingsConfigDict(
        env_file=(".env", "../.env"),
        env_file_encoding="utf-8",
        extra="ignore"
    )


def get_settings() -> Settings:
    return Settings()
