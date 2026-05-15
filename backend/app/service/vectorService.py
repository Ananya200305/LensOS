from app.db.repository.vectorRepo import VectorRepository

class VectorService:

    def __init__(self):
        self.__vectorRepo = VectorRepository()

    def store_vector(self, asset_id: int, user_id: int, embedding: list):
        self.__vectorRepo.upsert_vector(asset_id=asset_id, user_id=user_id, embedding=embedding)

    def search_similar_vectors(self,user_id : int,  query_embedding: list, limit: int = 5):
        return self.__vectorRepo.search_vector(user_id=user_id, query_embedding=query_embedding, limit=limit)
    
    def delete_vector(self, asset_id: int):
        self.__vectorRepo.delete_vector(asset_id=asset_id)

    
