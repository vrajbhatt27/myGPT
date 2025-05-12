# mygpt-backend/app/services/rag/chunker.py

from langchain.text_splitter import RecursiveCharacterTextSplitter


def split_text_into_chunks(
    text: str, chunk_size: int = 500, chunk_overlap: int = 100
) -> list[str]:
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\n\n", "\n", ".", " ", ""],
    )

    chunks = splitter.split_text(text)
    return chunks
