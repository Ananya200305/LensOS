from app.core.vector_db import client
from qdrant_client.models import Distance, VectorParams
from app.service.clipService import CLIP_VECTOR_SIZE

COLLECTION_NAME = "image_embeddings"


def create_image_embedding_collection():
    collections = client.get_collections().collections
    existing = [c.name for c in collections]

    if COLLECTION_NAME in existing:
        collection_info = client.get_collection(COLLECTION_NAME)
        current_size = collection_info.config.params.vectors.size
        if current_size == CLIP_VECTOR_SIZE:
            print("Image embedding collection already exists")
            return

        client.delete_collection(collection_name=COLLECTION_NAME)
        print("Recreated image embedding collection with CLIP dimension")

    client.create_collection(
        collection_name=COLLECTION_NAME,
        vectors_config=VectorParams(
            size=CLIP_VECTOR_SIZE,
            distance=Distance.COSINE
        )
    )

    print("Image embedding collection created")
