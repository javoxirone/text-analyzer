from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import File, FileAnalysis
from .services import compute_tfidf_for_file, update_all_file_analyses


@receiver(post_save, sender=File)
def file_saved_handler(sender, instance, created, **kwargs):
    try:
        tfidf_data = compute_tfidf_for_file(instance)
        FileAnalysis.objects.update_or_create(
            file=instance,
            defaults={"tfidf_data": tfidf_data}
        )
        update_all_file_analyses()
    except Exception as e:
        print(f"Error processing analysis for {instance.file_name}: {str(e)}")
