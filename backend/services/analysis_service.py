from backend.services.pdf_service import extract_text_from_pdf
from backend.services.gemini_service import analyze_contract

def analyze_pdf_contract(file_path: str) -> dict:
    """Extracts text from a PDF and coordinates the analysis using AI."""
    text = extract_text_from_pdf(file_path)
    analysis_result = analyze_contract(text)
    return analysis_result
