from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import os

def get_upload_path(instance, filename):
    return os.path.join('journal_entries', str(instance.author.id), filename)

class JournalEntry(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    image = models.ImageField(upload_to=get_upload_path, blank=True, null=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = 'Journal Entries'
    
    def __str__(self):
        return self.title
