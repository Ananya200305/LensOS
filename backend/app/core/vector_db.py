from decouple import config
from qdrant_client import QdrantClient

VECTOR_DB_URL = config("VECTOR_DB_URL")

client = QdrantClient(VECTOR_DB_URL)