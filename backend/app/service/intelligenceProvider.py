import json
from abc import ABC, abstractmethod
from typing import Any

from decouple import config
from openai import OpenAI
from pydantic import BaseModel, Field


class IntelligenceResult(BaseModel):
    detected_objects: list[str] = Field(default_factory=list)
    scene_label: str | None = None
    time_label: str | None = None
    environment_label: str | None = None


class IntelligenceProvider(ABC):
    @abstractmethod
    def extract_metadata(self, image_url: str) -> IntelligenceResult:
        raise NotImplementedError


class HuggingFaceIntelligenceProvider(IntelligenceProvider):
    def __init__(self):
        hf_token = config("HF_TOKEN")
        self._client = OpenAI(
            base_url="https://router.huggingface.co/v1",
            api_key=hf_token,
        )
        self._model = config("HF_INTELLIGENCE_MODEL", default="google/gemma-3n-E4B-it:together")

    def extract_metadata(self, image_url: str) -> IntelligenceResult:
        completion = self._client.chat.completions.create(
            model=self._model,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": """
Return ONLY a valid JSON object in this format:
{
  "detected_objects": ["object1", "object2", "object3"],
  "scene_label": "beach",
  "time_label": "sunset",
  "environment_label": "outdoor"
}

Rules:
- detected_objects must be short lowercase nouns.
- scene_label must be a single short scene phrase.
- time_label must be one of: morning, afternoon, sunset, night, unknown.
- environment_label must be one of: indoor, outdoor, unknown.
- If uncertain, use best-effort labels and an empty detected_objects list.
- No explanation, no markdown, no extra text.
"""
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": image_url
                            }
                        }
                    ]
                }
            ],
            temperature=0.1,
        )

        content = completion.choices[0].message.content
        cleaned = _clean_json_content(content)
        payload = json.loads(cleaned)
        return IntelligenceResult(
            detected_objects=_normalize_object_list(payload.get("detected_objects", [])),
            scene_label=_normalize_optional_text(payload.get("scene_label")),
            time_label=_normalize_optional_text(payload.get("time_label")),
            environment_label=_normalize_optional_text(payload.get("environment_label")),
        )


def _clean_json_content(content: str) -> str:
    text = content.strip()
    if text.startswith("```json"):
        text = text[7:]
    elif text.startswith("```"):
        text = text[3:]
    if text.endswith("```"):
        text = text[:-3]
    return text.strip()


def _normalize_object_list(value: Any) -> list[str]:
    if not isinstance(value, list):
        return []

    cleaned: list[str] = []
    seen: set[str] = set()
    for item in value:
        if item is None:
            continue
        text = str(item).strip().lower()
        if not text or text in seen:
            continue
        cleaned.append(text)
        seen.add(text)
    return cleaned


def _normalize_optional_text(value: Any) -> str | None:
    if value is None:
        return None
    text = str(value).strip().lower()
    return text or None
