from django.urls import reverse
from django.core.mail import send_mail
from django.contrib.auth.models import User
from celeryapp.celery import app

@app.task
def send_verify_email(user_id):
    try:
        user = User.objects.get(pk=user_id)
        send_mail(
            'Подтверждение вашего аккаунта',
            'Проследуйте по этой ссылке для подтверждения вашей почты: '
            f'http://localhost:8000{reverse('verify', args=[str(user.profile.verification_uuid)])}',
            'pixarcars111222@gmail.com',
            [user.email],
            fail_silently=False
        )
    except User.DoesNotExist:
        print('Попытка отправить сообщение несуществующему пользователю', user_id)