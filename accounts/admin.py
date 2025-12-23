from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import CustomUser
from .models import RecruiterProfile

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'role', 'is_approved', 'is_staff')
    list_filter = ('role', 'is_approved')
    search_fields = ('username', 'email')

class RecruiterProfileAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "is_approved")
    list_filter = ("is_approved",)
    search_fields = ("user__username", "user__email")






