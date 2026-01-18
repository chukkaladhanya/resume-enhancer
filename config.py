"""
Configuration management for Resume Enhancer application.
Handles environment variables and application settings.
"""

import os
from dotenv import load_dotenv
from typing import List

# Load environment variables from .env file
load_dotenv()

# API Configuration
GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
GEMINI_MODEL: str = os.getenv("GEMINI_MODEL", "gemini-1.5-flash")

# File Upload Configuration
MAX_FILE_SIZE_MB: int = int(os.getenv("MAX_FILE_SIZE_MB", "10"))
MAX_FILE_SIZE_BYTES: int = MAX_FILE_SIZE_MB * 1024 * 1024

SUPPORTED_FORMATS: List[str] = ["pdf", "docx"]

# Resume Sections
RESUME_SECTIONS: List[str] = [
    "Objective",
    "Education",
    "Experience",
    "Skills",
    "Projects",
    "Certifications",
    "Extracurricular Activities",
    "Declaration"
]

# Validation
def validate_config() -> tuple[bool, str]:
    """
    Validate that required configuration is present.
    
    Returns:
        tuple: (is_valid, error_message)
    """
    if not GEMINI_API_KEY:
        return False, (
            "⚠️ GEMINI_API_KEY not found!\n\n"
            "Please create a `.env` file by copying `.env.example` "
            "and add your Gemini API key.\n\n"
            "Get your API key from: https://makersuite.google.com/app/apikey"
        )
    return True, ""
