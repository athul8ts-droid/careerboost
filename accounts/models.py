from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings



class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('ADMIN', 'Admin'),
        ('RECRUITER', 'Recruiter'),
        ('USER', 'User'),
    )

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default='USER'
    )

    # Only recruiters need approval
    is_approved = models.BooleanField(default=False)

    # Recruiter-specific fields
    company_name = models.CharField(max_length=255, blank=True, null=True)
    company_email = models.EmailField(blank=True, null=True)
    company_website = models.URLField(blank=True, null=True)
    company_description = models.TextField(blank=True, null=True)

    def save(self, *args, **kwargs):
        # Auto-assign ADMIN role to superuser
        if self.is_superuser:
            self.role = 'ADMIN'
            self.is_approved = True

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.username} ({self.role})"




class RecruiterProfile(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    )

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    company_name = models.CharField(max_length=200)
    company_email = models.EmailField()
    phone_number = models.CharField(max_length=15)
    place = models.CharField(max_length=100)
    pincode = models.CharField(max_length=10)

    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='pending'
    )

    def __str__(self):
        return self.company_name




class ContactAdminMessage(models.Model):
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="admin_messages"
    )
    subject = models.CharField(max_length=200)
    message = models.TextField()

    admin_reply = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    replied_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"Message from {self.sender}"

