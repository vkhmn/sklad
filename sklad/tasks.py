from django.core.mail import send_mail
from sklad_django.celery import app
from sklad.models import *
from sklad_django.settings import EMAIL_HOST_USER


@app.task
def send_email_to_buyer(document_id, status):
    user_email = Document.objects.values(
        'buyer__email').filter(pk=document_id).first()
    user_email = user_email['buyer__email']

    messages = {
        Status.COLLECTED: {
            'header': 'Заказ собран',
            'text': 'QR-code'
        },
        Status.CANCELED: {
            'header': 'Заказ отменен',
            'text': 'Нет товара на складе'
        }
    }

    send_mail(
        messages[status]['header'],
        messages[status]['text'],
        EMAIL_HOST_USER,
        [user_email],
        fail_silently=False,
    )
