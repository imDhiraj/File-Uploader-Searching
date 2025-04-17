from PyPDF2 import PdfReader
from fastapi import HTTPException

def extract_text_from_pdf(file_path: str) -> str:
    """
    Extract text content from a PDF file.
    :param file_path: Path to the PDF file
    :return: Extracted text content
    """
    try:
        reader = PdfReader(file_path)
        text = ""
        for page in reader.pages:
            text += page.extract_text() or ""  # Extract text from each page
        return text
    except Exception as e:
        print(f"Error extracting text from PDF: {e}")
        raise HTTPException(status_code=400, detail="Failed to extract content from the PDF file")