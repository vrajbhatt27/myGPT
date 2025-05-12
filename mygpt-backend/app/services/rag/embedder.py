# mygpt-backend/app/services/rag/embedder_openai.py

import os
from typing import List

import openai

# Load OpenAI key from environment
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY


def get_openai_embeddings(
    texts: List[str], model: str = "text-embedding-3-small", batch_size: int = 100
) -> List[List[float]]:
    # Remove empty/whitespace chunks
    cleaned_texts = [text.strip() for text in texts if text.strip()]

    all_embeddings = []

    # 🔁 Break input into batches
    for i in range(0, len(cleaned_texts), batch_size):
        batch = cleaned_texts[i : i + batch_size]

        try:
            # 🚀 Make API call for the current batch
            response = openai.embeddings.create(input=batch, model=model)

            # 🎯 Extract embedding vectors
            embeddings = [item.embedding for item in response.data]
            all_embeddings.extend(embeddings)

        except Exception as e:
            raise RuntimeError(
                f"OpenAI embedding failed at batch {i // batch_size}: {str(e)}"
            )

    return all_embeddings
