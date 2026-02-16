from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import CustomUser, Order, Notification


@receiver(post_save, sender=Order)
def create_user_profile(sender, instance, created, **kwargs):
    if instance.status in ['paid', 'canceled']:
        Notification.objects.create(
            sender = instance.user,
            receiver = instance.user,
            type = instance.status,
            order = instance
        )

