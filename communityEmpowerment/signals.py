from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.management import call_command
from .models import Tag

@receiver(post_save, sender=Tag)
def recalculate_similarity(sender, instance, **kwargs):
    """
    Trigger similarity matrix recalculation whenever a Tag instance is updated or created.
    """
    if 'weight' in instance.get_dirty_fields():
        call_command('precompute_scheme_similarity')
