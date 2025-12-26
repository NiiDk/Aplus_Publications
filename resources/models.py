from django.db import models
from django.utils.text import slugify
from django.conf import settings
from shop.models import Subject, AcademicLevel

class Resource(models.Model):
    class ResourceType(models.TextChoices):
        CURRICULUM = 'CURRICULUM', 'GES Curriculum'
        CALENDAR = 'CALENDAR', 'Academic Calendar'
        TIMETABLE = 'TIMETABLE', 'Examination Timetable'
        CIRCULAR = 'CIRCULAR', 'Official Circular'
        OTHER = 'OTHER', 'Other Resource'

    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    resource_type = models.CharField(
        max_length=20, 
        choices=ResourceType.choices, 
        default=ResourceType.CURRICULUM
    )
    file = models.FileField(upload_to='resources/pdfs/', help_text="Upload the academic PDF file.")
    description = models.TextField(blank=True)
    
    # Optional academic associations
    academic_level = models.ForeignKey(AcademicLevel, on_delete=models.SET_NULL, null=True, blank=True)
    subject = models.ForeignKey(Subject, on_delete=models.SET_NULL, null=True, blank=True)

    download_count = models.PositiveIntegerField(default=0, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Academic Resource"
        verbose_name_plural = "Academic Resources"

    def __str__(self):
        return f"{self.get_resource_type_display()} - {self.title}"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

class ResourceDownload(models.Model):
    """Tracks downloads of academic resources."""
    resource = models.ForeignKey(Resource, on_delete=models.CASCADE, related_name='downloads')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='resource_downloads')
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(null=True, blank=True)
    downloaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Download of {self.resource.title} at {self.downloaded_at}"
