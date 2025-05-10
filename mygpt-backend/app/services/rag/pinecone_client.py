# mygpt-backend/app/services/rag/pinecone_client.py

import os

from pinecone import Pinecone
from pinecone import ServerlessSpec

# ✅ Setup Pinecone client (global)
pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))

# ✅ Load from env
PINECONE_INDEX = os.getenv("PINECONE_INDEX", "document-index")
PINECONE_DIM = 1536  # OpenAI embedding size
PINECONE_REGION = os.getenv("PINECONE_REGION", "us-east-1")
PINECONE_CLOUD = os.getenv("PINECONE_CLOUD", "aws")

# ✅ Create index if it doesn't exist
if PINECONE_INDEX not in pc.list_indexes().names():
    pc.create_index(
        name=PINECONE_INDEX,
        dimension=PINECONE_DIM,
        metric="cosine",
        spec=ServerlessSpec(cloud=PINECONE_CLOUD, region=PINECONE_REGION),
    )

# ✅ Connect to index
index = pc.Index(PINECONE_INDEX)


def upsert_embeddings(embeddings, metadata_list, namespace="default"):
    """
    Stores vectors with metadata in Pinecone.

    Args:
        embeddings (List[List[float]]): List of 1536-dim vectors.
        metadata_list (List[Dict]): Same-length metadata list.
        namespace (str): Logical grouping per file or session.
    """
    assert len(embeddings) == len(metadata_list), "Mismatch in embeddings/metadata"

    # Prepare for upsert
    vectors = [
        {"id": f"chunk_{i}", "values": vector, "metadata": metadata}
        for i, (vector, metadata) in enumerate(zip(embeddings, metadata_list))
    ]

    index.upsert(vectors=vectors, namespace=namespace)


def namespace_exists(namespace: str) -> bool:
    """
    Checks if any vectors exist under the given namespace.
    """
    stats = index.describe_index_stats()
    return namespace in stats.get("namespaces", {})
