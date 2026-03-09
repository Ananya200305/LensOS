import json
from fastapi import UploadFile, HTTPException
from sqlalchemy.orm import Session
from app.service.storageService import upload_file_to_s3, generate_presigned_url, delete_file_from_s3
from app.db.repository.assetRepo import AssetRepository
from app.service.captionService import generate_caption_and_tags

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

            #save to DB
            asset = self.__assetRepo.create_asset(user_id=user_id, file_key=file_key, caption=img_caption, tag=img_tags)

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

        return {"message": "Asset deleted successfully"}
