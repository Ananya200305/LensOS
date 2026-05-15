from collections.abc import Iterable
from datetime import datetime, timezone

from decouple import config

from app.db.models.asset import Asset
from app.db.schema.asset import RankingConfigResponse


class RankingService:
    def __init__(self):
        self.semantic_weight = config("RANKING_SEMANTIC_WEIGHT", cast=float, default=0.65)
        self.recency_weight = config("RANKING_RECENCY_WEIGHT", cast=float, default=0.15)
        self.keyword_weight = config("RANKING_KEYWORD_WEIGHT", cast=float, default=0.1)
        self.metadata_weight = config("RANKING_METADATA_WEIGHT", cast=float, default=0.1)
        self.intelligence_weight = config("RANKING_INTELLIGENCE_WEIGHT", cast=float, default=0.05)
        self.recent_days_window = config("RANKING_RECENT_DAYS_WINDOW", cast=int, default=7)
        self.warm_days_window = config("RANKING_WARM_DAYS_WINDOW", cast=int, default=30)
        self.cool_days_window = config("RANKING_COOL_DAYS_WINDOW", cast=int, default=90)
        self._normalize_weights()

    def score_asset(self, asset: Asset, semantic_similarity: float, query: str, filters) -> dict:
        semantic_similarity = _clamp_score(semantic_similarity)
        exact_keyword_boost = self._keyword_boost(asset=asset, query=query)
        metadata_match_boost = self._metadata_match_boost(asset=asset, filters=filters)
        recency_boost = self._recency_boost(asset=asset)
        intelligence_boost = self._intelligence_boost(asset=asset)

        final_score = (
            semantic_similarity * self.semantic_weight
            + recency_boost * self.recency_weight
            + exact_keyword_boost * self.keyword_weight
            + metadata_match_boost * self.metadata_weight
            + intelligence_boost * self.intelligence_weight
        )

        return {
            "semantic_similarity": round(semantic_similarity, 4),
            "intelligence_boost": round(intelligence_boost, 4),
            "exact_keyword_boost": round(exact_keyword_boost, 4),
            "metadata_match_boost": round(metadata_match_boost, 4),
            "recency_boost": round(recency_boost, 4),
            "final_score": round(_clamp_score(final_score), 4),
        }

    def sort_results(self, results: list[dict], sort_by: str) -> list[dict]:
        if sort_by == "recent":
            return sorted(results, key=lambda item: item["created_at"] or datetime.min.replace(tzinfo=timezone.utc), reverse=True)
        if sort_by == "oldest":
            return sorted(results, key=lambda item: item["created_at"] or datetime.min.replace(tzinfo=timezone.utc))
        if sort_by == "semantic":
            return sorted(results, key=lambda item: item["semantic_similarity"], reverse=True)
        return sorted(results, key=lambda item: item["final_score"], reverse=True)

    def get_config(self) -> RankingConfigResponse:
        return RankingConfigResponse(
            semantic_weight=self.semantic_weight,
            recency_weight=self.recency_weight,
            keyword_weight=self.keyword_weight,
            metadata_weight=self.metadata_weight,
            intelligence_weight=self.intelligence_weight,
            recent_days_window=self.recent_days_window,
            warm_days_window=self.warm_days_window,
            cool_days_window=self.cool_days_window,
        )

    def _keyword_boost(self, asset: Asset, query: str) -> float:
        query_terms = {term for term in query.lower().split() if term}
        if not query_terms:
            return 0.0

        searchable_terms = set()
        searchable_terms.update(_split_terms(asset.captions))
        searchable_terms.update(_normalize_iterable(asset.tags))
        searchable_terms.update(_normalize_iterable(asset.detected_objects))
        searchable_terms.update(_split_terms(asset.scene_label))

        matches = len(query_terms.intersection(searchable_terms))
        return _clamp_score(matches / max(len(query_terms), 1))

    def _metadata_match_boost(self, asset: Asset, filters) -> float:
        checks = []

        if filters.tags:
            checks.append(bool(set(_normalize_iterable(asset.tags)).intersection(_normalize_iterable(filters.tags))))
        if filters.objects:
            checks.append(bool(set(_normalize_iterable(asset.detected_objects)).intersection(_normalize_iterable(filters.objects))))
        if filters.scenes:
            checks.append((asset.scene_label or "").lower() in set(_normalize_iterable(filters.scenes)))
        if filters.environment:
            checks.append((asset.environment_label or "").lower() == filters.environment.lower())
        if filters.time_of_day:
            checks.append((asset.time_label or "").lower() in set(_normalize_iterable(filters.time_of_day)))

        if not checks:
            return 0.0

        return _clamp_score(sum(1.0 for match in checks if match) / len(checks))

    def _recency_boost(self, asset: Asset) -> float:
        if not asset.created_at:
            return 0.0

        now = datetime.now(timezone.utc)
        age_days = max((now - asset.created_at).total_seconds() / 86400, 0)
        if age_days <= self.recent_days_window:
            return 1.0
        if age_days <= self.warm_days_window:
            return 0.6
        if age_days <= self.cool_days_window:
            return 0.3
        return 0.1

    def _intelligence_boost(self, asset: Asset) -> float:
        return _clamp_score(asset.ranking_score or 0.0)

    def _normalize_weights(self):
        total = (
            self.semantic_weight
            + self.recency_weight
            + self.keyword_weight
            + self.metadata_weight
            + self.intelligence_weight
        )
        if total <= 0:
            self.semantic_weight = 1.0
            self.recency_weight = 0.0
            self.keyword_weight = 0.0
            self.metadata_weight = 0.0
            self.intelligence_weight = 0.0
            return

        self.semantic_weight /= total
        self.recency_weight /= total
        self.keyword_weight /= total
        self.metadata_weight /= total
        self.intelligence_weight /= total


def _normalize_iterable(values: Iterable | None) -> list[str]:
    if not values:
        return []
    return [str(value).strip().lower() for value in values if str(value).strip()]


def _split_terms(value: str | None) -> list[str]:
    if not value:
        return []
    return [term.strip().lower() for term in value.split() if term.strip()]


def _clamp_score(value: float) -> float:
    return max(0.0, min(float(value), 1.0))
