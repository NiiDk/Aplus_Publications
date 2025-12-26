from django.db import models
from django.utils.text import slugify
from django.urls import reverse

class AcademicLevel(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=120, unique=True)
    order = models.PositiveIntegerField(default=0)
    description = models.TextField(blank=True)

    class Meta:
        verbose_name = "Academic Level"
        verbose_name_plural = "Academic Levels"
        ordering = ['order', 'name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

class Subject(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=120, unique=True)
    academic_levels = models.ManyToManyField(AcademicLevel, related_name='subjects')
    is_core = models.BooleanField(default=True)
    description = models.TextField(blank=True)

    class Meta:
        verbose_name = "Subject"
        verbose_name_plural = "Subjects"
        ordering = ['name']
        unique_together = ('name', 'is_core')

    def __str__(self):
        type_str = "Core" if self.is_core else "Elective"
        return f"{self.name} ({type_str})"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.name}-{ 'core' if self.is_core else 'elective' }")
        super().save(*args, **kwargs)

class Textbook(models.Model):
    class Curriculum(models.TextChoices):
        NACCA = 'NACCA', 'NaCCA'
        WAEC = 'WAEC', 'WAEC'

    class BookType(models.TextChoices):
        TEXTBOOK = 'TEXTBOOK', 'Textbook'
        WORKBOOK = 'WORKBOOK', 'Workbook'
        PAST_QUESTIONS = 'PAST_QUESTIONS', 'Past Questions'

    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    subject = models.ForeignKey(Subject, on_delete=models.PROTECT, related_name='textbooks')
    academic_level = models.ForeignKey(AcademicLevel, on_delete=models.PROTECT, related_name='textbooks')
    book_type = models.CharField(max_length=20, choices=BookType.choices, default=BookType.TEXTBOOK)
    curriculum = models.CharField(max_length=10, choices=Curriculum.choices, default=Curriculum.NACCA)
    isbn = models.CharField("ISBN", max_length=20, unique=True, blank=True, null=True)
    description = models.TextField()
    cover_image = models.ImageField(upload_to='textbooks/covers/')
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    
    # SEO Fields
    meta_title = models.CharField(max_length=70, blank=True, help_text="SEO title tag.")
    meta_description = models.CharField(max_length=160, blank=True, help_text="SEO meta description.")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Textbook"
        verbose_name_plural = "Textbooks"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} - {self.academic_level.name}"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('shop:textbook_detail', kwargs={'slug': self.slug})
