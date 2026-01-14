from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse
import os

def get_upload_path(instance, filename):
    return os.path.join('journal_entries', str(instance.author.id), filename)

class JournalEntry(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    image = models.ImageField(upload_to=get_upload_path, blank=True, null=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    is_published = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = 'Journal Entries'
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('entry_detail', kwargs={'pk': self.pk})

class Comment(models.Model):
    entry = models.ForeignKey(JournalEntry, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['created_at']
    
    def __str__(self):
        return f'Comment by {self.author.username} on {self.entry.title}'

class PathEvent(models.Model):
    """Define Your Path - Events calendar for runs, hikes, and adventures"""
    EVENT_TYPES = [
        ('run', 'Run'),
        ('hike', 'Hike'),
        ('adventure', 'Adventure'),
        ('community', 'Community Event'),
        ('wellness', 'Wellness'),
        ('other', 'Other'),
    ]
    
    title = models.CharField(max_length=200)
    description = models.TextField()
    event_type = models.CharField(max_length=20, choices=EVENT_TYPES, default='adventure')
    event_date = models.DateTimeField()
    location = models.CharField(max_length=200, blank=True)
    image = models.ImageField(upload_to=get_upload_path, blank=True, null=True)
    max_participants = models.IntegerField(null=True, blank=True)
    is_published = models.BooleanField(default=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_events')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['event_date']
        verbose_name = 'Path Event'
        verbose_name_plural = 'Path Events'
    
    def __str__(self):
        return f'{self.title} - {self.event_date.strftime("%B %d, %Y")}'
    
    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('path_event_detail', kwargs={'pk': self.pk})
