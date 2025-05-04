# app/main.py
from io import BytesIO

from app.models.request_models import AskRequest
from app.models.response_models import AskResponse
from app.services.chat_service import ChatService
from app.services.rag.loaders import extract_text_from_pdf
from fastapi import FastAPI
from fastapi import File
from fastapi import HTTPException
from fastapi import UploadFile

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


@app.post("/extract/pdf")
async def extract_pdf(file: UploadFile = File(...)):
    """
    Accepts a PDF file upload and returns extracted text.
    """
    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="Only PDF files are supported.")

    try:
        file_bytes = await file.read()  # read the uploaded file into memory
        extracted_text = extract_text_from_pdf(BytesIO(file_bytes))  # use our loader
        return {"text": extracted_text[:5000]}  # optional: return only first 5000 chars

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Extraction failed: {str(e)}")
