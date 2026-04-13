from fastapi import UploadFile, HTTPException
from sqlalchemy.orm import Session
from app.service.storageService import upload_file_to_s3, generate_presigned_url, delete_file_from_s3
from app.db.repository.assetRepo import AssetRepository
from app.core.queue import enqueue_asset_processing
from app.service.clipService import get_text_embedding
from app.service.vectorService import VectorService

class AssetService: 
    def __init__(self, session: Session):
        self.__assetRepo = AssetRepository(session=session)

    def upload_user_asset(self, user_id: int, file: UploadFile):
        asset = None

        try: 
            file_key = upload_file_to_s3(file=file, user_id=user_id)
            asset = self.__assetRepo.create_asset(user_id=user_id, file_key=file_key, status="pending")
            enqueue_asset_processing(asset_id=asset.id, user_id=user_id, file_key=file_key)
            return asset
        
        except Exception as e:
            if asset:
                self.__assetRepo.mark_asset_failed(asset_id=asset.id)
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
        
        delete_file_from_s3(file_key=asset.file_key)
        self.__assetRepo.delete_asset(asset=asset)
        VectorService().delete_vector(asset_id=asset.id)

        return {"message": "Asset deleted successfully"}

    def get_asset_status(self, user_id: int, asset_id: int):
        asset = self.__assetRepo.get_asset_by_asset_id(asset_id=asset_id)

        if not asset:
            raise HTTPException(status_code=404, detail="Asset not found")

        if asset.user_id != user_id:
            raise HTTPException(status_code=403, detail="Unauthorized to access this asset")

        return {
            "id": asset.id,
            "status": asset.status,
            "caption": asset.captions,
            "tags": asset.tags,
            "created_at": asset.created_at,
        }
    
    def search_asset(self, user_id: int, query: str):
        query_embedding = get_text_embedding(text=query)
        search_results = VectorService().search_similar_vectors(user_id=user_id, query_embedding=query_embedding)
        print("Search results:", search_results)

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
                continue
            
            if asset.user_id != user_id or asset.status != "ready":
                continue

            signed_url = generate_presigned_url(asset.file_key)

            response.append({
                "id": asset.id,
                "image_url": signed_url,
                "caption": asset.captions,
                "tags": asset.tags,
                "status": asset.status,
                "score": result.score
            })
        return response
