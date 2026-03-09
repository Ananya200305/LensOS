from fastapi import UploadFile, HTTPException
from sqlalchemy.orm import Session
from app.service.storageService import upload_file_to_s3, generate_presigned_url
from app.db.repository.assetRepo import AssetRepository

class AssetService: 
    def __init__(self, session: Session):
        self.__assetRepo = AssetRepository(session=session)

    def upload_user_asset(self, user_id: int, file: UploadFile):
        try: 

            #upload to s3
            file_key = upload_file_to_s3(file=file, user_id=user_id)

            #save to DB
            asset = self.__assetRepo.create_asset(user_id=user_id, file_key=file_key)

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
            response.append({
                "id": asset.id,
                "image_url": signed_url,
                "status": asset.status,
                "caption": asset.captions,
                "created_at": asset.created_at
            })

        return response
