from django.core.management import BaseCommand
from django.contrib.auth.models import User
from django.core.management import call_command


class Command(BaseCommand):
    """Django команда для загрузки тестовых данных в базу данных."""

    def handle(self, *args, **options):
        if not User.objects.exists():
            self.stdout.write('Загрузка данных в базу данных...')
            call_command('loaddata', 'db.json')
            self.stdout.write(self.style.SUCCESS('Загрузка данных завершена!'))
