# app/models/response_models.py

from pydantic import BaseModel


class AskResponse(BaseModel):
    answer: str
