"""
Main URL Configuration for CareerBoost Project
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import redirect
from django.contrib.auth import views as auth_views


# Job application related views
from job_app.views import apply_job, application_success


# ============================================================
# ROOT REDIRECT VIEW
# ============================================================
def root_redirect(request):
    if request.user.is_authenticated:
        return redirect('dashboard')   # user_app dashboard
    return redirect('accounts:login')  # login page


# ============================================================
# URL PATTERNS
# ============================================================
urlpatterns = [

    # Root
    path('', root_redirect, name='root'),

    # Admin
    path('admin/', admin.site.urls),

    # Authentication
    path('accounts/', include('accounts.urls')),

    # Logout (ONLY ONCE)
    path(
        'logout/',
        auth_views.LogoutView.as_view(next_page='accounts:login'),
        name='logout'
    ),

    # User app (dashboard, profile, etc.)
    path('', include('user_app.urls')),

    # Jobs
    path('jobs/', include('job_app.urls')),
    path('apply/<int:job_id>/', apply_job, name='apply_job'),
    path('success/', application_success, name='application_success'),

    # Resume
    path('resume/', include('resume_app.urls')),

    # Support
    path('support/', include('support.urls')),
]


# ============================================================
# MEDIA FILES (Development Only)
# ============================================================
if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )
