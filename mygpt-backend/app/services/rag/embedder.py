# app/services/rag/embedder.py

import os
from typing import List

import httpx

CLAUDE_EMBEDDING_URL = "https://api.anthropic.com/v1/embeddings"
CLAUDE_EMBEDDING_MODEL = "claude-3-sonnet-20240229-embed"
CLAUDE_API_KEY = os.getenv("CLAUDE_API_KEY")


def get_claude_embeddings(texts: List[str], batch_size: int = 100) -> List[List[float]]:
    """
    Fetches embeddings from Claude for a list of text chunks in safe batches.

    Args:
        texts (List[str]): Cleaned list of non-empty text chunks.
        batch_size (int): Number of chunks to send per request (max 100).

    Returns:
        List[List[float]]: List of embedding vectors.
    """
    headers = {
        "x-api-key": CLAUDE_API_KEY,
        "anthropic-version": "2023-06-01",
        "Content-Type": "application/json",
    }

    # ✅ Clean up blank chunks
    texts = [text.strip() for text in texts if text.strip()]

    embeddings = []

    for i in range(0, len(texts), batch_size):
        batch = texts[i : i + batch_size]
        payload = {"model": CLAUDE_EMBEDDING_MODEL, "input": batch}

        try:
            response = httpx.post(
                CLAUDE_EMBEDDING_URL, headers=headers, json=payload, timeout=30
            )
            response.raise_for_status()
            data = response.json()

            batch_embeddings = [item["embedding"] for item in data["data"]]
            embeddings.extend(batch_embeddings)

        except Exception as e:
            raise RuntimeError(
                f"Claude embedding API failed on batch {i // batch_size}: {str(e)}"
            )

    return embeddings
