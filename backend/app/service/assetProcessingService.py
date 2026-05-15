import logging
from collections.abc import Callable

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.db.repository.assetRepo import AssetRepository
from app.db.schema.asset import AssetIntelligenceUpdate, AssetProcessingReport, ProcessingIssue
from app.service.captionService import generate_caption_and_tags
from app.service.clipService import get_image_embedding
from app.service.intelligenceService import IntelligenceService
from app.service.storageService import download_file_from_s3, generate_presigned_url
from app.service.vectorService import VectorService

logger = logging.getLogger(__name__)


class AssetProcessingService:
    def __init__(self, session: Session):
        self.__assetRepo = AssetRepository(session=session)
        self.__vectorService = VectorService()
        self.__intelligenceService = IntelligenceService()

    def process_asset(self, asset_id: int, user_id: int, file_key: str) -> AssetProcessingReport:
        asset = self.__assetRepo.get_asset_by_asset_id(asset_id=asset_id)
        if not asset or asset.user_id != user_id:
            raise HTTPException(status_code=404, detail="Asset not found")

        report = AssetProcessingReport(
            asset_id=asset_id,
            user_id=user_id,
            status="processing",
        )

        try:
            logger.info("Marking asset as processing asset_id=%s user_id=%s", asset_id, user_id)
            self.__assetRepo.update_asset_status(asset=asset, status="processing")
            report.completed_stages.append("mark_processing")

            logger.info("Downloading S3 object asset_id=%s", asset_id)
            image_bytes = download_file_from_s3(file_key=file_key)
            report.completed_stages.append("download_s3")

            image_url = generate_presigned_url(file_key=file_key)
            caption_payload = self._run_optional_stage(
                report=report,
                stage_name="caption_and_tags",
                callback=lambda: generate_caption_and_tags(image_url=image_url),
                fallback={"caption": "Description unavailable", "tags": []},
            )
            caption = caption_payload["caption"]
            tags = caption_payload["tags"]
            print("Generated caption:", caption)
            print("Generated tags:", tags)

            intelligence_data = self._run_optional_stage(
                report=report,
                stage_name="intelligence_metadata",
                callback=lambda: self.__intelligenceService.extract_asset_intelligence(
                    image_url=image_url,
                    ranking_score_factory=_default_ranking_score,
                ),
                fallback=AssetIntelligenceUpdate(),
            )

            logger.info("Generating CLIP embedding asset_id=%s", asset_id)
            embedding = get_image_embedding(image_bytes=image_bytes)
            report.completed_stages.append("clip_embedding")

            logger.info("Upserting vector asset_id=%s", asset_id)
            self.__vectorService.store_vector(
                asset_id=asset.id,
                user_id=user_id,
                embedding=embedding,
            )
            report.completed_stages.append("qdrant_upsert")

            logger.info("Saving intelligence metadata asset_id=%s", asset_id)
            self.__assetRepo.update_asset_intelligence(
                asset=asset,
                intelligence_data=intelligence_data,
            )
            report.completed_stages.append("save_intelligence")

            logger.info("Marking asset ready asset_id=%s", asset_id)
            self.__assetRepo.update_asset_processing_result(
                asset=asset,
                caption=caption,
                tags=tags,
                status="ready",
            )
            report.completed_stages.append("save_caption_tags")
            self.__assetRepo.touch_processed_at(asset=asset)
            report.completed_stages.append("mark_processed_at")
            report.status = "ready"
            return report
        except Exception:
            logger.exception("Processing pipeline failed asset_id=%s", asset_id)
            self.__assetRepo.mark_asset_failed(asset_id=asset_id)
            report.status = "failed"
            raise

    def prepare_asset_for_reprocess(self, asset_id: int, user_id: int):
        asset = self.__assetRepo.get_asset_by_asset_id(asset_id=asset_id)
        if not asset or asset.user_id != user_id:
            raise HTTPException(status_code=404, detail="Asset not found")

        return self.__assetRepo.reset_asset_processing(asset=asset)

    def _run_optional_stage(
        self,
        report: AssetProcessingReport,
        stage_name: str,
        callback: Callable,
        fallback,
    ):
        try:
            logger.info("Running optional stage stage=%s asset_id=%s", stage_name, report.asset_id)
            result = callback()
            report.completed_stages.append(stage_name)
            return result
        except Exception as error:
            logger.exception(
                "Optional stage degraded stage=%s asset_id=%s error=%s",
                stage_name,
                report.asset_id,
                error,
            )
            report.warnings.append(
                ProcessingIssue(
                    stage=stage_name,
                    message=str(error),
                )
            )
            return fallback


def _default_ranking_score(intelligence_result) -> float:
    score = 0.0
    score += min(len(intelligence_result.detected_objects), 5) * 0.1
    if intelligence_result.scene_label:
        score += 0.2
    if intelligence_result.time_label:
        score += 0.1
    if intelligence_result.environment_label:
        score += 0.1
    return round(score, 4)
