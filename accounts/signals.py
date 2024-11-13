from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.urls import reverse


@receiver(signal=post_save, sender=User)
def send_verify_email(sender, instance, *args, **kwargs):
    if not instance.is_staff and not instance.profile.is_verified:
        send_mail(
            'Подтверждение вашего аккаунта',
            'Проследуйте по этой ссылке для подтверждения вашей почты: '
            f'http://localhost:8000{reverse('verify', args=[str(instance.profile.verification_uuid)])}',
            'pixarcars111222@gmail.com',
            [instance.email],
            fail_silently=False
        )
