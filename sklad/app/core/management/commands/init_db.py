from django.core.management import BaseCommand
from django.contrib.auth.models import User
from django.core.management import call_command


class Command(BaseCommand):
    """Django команда для загрузки тестовых данных в базу данных."""

    def handle(self, *args, **options):
        self.stdout.write('Загрузка данных в базу данных...')
        if not User.objects.exists():
            call_command('loaddata', 'db.json')

        self.stdout.write(self.style.SUCCESS('Загрузка данных завершена!'))