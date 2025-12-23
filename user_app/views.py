"""
Views for user authentication and dashboard access.
Uses CustomUser (AUTH_USER_MODEL) correctly.
"""

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import get_user_model
from job_app.models import Job, JobApplication
from django.conf import settings
from django.contrib import messages
from django.core.mail import send_mail
from .models import ContactMessage





# Get Custom User model
User = get_user_model()


# ============================================================
# HOME PAGE
# ============================================================
def home(request):
    """Landing page."""
    return render(request, 'home.html')


# ============================================================
# USER REGISTRATION
# ============================================================
def register(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")

        # ✅ STOP immediately if username exists
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect("register")

        # ✅ STOP immediately if email exists
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists")
            return redirect("register")

        # ✅ Create user only if all checks passed
        User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        messages.success(
            request,
            "Account created successfully. Please login."
        )
        return redirect("accounts:login")

    return render(request, "register.html")


# ============================================================
# USER LOGIN
# ============================================================
from django.contrib import messages


def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user:
            # 🔒 BLOCKED CHECK (BEFORE LOGIN)
            if hasattr(user, "profile") and user.profile.is_blocked:
                messages.error(
                    request,
                    "Your account has been blocked by admin. Please contact support.",
                    extra_tags="blocked"   # ⭐ IMPORTANT
                )
                return redirect("accounts:login")

            # ✅ ALLOW LOGIN
            login(request, user)

            # ✅ ADMIN FIRST
            if user.is_superuser:
                return redirect("accounts:pending_recruiters")

            # ✅ RECRUITER
            if user.role == "RECRUITER":
                return redirect("accounts:recruiter_dashboard")

            # ✅ NORMAL USER
            return redirect("dashboard")

        messages.error(request, "Invalid credentials")

    return render(request, "login.html")



# ============================================================
# USER LOGOUT
# ============================================================
def logout_view(request):
    """User logout."""
    logout(request)
    return redirect('login')


# ============================================================
# USER DASHBOARD
# ============================================================
@login_required(login_url='login')
def dashboard(request):

    # ❌ Recruiters cannot access user dashboard
    if request.user.role == "RECRUITER":
        return redirect("accounts:recruiter_dashboard")

    return render(request, "dashboard.html")






