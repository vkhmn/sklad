from django.core.mail import send_mail

from sklad_django.celery import app
from sklad_django.settings import EMAIL_HOST_USER
from sklad.enams import messages
from sklad.models import Document


@app.task
def send_email_to_buyer(document_id, status):
    user_email = Document.objects.get(pk=document_id).buyer.email

    if not user_email:
        raise ValueError('У покупателя нет email адреса')

    try:
        subject = messages[status]['subject']
        message = messages[status]['message']
    except KeyError as e:
        print(f'Нет одного из ключей: {status}, subject, message')
    else:
        send_mail(
            subject,
            message,
            EMAIL_HOST_USER,
            [user_email],
            fail_silently=False,
        )
