from django.contrib import admin
from .models import NewsAnnouncement

@admin.register(NewsAnnouncement)
class NewsAnnouncementAdmin(admin.ModelAdmin):
    list_display = ('title', 'priority', 'is_homepage_highlight', 'scheduled_at', 'is_published')
    list_filter = ('priority', 'is_homepage_highlight', 'is_published', 'scheduled_at')
    search_fields = ('title', 'content')
    list_editable = ('priority', 'is_homepage_highlight', 'is_published')
    date_hierarchy = 'scheduled_at'
    ordering = ('-priority', '-scheduled_at')

    fieldsets = (
        ('Content', {
            'fields': ('title', 'content')
        }),
        ('Display Settings', {
            'fields': ('priority', 'is_homepage_highlight')
        }),
        ('Scheduling', {
            'fields': ('is_published', 'scheduled_at')
        }),
    )
