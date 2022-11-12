from config.settings.base import *
import socket


DEBUG = True

ALLOWED_HOSTS = []
BASE_URL = 'http://127.0.0.1:8000'

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
