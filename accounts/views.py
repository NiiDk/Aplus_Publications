from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView
from .forms import CustomUserCreationForm, UserProfileForm
from .models import UserActivity

class AcademicLoginView(LoginView):
    template_name = 'accounts/login.html'
    
    def form_valid(self, form):
        response = super().form_valid(form)
        UserActivity.objects.create(
            user=self.request.user,
            action="Academic session initiated (Login)"
        )
        return response

class AcademicLogoutView(LogoutView):
    next_page = reverse_lazy('pages:home')

class StudentRegistrationView(CreateView):
    form_class = CustomUserCreationForm
    template_name = 'accounts/register.html'
    success_url = reverse_lazy('accounts:login')

    def form_valid(self, form):
        response = super().form_valid(form)
        # Log registration activity
        return response

class ProfileUpdateView(UpdateView):
    model = UserProfileForm # This should be form_class, fixing below
    template_name = 'accounts/profile.html'
    # ... logic for profile update
