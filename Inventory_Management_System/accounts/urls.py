from django.urls import path
from django.shortcuts import redirect
from .views import LoginView, LogoutView, DashboardView, RegisterEmployeeView

urlpatterns = [
    path("", lambda request: redirect("login")), 
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("dashboard/", DashboardView.as_view(), name="dashboard"),
    path("register-employee/", RegisterEmployeeView.as_view(), name="register_employee"),
]
