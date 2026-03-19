import json
from fastapi import UploadFile, HTTPException
from app.service.embeddingService import generate_embedding
from sqlalchemy.orm import Session
from app.service.storageService import upload_file_to_s3, generate_presigned_url, delete_file_from_s3
from app.db.repository.assetRepo import AssetRepository
from app.service.captionService import generate_caption_and_tags
from app.service.vectorService import VectorService

class AssetService: 
    def __init__(self, session: Session):
        self.__assetRepo = AssetRepository(session=session)

    def upload_user_asset(self, user_id: int, file: UploadFile):
        try: 

            #upload to s3
            file_key = upload_file_to_s3(file=file, user_id=user_id)

            #generate img URL for captioning
            image_url = generate_presigned_url(file_key=file_key)

            #generate caption and tags using AI pipeline
            ai_response = generate_caption_and_tags(image_url=image_url)
            img_caption = ai_response["caption"]
            img_tags = ai_response["tags"]

            embedding_text = f"caption: {img_caption}. tags: {' '.join(img_tags)}"
            vector_emebedding = generate_embedding(text=embedding_text)

            #save to DB
            asset = self.__assetRepo.create_asset(user_id=user_id, file_key=file_key, caption=img_caption, tag=img_tags)

            VectorService().store_vector(asset_id=asset.id, user_id=user_id, embedding=vector_emebedding)

            return asset
        
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Failed to upload asset: {str(e)}",
            )
        
    def get_asset_for_user(self, user_id: int):
        assets = self.__assetRepo.get_asset_by_user_id(user_id=user_id)

        response = []

        for asset in assets: 
            signed_url = generate_presigned_url(file_key = asset.file_key)
            tags = asset.tags 
            response.append({
                "id": asset.id,
                "image_url": signed_url,
                "status": asset.status,
                "caption": asset.captions,
                "tags": tags,
                "created_at": asset.created_at
            })

        return response
    
    
    def delete_asset(self, user_id: int, asset_id: int):
        asset = self.__assetRepo.get_asset_by_asset_id(asset_id=asset_id)

        if not asset:
            raise HTTPException(status_code=404, detail="Asset not found")
        
        if asset.user_id != user_id:
            raise HTTPException(status_code=403, detail="Unauthorized to delete this asset")
        
        #delete from s3
        delete_file_from_s3(file_key=asset.file_key)

        #delete from DB
        self.__assetRepo.delete_asset(asset=asset)

        #delete from Qdrant
        VectorService().delete_vector( asset_id=asset.id)

        return {"message": "Asset deleted successfully"}
    
    def search_asset(self, user_id: int, query: str):

        #step1: generate embedding for the query
        query_embedding = generate_embedding(text=query)

        #step2: search in vector DB and get relevant asset IDs
        search_results = VectorService().search_similar_vectors(user_id = user_id, query_embedding=query_embedding)
        print("Raw search results from vector DB:", search_results)

        asset_ids = [result.payload['asset_id'] for result in search_results]

        if not asset_ids:
            return []
        
        #step3: fetch asset details from DB and return
        assets = self.__assetRepo.get_assets_by_asset_ids(asset_ids=asset_ids)

        asset_map = {asset.id: asset for asset in assets}

        response = []

        for result in search_results: 
            asset_id = result.payload['asset_id']
            asset = asset_map.get(asset_id)

            if not asset:
                print("problem is here")
                continue
            
            if asset.user_id != user_id:
                print("problem is here 1")
                continue

            signed_url = generate_presigned_url(asset.file_key)

            response.append({
                "id": asset.id,
                "image_url": signed_url,
                "caption": asset.captions,
                "tags": asset.tags,
                "score": result.score
            })
        return response
