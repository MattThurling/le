from openai import OpenAI
import json
import os

client = OpenAI(api_key=os.getenv('OPENAI_KEY'))

def generate_set(language, theme, count):
    prompt = f"""
    Generate a list of {count} Taboo-style cards in {language} on the theme of "{theme}".
    Each card must be a JSON object with two fields:
    - "target": the main word
    - "taboo_words": an array of exactly 7 common taboo words

    Return only a valid JSON array of cards, and nothing else.

    Example:
    [
    {{
        "target": "resume",
        "taboo_words": ["CV", "job", "apply", "experience", "skills", "document", "career"]
    }},
    ...
    ]
    """

    response = client.responses.create(
        model="gpt-4o-2024-08-06",
        input=[
            {"role": "system", "content": "You generate structured Taboo game data."},
            {"role": "user", "content": prompt}
        ],
        text={
            "format": {
                "type": "json_schema",
                "name": "taboo_set",
                "schema": {
                    "type": "object",
                    "properties": {
                        "cards": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "target": {"type": "string"},
                                    "taboo_words": {
                                        "type": "array",
                                        "items": {"type": "string"}
                                    }
                                },
                                "required": ["target", "taboo_words"],
                                "additionalProperties": False
                            }
                        }
                    },
                    "required": ["cards"],
                    "additionalProperties": False
                },
                "strict": True
            }
        }
    )

    return json.loads(response.output_text)

