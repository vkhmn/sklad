from django.core.mail import send_mail
from django.template.loader import render_to_string

from sklad_django.celery import app
from sklad_django.settings import EMAIL_HOST_USER
from sklad.enams import messages
from sklad.models import Document
from sklad.qr import make_code
from sklad.utils import encode


@app.task
def send_email_to_buyer(document_id, status):
    user_email = Document.objects.get(pk=document_id).buyer.email

    if not user_email:
        raise ValueError('У покупателя нет email адреса')

    code = encode(document_id)
    url = f'http://127.0.0.0:8000/document/confirm/?code={code}'
    qrcode = make_code(url)

    try:
        context = {
            'subject': messages[status]['subject'],
            'message': messages[status]['message'],
            'qrcode': qrcode,
        }
    except KeyError:
        print(f'Нет одного из ключей: {status}, subject, message')
    else:
        html_message = render_to_string('sklad/email.html', context)
        send_mail(
            context['subject'],
            None,
            EMAIL_HOST_USER,
            [user_email],
            fail_silently=False,
            html_message=html_message
        )
