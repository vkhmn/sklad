# Generated by Django 4.1.2 on 2022-10-21 00:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contactor', '0006_rename_name_person_full_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bankdetails',
            name='account',
            field=models.CharField(max_length=20, unique=True, verbose_name='Номер счета'),
        ),
    ]