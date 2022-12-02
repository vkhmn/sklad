from datetime import timedelta
from config.settings.base import *
import socket


DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1']
BASE_URL = 'http://127.0.0.1:8000'

NGROK_USE = False
NGROK_URL = '8b68-164-138-92-119.ap.ngrok.io'
if NGROK_USE:
    CSRF_TRUSTED_ORIGINS = [f'https://{NGROK_URL}']
    BASE_URL = f'https://{NGROK_URL}'
    ALLOWED_HOSTS += [NGROK_URL]

INSTALLED_APPS += [
    'debug_toolbar',
]

MIDDLEWARE += [
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]

INTERNAL_IPS = [
    '127.0.0.1',
]
# ips into Docker
hostname, _, ips = socket.gethostbyname_ex(socket.gethostname())
INTERNAL_IPS += [".".join(ip.split(".")[:-1] + ["1"]) for ip in ips]
CRON_TIME = dict(minute='*/2')

DOCUMENT_TIME_OUT = timedelta(minutes=2)
