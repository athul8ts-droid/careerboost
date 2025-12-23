from django.contrib import admin

# Register your models here.
from .models import Resume



@admin.register(Resume)
class ResumeAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "uploaded_at")
    search_fields = ("user__username",)
