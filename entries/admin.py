from django.contrib import admin
from .models import JournalEntry, Comment

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
