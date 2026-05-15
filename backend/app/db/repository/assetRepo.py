from .base import BaseRepository
from app.db.models.asset import Asset
from app.db.schema.asset import AssetIntelligenceUpdate
from fastapi import HTTPException
from sqlalchemy import or_
from sqlalchemy.sql import func

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

    def get_filtered_assets_by_asset_ids(self, user_id: int, asset_ids: list[int], filters):
        query = self.session.query(Asset).filter(
            Asset.user_id == user_id,
            Asset.status == "ready",
            Asset.id.in_(asset_ids),
        )

        if filters.tags:
            query = query.filter(Asset.tags.contains(filters.tags))
        if filters.objects:
            query = query.filter(Asset.detected_objects.contains(filters.objects))
        if filters.scenes:
            normalized_scenes = [scene.lower() for scene in filters.scenes]
            query = query.filter(func.lower(Asset.scene_label).in_(normalized_scenes))
        if filters.environment:
            query = query.filter(func.lower(Asset.environment_label) == filters.environment.lower())
        if filters.time_of_day:
            normalized_times = [time_value.lower() for time_value in filters.time_of_day]
            query = query.filter(func.lower(Asset.time_label).in_(normalized_times))
        if filters.date_from:
            query = query.filter(Asset.created_at >= filters.date_from)
        if filters.date_to:
            query = query.filter(Asset.created_at <= filters.date_to)

        return query.all()

    def get_asset_filter_options(self, user_id: int):
        assets = self.session.query(Asset).filter(
            Asset.user_id == user_id,
            Asset.status == "ready",
        ).all()

        tags = set()
        objects = set()
        scenes = set()
        environments = set()
        time_of_day = set()

        for asset in assets:
            tags.update(asset.tags or [])
            objects.update(asset.detected_objects or [])
            if asset.scene_label:
                scenes.add(asset.scene_label)
            if asset.environment_label:
                environments.add(asset.environment_label)
            if asset.time_label:
                time_of_day.add(asset.time_label)

        return {
            "tags": sorted(tags),
            "detected_objects": sorted(objects),
            "scenes": sorted(scenes),
            "environments": sorted(environments),
            "time_of_day": sorted(time_of_day),
        }

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

    def update_asset_intelligence(self, asset: Asset, intelligence_data: AssetIntelligenceUpdate):
        try:
            asset.detected_objects = intelligence_data.detected_objects
            asset.scene_label = intelligence_data.scene_label
            asset.time_label = intelligence_data.time_label
            asset.environment_label = intelligence_data.environment_label
            asset.processed_at = intelligence_data.processed_at
            asset.ranking_score = intelligence_data.ranking_score
            self.session.commit()
            self.session.refresh(asset)
            return asset
        except Exception as e:
            self.session.rollback()
            raise HTTPException(status_code=500, detail="Database intelligence update error: " + str(e))

    def reset_asset_processing(self, asset: Asset):
        try:
            asset.status = "pending"
            asset.captions = None
            asset.tags = []
            asset.detected_objects = []
            asset.scene_label = None
            asset.time_label = None
            asset.environment_label = None
            asset.processed_at = None
            asset.ranking_score = 0.0
            self.session.commit()
            self.session.refresh(asset)
            return asset
        except Exception as e:
            self.session.rollback()
            raise HTTPException(status_code=500, detail="Database reset error: " + str(e))

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

    def touch_processed_at(self, asset: Asset):
        try:
            asset.processed_at = func.now()
            self.session.commit()
            self.session.refresh(asset)
            return asset
        except Exception as e:
            self.session.rollback()
            raise HTTPException(status_code=500, detail="Database processed_at update error: " + str(e))
    
    def delete_asset(self, asset: Asset):
        try:
            self.session.delete(asset)
            self.session.commit()
        except Exception as e:
            self.session.rollback()
            raise HTTPException(status_code=500, detail="Database Delete error: " + str(e))
