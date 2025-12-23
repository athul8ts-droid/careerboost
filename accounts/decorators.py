from django.shortcuts import redirect
from django.contrib.auth.decorators import user_passes_test
from django.contrib import messages
from accounts.models import RecruiterProfile


def admin_required(view_func):
    return user_passes_test(
        lambda u: u.is_authenticated and u.is_superuser,
        login_url="accounts:login"
    )(view_func)


def recruiter_required(view_func):
    def wrapper(request, *args, **kwargs):

        if not request.user.is_authenticated:
            return redirect("accounts:login")

        try:
            RecruiterProfile.objects.get(user=request.user)
        except RecruiterProfile.DoesNotExist:
            messages.error(
                request,
                "Recruiter access required."
            )
            return redirect("accounts:dashboard")

        return view_func(request, *args, **kwargs)

    return wrapper


def recruiter_approved_required(view_func):
    def wrapper(request, *args, **kwargs):

        if not request.user.is_authenticated:
            return redirect("accounts:login")

        try:
            profile = RecruiterProfile.objects.get(user=request.user)
        except RecruiterProfile.DoesNotExist:
            messages.error(
                request,
                "Recruiter profile not found. Contact admin."
            )
            return redirect("accounts:dashboard")

        if profile.status != "approved":
            messages.warning(
                request,
                "Your recruiter account is pending approval."
            )
            return redirect("accounts:pending_approval")

        return view_func(request, *args, **kwargs)

    return wrapper
