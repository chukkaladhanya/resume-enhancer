"""
Utility functions for extracting text from resume files.
Supports PDF and DOCX formats.
"""

import fitz  # PyMuPDF
import docx
from typing import BinaryIO, Optional
import streamlit as st


def extract_text_from_pdf(file: BinaryIO) -> str:
    """
    Extract text content from a PDF file.
    
    Args:
        file: Binary file object (PDF)
        
    Returns:
        str: Extracted text content
        
    Raises:
        Exception: If PDF extraction fails
    """
    try:
        doc = fitz.open(stream=file.read(), filetype="pdf")
        text = ""
        for page in doc:
            text += page.get_text()
        doc.close()
        
        if not text.strip():
            raise ValueError("PDF appears to be empty or contains only images")
            
        return text.strip()
    except Exception as e:
        raise Exception(f"Failed to extract text from PDF: {str(e)}")


def extract_text_from_docx(file: BinaryIO) -> str:
    """
    Extract text content from a DOCX file.
    
    Args:
        file: Binary file object (DOCX)
        
    Returns:
        str: Extracted text content
        
    Raises:
        Exception: If DOCX extraction fails
    """
    try:
        doc = docx.Document(file)
        text = "\n".join([para.text for para in doc.paragraphs])
        
        if not text.strip():
            raise ValueError("DOCX appears to be empty")
            
        return text.strip()
    except Exception as e:
        raise Exception(f"Failed to extract text from DOCX: {str(e)}")


def validate_file_size(file: BinaryIO, max_size_bytes: int) -> tuple[bool, str]:
    """
    Validate that uploaded file does not exceed size limit.
    
    Args:
        file: Uploaded file object
        max_size_bytes: Maximum allowed file size in bytes
        
    Returns:
        tuple: (is_valid, error_message)
    """
    file.seek(0, 2)  # Seek to end
    file_size = file.tell()
    file.seek(0)  # Reset to beginning
    
    if file_size > max_size_bytes:
        max_mb = max_size_bytes / (1024 * 1024)
        actual_mb = file_size / (1024 * 1024)
        return False, f"File size ({actual_mb:.1f}MB) exceeds limit of {max_mb:.0f}MB"
    
    return True, ""


def extract_resume_text(file: BinaryIO, filename: str) -> Optional[str]:
    """
    Extract text from resume file with error handling.
    
    Args:
        file: Binary file object
        filename: Name of the file
        
    Returns:
        str: Extracted text, or None if extraction fails
    """
    ext = filename.split('.')[-1].lower()
    
    try:
        if ext == "pdf":
            return extract_text_from_pdf(file)
        elif ext == "docx":
            return extract_text_from_docx(file)
        else:
            st.error(f"Unsupported file format: {ext}")
            return None
    except Exception as e:
        st.error(f"Error extracting text: {str(e)}")
        return None
