# app/models/request_models.py

from pydantic import BaseModel
from pydantic import Field


class AskRequest(BaseModel):
    question: str = Field(..., min_length=1, description="The question to ask the AI.")
