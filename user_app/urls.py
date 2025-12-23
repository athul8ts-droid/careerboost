from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),

    # 🔐 Authentication
    path('register/', views.register, name='register'),

    # 🧭 Dashboard
    path('dashboard/', views.dashboard, name='dashboard'),
    

]
