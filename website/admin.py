from django.contrib import admin
from .models import Prompt, Page, Post, TimeLog, Level, Attainment, Organisation, Language, User

# Common admin config
class BaseAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at')
    search_fields = ('title', 'content')
    list_filter = ('created_at',)
    ordering = ('-created_at',)

@admin.register(Prompt, Page, Post)
class ContentAdmin(BaseAdmin):
    pass

@admin.register(TimeLog)
class TimeLogAdmin(admin.ModelAdmin):
    list_display = ('activity', 'created_at')
    search_fields = ('activity',)
    list_filter = ('created_at',)
    ordering = ('-created_at',)

@admin.register(Level, Attainment, Organisation, Language, User)
class LevelAdmin(admin.ModelAdmin):
    pass