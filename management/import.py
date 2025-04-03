import json
from website.models import Prompt, Organisation, User, Language

with open('prompts.json', 'r') as file:
    data = json.load(file)


for entry in data:
    user = User.objects.get(username="Matt")
    if entry["organisation"] == "french":
        language = Language.objects.get(name="French")
    else:
        language = Language.objects.get(name="English") 
    Prompt.objects.create(
        title=entry["title"],
        content=entry["content"],
        user = user,
        language = language,
        level = entry["level"],
        image = entry["image"],
    )
