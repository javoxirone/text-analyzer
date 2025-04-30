import os
from django.db import models


# Create your models here.
class File(models.Model):
    file = models.FileField(upload_to='files/', null=False, blank=False, verbose_name="Файл")
    file_name = models.CharField(max_length=255, null=False, blank=True, verbose_name="Имя файла", editable=False)
    is_public = models.BooleanField(default=False, null=False, blank=False, verbose_name="Статус видимости (публичный?)")
    uploaded_at = models.DateTimeField(auto_now_add=True, null=False, blank=False, verbose_name="Дата и время загрузки")

    def save(self, *args, **kwargs):
        if not self.file_name and self.file:
            filename = self.file.name.split('/')[-1]

            if len(filename) > 255:
                name, ext = os.path.splitext(filename)
                truncated_name = name[:251 - len(ext)]
                filename = f"{truncated_name}...{ext}"

            self.file_name = filename
        super().save(*args, **kwargs)

    def __str__(self):
        return self.file_name

    class Meta:
        verbose_name = "Файл"
        verbose_name_plural = "Файлы"
