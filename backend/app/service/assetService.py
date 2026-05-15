from fastapi import UploadFile, HTTPException
from sqlalchemy.orm import Session
from app.db.schema.asset import (
    AssetFilterOptions,
    AssetIntelligenceResponse,
    AssetReprocessResponse,
    HybridSearchRequest,
    HybridSearchResponse,
)
from app.service.storageService import upload_file_to_s3, generate_presigned_url, delete_file_from_s3
from app.db.repository.assetRepo import AssetRepository
from app.core.queue import enqueue_asset_processing, enqueue_asset_reprocess
from app.service.clipService import get_text_embedding
from app.service.assetProcessingService import AssetProcessingService
from app.service.rankingService import RankingService
from app.service.vectorService import VectorService

class AssetService: 
    def __init__(self, session: Session):
        self.__assetRepo = AssetRepository(session=session)
        self.__rankingService = RankingService()

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
                "detected_objects": asset.detected_objects or [],
                "scene_label": asset.scene_label,
                "time_label": asset.time_label,
                "environment_label": asset.environment_label,
                "processed_at": asset.processed_at,
                "ranking_score": asset.ranking_score,
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
            "detected_objects": asset.detected_objects or [],
            "scene_label": asset.scene_label,
            "time_label": asset.time_label,
            "environment_label": asset.environment_label,
            "processed_at": asset.processed_at,
            "ranking_score": asset.ranking_score,
            "created_at": asset.created_at,
        }
    
    def search_asset(self, user_id: int, query: str):
        query_embedding = get_text_embedding(text=query)
        search_results = VectorService().search_similar_vectors(user_id=user_id, query_embedding=query_embedding)

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

            response.append(self._serialize_asset(asset=asset, extra={"score": result.score}))
        return response

    def hybrid_search_assets(self, user_id: int, search_request: HybridSearchRequest) -> HybridSearchResponse:
        page = max(search_request.page, 1)
        page_size = min(max(search_request.page_size, 1), 100)
        vector_limit = max(page * page_size * 3, 50)

        query_embedding = get_text_embedding(text=search_request.query)
        search_results = VectorService().search_similar_vectors(
            user_id=user_id,
            query_embedding=query_embedding,
            limit=vector_limit,
        )

        asset_ids = [result.payload["asset_id"] for result in search_results]
        if not asset_ids:
            return HybridSearchResponse(page=page, page_size=page_size, total=0, results=[])

        filtered_assets = self.__assetRepo.get_filtered_assets_by_asset_ids(
            user_id=user_id,
            asset_ids=asset_ids,
            filters=search_request,
        )
        asset_map = {asset.id: asset for asset in filtered_assets}

        ranked_results = []
        for result in search_results:
            asset_id = result.payload["asset_id"]
            asset = asset_map.get(asset_id)
            if not asset:
                continue

            ranking = self.__rankingService.score_asset(
                asset=asset,
                semantic_similarity=result.score,
                query=search_request.query,
                filters=search_request,
            )
            ranked_results.append(
                self._serialize_asset(
                    asset=asset,
                    extra=ranking,
                )
            )

        sorted_results = self.__rankingService.sort_results(
            results=ranked_results,
            sort_by=search_request.sort_by,
        )
        total = len(sorted_results)
        start_index = (page - 1) * page_size
        end_index = start_index + page_size
        paged_results = sorted_results[start_index:end_index]

        return HybridSearchResponse(
            page=page,
            page_size=page_size,
            total=total,
            results=paged_results,
        )

    def get_asset_filters(self, user_id: int) -> AssetFilterOptions:
        filter_options = self.__assetRepo.get_asset_filter_options(user_id=user_id)
        return AssetFilterOptions(**filter_options)

    def get_ranking_config(self):
        return self.__rankingService.get_config()

    def get_asset_intelligence(self, user_id: int, asset_id: int) -> AssetIntelligenceResponse:
        asset = self.__assetRepo.get_asset_by_asset_id(asset_id=asset_id)

        if not asset:
            raise HTTPException(status_code=404, detail="Asset not found")

        if asset.user_id != user_id:
            raise HTTPException(status_code=403, detail="Unauthorized to access this asset")

        return AssetIntelligenceResponse(
            asset_id=asset.id,
            status=asset.status,
            caption=asset.captions,
            tags=asset.tags or [],
            detected_objects=asset.detected_objects or [],
            scene_label=asset.scene_label,
            time_label=asset.time_label,
            environment_label=asset.environment_label,
            processed_at=asset.processed_at,
            ranking_score=asset.ranking_score,
        )

    def reprocess_asset(self, user_id: int, asset_id: int) -> AssetReprocessResponse:
        asset = self.__assetRepo.get_asset_by_asset_id(asset_id=asset_id)

        if not asset:
            raise HTTPException(status_code=404, detail="Asset not found")

        if asset.user_id != user_id:
            raise HTTPException(status_code=403, detail="Unauthorized to reprocess this asset")

        reset_asset = AssetProcessingService(session=self.__assetRepo.session).prepare_asset_for_reprocess(
            asset_id=asset_id,
            user_id=user_id,
        )
        enqueue_asset_reprocess(
            asset_id=reset_asset.id,
            user_id=user_id,
            file_key=reset_asset.file_key,
        )

        return AssetReprocessResponse(
            asset_id=reset_asset.id,
            status=reset_asset.status,
            message="Asset reprocessing queued successfully",
        )

    def _serialize_asset(self, asset, extra: dict | None = None):
        payload = {
            "id": asset.id,
            "user_id": asset.user_id,
            "file_key": asset.file_key,
            "image_url": generate_presigned_url(asset.file_key),
            "status": asset.status,
            "caption": asset.captions,
            "tags": asset.tags,
            "detected_objects": asset.detected_objects or [],
            "scene_label": asset.scene_label,
            "time_label": asset.time_label,
            "environment_label": asset.environment_label,
            "processed_at": asset.processed_at,
            "ranking_score": asset.ranking_score,
            "created_at": asset.created_at,
        }
        if extra:
            payload.update(extra)
        return payload
