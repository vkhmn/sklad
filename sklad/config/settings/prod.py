from datetime import timedelta
from config.settings.base import *

DEBUG = False
ALLOWED_HOSTS = ['vkhmn.ru', 'sklad.vkhmn.ru', '127.0.0.1']
BASE_URL = 'http://sklad.vkhmn.ru'
CRON_TIME = dict(minute=0)
DOCUMENT_TIME_OUT = timedelta(days=2)
