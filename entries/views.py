from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseForbidden
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.conf import settings
from django.db.models import Q
from .models import (
    JournalEntry, Comment, PathEvent, PathEventRegistration, PathEventComment,
    DiaryPage, DiaryComment, MediaItem, AboutPage,
)
from .forms import (
    JournalEntryForm, CommentForm, PathEventForm, PathEventCommentForm,
    DiaryPageForm, DiaryCommentForm, MediaItemForm, AboutPageForm,
)
from django.utils import timezone
from datetime import datetime, timedelta, timezone as dt_timezone
import calendar

DEBUG = settings.DEBUG

def is_admin(user):
    return user.is_authenticated and user.is_staff

def home(request):
    # Landing for guests; dedicated home page for logged-in users
    if request.user.is_authenticated:
        if request.user.is_staff:
            entries = JournalEntry.objects.all().order_by('-created_at')
        else:
            entries = JournalEntry.objects.filter(
                Q(is_published=True) | Q(author=request.user)
            ).order_by('-created_at')
        return render(request, 'entries/home.html', {'entries': entries})
    entries = JournalEntry.objects.filter(is_published=True)[:3]
    return render(request, 'entries/landing.html', {'entries': entries})


def entries_list(request):
    """Journal / stories list (logged-in users; staff see all, others see published + their own)."""
    if request.user.is_staff:
        entries = JournalEntry.objects.all().order_by('-created_at')
    else:
        entries = JournalEntry.objects.filter(
            Q(is_published=True) | Q(author=request.user)
        ).order_by('-created_at')
    return render(request, 'entries/entries_list.html', {'entries': entries})

def entry_detail(request, pk):
    # Staff see all; others see if published or they are the author
    entry = get_object_or_404(JournalEntry, pk=pk)
    if not entry.is_published and not request.user.is_staff and entry.author != request.user:
        return HttpResponseForbidden("This entry is not available.")
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

@login_required
def entry_create(request):
    """Any logged-in user can create an entry (define themselves)."""
    if request.method == 'POST':
        form = JournalEntryForm(request.POST, request.FILES)
        if form.is_valid():
            entry = form.save(commit=False)
            entry.author = request.user
            entry.save()
            messages.success(request, 'Entry created successfully!')
            return redirect('entry_detail', pk=entry.pk)
        else:
            messages.error(request, 'Please fix the errors below and try again.')
    else:
        form = JournalEntryForm()
    return render(request, 'entries/entry_form.html', {'form': form, 'title': 'New Entry'})

@login_required
def entry_edit(request, pk):
    """Author or staff can edit."""
    entry = get_object_or_404(JournalEntry, pk=pk)
    if not request.user.is_staff and entry.author != request.user:
        return HttpResponseForbidden("You can only edit your own entries.")
    if request.method == 'POST':
        form = JournalEntryForm(request.POST, request.FILES, instance=entry)
        if form.is_valid():
            form.save()
            messages.success(request, 'Entry updated successfully!')
            return redirect('entry_detail', pk=entry.pk)
    else:
        form = JournalEntryForm(instance=entry)
    return render(request, 'entries/entry_form.html', {'form': form, 'title': 'Edit Entry'})

@login_required
def entry_delete(request, pk):
    """Author or staff can delete."""
    entry = get_object_or_404(JournalEntry, pk=pk)
    if not request.user.is_staff and entry.author != request.user:
        return HttpResponseForbidden("You can only delete your own entries.")
    if request.method == 'POST':
        entry.delete()
        messages.success(request, 'Entry deleted successfully!')
        return redirect('home')
    return render(request, 'entries/entry_confirm_delete.html', {'entry': entry})


@user_passes_test(is_admin)
def entry_toggle_publish(request, pk):
    """Toggle is_published for an entry. Staff only. Redirects back to entry detail."""
    entry = get_object_or_404(JournalEntry, pk=pk)
    entry.is_published = not entry.is_published
    entry.save()
    if entry.is_published:
        messages.success(request, 'Entry is now published.')
    else:
        messages.success(request, 'Entry is now a draft (hidden from visitors).')
    return redirect('entry_detail', pk=entry.pk)

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

def logout_view(request):
    """Log out and redirect to home. Accepts GET so nav link works."""
    logout(request)
    return redirect('home')

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
            # Redirect staff to home, regular users to home
            return redirect('home')
        else:
            error_message = 'Invalid email/username or password. Please try again.'
            # Debug info (remove in production)
            if DEBUG:
                print(f"Login attempt failed for: {username_or_email}")
    
    form = AuthenticationForm()
    return render(request, 'entries/login.html', {'form': form, 'error_message': error_message})

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
    
    form = AuthenticationForm()
    return render(request, 'entries/admin_login.html', {'form': form, 'error_message': error_message})

# Define Your Path - Events Calendar Views
def path_events_calendar(request):
    """Calendar view showing all upcoming path events"""
    now = timezone.now()
    
    # Handle search query
    search_query = request.GET.get('search', '').strip()
    search_date = request.GET.get('search_date', '').strip()
    
    # Base queryset - show all events for staff, only published for others
    if request.user.is_staff:
        base_events = PathEvent.objects.all()
    else:
        base_events = PathEvent.objects.filter(is_published=True)
    
    # Apply search filters
    if search_query:
        base_events = base_events.filter(
            Q(title__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(location__icontains=search_query) |
            Q(event_type__icontains=search_query)
        )
    
    if search_date:
        try:
            # Try to parse date (format: YYYY-MM-DD)
            search_date_obj = datetime.strptime(search_date, '%Y-%m-%d').date()
            search_datetime_start = timezone.make_aware(datetime.combine(search_date_obj, datetime.min.time()))
            search_datetime_end = timezone.make_aware(datetime.combine(search_date_obj, datetime.max.time()))
            base_events = base_events.filter(
                event_date__gte=search_datetime_start,
                event_date__lte=search_datetime_end
            )
        except (ValueError, TypeError):
            pass  # Invalid date format, ignore
    
    upcoming_events = base_events.filter(event_date__gte=now).order_by('event_date')
    past_events = base_events.filter(event_date__lt=now).order_by('-event_date')[:5]
    
    # Get current month/year for calendar
    year = request.GET.get('year', now.year)
    month = request.GET.get('month', now.month)
    try:
        year = int(year)
        month = int(month)
    except (ValueError, TypeError):
        year = now.year
        month = now.month
    
    # Get events for this month - use timezone-aware datetime
    month_start = timezone.make_aware(datetime(year, month, 1))
    if month == 12:
        month_end = timezone.make_aware(datetime(year + 1, 1, 1))
    else:
        month_end = timezone.make_aware(datetime(year, month + 1, 1))
    
    # Apply search filters to month events too
    month_events = base_events.filter(
        event_date__gte=month_start,
        event_date__lt=month_end
    )
    
    # Create calendar
    cal = calendar.monthcalendar(year, month)
    events_by_date = {}
    for event in month_events:
        # Get the day from the event date (in the same timezone)
        event_day_local = event.event_date.astimezone(timezone.get_current_timezone()).day
        # Also check if it's the same month/year to avoid cross-month issues
        event_month = event.event_date.astimezone(timezone.get_current_timezone()).month
        event_year = event.event_date.astimezone(timezone.get_current_timezone()).year
        
        if event_month == month and event_year == year:
            if event_day_local not in events_by_date:
                events_by_date[event_day_local] = []
            events_by_date[event_day_local].append(event)
    
    # Navigation
    prev_month = month - 1
    prev_year = year
    if prev_month == 0:
        prev_month = 12
        prev_year -= 1
    
    next_month = month + 1
    next_year = year
    if next_month == 13:
        next_month = 1
        next_year += 1
    
    month_name = calendar.month_name[month]
    
    # Create a calendar grid with events for easier template rendering
    calendar_with_events = []
    for week in cal:
        week_data = []
        for day in week:
            day_data = {
                'day': day,
                'events': events_by_date.get(day, []) if day != 0 else []
            }
            week_data.append(day_data)
        calendar_with_events.append(week_data)
    
    return render(request, 'entries/path_events_calendar.html', {
        'upcoming_events': upcoming_events,
        'past_events': past_events,
        'calendar': cal,
        'calendar_with_events': calendar_with_events,
        'events_by_date': events_by_date,
        'year': year,
        'month': month,
        'month_name': month_name,
        'prev_month': prev_month,
        'prev_year': prev_year,
        'next_month': next_month,
        'next_year': next_year,
        'now': now,
        'search_query': search_query,
        'search_date': search_date,
    })

def path_event_detail(request, pk):
    """View individual path event. Logged-in users can join, leave, and comment on published events."""
    if request.user.is_staff:
        event = get_object_or_404(PathEvent, pk=pk)
    else:
        event = get_object_or_404(PathEvent, pk=pk, is_published=True)

    comments = event.event_comments.all()
    comment_form = PathEventCommentForm() if request.user.is_authenticated else None
    if request.method == 'POST' and request.user.is_authenticated:
        if 'comment' in request.POST:
            form = PathEventCommentForm(request.POST)
            if form.is_valid():
                c = form.save(commit=False)
                c.event = event
                c.author = request.user
                c.save()
                messages.success(request, 'Comment posted.')
                return redirect('path_event_detail', pk=event.pk)
            comment_form = form

    registrations = event.registrations.all()
    participant_count = registrations.count()
    user_has_joined = request.user.is_authenticated and event.registrations.filter(user=request.user).exists()
    comment_count = comments.count()

    return render(request, 'entries/path_event_detail.html', {
        'event': event,
        'comments': comments,
        'comment_count': comment_count,
        'comment_form': comment_form,
        'registrations': registrations,
        'participant_count': participant_count,
        'user_has_joined': user_has_joined,
    })

@login_required
def path_event_join(request, pk):
    """Join a published event. Respects max_participants. POST only."""
    if request.method != 'POST':
        return redirect('path_event_detail', pk=pk)
    if request.user.is_staff:
        event = get_object_or_404(PathEvent, pk=pk)
    else:
        event = get_object_or_404(PathEvent, pk=pk, is_published=True)
    if event.registrations.filter(user=request.user).exists():
        messages.info(request, "You're already joined.")
        return redirect('path_event_detail', pk=event.pk)
    if event.max_participants and event.registrations.count() >= event.max_participants:
        messages.warning(request, "This event is full.")
        return redirect('path_event_detail', pk=event.pk)
    PathEventRegistration.objects.create(event=event, user=request.user)
    messages.success(request, "You're in! See you there.")
    return redirect('path_event_detail', pk=event.pk)


@login_required
def path_event_leave(request, pk):
    """Leave an event. POST only."""
    if request.method != 'POST':
        return redirect('path_event_detail', pk=pk)
    if request.user.is_staff:
        event = get_object_or_404(PathEvent, pk=pk)
    else:
        event = get_object_or_404(PathEvent, pk=pk, is_published=True)
    event.registrations.filter(user=request.user).delete()
    messages.success(request, "You've left this event.")
    return redirect('path_event_detail', pk=event.pk)


@user_passes_test(is_admin)
def path_event_create(request):
    """Create a new path event - admin only"""
    if request.method == 'POST':
        form = PathEventForm(request.POST, request.FILES)
        if form.is_valid():
            event = form.save(commit=False)
            event.created_by = request.user
            event.save()
            messages.success(request, 'Path event created successfully!')
            return redirect('path_event_detail', pk=event.pk)
    else:
        form = PathEventForm()
        # Pre-fill date if provided in query string
        date_str = request.GET.get('date', '').strip()
        if date_str:
            try:
                # Parse date (format: YYYY-MM-DD)
                date_obj = datetime.strptime(date_str, '%Y-%m-%d').date()
                # Set default time to noon (12:00 PM)
                default_time = datetime.min.time().replace(hour=12, minute=0)
                default_datetime = datetime.combine(date_obj, default_time)
                # Make timezone-aware
                default_datetime = timezone.make_aware(default_datetime)
                # Format for datetime-local input (YYYY-MM-DDTHH:MM)
                form.fields['event_date'].initial = default_datetime.strftime('%Y-%m-%dT%H:%M')
            except (ValueError, TypeError):
                pass  # Invalid date format, ignore
    return render(request, 'entries/path_event_form.html', {'form': form, 'title': 'Define a New Path'})

@user_passes_test(is_admin)
def path_event_edit(request, pk):
    """Edit a path event - admin only"""
    event = get_object_or_404(PathEvent, pk=pk)
    if request.method == 'POST':
        form = PathEventForm(request.POST, request.FILES, instance=event)
        if form.is_valid():
            form.save()
            messages.success(request, 'Path event updated successfully!')
            return redirect('path_event_detail', pk=event.pk)
    else:
        form = PathEventForm(instance=event)
    return render(request, 'entries/path_event_form.html', {'form': form, 'title': 'Edit Path Event'})

@user_passes_test(is_admin)
def path_event_delete(request, pk):
    """Delete a path event - admin only"""
    event = get_object_or_404(PathEvent, pk=pk)
    if request.method == 'POST':
        event.delete()
        messages.success(request, 'Path event deleted successfully!')
        return redirect('path_events_calendar')
    return render(request, 'entries/path_event_confirm_delete.html', {'event': event})

# DeAnna's Diary Views
def is_deanna(user):
    """Check if user is DeAnna (staff)"""
    return user.is_authenticated and user.is_staff

def diary_list(request):
    """List all diary pages - only DeAnna can see drafts, public pages visible to all"""
    if not request.user.is_authenticated:
        # Show only public pages to non-authenticated users
        pages = DiaryPage.objects.filter(status='public').order_by('-created_at')
    elif request.user.is_staff:
        # DeAnna/staff can see all pages
        pages = DiaryPage.objects.all().order_by('-created_at')
    else:
        # Regular users see only public pages
        pages = DiaryPage.objects.filter(status='public').order_by('-created_at')
    
    return render(request, 'entries/diary_list.html', {'pages': pages})

def diary_page_detail(request, pk):
    """View individual diary page. Public pages show comments; any logged-in user can comment."""
    page = get_object_or_404(DiaryPage, pk=pk)

    if page.status == 'draft' and not request.user.is_staff:
        return HttpResponseForbidden("This page is private.")

    comments = page.diary_comments.all()
    comment_form = None
    if request.user.is_authenticated and (page.status == 'public' or request.user.is_staff):
        comment_form = DiaryCommentForm()

    if request.method == 'POST' and request.user.is_authenticated and (page.status == 'public' or request.user.is_staff):
        form = DiaryCommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.page = page
            comment.author = request.user
            comment.save()
            messages.success(request, 'Your comment has been posted!')
            return redirect('diary_page_detail', pk=page.pk)
        comment_form = form  # show errors

    if page.status == 'public' or request.user.is_staff:
        return render(request, 'entries/diary_page_detail.html', {
            'page': page,
            'comments': comments,
            'comment_count': comments.count(),
            'comment_form': comment_form,
        })
    return HttpResponseForbidden("You don't have permission to view this page.")

@user_passes_test(is_deanna)
def diary_page_create(request):
    """Create a new diary page - DeAnna only"""
    if request.method == 'POST':
        form = DiaryPageForm(request.POST, request.FILES)
        if form.is_valid():
            page = form.save(commit=False)
            page.author = request.user
            page.save()
            messages.success(request, 'Diary page created successfully!')
            return redirect('diary_page_detail', pk=page.pk)
    else:
        form = DiaryPageForm()
    return render(request, 'entries/diary_page_form.html', {'form': form, 'title': 'New Diary Page'})

@user_passes_test(is_deanna)
def diary_page_edit(request, pk):
    """Edit a diary page - DeAnna only"""
    page = get_object_or_404(DiaryPage, pk=pk)
    if request.method == 'POST':
        form = DiaryPageForm(request.POST, request.FILES, instance=page)
        if form.is_valid():
            form.save()
            messages.success(request, 'Diary page updated successfully!')
            return redirect('diary_page_detail', pk=page.pk)
    else:
        form = DiaryPageForm(instance=page)
    return render(request, 'entries/diary_page_form.html', {'form': form, 'title': 'Edit Diary Page', 'page': page})

@user_passes_test(is_deanna)
def diary_page_delete(request, pk):
    """Delete a diary page - DeAnna only"""
    page = get_object_or_404(DiaryPage, pk=pk)
    if request.method == 'POST':
        page.delete()
        messages.success(request, 'Diary page deleted successfully!')
        return redirect('diary_list')
    return render(request, 'entries/diary_page_confirm_delete.html', {'page': page})


# ---- Media Library (staff only) ----

@user_passes_test(is_admin)
def media_library(request):
    """List all media items and show upload form."""
    items = MediaItem.objects.all()
    if request.method == 'POST':
        form = MediaItemForm(request.POST, request.FILES)
        if form.is_valid():
            item = form.save(commit=False)
            item.uploaded_by = request.user
            item.save()
            messages.success(request, 'File uploaded.')
            return redirect('media_library')
        return render(request, 'entries/media_library.html', {'items': items, 'form': form})
    form = MediaItemForm()
    return render(request, 'entries/media_library.html', {'items': items, 'form': form})


@user_passes_test(is_admin)
def media_delete(request, pk):
    """Delete a media item."""
    item = get_object_or_404(MediaItem, pk=pk)
    if request.method == 'POST':
        item.delete()
        messages.success(request, 'Media item deleted.')
        return redirect('media_library')
    return redirect('media_library')
