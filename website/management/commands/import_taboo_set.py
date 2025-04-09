import csv
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from website.models import Word, Language, TabooSet, TabooCard, TabooCardTabooWord

User = get_user_model()

class Command(BaseCommand):
    help = 'Import taboo cards from a CSV file (expects Target + Taboo 1..7 columns)'

    def add_arguments(self, parser):
        parser.add_argument('csv_path', type=str, help='Path to the CSV file')
        parser.add_argument('set_name', type=str, help='Name of the TabooSet')
        parser.add_argument('username', type=str, help='Username (owner of the TabooSet)')
        parser.add_argument('language_name', type=str, help='Language name (e.g., English)')

    def handle(self, *args, **options):
        csv_path = options['csv_path']
        set_name = options['set_name']
        username = options['username']
        language_name = options['language_name']

        user = User.objects.get(username=username)
        language = Language.objects.get(name=language_name)
        taboo_set, _ = TabooSet.objects.get_or_create(name=set_name, owner=user, language=language)

        def get_word(word_str):
            word_str = word_str.strip()
            if not word_str:
                return None
            word_obj, _ = Word.objects.get_or_create(word__iexact=word_str, language=language, defaults={
                'word': word_str,
                'part_of_speech': 'noun'  # or guess/detect if you want
            })
            return word_obj

        with open(csv_path, newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                target_word = get_word(row.get("Target", ""))
                if not target_word:
                    self.stdout.write(self.style.WARNING(f"⚠️ Skipped (target not found or blank): {row.get('Target')}"))
                    continue

                card = TabooCard.objects.create(taboo_set=taboo_set, target=target_word)
                added_count = 0

                for i in range(1, 8):
                    key = f"Taboo {i}"
                    word = row.get(key)
                    taboo_word = get_word(word) if word else None

                    if taboo_word:
                        TabooCardTabooWord.objects.create(card=card, taboo_word=taboo_word)
                        added_count += 1
                    elif word:
                        self.stdout.write(self.style.WARNING(
                            f"   ↳ Taboo word not found or invalid: '{word}' (card: {target_word.word})"
                        ))

                if added_count < 1:
                    self.stdout.write(self.style.WARNING(
                        f"❌ Deleted card with no valid taboo words: {target_word.word}"
                    ))
                    card.delete()
                else:
                    self.stdout.write(self.style.SUCCESS(
                        f"✅ Imported: {target_word.word} ({added_count} taboo word(s))"
                    ))
