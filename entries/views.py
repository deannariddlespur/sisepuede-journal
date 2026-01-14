from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseForbidden
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from .models import JournalEntry, Comment
from .forms import JournalEntryForm, CommentForm

def is_admin(user):
    return user.is_authenticated and user.is_staff

def home(request):
    # Show all published entries to everyone
    entries = JournalEntry.objects.filter(is_published=True)
    return render(request, 'entries/home.html', {'entries': entries})

def entry_detail(request, pk):
    # Anyone can view published entries
    entry = get_object_or_404(JournalEntry, pk=pk, is_published=True)
    comments = entry.comments.all()
    comment_form = None
    
    if request.user.is_authenticated:
        comment_form = CommentForm()
    
    if request.method == 'POST' and request.user.is_authenticated:
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.entry = entry
            comment.author = request.user
            comment.save()
            messages.success(request, 'Your comment has been posted!')
            return redirect('entry_detail', pk=entry.pk)
    
    return render(request, 'entries/entry_detail.html', {
        'entry': entry,
        'comments': comments,
        'comment_form': comment_form,
    })

@user_passes_test(is_admin)
def entry_create(request):
    if request.method == 'POST':
        form = JournalEntryForm(request.POST, request.FILES)
        if form.is_valid():
            entry = form.save(commit=False)
            entry.author = request.user
            entry.save()
            messages.success(request, 'Entry created successfully!')
            return redirect('entry_detail', pk=entry.pk)
    else:
        form = JournalEntryForm()
    return render(request, 'entries/entry_form.html', {'form': form, 'title': 'New Entry'})

@user_passes_test(is_admin)
def entry_edit(request, pk):
    entry = get_object_or_404(JournalEntry, pk=pk)
    if request.method == 'POST':
        form = JournalEntryForm(request.POST, request.FILES, instance=entry)
        if form.is_valid():
            form.save()
            messages.success(request, 'Entry updated successfully!')
            return redirect('entry_detail', pk=entry.pk)
    else:
        form = JournalEntryForm(instance=entry)
    return render(request, 'entries/entry_form.html', {'form': form, 'title': 'Edit Entry'})

@user_passes_test(is_admin)
def entry_delete(request, pk):
    entry = get_object_or_404(JournalEntry, pk=pk)
    if request.method == 'POST':
        entry.delete()
        messages.success(request, 'Entry deleted successfully!')
        return redirect('home')
    return render(request, 'entries/entry_confirm_delete.html', {'entry': entry})

@login_required
def add_comment(request, pk):
    entry = get_object_or_404(JournalEntry, pk=pk, is_published=True)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.entry = entry
            comment.author = request.user
            comment.save()
            messages.success(request, 'Your comment has been posted!')
    return redirect('entry_detail', pk=entry.pk)

def login_view(request):
    # Regular viewer login - anyone can login to comment
    if request.user.is_authenticated:
        return redirect('home')
    
    error_message = None
    
    if request.method == 'POST':
        username_or_email = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')
        
        user = None
        
        # Try username first
        if username_or_email:
            user = authenticate(request, username=username_or_email, password=password)
        
        # If that fails, try email
        if user is None and '@' in username_or_email:
            from django.contrib.auth import get_user_model
            User = get_user_model()
            try:
                user_obj = User.objects.get(email=username_or_email)
                user = authenticate(request, username=user_obj.username, password=password)
            except User.DoesNotExist:
                pass
        
        if user is not None and user.is_active:
            login(request, user)
            return redirect('home')
        else:
            error_message = 'Invalid email/username or password. Please try again.'
    
    from django.contrib.auth.forms import AuthenticationForm
    form = AuthenticationForm()
    if error_message:
        form.add_error(None, error_message)
    
    return render(request, 'entries/login.html', {'form': form})

def admin_login_view(request):
    # Admin-only login - redirects to Django admin
    if request.user.is_authenticated and request.user.is_staff:
        return redirect('/admin/')
    
    error_message = None
    
    if request.method == 'POST':
        username_or_email = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')
        
        user = None
        
        # Try username first
        if username_or_email:
            user = authenticate(request, username=username_or_email, password=password)
        
        # If that fails, try email
        if user is None and '@' in username_or_email:
            from django.contrib.auth import get_user_model
            User = get_user_model()
            try:
                user_obj = User.objects.get(email=username_or_email)
                user = authenticate(request, username=user_obj.username, password=password)
            except User.DoesNotExist:
                pass
        
        if user is not None and user.is_active and user.is_staff:
            login(request, user)
            return redirect('/admin/')
        else:
            error_message = 'Invalid credentials or you do not have admin access.'
    
    from django.contrib.auth.forms import AuthenticationForm
    form = AuthenticationForm()
    if error_message:
        form.add_error(None, error_message)
    
    return render(request, 'entries/admin_login.html', {'form': form})
