from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Client
from .integrations import assign_employee_to_client

@receiver(post_save, sender=Client)
def auto_assign_employee(sender, instance, created, **kwargs):
    if created:
        assign_employee_to_client(instance)
