from app.core.vector_db import client
from app.db.models.image_embedding import COLLECTION_NAME
from qdrant_client.models import PointStruct,Filter, FieldCondition, MatchValue
from fastapi import HTTPException

threshold = 0.15

class VectorRepository:

    def upsert_vector(self, asset_id: int, user_id: int, embedding: list):
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
        

    def search_vector(self,user_id: int,query_embedding: list, limit: int = 5):
        try:
            results = client.query_points(
                collection_name = COLLECTION_NAME,
                query = query_embedding,
                limit = limit,
                query_filter = Filter(
                    must = [
                        FieldCondition(
                            key = "user_id",
                            match = MatchValue(value=user_id)
                        )
                    ]
                )
            )
            filtered_points = [point for point in results.points if point.score >= threshold]
            return filtered_points
        except Exception as e: 
            raise HTTPException(status_code=500, detail="Vector search failed: " + str(e))
        
    def delete_vector(self, asset_id: int):
        try:
            client.delete(
                collection_name = COLLECTION_NAME,
                points_selector = [asset_id]
            )
        except Exception as e:
            error_message = str(e).lower()
            if "not found" in error_message or "does not exist" in error_message:
                return
            raise HTTPException(status_code=500, detail="Vector deletion failed: " + str(e))
