from django.contrib import admin
from .models import Page, FAQ, Enquiry

@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'last_updated', 'is_active')
    prepopulated_fields = {'slug': ('title',)}

@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ('question', 'category', 'order')
    list_editable = ('order', 'category')
    list_filter = ('category',)

@admin.register(Enquiry)
class EnquiryAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'role', 'created_at', 'is_read')
    list_filter = ('is_read', 'role', 'created_at')
    search_fields = ('name', 'email', 'message')
    readonly_fields = ('name', 'email', 'role', 'message', 'created_at')
    list_editable = ('is_read',)
