import logging
from datetime import datetime, timezone
from typing import Callable

from decouple import config

from app.db.schema.asset import AssetIntelligenceUpdate
from app.service.intelligenceProvider import (
    HuggingFaceIntelligenceProvider,
    IntelligenceProvider,
    IntelligenceResult,
)

logger = logging.getLogger(__name__)


class IntelligenceService:
    def __init__(self, provider: IntelligenceProvider | None = None):
        self._provider = provider or build_intelligence_provider()
        self._retry_max = config("INTELLIGENCE_RETRY_MAX", cast=int, default=2)

    def extract_asset_intelligence(
        self,
        image_url: str,
        ranking_score_factory: Callable[[IntelligenceResult], float] | None = None,
    ) -> AssetIntelligenceUpdate:
        last_error: Exception | None = None

        for attempt in range(1, self._retry_max + 2):
            try:
                result = self._provider.extract_metadata(image_url=image_url)
                ranking_score = 0.0
                if ranking_score_factory is not None:
                    ranking_score = ranking_score_factory(result)

                return AssetIntelligenceUpdate(
                    detected_objects=result.detected_objects,
                    scene_label=result.scene_label,
                    time_label=result.time_label,
                    environment_label=result.environment_label,
                    processed_at=datetime.now(timezone.utc),
                    ranking_score=ranking_score,
                )
            except Exception as error:
                last_error = error
                logger.warning(
                    "Intelligence extraction failed attempt=%s/%s error=%s",
                    attempt,
                    self._retry_max + 1,
                    error,
                )

        raise last_error or RuntimeError("Intelligence extraction failed")


def build_intelligence_provider() -> IntelligenceProvider:
    provider_name = config("INTELLIGENCE_PROVIDER", default="huggingface").strip().lower()

    if provider_name == "huggingface":
        return HuggingFaceIntelligenceProvider()

    raise ValueError(f"Unsupported intelligence provider: {provider_name}")
