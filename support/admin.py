from django.contrib import admin
from .models import SupportMessage


@admin.register(SupportMessage)
class SupportMessageAdmin(admin.ModelAdmin):
    list_display = ("user", "subject", "created_at", "replied_at")
    search_fields = ("user__username", "subject")

