from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from .models import JournalEntry
from .forms import JournalEntryForm

def home(request):
    if request.user.is_authenticated:
        entries = JournalEntry.objects.filter(author=request.user)
        return render(request, 'entries/home.html', {'entries': entries})
    else:
        return redirect('login')

@login_required
def entry_detail(request, pk):
    entry = get_object_or_404(JournalEntry, pk=pk, author=request.user)
    return render(request, 'entries/entry_detail.html', {'entry': entry})

@login_required
def entry_create(request):
    if request.method == 'POST':
        form = JournalEntryForm(request.POST, request.FILES)
        if form.is_valid():
            entry = form.save(commit=False)
            entry.author = request.user
            entry.save()
            return redirect('entry_detail', pk=entry.pk)
    else:
        form = JournalEntryForm()
    return render(request, 'entries/entry_form.html', {'form': form, 'title': 'New Entry'})

@login_required
def entry_edit(request, pk):
    entry = get_object_or_404(JournalEntry, pk=pk, author=request.user)
    if request.method == 'POST':
        form = JournalEntryForm(request.POST, request.FILES, instance=entry)
        if form.is_valid():
            form.save()
            return redirect('entry_detail', pk=entry.pk)
    else:
        form = JournalEntryForm(instance=entry)
    return render(request, 'entries/entry_form.html', {'form': form, 'title': 'Edit Entry'})

@login_required
def entry_delete(request, pk):
    entry = get_object_or_404(JournalEntry, pk=pk, author=request.user)
    if request.method == 'POST':
        entry.delete()
        return redirect('home')
    return render(request, 'entries/entry_confirm_delete.html', {'entry': entry})

def login_view(request):
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
