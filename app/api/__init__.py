from fastapi import APIRouter
from .extractor import router as extractor_router

router = APIRouter()
router.include_router(extractor_router, prefix="/extractor", tags=["Extractor"])
