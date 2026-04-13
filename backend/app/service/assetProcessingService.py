import logging

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.db.repository.assetRepo import AssetRepository
from app.service.captionService import generate_caption_and_tags
from app.service.clipService import get_image_embedding
from app.service.storageService import download_file_from_s3, generate_presigned_url
from app.service.vectorService import VectorService

logger = logging.getLogger(__name__)


class AssetProcessingService:
    def __init__(self, session: Session):
        self.__assetRepo = AssetRepository(session=session)
        self.__vectorService = VectorService()

    def process_asset(self, asset_id: int, user_id: int, file_key: str):
        asset = self.__assetRepo.get_asset_by_asset_id(asset_id=asset_id)
        if not asset or asset.user_id != user_id:
            raise HTTPException(status_code=404, detail="Asset not found")

        try:
            logger.info("Marking asset as processing asset_id=%s", asset_id)
            self.__assetRepo.update_asset_status(asset=asset, status="processing")

            logger.info("Downloading S3 object asset_id=%s", asset_id)
            image_bytes = download_file_from_s3(file_key=file_key)

            logger.info("Generating caption and tags asset_id=%s", asset_id)
            image_url = generate_presigned_url(file_key=file_key)
            ai_response = generate_caption_and_tags(image_url=image_url)
            caption = ai_response["caption"]
            tags = ai_response["tags"]

            logger.info("Generating CLIP embedding asset_id=%s", asset_id)
            embedding = get_image_embedding(image_bytes=image_bytes)

            logger.info("Upserting vector asset_id=%s", asset_id)
            self.__vectorService.store_vector(
                asset_id=asset.id,
                user_id=user_id,
                embedding=embedding,
            )

            logger.info("Marking asset ready asset_id=%s", asset_id)
            self.__assetRepo.update_asset_processing_result(
                asset=asset,
                caption=caption,
                tags=tags,
                status="ready",
            )
        except Exception:
            logger.exception("Processing pipeline failed asset_id=%s", asset_id)
            self.__assetRepo.mark_asset_failed(asset_id=asset_id)
            raise
