# app/main.py
import logging
from io import BytesIO

from app.models.request_models import AskRequest
from app.models.response_models import AskResponse
from app.services.chat_service import ChatService
from app.services.rag.chunker import split_text_into_chunks
from app.services.rag.embedder import get_openai_embeddings
from app.services.rag.loaders import extract_text_from_file
from app.services.rag.pinecone_client import upsert_embeddings
from fastapi import FastAPI
from fastapi import File
from fastapi import HTTPException
from fastapi import UploadFile

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

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


@app.post("/upload")
async def upload_and_store(file: UploadFile = File(...)):
    file_bytes = BytesIO(await file.read())
    file_type = file.content_type.split("/")[-1]  # 'pdf' or 'csv'
    file_name = file.filename

    # Step 1: Extract raw text
    text = extract_text_from_file(file_bytes, file_type)

    # Step 2: Chunk it
    chunks = split_text_into_chunks(text, chunk_size=500, chunk_overlap=100)

    # Step 3: Embed chunks
    embeddings = get_openai_embeddings(chunks)

    # Step 4: Build metadata
    metadata_list = [
        {
            "file_name": file_name,
            "chunk_index": i,
            "chunk_text": chunk,
            "source_type": file_type,
        }
        for i, chunk in enumerate(chunks)
    ]

    # Step 5: Store in Pinecone
    upsert_embeddings(embeddings, metadata_list, namespace=file_name)

    return {
        "message": f"{len(chunks)} chunks embedded and stored successfully!",
        "file": file_name,
        "namespace": file_name,
    }
