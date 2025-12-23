"""
Job App Views

Handles:
- Job creation (approved recruiters only)
- Job listing & details
- Job deletion (admin only)
- Job applications
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test

from .forms import JobForm
from .models import Job, JobApplication
from accounts.decorators import recruiter_required
from accounts.models import RecruiterProfile
from django.contrib import messages
from django.http import HttpResponseForbidden



# ============================================================
# ADD JOB (APPROVED RECRUITERS ONLY)
# ============================================================
@login_required
@recruiter_required
@login_required
@recruiter_required
def add_job(request):
    """
    Allows only approved recruiters to post jobs.
    """
    if request.method == "POST":
        form = JobForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.posted_by = request.user   
            job.save()
            messages.success(request, "Job posted successfully.")
            return redirect("dashboard")
    else:
        form = JobForm()

    return render(request, "add_job.html", {"form": form})



# ============================================================
# JOB LIST
# ============================================================
@login_required
def job_list(request):
    """
    Displays all jobs (latest first).
    """

    jobs = Job.objects.all().order_by('-created_at')
    return render(request, 'job_list.html', {'jobs': jobs})


# ============================================================
# JOB DETAIL
# ============================================================
@login_required
def job_detail(request, job_id):
    job = get_object_or_404(Job, id=job_id)

    has_applied = False

    if request.user.is_authenticated:
        has_applied = JobApplication.objects.filter(
            job=job,
            user=request.user
        ).exists()

    context = {
        "job": job,
        "has_applied": has_applied,
    }

    return render(request, "job_detail.html", context)


# ============================================================
# DELETE JOB (ADMIN ONLY)
# ============================================================
@login_required
def delete_job(request, job_id):

    # Only allow POST
    if request.method != "POST":
        return HttpResponseForbidden("Invalid request")

    job = get_object_or_404(Job, id=job_id)

    # Ownership check (MOST IMPORTANT)
    if job.posted_by != request.user:
        return HttpResponseForbidden("You are not allowed to delete this job")

    # Recruiter approval check
    if not request.user.is_approved:
        return HttpResponseForbidden("Recruiter not approved")

    job.delete()
    return redirect("accounts:recruiter_dashboard")


# ============================================================
# APPLY FOR JOB
# ============================================================
@login_required
def apply_job(request, job_id):
    """
    Allows users to apply for a job.
    """

    job = get_object_or_404(Job, id=job_id)

    if request.method == "POST":
        resume = request.FILES.get("resume")
        cover_letter = request.POST.get("cover_letter")

        JobApplication.objects.create(
            job=job,
            user=request.user,
            resume=resume,
            cover_letter=cover_letter
        )

        return redirect("job_app:application_success")

    return render(request, "apply_job.html", {"job": job})


# ============================================================
# APPLICATION SUCCESS
# ============================================================
def application_success(request):
    """
    Shows success message after applying.
    """

    return render(request, 'application_success.html')


@login_required
def view_applicants(request, job_id):

    # 🔒 Security: recruiter can see only THEIR job
    job = get_object_or_404(
        Job,
        id=job_id,
        posted_by=request.user
    )

    applications = job.applications.select_related('user')

    return render(request, 'view_applicants.html', {
        'job': job,
        'applications': applications
    })
