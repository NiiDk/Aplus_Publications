from django.db import models
from django.utils import timezone

class NewsAnnouncement(models.Model):
    class Priority(models.IntegerChoices):
        LOW = 1, 'Low'
        NORMAL = 2, 'Normal'
        HIGH = 3, 'High'
        URGENT = 4, 'Urgent'

    title = models.CharField(max_length=255)
    content = models.TextField(help_text="Keep announcements concise for mobile readability.")
    
    priority = models.IntegerField(choices=Priority.choices, default=Priority.NORMAL)
    is_homepage_highlight = models.BooleanField(
        default=False, 
        help_text="Check to display this prominently on the home page."
    )
    
    is_published = models.BooleanField(default=True)
    scheduled_at = models.DateTimeField(
        default=timezone.now, 
        help_text="When should this announcement become visible?"
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-priority', '-scheduled_at']
        verbose_name = "Announcement"
        verbose_name_plural = "Announcements"

    def __str__(self):
        return f"[{self.get_priority_display()}] {self.title}"

    @property
    def is_active(self):
        return self.is_published and self.scheduled_at <= timezone.now()
