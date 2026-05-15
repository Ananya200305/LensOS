from decouple import config
import json
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

HF_TOKEN = config("HF_TOKEN")

client = OpenAI(
    base_url="https://router.huggingface.co/v1",
    api_key=HF_TOKEN,
)


def generate_caption_and_tags(image_url: str) -> dict:
    try:
        completion = client.chat.completions.create(
            model="google/gemma-3n-E4B-it:together",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": """
Return ONLY a valid JSON object in this format:
{
  "caption": "<short caption under 15 words>",
  "tags": ["tag1", "tag2", "tag3", "tag4", "tag5"]
}

Rules:
- Caption must be short and descriptive
- Tags must be single words
- "tags" MUST be a JSON array, NOT a string
- Do NOT wrap tags in quotes
- No extra text
- No explanation
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
            temperature=0.2,
        )

        content = completion.choices[0].message.content

        # robust JSON extraction
        result = _extract_json(content)

        return {
            "caption": _normalize_caption(result.get("caption")),
            "tags": _normalize_tags(result.get("tags", []))
        }

    except Exception as e:
        print("AI Service Error:", str(e))
        return {
            "caption": "Description unavailable",
            "tags": []
        }


# -------------------------
# Robust JSON extractor
# -------------------------
def _extract_json(content: str) -> dict:
    content = content.strip()

    # Remove markdown code blocks safely
    if content.startswith("```"):
        parts = content.split("```")
        if len(parts) >= 2:
            content = parts[1]

    content = content.strip()

    # Try direct JSON parse
    try:
        return json.loads(content)
    except json.JSONDecodeError:
        pass

    # Fallback: extract JSON substring
    start = content.find("{")
    end = content.rfind("}")

    if start != -1 and end != -1:
        try:
            return json.loads(content[start:end + 1])
        except json.JSONDecodeError:
            pass

    return {}


# -------------------------
# Caption normalization
# -------------------------
def _normalize_caption(value) -> str:
    if value is None:
        return "Description unavailable"

    caption = str(value).strip()
    return caption or "Description unavailable"


# -------------------------
# Tag normalization (bulletproof)
# -------------------------
def _normalize_tags(value) -> list[str]:
    if not value:
        return []

    # Case 1: stringified JSON
    if isinstance(value, str):
        value = value.strip()

        try:
            value = json.loads(value)
        except json.JSONDecodeError:
            # fallback cleanup
            value = (
                value.replace("[", "")
                .replace("]", "")
                .replace('"', "")
                .replace("'", "")
            )
            value = value.split(",")

    # Ensure list
    if not isinstance(value, list):
        return []

    normalized_tags = []
    seen = set()

    for item in value:
        tag = str(item).strip().lower()
        if tag and tag not in seen:
            normalized_tags.append(tag)
            seen.add(tag)

    return normalized_tags