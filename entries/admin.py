from django.contrib import admin
from .models import JournalEntry, Comment, PathEvent, DiaryPage, MediaItem

@admin.register(JournalEntry)
class JournalEntryAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'is_published', 'created_at']
    list_filter = ['is_published', 'created_at']
    search_fields = ['title', 'content']

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['entry', 'author', 'created_at']
    list_filter = ['created_at']
    search_fields = ['content', 'author__username']

@admin.register(PathEvent)
class PathEventAdmin(admin.ModelAdmin):
    list_display = ['title', 'event_type', 'event_date', 'location', 'is_published', 'created_by']
    list_filter = ['event_type', 'is_published', 'event_date']
    search_fields = ['title', 'description', 'location']
    date_hierarchy = 'event_date'

@admin.register(DiaryPage)
class DiaryPageAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'status', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['title', 'content']
    date_hierarchy = 'created_at'


@admin.register(MediaItem)
class MediaItemAdmin(admin.ModelAdmin):
    list_display = ['title', 'file', 'uploaded_by', 'created_at']
    list_filter = ['created_at']
    search_fields = ['title', 'file']
