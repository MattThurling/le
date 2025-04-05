import csv
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from website.models import Word, Language, TabooSet, TabooCard, TabooCardTabooWord

User = get_user_model()

class Command(BaseCommand):
    help = 'Import taboo cards from a CSV file with 1 to 7 taboo words'

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
            return Word.objects.filter(word__iexact=word_str.strip(), language=language).first()

        with open(csv_path, newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                target_word = get_word(row["Target"])
                if not target_word:
                    self.stdout.write(self.style.WARNING(f"⚠️ Skipped (target not found): {row['Target']}"))
                    continue

                card = TabooCard.objects.create(taboo_set=taboo_set, target=target_word)
                added_count = 0

                for i in range(1, 8):  # Taboo 1 to 7
                    key = f"Taboo {i}"
                    if row.get(key):
                        taboo_word = get_word(row[key])
                        if taboo_word:
                            TabooCardTabooWord.objects.create(card=card, taboo_word=taboo_word)
                            added_count += 1
                        else:
                            self.stdout.write(self.style.WARNING(
                                f"   ↳ Taboo word not found: {row[key]} (card: {target_word.word})"
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
