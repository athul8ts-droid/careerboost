from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views

app_name = "accounts"

urlpatterns = [

    # ==================================================
    # AUTH
    # ==================================================
    path("login/", views.custom_login, name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("dashboard/", views.dashboard, name="dashboard"),

    # ==================================================
    # RECRUITER – REGISTRATION & DASHBOARD
    # ==================================================
    path(
        "recruiter/register/",
        views.recruiter_register,
        name="recruiter_register"
    ),
    path(
        "recruiter/dashboard/",
        views.recruiter_dashboard,
        name="recruiter_dashboard"
    ),
    path(
        "pending-approval/",
        views.pending_approval,
        name="pending_approval"
    ),

    # ==================================================
    # ADMIN – RECRUITER APPROVAL FLOW
    # ==================================================
    path(
        "recruiters/pending/",
        views.pending_recruiters,
        name="pending_recruiters"
    ),
    path(
        "recruiters/approve/<int:user_id>/",
        views.approve_recruiter,
        name="approve_recruiter"
    ),

    # ==================================================
    # ADMIN – APPROVED / BLOCK / UNBLOCK
    # ==================================================
    path(
        "recruiters/approved/",
        views.approved_recruiters,
        name="approved_recruiters"
    ),
    path(
        "recruiters/blocked/",
        views.blocked_recruiters,
        name="blocked_recruiters"
    ),
    path(
        "recruiters/block/<int:user_id>/",
        views.block_recruiter,
        name="block_recruiter"
    ),
    path(
        "recruiters/unblock/<int:user_id>/",
        views.unblock_recruiter,
        name="unblock_recruiter"
    ),
]
