from .base import BaseRepository
from app.db.models.asset import Asset
from fastapi import HTTPException

class AssetRepository(BaseRepository):
    
    def create_asset(self, user_id: int, file_key: str, caption: str = None, tag: list = None):

        try:
            new_asset = Asset(
                user_id = user_id,
                file_key = file_key,
                status = "uploaded",
                captions = caption,
                tags = tag or []
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
    
    def get_asset_by_asset_id(self, asset_id: int):
        asset = self.session.query(Asset).filter(Asset.id == asset_id).first() 
        return asset
    
    def get_assets_by_asset_ids(self, asset_ids: list):
        assets = self.session.query(Asset).filter(Asset.id.in_(asset_ids)).all()
        return assets
    
    def delete_asset(self, asset: Asset):
        try:
            self.session.delete(asset)
            self.session.commit()
        except Exception as e:
            self.session.rollback()
            raise HTTPException(status_code=500, detail="Database Delete error: " + str(e))

