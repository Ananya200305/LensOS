from sentence_transformers import SentenceTransformer
from fastapi import HTTPException

model = SentenceTransformer("BAAI/bge-small-en-v1.5")

def generate_embedding(text: str):
    try:
        embedding = model.encode(text, normalize_embeddings=True).tolist()
        return embedding
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to generate embedding: {str(e)}",
        )