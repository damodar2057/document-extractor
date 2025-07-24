from pydantic import BaseModel
from typing import List

class ExtractRequest(BaseModel):
    # If you want to pass file URL or base64 string instead of upload
    # For now, we only use file upload directly
    pass

class ExtractResponse(BaseModel):
    texts: str
