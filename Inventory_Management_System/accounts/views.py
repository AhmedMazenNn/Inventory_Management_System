from django.contrib.auth import get_user_model
from django.contrib.auth.views import LoginView as AuthLoginView, LogoutView as AuthLogoutView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render, redirect
from django.views import View
from .forms import EmployeeRegistrationForm
from django.contrib import messages


User = get_user_model()

class LoginView(AuthLoginView):
    template_name = "accounts/login.html"

class LogoutView(AuthLogoutView):
    next_page = "login"

class DashboardView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, "accounts/dashboard.html")

class RegisterEmployeeView(LoginRequiredMixin, UserPassesTestMixin, View):
    template_name = "accounts/register_employee.html"

    def test_func(self):
        return self.request.user.role == "manager"

    def get(self, request):
        form = EmployeeRegistrationForm()
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        form = EmployeeRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.role = "employee"
            user.set_password(form.cleaned_data["password"])
            user.save()
            messages.success(request, f"Employee '{user.username}' registered successfully.")
            return redirect("dashboard")
        return render(request, self.template_name, {"form": form})
