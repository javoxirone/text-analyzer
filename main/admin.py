from django.contrib import admin
from .models import File, FileAnalysis


class FileAnalysisInline(admin.TabularInline):
    model = FileAnalysis
    extra = 0
    fk_name = 'file'


class FileAdmin(admin.ModelAdmin):
    list_display = ('file_name', 'file', 'uploaded_at')
    list_display_links = ('file_name', 'file')
    inlines = [FileAnalysisInline]


# Register your models here.
admin.site.register(File, FileAdmin)
