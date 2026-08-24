from pathlib import Path

import pymupdf
from docx import Document


def extract_pdf_text(file_path: str) -> str:
    """Extract readable text from a PDF resume."""
    document = pymupdf.open(file_path)

    text_parts = []

    for page in document:
        text_parts.append(page.get_text())

    document.close()

    return "\n".join(text_parts).strip()


def extract_docx_text(file_path: str) -> str:
    """Extract readable text from a DOCX resume."""
    document = Document(file_path)

    paragraphs = [
        paragraph.text.strip()
        for paragraph in document.paragraphs
        if paragraph.text.strip()
    ]

    return "\n".join(paragraphs).strip()


def extract_resume_text(file_path: str) -> str:
    """Select the appropriate parser based on the resume file type."""
    extension = Path(file_path).suffix.lower()

    if extension == ".pdf":
        return extract_pdf_text(file_path)

    if extension == ".docx":
        return extract_docx_text(file_path)

    raise ValueError(
        f"Unsupported file type: {extension}"
    )