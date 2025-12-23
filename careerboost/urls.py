"""
Main URL Configuration for CareerBoost Project

This file acts as the central routing hub of the application.
It connects different apps (user, job, resume) to the main project
and defines global routes like admin, login, logout, and root redirect.
"""

from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import redirect

# Job application related views
from job_app.views import apply_job, application_success


# ============================================================
# ROOT REDIRECT VIEW
# ============================================================
# Redirects users based on authentication status:
# - Authenticated users → Dashboard
# - Unauthenticated users → Login page
def root_redirect(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    return redirect('accounts:login')


# ============================================================
# URL PATTERNS
# ============================================================
urlpatterns = [

    # ------------------------
    # Root URL
    # ------------------------
    path('', root_redirect, name='root'),

    # ------------------------
    # Django Admin Panel
    # ------------------------
    path('admin/', admin.site.urls),

    # ------------------------
    # User Authentication & Dashboard
    # (login, register, dashboard, profile, etc.)
    # ------------------------
    path('', include('user_app.urls')),

    # ------------------------
    # Logout
    # ------------------------
    # Uses Django's built-in LogoutView
    path(
        'logout/',
        auth_views.LogoutView.as_view(next_page='login'),
        name='logout'
    ),

    # ------------------------
    # Job Management
    # ------------------------
    # Job listing, job details, add/delete jobs
    path('jobs/', include('job_app.urls')),

    # Job application flow
    path('apply/<int:job_id>/', apply_job, name='apply_job'),
    path('success/', application_success, name='application_success'),

    # ------------------------
    # Resume Management
    # ------------------------
    path('resume/', include('resume_app.urls')),
    path('accounts/', include('accounts.urls')), 
    path("logout/", auth_views.LogoutView.as_view(), name="logout"), 
    path("support/", include("support.urls")),
]


# ============================================================
# MEDIA FILES (Development Only)
# ============================================================
# Enables serving uploaded media files (resumes, PDFs, etc.)
# during development mode.
if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )
