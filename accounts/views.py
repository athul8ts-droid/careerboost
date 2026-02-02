from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.contrib.auth import get_user_model, authenticate, login

from job_app.models import Job
from .models import RecruiterProfile

User = get_user_model()


# =========================
# ADMIN CHECK
# =========================
def is_admin(user):
    return user.is_superuser or getattr(user, "role", None) == "ADMIN"


# =========================
# ADMIN – PENDING RECRUITERS
# =========================
@login_required
@user_passes_test(is_admin)
def pending_recruiters(request):
    recruiters = (
        RecruiterProfile.objects
        .filter(status="pending")
        .select_related("user")
    )
    return render(
        request,
        "accounts/pending_recruiters.html",
        {"recruiters": recruiters}
    )


# =========================
# ADMIN – APPROVE RECRUITER
# =========================
@login_required
@user_passes_test(is_admin)
def approve_recruiter(request, user_id):
    user = get_object_or_404(User, id=user_id, role="RECRUITER")
    profile = get_object_or_404(RecruiterProfile, user=user)

    # 🔥 SINGLE SOURCE OF TRUTH
    user.is_active = True
    user.is_approved = True
    user.save()

    profile.status = "approved"
    profile.save()

    messages.success(request, "Recruiter approved successfully.")
    return redirect("accounts:pending_recruiters")


# =========================
# ADMIN – BLOCK RECRUITER
# =========================
@login_required
@user_passes_test(is_admin)
def block_recruiter(request, user_id):
    profile = get_object_or_404(
        RecruiterProfile,
        user__id=user_id
    )

    profile.status = "blocked"
    profile.save()

    profile.user.is_active = False
    profile.user.is_approved = False
    profile.user.save()

    messages.success(request, "Recruiter blocked successfully.")
    return redirect("accounts:approved_recruiters")


# =========================
# ADMIN – UNBLOCK RECRUITER
# =========================
@login_required
@user_passes_test(is_admin)
def unblock_recruiter(request, user_id):
    profile = get_object_or_404(
        RecruiterProfile,
        user__id=user_id
    )

    profile.status = "approved"
    profile.save()

    profile.user.is_active = True
    profile.user.is_approved = True
    profile.user.save()

    messages.success(request, "Recruiter unblocked successfully.")
    return redirect("accounts:blocked_recruiters")


# =========================
# ADMIN – APPROVED RECRUITERS
# =========================
@login_required
@user_passes_test(is_admin)
def approved_recruiters(request):
    recruiters = (
        RecruiterProfile.objects
        .filter(status="approved")
        .select_related("user")
    )
    return render(
        request,
        "accounts/approved_recruiters.html",
        {"recruiters": recruiters}
    )


# =========================
# ADMIN – BLOCKED RECRUITERS
# =========================
@login_required
@user_passes_test(is_admin)
def blocked_recruiters(request):
    recruiters = (
        RecruiterProfile.objects
        .filter(status="blocked")
        .select_related("user")
    )
    return render(
        request,
        "accounts/blocked_recruiters.html",
        {"recruiters": recruiters}
    )


# =========================
# RECRUITER REGISTER
# =========================
def recruiter_register(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return redirect("accounts:recruiter_register")

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            role="RECRUITER",
            is_active=True,
            is_approved=False,   # 🔥 DEFAULT
        )

        RecruiterProfile.objects.create(
            user=user,
            company_name=request.POST.get("company_name"),
            company_email=request.POST.get("company_email"),
            phone_number=request.POST.get("phone_number"),
            place=request.POST.get("place"),
            pincode=request.POST.get("pincode"),
            status="pending",
        )

        messages.success(
            request,
            "Registration successful. Await admin approval."
        )
        return redirect("accounts:login")

    return render(request, "accounts/recruiter_register.html")


# =========================
# MAIN DASHBOARD ROUTER
# =========================
@login_required
def dashboard(request):
    user = request.user

    if is_admin(user):
        return redirect("accounts:pending_recruiters")

    if user.role == "RECRUITER":
        if not user.is_approved:
            return redirect("accounts:pending_approval")

        return redirect("accounts:recruiter_dashboard")

    return render(request, "dashboard.html")


# =========================
# RECRUITER DASHBOARD
# =========================
@login_required
def recruiter_dashboard(request):
    user = request.user
    profile = get_object_or_404(RecruiterProfile, user=user)

    if not user.is_approved or profile.status != "approved":
        return redirect("accounts:pending_approval")

    jobs = Job.objects.filter(
        posted_by=user
    ).order_by("-created_at")

    return render(
        request,
        "accounts/recruiter_dashboard.html",
        {"profile": profile, "jobs": jobs}
    )


# =========================
# RECRUITER – PENDING / BLOCKED PAGE
# =========================
@login_required
def pending_approval(request):
    return render(request, "accounts/pending_approval.html")


# =========================
# LOGIN
# =========================
def custom_login(request):
    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "").strip()

        try:
            user_obj = User.objects.get(username=username)
        except User.DoesNotExist:
            messages.error(request, "Invalid username or password.")
            return redirect("accounts:login")

        if not user_obj.is_active:
            messages.error(
                request,
                "Your account is blocked by admin. Please contact support."
            )
            return redirect("accounts:login")

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user:
            login(request, user)
            return redirect("accounts:dashboard")

        messages.error(request, "Invalid username or password.")
        return redirect("accounts:login")

    return render(request, "accounts/login.html")
