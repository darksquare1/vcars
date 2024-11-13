from django.db.models.signals import post_save
from django.dispatch import receiver
from accounts.models import Profile
from accounts.tasks import send_verify_email as send_email


@receiver(signal=post_save, sender=Profile)
def send_verify_email(sender, instance, *args, **kwargs):
    if not instance.user.is_staff and not instance.is_verified:
        send_email(instance.user.pk)