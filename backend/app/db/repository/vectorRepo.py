from app.core.vector_db import client
from app.db.models.image_embedding import COLLECTION_NAME
from qdrant_client.models import PointStruct
from fastapi import HTTPException

class VectorRepository:

    def create_vector(self, asset_id: int, user_id: int, embedding: list):
        try:
            client.upsert(
                collection_name=COLLECTION_NAME,
                points=[
                    PointStruct(
                        id=asset_id,
                        vector=embedding,
                        payload={"user_id": user_id, "asset_id": asset_id}
                    )
                ]
            )
        except Exception as e:
            raise HTTPException(status_code=500, detail="Vector insertion failed: " + str(e))
        

    def search_vector(self, query_embedding: list, limit: int = 5):
        try:
            results = client.search(
                collection_name = COLLECTION_NAME,
                query_vector = query_embedding,
                limit = limit
            )
        except Exception as e: 
            raise HTTPException(status_code=500, detail="Vector search failed: " + str(e))
        
    def delete_vector(self, asset_id: int):
        try:
            client.delete(
                collection_name = COLLECTION_NAME,
                points_selector = {asset_id}
            )
        except Exception as e:
            raise HTTPException(status_code=500, detail="Vector deletion failed: " + str(e))