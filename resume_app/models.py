from django.db import models
from django.conf import settings


class Resume(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='resumes'
    )

    # File upload field
    resume_file = models.FileField(upload_to='resumes/')

    # Auto timestamp of upload
    uploaded_at = models.DateTimeField(auto_now_add=True)

    # Extracted resume text
    analyzed_text = models.TextField(blank=True, null=True)

    # AI Match Score / ATS Score
    score = models.IntegerField(blank=True, null=True)

    # AI suggestions for improvement
    suggestions = models.TextField(blank=True, null=True)

    # Optional: AI-generated summary of the resume
    summary = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.user.username}'s Resume"
