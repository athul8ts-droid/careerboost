"""
Database models for Job App

Defines core job-related entities:
- Job: Job postings created by users
- JobApplication: Applications submitted for jobs
"""

from django.db import models
from django.conf import settings


# ============================================================
# JOB MODEL
# ============================================================
class Job(models.Model):
    """
    Represents a job posting created by a recruiter.
    """

    title = models.CharField(max_length=200)
    company = models.CharField(max_length=200)
    location = models.CharField(max_length=200)
    description = models.TextField()

    skills_required = models.TextField(
        help_text="Comma separated skills (python, sql, django)"
    )

    posted_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="posted_jobs"
    )

    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


# ============================================================
# JOB APPLICATION MODEL
# ============================================================
class JobApplication(models.Model):
    """
    Stores job applications submitted by users.
    """

    job = models.ForeignKey(
        Job,
        on_delete=models.CASCADE,
        related_name="applications"
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="job_applications"
    )

    resume = models.FileField(upload_to='applications/')
    cover_letter = models.TextField(blank=True, null=True)
    applied_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} applied for {self.job.title}"
