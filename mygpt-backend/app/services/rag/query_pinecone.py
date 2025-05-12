from app.services.rag.embedder import get_openai_embeddings
from app.services.rag.pinecone_client import index
from app.services.utils import normalize_question


def query_top_k_chunks(question: str, namespace: str = "default", top_k: int = 3):
    """
    Embed the user question and query Pinecone for top-k relevant chunks.

    Args:
        question (str): User input.
        namespace (str): Scope of the search (usually file name).
        top_k (int): Number of chunks to retrieve.

    Returns:
        List[Dict]: List of top matching metadata dicts.
    """
    # Step 1: Embed question
    question = normalize_question(question)
    query_vec = get_openai_embeddings([question])[0]  # just one

    # Step 2: Query Pinecone
    result = index.query(
        vector=query_vec, top_k=top_k, include_metadata=True, namespace=namespace
    )

    return [match.metadata for match in result.matches]
