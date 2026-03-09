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
    """
    Generates caption and tags using Gemma 3n vision model.
    Returns:
        {
            "caption": str,
            "tags": list[str]
        }
    """

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

        # Parse JSON safely
        cleaned = content.strip().strip('```json').strip('```')
        result = json.loads(cleaned)

        return {
            "caption": result.get("caption", "Description unavailable"),
            "tags": result.get("tags", [])
        }

    except json.JSONDecodeError:
        print("JSON parsing failed.")
        return {
            "caption": "Description unavailable",
            "tags": []
        }

    except Exception as e:
        print("AI Service Error:", str(e))
        return {
            "caption": "Description unavailable",
            "tags": []
        }