from config.settings.base import *


DEBUG = False
ALLOWED_HOSTS = ['vkhmn.ru']
BASE_URL = 'http://vkhmn.ru:8000'
CRON_TIME = dict(minute=0)
DOCUMENT_TIME_OUT = timedelta(days=2)