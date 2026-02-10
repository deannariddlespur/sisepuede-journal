"""
URL configuration for journal project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from entries import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('admin-login/', views.admin_login_view, name='admin_login'),
    path('', views.home, name='home'),
    path('entries/', views.entries_list, name='entries_list'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('entry/<int:pk>/', views.entry_detail, name='entry_detail'),
    path('entry/new/', views.entry_create, name='entry_create'),
    path('entry/<int:pk>/edit/', views.entry_edit, name='entry_edit'),
    path('entry/<int:pk>/toggle-publish/', views.entry_toggle_publish, name='entry_toggle_publish'),
    path('entry/<int:pk>/delete/', views.entry_delete, name='entry_delete'),
    path('entry/<int:pk>/comment/', views.add_comment, name='add_comment'),
    path('define-your-path/', views.path_events_calendar, name='path_events_calendar'),
    path('define-your-path/event/<int:pk>/', views.path_event_detail, name='path_event_detail'),
    path('define-your-path/new/', views.path_event_create, name='path_event_create'),
    path('define-your-path/<int:pk>/edit/', views.path_event_edit, name='path_event_edit'),
    path('define-your-path/<int:pk>/delete/', views.path_event_delete, name='path_event_delete'),
    path('deannas-diary/', views.diary_list, name='diary_list'),
    path('deannas-diary/<int:pk>/', views.diary_page_detail, name='diary_page_detail'),
    path('deannas-diary/new/', views.diary_page_create, name='diary_page_create'),
    path('deannas-diary/<int:pk>/edit/', views.diary_page_edit, name='diary_page_edit'),
    path('deannas-diary/<int:pk>/delete/', views.diary_page_delete, name='diary_page_delete'),
]

# Serve static and media files
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
else:
    # In production, static files should be served by web server (Nginx, etc.)
    # But we'll serve them via Django for Railway
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
