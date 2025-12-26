from django.contrib import admin
from .models import Resource, ResourceDownload

@admin.register(Resource)
class ResourceAdmin(admin.ModelAdmin):
    list_display = ('title', 'resource_type', 'academic_level', 'download_count', 'created_at')
    list_filter = ('resource_type', 'academic_level', 'created_at')
    search_fields = ('title', 'description')
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ('download_count',)

@admin.register(ResourceDownload)
class ResourceDownloadAdmin(admin.ModelAdmin):
    list_display = ('resource', 'ip_address', 'downloaded_at')
    readonly_fields = ('resource', 'ip_address', 'user_agent', 'downloaded_at')
    
    def has_add_permission(self, request):
        return False
