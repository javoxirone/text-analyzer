from django.contrib import admin
from .models import File


class FileAdmin(admin.ModelAdmin):
    list_display = ('file_name', 'file', 'uploaded_at')
    list_display_links = ('file_name', 'file')

# Register your models here.
admin.site.register(File, FileAdmin)
