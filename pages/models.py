from django.db import models
from django.urls import reverse

class Page(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    content = models.TextField()
    
    # SEO Fields
    meta_title = models.CharField(max_length=70, blank=True)
    meta_description = models.CharField(max_length=160, blank=True)
    
    last_updated = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['title']
        verbose_name = "Static Page"
        verbose_name_plural = "Static Pages"

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('pages:page_detail', kwargs={'slug': self.slug})

class FAQ(models.Model):
    question = models.CharField(max_length=255)
    answer = models.TextField()
    order = models.PositiveIntegerField(default=0)
    category = models.CharField(max_length=100, blank=True)

    class Meta:
        verbose_name = "FAQ"
        verbose_name_plural = "FAQs"
        ordering = ['order', 'question']

    def __str__(self):
        return self.question

class Enquiry(models.Model):
    """
    Captures formal contact inquiries from the platform.
    """
    name = models.CharField(max_length=255)
    email = models.EmailField()
    role = models.CharField(max_length=50, blank=True)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Academic Enquiry"
        verbose_name_plural = "Academic Enquiries"
        ordering = ['-created_at']

    def __str__(self):
        return f"Enquiry from {self.name} ({self.email})"
