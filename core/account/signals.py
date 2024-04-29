from django.db.models.signals import post_save
from django.dispatch import receiver



from .models import DriverProfile,CustomerProfile,User


@receiver(post_save, sender=User)
def create_profile_handler(sender, instance, created, **kwargs):
    if created:
        if instance.is_driver:
            DriverProfile.objects.create(user=instance)
        elif instance.is_customer:
            CustomerProfile.objects.create(user=instance)
