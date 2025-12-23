"""
URL configuration for Resume App

Handles resume upload and analysis result views.
"""

from django.urls import path
from . import views


# ============================================================
# RESUME APP URL PATTERNS
# ============================================================
urlpatterns = [
    # Upload resume for analysis
    path('upload/', views.upload_resume, name='upload_resume'),

    # View analyzed resume result
    path(
        'result/<int:resume_id>/',
        views.resume_result,
        name='resume_result'
    ),
]
