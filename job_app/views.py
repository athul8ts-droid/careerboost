"""
Job App Views

Handles:
- Job creation (approved recruiters only)
- Job listing & details
- Job deletion (job owner or admin)
- Job applications
- View applicants (recruiter only)
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseForbidden
from django.db.models import Q

from .forms import JobForm
from .models import Job, JobApplication
from accounts.decorators import recruiter_required
from accounts.models import RecruiterProfile


# ============================================================
# ADD JOB (APPROVED RECRUITERS ONLY)
# ============================================================
@login_required
@recruiter_required
def add_job(request):
    """
    Allows only approved recruiters to post jobs.
    """

    recruiter_profile = getattr(request.user, "recruiterprofile", None)
    if not recruiter_profile or recruiter_profile.status != "approved":
        messages.error(request, "Your recruiter account is not approved yet.")
        return redirect("accounts:recruiter_dashboard")

    if request.method == "POST":
        form = JobForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.posted_by = request.user
            job.save()
            messages.success(request, "Job posted successfully.")
            return redirect("accounts:recruiter_dashboard")
    else:
        form = JobForm()

    return render(request, "jobs/add_job.html", {"form": form})


# ============================================================
# JOB LIST (USERS)
# ============================================================
@login_required
def job_list(request):
    query = request.GET.get("q")

    jobs = Job.objects.filter(
        posted_by__recruiterprofile__status="approved",
        is_active=True
    )

    if query:
        jobs = jobs.filter(
            Q(title__icontains=query) |
            Q(company__icontains=query) |
            Q(location__icontains=query)
        )

    return render(request, "jobs/job_list.html", {
        "jobs": jobs,
        "query": query
    })


# ============================================================
# JOB DETAIL
# ============================================================
@login_required
def job_detail(request, job_id):
    job = get_object_or_404(Job, id=job_id)

    recruiter_profile = getattr(job.posted_by, "recruiterprofile", None)
    if not recruiter_profile or recruiter_profile.status != "approved":
        messages.error(request, "This job is no longer available.")
        return redirect("job_app:job_list")

    has_applied = JobApplication.objects.filter(
        job=job,
        user=request.user
    ).exists()

    return render(request, "jobs/job_detail.html", {
        "job": job,
        "has_applied": has_applied
    })


# ============================================================
# DELETE JOB (OWNER OR ADMIN)
# ============================================================
@login_required
def delete_job(request, job_id):

    if request.method != "POST":
        return HttpResponseForbidden("Invalid request")

    job = get_object_or_404(Job, id=job_id)

    # Admin can delete any job
    if request.user.is_superuser:
        job.delete()
        messages.success(request, "Job deleted successfully.")
        return redirect("admin_dashboard")

    # Recruiter can delete ONLY their job
    if job.posted_by != request.user:
        return HttpResponseForbidden("You are not allowed to delete this job.")

    recruiter_profile = getattr(request.user, "recruiterprofile", None)
    if not recruiter_profile or recruiter_profile.status != "approved":
        return HttpResponseForbidden("Recruiter not approved.")

    job.delete()
    messages.success(request, "Job deleted successfully.")
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

    recruiter_profile = getattr(job.posted_by, "recruiterprofile", None)
    if not recruiter_profile or recruiter_profile.status != "approved":
        messages.error(request, "Applications for this job are disabled.")
        return redirect("job_app:job_list")

    if JobApplication.objects.filter(job=job, user=request.user).exists():
        messages.warning(request, "You have already applied for this job.")
        return redirect("job_app:job_detail", job_id=job.id)

    if request.method == "POST":
        resume = request.FILES.get("resume")
        cover_letter = request.POST.get("cover_letter")

        JobApplication.objects.create(
            job=job,
            user=request.user,
            resume=resume,
            cover_letter=cover_letter
        )

        messages.success(request, "Application submitted successfully!")
        return redirect("job_app:application_success")

    return render(request, "jobs/apply_job.html", {"job": job})


# ============================================================
# APPLICATION SUCCESS
# ============================================================
@login_required
def application_success(request):
    return render(request, "jobs/application_success.html")


# ============================================================
# VIEW APPLICANTS (RECRUITER)
# ============================================================
@login_required
@recruiter_required
def view_applicants(request, job_id):

    job = get_object_or_404(
        Job,
        id=job_id,
        posted_by=request.user
    )

    applications = job.applications.select_related("user")

    return render(request, "jobs/view_applicants.html", {
        "job": job,
        "applications": applications
    })
