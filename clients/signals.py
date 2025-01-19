from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Client

@receiver(post_save, sender=Client)
def create_client_profile(sender, instance, created, **kwargs):
    """
    يتم استدعاء هذه الإشارة عند إنشاء عميل جديد.
    """
    if created:
        print(f"New client created: {instance.name}")
