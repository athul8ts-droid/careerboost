from django.urls import path
from . import views
from .views import contact_admin

app_name = 'support'

urlpatterns = [
    path('contact/', views.contact_admin, name='contact_admin'),
    path('my-messages/', views.my_messages, name='my_messages'),

     # ADMIN
    path("admin/messages/", views.admin_message_list, name="admin_message_list"),
    path(
        "admin/messages/<int:message_id>/reply/",
        views.admin_reply,
        name="admin_reply"
    ),

]
