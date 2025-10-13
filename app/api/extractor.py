from fastapi import APIRouter, UploadFile, File, HTTPException
from app.services.extractor import extract_document
from app.schemas.extractor import ExtractResponse
import shutil
import os
import tempfile

from app.services.llm_service import extract_rc_data_by_llm
from app.services.llm_service import extract_expense_data_by_llm

router = APIRouter()

@router.post("/extract", )
async def extract_text(file: UploadFile = File(...)):
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported.")

    # Save uploaded file temporarily
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        shutil.copyfileobj(file.file, tmp)
        temp_path = tmp.name

    try:
        texts = extract_rc_data_by_llm(extract_document(temp_path))
    finally:
        os.unlink(temp_path)

    return texts

@router.post("/scan-expense-doc", )
async def extract_expense_document(file: UploadFile = File(...)):
    # Save uploaded file temporarily
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        shutil.copyfileobj(file.file, tmp)
        temp_path = tmp.name

    try:
        texts = extract_expense_data_by_llm(extract_document(temp_path))
    finally:
        os.unlink(temp_path)

    return texts


