# app/main.py
from app.models.request_models import AskRequest
from app.models.response_models import AskResponse
from app.services.chat_service import ChatService
from fastapi import FastAPI
from fastapi import HTTPException

app = FastAPI()


@app.get("/ping")
async def ping():
    return {"message": "pong"}


@app.post("/ask", response_model=AskResponse)
async def ask_question(request: AskRequest):
    question = request.question.strip()

    if len(question) < 3:
        raise HTTPException(
            status_code=400,
            detail="Question is too short. Please ask a more meaningful question.",
        )

    # USE SERVICE NOW!
    answer = ChatService.get_answer(question)

    return AskResponse(answer=answer)
