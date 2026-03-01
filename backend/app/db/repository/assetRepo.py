from .base import BaseRepository
from app.db.models.asset import Asset
from fastapi import HTTPException

class AssetRepository(BaseRepository):
    
    def create_asset(self, user_id: int, file_key: str):

        try:
            new_asset = Asset(
                user_id = user_id,
                file_key = file_key,
                status = "uploaded"
            )

            self.session.add(instance = new_asset)
            self.session.commit()
            self.session.refresh(instance = new_asset)

            return new_asset
        except Exception as e:
            self.session.rollback()
            raise HTTPException(status_code=500, detail="Database error: " + str(e))
        

        
    def get_asset_by_user_id(self, user_id: int):
            asset = self.session.query(Asset).filter(Asset.user_id == user_id).order_by(Asset.created_at.desc()).all() 
            return asset

