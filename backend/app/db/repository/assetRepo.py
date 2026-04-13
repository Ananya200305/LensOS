from .base import BaseRepository
from app.db.models.asset import Asset
from fastapi import HTTPException

class AssetRepository(BaseRepository):
    
    def create_asset(self, user_id: int, file_key: str, caption: str = None, tag: list = None, status: str = "pending"):

        try:
            new_asset = Asset(
                user_id = user_id,
                file_key = file_key,
                status = status,
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

    def update_asset_status(self, asset: Asset, status: str):
        try:
            asset.status = status
            self.session.commit()
            self.session.refresh(asset)
            return asset
        except Exception as e:
            self.session.rollback()
            raise HTTPException(status_code=500, detail="Database status update error: " + str(e))

    def update_asset_processing_result(self, asset: Asset, caption: str, tags: list, status: str = "ready"):
        try:
            asset.captions = caption
            asset.tags = tags
            asset.status = status
            self.session.commit()
            self.session.refresh(asset)
            return asset
        except Exception as e:
            self.session.rollback()
            raise HTTPException(status_code=500, detail="Database processing update error: " + str(e))

    def mark_asset_failed(self, asset_id: int):
        asset = self.get_asset_by_asset_id(asset_id=asset_id)
        if not asset:
            return None

        try:
            asset.status = "failed"
            self.session.commit()
            self.session.refresh(asset)
            return asset
        except Exception as e:
            self.session.rollback()
            raise HTTPException(status_code=500, detail="Database failed status update error: " + str(e))
    
    def delete_asset(self, asset: Asset):
        try:
            self.session.delete(asset)
            self.session.commit()
        except Exception as e:
            self.session.rollback()
            raise HTTPException(status_code=500, detail="Database Delete error: " + str(e))
