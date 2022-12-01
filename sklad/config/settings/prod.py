from datetime import timedelta
from config.settings.base import *

DEBUG = False
ALLOWED_HOSTS = ['vkhmn.ru', '127.0.0.1']
BASE_URL = 'http://vkhmn.ru:8000'
CRON_TIME = dict(minute=0)
DOCUMENT_TIME_OUT = timedelta(days=2)
