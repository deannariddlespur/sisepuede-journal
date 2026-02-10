from django import forms
from .models import JournalEntry, Comment, PathEvent, PathEventComment, DiaryPage, DiaryComment, MediaItem, AboutPage

class JournalEntryForm(forms.ModelForm):
    class Meta:
        model = JournalEntry
        fields = ['title', 'content', 'image', 'is_published']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 15,
            }),
            'image': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*',
            }),
            'is_published': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
            }),
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Write your comment...',
            }),
        }

class PathEventForm(forms.ModelForm):
    class Meta:
        model = PathEvent
        fields = ['title', 'description', 'event_type', 'event_date', 'event_end_date', 'location', 'image', 'max_participants', 'is_published']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 8,
            }),
            'event_type': forms.Select(attrs={
                'class': 'form-control',
            }),
            'event_date': forms.DateTimeInput(attrs={
                'class': 'form-control',
                'type': 'datetime-local',
            }),
            'event_end_date': forms.DateTimeInput(attrs={
                'class': 'form-control',
                'type': 'datetime-local',
            }),
            'location': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'image': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*',
            }),
            'max_participants': forms.NumberInput(attrs={
                'class': 'form-control',
            }),
            'is_published': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
            }),
        }


class PathEventCommentForm(forms.ModelForm):
    class Meta:
        model = PathEventComment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Join the discussion...',
            }),
        }


class DiaryPageForm(forms.ModelForm):
    class Meta:
        model = DiaryPage
        fields = ['title', 'content', 'image', 'status']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 20,
            }),
            'image': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*',
            }),
            'status': forms.Select(attrs={
                'class': 'form-control',
            }),
        }


class DiaryCommentForm(forms.ModelForm):
    class Meta:
        model = DiaryComment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Write your comment...',
            }),
        }


class MediaItemForm(forms.ModelForm):
    class Meta:
        model = MediaItem
        fields = ['file', 'title']
        widgets = {
            'file': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*,video/*',
            }),
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Optional label',
            }),
        }


class AboutPageForm(forms.ModelForm):
    class Meta:
        model = AboutPage
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 16,
                'placeholder': 'About page content (plain text or HTML)...',
            }),
        }

