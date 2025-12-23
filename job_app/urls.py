from django.urls import path
from . import views

app_name = "job_app"

urlpatterns = [

    # ------------------------
    # Job Management
    # ------------------------

    path("add/", views.add_job, name="add_job"),
    path("list/", views.job_list, name="job_list"),
    path("<int:job_id>/", views.job_detail, name="job_detail"),
    path("<int:job_id>/delete/", views.delete_job, name="delete_job"),

    # ------------------------
    # Job Application Flow
    # ------------------------

    path("apply/<int:job_id>/", views.apply_job, name="apply_job"),
    path("success/", views.application_success, name="application_success"),

    path(
    'job/<int:job_id>/applicants/',
    views.view_applicants,
    name='view_applicants'
),

    
]
