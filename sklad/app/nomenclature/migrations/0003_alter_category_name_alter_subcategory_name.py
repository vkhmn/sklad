# Generated by Django 4.1.2 on 2022-10-20 02:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nomenclature', '0002_store'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(max_length=100, unique=True, verbose_name='Категория'),
        ),
        migrations.AlterField(
            model_name='subcategory',
            name='name',
            field=models.CharField(max_length=100, unique=True, verbose_name='Подкатегория'),
        ),
    ]
