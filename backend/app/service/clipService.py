from io import BytesIO
from functools import lru_cache

import torch
from PIL import Image
from transformers import CLIPModel, CLIPProcessor

CLIP_MODEL_NAME = "openai/clip-vit-base-patch32"
CLIP_VECTOR_SIZE = 512


@lru_cache(maxsize=1)
def get_clip_components():
    processor = CLIPProcessor.from_pretrained(CLIP_MODEL_NAME)
    model = CLIPModel.from_pretrained(CLIP_MODEL_NAME)
    model.eval()
    return processor, model


def normalize_embedding(embedding: torch.Tensor) -> list[float]:
    normalized = torch.nn.functional.normalize(embedding, p=2, dim=-1)
    return normalized.squeeze(0).tolist()


def get_image_embedding(image_bytes: bytes) -> list[float]:
    processor, model = get_clip_components()
    image = Image.open(BytesIO(image_bytes)).convert("RGB")
    inputs = processor(images=image, return_tensors="pt")

    with torch.no_grad():
        image_features = model.get_image_features(**inputs)

    return normalize_embedding(image_features.pooler_output)


def get_text_embedding(text: str) -> list[float]:
    processor, model = get_clip_components()
    inputs = processor(text=[text], return_tensors="pt", padding=True, truncation=True)

    with torch.no_grad():
        text_features = model.get_text_features(**inputs)

    return normalize_embedding(text_features.pooler_output)
