import pymupdf
import pytesseract
from pdf2image import convert_from_path
from PIL import Image
from typing import List
import os
import sys

# Set Tesseract path for Windows (uncomment and adjust if needed)
if sys.platform == "win32":
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def extract_text_with_pymupdf(pdf_path: str) -> List[str]:
    """Extract text from PDF using PyMuPDF"""
    doc = pymupdf.open(pdf_path)
    texts = []
    for page in doc:
        text = page.get_text("text")  #type: ignore
        texts.append(text.strip())
    return texts

def extract_text_with_ocr(pdf_path: str) -> List[str]:
    """Extract text from PDF using OCR"""
    try:
        images = convert_from_path(pdf_path)
        texts = [pytesseract.image_to_string(img) for img in images]
        return texts
    except Exception as e:
        print(f"Error in OCR extraction from PDF: {e}")
        return []

def extract_text_from_image(image_path: str) -> List[str]:
    """Extract text from image using OCR"""
    try:
        image = Image.open(image_path)
        text = pytesseract.image_to_string(image)
        return [text.strip()] if text.strip() else []
    except pytesseract.TesseractNotFoundError:
        raise Exception("Tesseract OCR is not installed. Please install Tesseract OCR to process images.")
    except Exception as e:
        print(f"Error extracting text from image: {e}")
        raise Exception(f"Failed to extract text from image: {str(e)}")

def is_text_sufficient(text: str, threshold: int = 100) -> bool:
    """Check if extracted text meets minimum threshold"""
    return len(text.strip()) >= threshold

def is_image_file(filename: str) -> bool:
    """Check if file is an image"""
    image_extensions = ['.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.tif', '.webp']
    return any(filename.lower().endswith(ext) for ext in image_extensions)

def is_pdf_file(filename: str) -> bool:
    """Check if file is a PDF"""
    return filename.lower().endswith('.pdf')

def extract_document(file_path: str, filename: str = "") -> List[str]:
    """
    Extract text from PDF or image file, falling back to OCR if needed.
    Returns list of extracted text strings.
    """
    # Determine file type
    check_filename = filename if filename else file_path
    
    # Handle images
    if is_image_file(check_filename):
        texts = extract_text_from_image(file_path)
        if not texts or not any(t.strip() for t in texts):
            raise Exception("No text could be extracted from the image. The image may be blank or unreadable.")
        return texts
    
    # Handle PDFs
    elif is_pdf_file(check_filename):
        pymupdf_texts = extract_text_with_pymupdf(file_path)
        final_texts = []
        
        for i, text in enumerate(pymupdf_texts):
            if is_text_sufficient(text):
                final_texts.append(text)
            else:
                # If text extraction fails, use OCR for remaining pages
                try:
                    ocr_texts = extract_text_with_ocr(file_path)
                    final_texts.extend(ocr_texts[i:])
                except Exception as e:
                    print(f"OCR fallback failed: {e}")
                    # Continue with whatever text we have
                break
        
        if not final_texts or not any(t.strip() for t in final_texts):
            raise Exception("No text could be extracted from the PDF. The document may be blank or unreadable.")
        
        return final_texts
    
    else:
        raise ValueError(f"Unsupported file type: {check_filename}")