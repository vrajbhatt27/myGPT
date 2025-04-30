# app/models/request_models.py

from pydantic import BaseModel, Field

class AskRequest(BaseModel):
    question: str = Field(..., min_length=1, description="The question to ask the AI.")
