import csv
from django.contrib.auth.models import User
from website.models import Word, TabooSet, TabooWord

def get_existing_word(word_str, language):
    cleaned = word_str.strip()
    try:
        return Word.objects.get(word__iexact=cleaned, language=language)
    except Word.DoesNotExist:
        return None

def import_taboo_csv(csv_path, set_name, username):
    user = User.objects.get(username=username)
    taboo_set, _ = TabooSet.objects.get_or_create(name=set_name, owner=user)

    with open(csv_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            target = get_existing_word(row["Word"])
            taboo1 = get_existing_word(row["Taboo Word 1"])
            taboo2 = get_existing_word(row["Taboo Word 2"])
            taboo3 = get_existing_word(row["Taboo Word 3"])

            if not all([target, taboo1, taboo2, taboo3]):
                print(f"⚠️ Skipped (missing words): {row}")
                continue

            TabooWord.objects.create(
                taboo_set=taboo_set,
                target=target,
                taboo1=taboo1,
                taboo2=taboo2,
                taboo3=taboo3
            )
            print(f"✅ Imported: {target.word}")
