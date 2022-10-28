from django.core.mail import send_mail
from django.template.loader import render_to_string

from config.celery import app
from config.settings import EMAIL_HOST_USER


@app.task
def send_email_to_buyer(email, message):
    print(message)
    html_message = render_to_string('document/email.html', message)
    subject = message.get('subject', '')

    send_mail(
        subject,
        None,
        EMAIL_HOST_USER,
        [email],
        fail_silently=False,
        html_message=html_message
    )
