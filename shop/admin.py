from django.contrib import admin
from .models import AcademicLevel, Subject, Textbook

@admin.register(AcademicLevel)
class AcademicLevelAdmin(admin.ModelAdmin):
    list_display = ('name', 'order', 'slug')
    list_editable = ('order',)
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)
    ordering = ('order', 'name')

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_core', 'slug')
    list_filter = ('is_core', 'academic_levels')
    prepopulated_fields = {'slug': ('name', 'is_core')}
    filter_horizontal = ('academic_levels',)
    search_fields = ('name',)
    ordering = ('name',)

@admin.register(Textbook)
class TextbookAdmin(admin.ModelAdmin):
    list_display = ('title', 'subject', 'academic_level', 'book_type', 'price', 'curriculum', 'isbn')
    list_filter = ('book_type', 'curriculum', 'academic_level', 'subject')
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ('title', 'isbn', 'description')
    autocomplete_fields = ('subject', 'academic_level')
    fieldsets = (
        ('Publication Details', {
            'fields': ('title', 'slug', 'isbn', 'book_type', 'curriculum', 'price')
        }),
        ('Academic Categorization', {
            'fields': ('subject', 'academic_level')
        }),
        ('Content', {
            'fields': ('description', 'cover_image')
        }),
        ('SEO Metadata', {
            'fields': ('meta_title', 'meta_description'),
            'classes': ('collapse',)
        }),
    )
