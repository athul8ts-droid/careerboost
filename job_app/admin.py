"""
Admin configuration for Job App

This file customizes how Job and JobApplication models
appear and behave in the Django admin panel.
"""

from django.contrib import admin
from .models import Job, JobApplication


# ============================================================
# JOB ADMIN CONFIGURATION
# ============================================================
@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    """
    Admin interface configuration for Job model.
    """

    # Fields displayed in the job list view
    list_display = (
        'title',
        'company',
        'location',
        'is_active',
        'created_at',
    )

    # Enable filtering by job status and company
    list_filter = (
        'is_active',
        'company',
        'location',
    )

    # Enable search functionality in admin
    search_fields = (
        'title',
        'company',
        'skills_required',
    )

    # Order jobs by latest created
    ordering = ('-created_at',)


# ============================================================
# JOB APPLICATION ADMIN CONFIGURATION
# ============================================================
@admin.register(JobApplication)
class JobApplicationAdmin(admin.ModelAdmin):
    """
    Admin interface configuration for JobApplication model.
    """

    # Fields displayed in application list view
    list_display = (
        'job',
        'user',
        'applied_on',   # ✅ FIXED HERE
    )

    # Enable filtering by job and user
    list_filter = (
        'job',
        'user',
    )

    # Enable search in admin panel
    search_fields = (
        'job__title',
        'user__username',
    )

    # Order applications by latest first
    ordering = ('-applied_on',)
