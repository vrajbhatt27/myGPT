# app/main.py
import logging
from io import BytesIO

from app.models.response_models import AskResponse
from app.services.chat_service import ChatService
from app.services.rag.chunker import split_text_into_chunks
from app.services.rag.embedder import get_openai_embeddings
from app.services.rag.loaders import extract_text_from_file
from app.services.rag.pinecone_client import namespace_exists
from app.services.rag.pinecone_client import upsert_embeddings
from fastapi import FastAPI
from fastapi import File
from fastapi import Form
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
async def ask_question(
    question: str = Form(...),
    file: UploadFile = File(None),  # Optional
):
    question = question.strip()
    if len(question) < 3:
        raise HTTPException(status_code=400, detail="Question is too short.")

    # Default namespace (used when no file is uploaded)
    namespace = "default"

    if file:
        file_bytes = BytesIO(await file.read())
        file_type = file.content_type.split("/")[-1]
        file_name = file.filename
        namespace = file_name  # override namespace

        if not namespace_exists(namespace):
            # Upload pipeline
            text = extract_text_from_file(file_bytes, file_type)
            chunks = split_text_into_chunks(text, chunk_size=500, chunk_overlap=100)
            embeddings = get_openai_embeddings(chunks)

            metadata_list = [
                {
                    "file_name": file_name,
                    "chunk_index": i,
                    "chunk_text": chunk,
                    "source_type": file_type,
                }
                for i, chunk in enumerate(chunks)
            ]

            upsert_embeddings(embeddings, metadata_list, namespace=namespace)
        else:
            logging.info("=" * 20)
            logging.info(f"Namespace {namespace} already exists. Skipping upload.")
            logging.info("=" * 20)

    # Always call Claude with user question and selected namespace
    answer = ChatService.get_answer(question, namespace=namespace)
    return AskResponse(answer=answer)
