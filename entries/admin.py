from django.contrib import admin
from .models import JournalEntry, Comment, PathEvent, PathEventRegistration, PathEventComment, DiaryPage, DiaryComment, MediaItem, AboutPage

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


@admin.register(PathEventRegistration)
class PathEventRegistrationAdmin(admin.ModelAdmin):
    list_display = ['event', 'user', 'joined_at']
    list_filter = ['joined_at']


@admin.register(PathEventComment)
class PathEventCommentAdmin(admin.ModelAdmin):
    list_display = ['event', 'author', 'created_at']
    list_filter = ['created_at']
    search_fields = ['content', 'author__username']


@admin.register(DiaryPage)
class DiaryPageAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'status', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['title', 'content']
    date_hierarchy = 'created_at'


@admin.register(DiaryComment)
class DiaryCommentAdmin(admin.ModelAdmin):
    list_display = ['page', 'author', 'created_at']
    list_filter = ['created_at']
    search_fields = ['content', 'author__username']


@admin.register(MediaItem)
class MediaItemAdmin(admin.ModelAdmin):
    list_display = ['title', 'file', 'uploaded_by', 'created_at']
    list_filter = ['created_at']
    search_fields = ['title', 'file']


@admin.register(AboutPage)
class AboutPageAdmin(admin.ModelAdmin):
    list_display = ['id', 'updated_at', 'has_content', 'has_image']
    list_display_links = ['id', 'updated_at']
    fields = ['content', 'image', 'updated_at']
    readonly_fields = ['updated_at']

    def has_content(self, obj):
        return bool(obj.content and obj.content.strip())
    has_content.boolean = True
    has_content.short_description = 'Has content'

    def has_image(self, obj):
        return bool(obj.image)
    has_image.boolean = True
    has_image.short_description = 'Has image'
