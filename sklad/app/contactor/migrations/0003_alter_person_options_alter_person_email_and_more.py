# Generated by Django 4.1.2 on 2022-10-20 01:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contactor', '0002_alter_bankdetails_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='person',
            options={'verbose_name': 'Контактное лицо', 'verbose_name_plural': 'Контактные лица'},
        ),
        migrations.AlterField(
            model_name='person',
            name='email',
            field=models.EmailField(max_length=254, unique=True, verbose_name='Email'),
        ),
        migrations.AlterField(
            model_name='person',
            name='phone',
            field=models.IntegerField(unique=True, verbose_name='Телефон'),
        ),
    ]
