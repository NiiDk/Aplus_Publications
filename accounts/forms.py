from django import forms
from django.conf import settings
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User, Profile

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('email', 'username', 'first_name', 'last_name', 'role')

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('email', 'username', 'first_name', 'last_name', 'role')

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('profile_picture', 'institution', 'phone_number', 'bio')
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Academic background...', 'class': 'italic'}),
        }
