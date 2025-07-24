from fastapi import FastAPI
from dotenv import load_dotenv
load_dotenv()
from app.core import settings
from app.api import extractor


app = FastAPI(title=settings.app_name)
app.include_router(extractor.router, prefix=settings.app_prefix)

@app.get("/")
async def root():
    return {"message": "Welcome to Document Extractor API"}
