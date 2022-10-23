from django.core.mail import send_mail
from django.template.loader import render_to_string

from config.celery import app
from config.settings import EMAIL_HOST_USER
from app.core.utils import get_confirm_url, make_qrcode
from .enums import messages
from .models import Document, Status

# TODO:
# Add new periodic task -> Cancel old orders


@app.task
def send_email_to_buyer(document_id, status):
    user_email = Document.objects.get(pk=document_id).buyer.person.email

    if not user_email:
        raise ValueError('У покупателя нет email адреса')

    context = dict()
    try:
        context['subject'] = messages[status]['subject']
        context['message'] = messages[status]['message']
    except KeyError:
        print(f'Нет одного из ключей: {status}, subject, message')
    else:
        if status == Status.COLLECTED:
            context['qrcode'] = make_qrcode(document_id)
            context['url'] = get_confirm_url(document_id)

        html_message = render_to_string('document/email.html', context)

        send_mail(
            context['subject'],
            None,
            EMAIL_HOST_USER,
            [user_email],
            fail_silently=False,
            html_message=html_message
        )
