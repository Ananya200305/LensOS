from app.core.vector_db import client
from qdrant_client.models import Distance, VectorParams

COLLECTION_NAME = "image_embeddings"


def create_image_embedding_collection():

    collections = client.get_collections().collections
    existing = [c.name for c in collections]

    if COLLECTION_NAME not in existing:

        client.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=VectorParams(
                size=384,   # BGE-small embedding size
                distance=Distance.COSINE
            )
        )

        print("Image embedding collection created")

    else:
        print("Image embedding collection already exists")