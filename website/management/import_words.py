import os
import json
from django.db import IntegrityError
from website.models import Word, Language

# Set your folder path here
FOLDER_PATH = "words"

language = Language.objects.get(name="English")

for filename in os.listdir(FOLDER_PATH):
    if filename.endswith(".json"):
        filepath = os.path.join(FOLDER_PATH, filename)
        with open(filepath, "r", encoding="utf-8") as file:
            data = json.load(file)

        for word_key, word_data in data.items():
            word_text = word_data.get("word")
            meanings = word_data.get("meanings", [])

            if not meanings:
                continue 

            first_meaning = meanings[0]
            part_of_speech = first_meaning.get("speech_part")

            try:
                Word.objects.create(
                    word=word_text,
                    language=language,
                    part_of_speech=part_of_speech,
                )
                print(f"Added: {word_text}")
            except IntegrityError:
                print(f"Skipped (already exists): {word_text}")
