from PIL import Image
from django.core.files.base import ContentFile
from io import BytesIO
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse
import os


def resize_image(image_field, max_width=1200, max_height=1200):
    img = Image.open(image_field.path)

    if img.mode in ("RGBA", "P"):
        img = img.convert("RGB")

    if img.height > max_height or img.width > max_width:
        img.thumbnail((max_width, max_height))

        buffer = BytesIO()
        img.save(buffer, format="JPEG", quality=85)
        image_field.save(image_field.name, ContentFile(buffer.getvalue()), save=False)


def get_upload_path(instance, filename):
    user_id = None
    if hasattr(instance, 'author') and instance.author:
        user_id = instance.author.id
    elif hasattr(instance, 'created_by') and instance.created_by:
        user_id = instance.created_by.id

    model_name = instance.__class__.__name__
    if model_name == 'PathEvent':
        folder = 'path_events'
    elif model_name == 'DiaryPage':
        folder = 'diary_pages'
    else:
        folder = 'journal_entries'

    if user_id:
        return os.path.join(folder, str(user_id), filename)
    else:
        return os.path.join(folder, 'unknown', filename)


def media_library_upload_path(instance, filename):
    user_id = instance.uploaded_by.id if instance.uploaded_by_id else 'unknown'
    return os.path.join('media_library', str(user_id), filename)


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

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.image:
            resize_image(self.image)
            super().save(update_fields=["image"])


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
    event_date = models.DateTimeField(help_text='Start date & time')
    event_end_date = models.DateTimeField(null=True, blank=True, help_text='End date & time (optional)')
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
        return reverse('path_event_detail', kwargs={'pk': self.pk})

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.image:
            resize_image(self.image)
            super().save(update_fields=["image"])


class PathEventRegistration(models.Model):
    event = models.ForeignKey(PathEvent, on_delete=models.CASCADE, related_name='registrations')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='event_registrations')
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['joined_at']
        unique_together = [['event', 'user']]

    def __str__(self):
        return f'{self.user.username} → {self.event.title}'


class PathEventComment(models.Model):
    event = models.ForeignKey(PathEvent, on_delete=models.CASCADE, related_name='event_comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f'Comment by {self.author.username} on {self.event.title}'


class DiaryPage(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('public', 'Public'),
    ]

    title = models.CharField(max_length=200)
    content = models.TextField()
    image = models.ImageField(upload_to=get_upload_path, blank=True, null=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='diary_pages')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Diary Page'
        verbose_name_plural = 'Diary Pages'

    def __str__(self):
        return f'{self.title} ({self.get_status_display()})'

    def get_absolute_url(self):
        return reverse('diary_page_detail', kwargs={'pk': self.pk})

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.image:
            resize_image(self.image)
            super().save(update_fields=["image"])


class DiaryComment(models.Model):
    page = models.ForeignKey(DiaryPage, on_delete=models.CASCADE, related_name='diary_comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f'Comment by {self.author.username} on {self.page.title}'


class MediaItem(models.Model):
    FILE_TYPE_IMAGE = 'image'
    FILE_TYPE_VIDEO = 'video'
    FILE_TYPE_OTHER = 'other'
    FILE_TYPE_CHOICES = [
        (FILE_TYPE_IMAGE, 'Image'),
        (FILE_TYPE_VIDEO, 'Video'),
        (FILE_TYPE_OTHER, 'Other'),
    ]

    file = models.FileField(upload_to=media_library_upload_path)
    title = models.CharField(max_length=255, blank=True)
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='media_uploads')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Media item'
        verbose_name_plural = 'Media library'

    def __str__(self):
        return self.title or self.file.name


class AboutPage(models.Model):
    content = models.TextField(blank=True)
    image = models.ImageField(upload_to='about/', blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'About page'
        verbose_name_plural = 'About page'

    def __str__(self):
        return 'About page'
