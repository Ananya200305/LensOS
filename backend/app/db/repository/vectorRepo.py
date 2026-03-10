from app.core.vector_db import client
from app.db.models.image_embedding import COLLECTION_NAME
from qdrant_client.models import PointStruct,Filter, FieldCondition, MatchValue
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
        

    def search_vector(self,user_id : int, query_embedding: list, limit: int = 5):
        try:
            results = client.query_points(
                collection_name = COLLECTION_NAME,
                query = query_embedding,
                limit = limit,
                query_filter=Filter(
                    must=[
                        FieldCondition(
                            key="user_id",
                            match=MatchValue(value=user_id)
                        )
                    ]
                )
            )
            return results.points
        except Exception as e: 
            raise HTTPException(status_code=500, detail="Vector search failed: " + str(e))
        
    def delete_vector(self, asset_id: int):
        try:
            client.delete(
                collection_name = COLLECTION_NAME,
                points_selector = [asset_id]
            )
        except Exception as e:
            raise HTTPException(status_code=500, detail="Vector deletion failed: " + str(e))