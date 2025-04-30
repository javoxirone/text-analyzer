import os
from django.db import models

from main.services import compute_tf_idf, handle_text_file
from project.settings import BASE_DIR


# Create your models here.
class File(models.Model):
    file = models.FileField(upload_to='files/', null=False, blank=False, verbose_name="Файл")
    file_name = models.CharField(max_length=255, null=False, blank=True, verbose_name="Имя файла", editable=False)
    is_public = models.BooleanField(default=False, null=False, blank=False,
                                    verbose_name="Статус видимости (публичный?)")
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
        analysis_result = handle_text_file(os.path.join(BASE_DIR, self.file.path))
        tfidf_data = [
            {"word": word, "tf": tf, "idf": idf}
            for word, tf, idf in analysis_result
        ]
        new_file_analysis = FileAnalysis.objects.create(file=self, tfidf_data=tfidf_data)

    def __str__(self):
        return self.file_name

    class Meta:
        verbose_name = "Файл"
        verbose_name_plural = "Файлы"


class FileAnalysis(models.Model):
    file = models.OneToOneField(File, null=False, blank=False, verbose_name="Файл", on_delete=models.CASCADE)
    tfidf_data = models.JSONField(null=False, blank=True, verbose_name="Данные TF-IDF")
    created_at = models.DateTimeField(auto_now_add=True, null=False, blank=False, verbose_name="Дата и время загрузки")

    def __str__(self):
        return f"{self.pk} - {self.created_at}"

    class Meta:
        verbose_name = "Файл"
        verbose_name_plural = "Файлы"
