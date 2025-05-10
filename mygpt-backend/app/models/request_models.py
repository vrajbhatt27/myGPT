# app/models/request_models.py

# Deprecated for multipart/form-data /ask route
# Retained here for potential JSON-only use

from pydantic import BaseModel
from pydantic import Field


class AskRequest(BaseModel):
    question: str = Field(..., min_length=1, description="The question to ask the AI.")
