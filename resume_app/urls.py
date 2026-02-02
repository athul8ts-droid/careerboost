from django.urls import path
from . import views

urlpatterns = [
    path("upload/", views.upload_resume, name="upload_resume"),
    path("result/<int:resume_id>/", views.resume_result, name="resume_result"),
]
