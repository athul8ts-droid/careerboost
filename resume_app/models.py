from django.db import models
from django.conf import settings


class Resume(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='resumes'
    )

    resume_file = models.FileField(upload_to='resumes/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    # Extracted resume text
    analyzed_text = models.TextField(blank=True, null=True)

    # ✅ ADD THIS
    job_description = models.TextField(blank=True, null=True)

    # ATS Score
    score = models.FloatField(blank=True, null=True)

    # Optional AI fields
    suggestions = models.TextField(blank=True, null=True)
    summary = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.user.username}'s Resume"