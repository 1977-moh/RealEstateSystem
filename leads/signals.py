from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Lead

@receiver(post_save, sender=Lead)
def notify_assigned_employee(sender, instance, created, **kwargs):
    """
    إشعار عند إنشاء Lead جديد.
    """
    if created and instance.assigned_to:
        print(f"New lead assigned to {instance.assigned_to.full_name}: {instance.name}")
