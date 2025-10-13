from fastapi import APIRouter, UploadFile, File, HTTPException
from app.services.extractor import extract_document, is_image_file, is_pdf_file
import shutil
import os
import tempfile
from app.services.llm_service import extract_rc_data_by_llm, extract_expense_data_by_llm

router = APIRouter()

ALLOWED_EXTENSIONS = ['.pdf', '.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.tif', '.webp']

def is_allowed_file(filename: str) -> bool:
    """Check if file type is allowed"""
    return any(filename.lower().endswith(ext) for ext in ALLOWED_EXTENSIONS)

@router.post("/extract")
async def extract_rc_text(file: UploadFile = File(...)):
    """Extract RC (Registration Certificate) data from PDF or image"""
    # Check if filename exists
    if not file.filename:
        raise HTTPException(status_code=400, detail="No filename provided")
    
    if not is_allowed_file(file.filename):
        raise HTTPException(
            status_code=400, 
            detail=f"Unsupported file type. Allowed types: {', '.join(ALLOWED_EXTENSIONS)}"
        )
    
    # Determine file extension
    file_extension = os.path.splitext(file.filename)[1].lower()
    
    # Save uploaded file temporarily
    with tempfile.NamedTemporaryFile(delete=False, suffix=file_extension) as tmp:
        shutil.copyfileobj(file.file, tmp)
        temp_path = tmp.name
    
    try:
        # Extract text from PDF or image
        extracted_texts = extract_document(temp_path, file.filename)
        
        # Process with LLM
        result = extract_rc_data_by_llm(extracted_texts)
        return result
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing document: {str(e)}")
    finally:
        # Clean up temporary file
        if os.path.exists(temp_path):
            os.unlink(temp_path)

@router.post("/scan-expense-doc")
async def extract_expense_document(file: UploadFile = File(...)):
    """Extract expense data from PDF or image"""
    # Check if filename exists
    if not file.filename:
        raise HTTPException(status_code=400, detail="No filename provided")
    
    if not is_allowed_file(file.filename):
        raise HTTPException(
            status_code=400, 
            detail=f"Unsupported file type. Allowed types: {', '.join(ALLOWED_EXTENSIONS)}"
        )
    
    # Determine file extension
    file_extension = os.path.splitext(file.filename)[1].lower()
    
    # Save uploaded file temporarily
    with tempfile.NamedTemporaryFile(delete=False, suffix=file_extension) as tmp:
        shutil.copyfileobj(file.file, tmp)
        temp_path = tmp.name
    
    try:
        # Extract text from PDF or image
        extracted_texts = extract_document(temp_path, file.filename)
        
        # Process with LLM
        result = extract_expense_data_by_llm(extracted_texts)
        return result
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing document: {str(e)}")
    finally:
        # Clean up temporary file
        if os.path.exists(temp_path):
            os.unlink(temp_path)