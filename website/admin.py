from django.contrib import admin
from .models import Prompt, Page, Post, TimeLog, Level, Attainment, Organisation, Language, User, Word, TabooWord, TabooSet, TabooCard, TabooCardTabooWord

# Common admin config
class BaseAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at')
    search_fields = ('title', 'content')
    list_filter = ('created_at',)
    ordering = ('-created_at',)

@admin.register(Page, Post)
class ContentAdmin(BaseAdmin):
    pass

@admin.register(Prompt)
class PromptAdmin(admin.ModelAdmin):
    list_display = ('title', 'language')
    exclude = ('user',)

    def save_model(self, request, obj, form, change):
        obj.user = request.user
        obj.save()

@admin.register(TimeLog)
class TimeLogAdmin(admin.ModelAdmin):
    list_display = ('activity', 'created_at')
    search_fields = ('activity',)
    list_filter = ('created_at',)
    ordering = ('-created_at',)

@admin.register(Level, Attainment, Organisation, Language, User)
class LevelAdmin(admin.ModelAdmin):
    pass

@admin.register(TabooSet)
class TabooSetAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner', 'language')
    search_fields = ('name', 'owner__username')
    list_filter = ('language',)


class TabooCardTabooWordInline(admin.TabularInline):
    model = TabooCardTabooWord
    extra = 1
    max_num = 7
    autocomplete_fields = ['taboo_word']


@admin.register(TabooCard)
class TabooCardAdmin(admin.ModelAdmin):
    list_display = ('target', 'taboo_set')
    search_fields = ('target__word', 'taboo_set__name')
    list_filter = ('taboo_set__language',)
    inlines = [TabooCardTabooWordInline]
    autocomplete_fields = ['target', 'taboo_set']


@admin.register(Word)
class WordAdmin(admin.ModelAdmin):
    search_fields = ('word',)
    list_filter = ('language',)