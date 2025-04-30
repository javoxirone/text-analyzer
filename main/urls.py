from django.urls import path

from .views import index_view, new_file_upload_view

urlpatterns = [
    path('', index_view, name='index'),
    path('new-file-upload/', new_file_upload_view, name='new-file-upload'),
]
