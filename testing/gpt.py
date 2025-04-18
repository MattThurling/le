from openai import OpenAI
import os

gpt_client = OpenAI(api_key=os.getenv("OPENAI_KEY"))

prompt = f"""
Generate a list of 20 Taboo-style cards in English on the theme of "fishing".
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

response = gpt_client.responses.create(
    model="gpt-4o",
    # input="Write a one-sentence bedtime story about a unicorn."
    input=[
        {
            "role": "user",
            "content": [{"type": "input_text", "text": prompt}]
        }
    ],
  )

print(response.output_text)
