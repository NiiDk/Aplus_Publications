from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

class User(AbstractUser):
    class Roles(models.TextChoices):
        STUDENT = 'STUDENT', _('Student')
        TEACHER = 'TEACHER', _('Teacher')
        PARENT = 'PARENT', _('Parent')
        SCHOOL = 'SCHOOL', _('School Admin')

    role = models.CharField(
        max_length=20,
        choices=Roles.choices,
        default=Roles.STUDENT,
        help_text=_("The primary academic role of the user.")
    )
    email = models.EmailField(_('email address'), unique=True)

    # Use email as the primary identifier for a more modern academic login
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    def __str__(self):
        return f"{self.get_full_name()} ({self.role})"

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    institution = models.CharField(max_length=255, blank=True, help_text=_("Academic institution or school name."))
    bio = models.TextField(blank=True, help_text=_("Brief academic or professional biography."))
    phone_number = models.CharField(max_length=15, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Profile for {self.user.email}"

class UserActivity(models.Model):
    """
    Hook for tracking significant academic platform interactions.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='activities')
    action = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)
    metadata = models.JSONField(default=dict, blank=True)

    class Meta:
        verbose_name_plural = "User Activities"
        ordering = ['-timestamp']

    def __str__(self):
        return f"{self.user.email} - {self.action} at {self.timestamp}"
