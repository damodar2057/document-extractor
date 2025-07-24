import pymupdf
import pytesseract
from pdf2image import convert_from_path
from typing import List

from app.services.llm_service import extract_rc_data


def extract_text_with_pymupdf(pdf_path: str) -> List[str]:
    doc = pymupdf.open(pdf_path)
    texts = []
    for page in doc:
        text = page.get_text("text")
        texts.append(text.strip())
    return texts

def extract_text_with_ocr(pdf_path: str) -> List[str]:
    images = convert_from_path(pdf_path)
    texts = [pytesseract.image_to_string(img) for img in images]
    return texts

def is_text_sufficient(text: str, threshold: int = 100) -> bool:
    return len(text.strip()) >= threshold

def extract_document(pdf_path: str) -> str:
    pymupdf_texts = extract_text_with_pymupdf(pdf_path)
    final_texts = []

    for i, text in enumerate(pymupdf_texts):
        if is_text_sufficient(text):
            final_texts.append(text)
        else:
            ocr_texts = extract_text_with_ocr(pdf_path)
            final_texts.extend(ocr_texts[i:])
            break

    """ Now pass it to llm for text extraction """
    return extract_rc_data(final_texts)

