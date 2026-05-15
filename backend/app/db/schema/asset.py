from datetime import datetime

from pydantic import BaseModel


class ProcessingIssue(BaseModel):
    stage: str
    message: str


class AssetIntelligenceFields(BaseModel):
    detected_objects: list[str] = []
    scene_label: str | None = None
    time_label: str | None = None
    environment_label: str | None = None
    processed_at: datetime | None = None
    ranking_score: float = 0.0


class AssetIntelligenceUpdate(BaseModel):
    detected_objects: list[str] = []
    scene_label: str | None = None
    time_label: str | None = None
    environment_label: str | None = None
    processed_at: datetime | None = None
    ranking_score: float = 0.0


class AssetResponse(AssetIntelligenceFields):
    id: int
    user_id: int
    file_key: str
    status: str
    caption: str | None = None
    tags: list[str] = []
    created_at: datetime | None = None


class AssetProcessingReport(BaseModel):
    asset_id: int
    user_id: int
    status: str
    completed_stages: list[str] = []
    warnings: list[ProcessingIssue] = []


class HybridSearchRequest(BaseModel):
    query: str
    tags: list[str] = []
    objects: list[str] = []
    scenes: list[str] = []
    environment: str | None = None
    time_of_day: list[str] = []
    date_from: datetime | None = None
    date_to: datetime | None = None
    page: int = 1
    page_size: int = 20
    sort_by: str = "relevance"


class HybridSearchResult(AssetResponse):
    semantic_similarity: float = 0.0
    intelligence_boost: float = 0.0
    final_score: float = 0.0
    exact_keyword_boost: float = 0.0
    metadata_match_boost: float = 0.0
    recency_boost: float = 0.0
    image_url: str | None = None


class RankingConfigResponse(BaseModel):
    semantic_weight: float
    recency_weight: float
    keyword_weight: float
    metadata_weight: float
    intelligence_weight: float
    recent_days_window: int
    warm_days_window: int
    cool_days_window: int


class HybridSearchResponse(BaseModel):
    page: int
    page_size: int
    total: int
    results: list[HybridSearchResult]


class AssetFilterOptions(BaseModel):
    tags: list[str] = []
    detected_objects: list[str] = []
    scenes: list[str] = []
    environments: list[str] = []
    time_of_day: list[str] = []


class AssetIntelligenceResponse(BaseModel):
    asset_id: int
    status: str
    caption: str | None = None
    tags: list[str] = []
    detected_objects: list[str] = []
    scene_label: str | None = None
    time_label: str | None = None
    environment_label: str | None = None
    processed_at: datetime | None = None
    ranking_score: float = 0.0


class AssetReprocessResponse(BaseModel):
    asset_id: int
    status: str
    message: str
