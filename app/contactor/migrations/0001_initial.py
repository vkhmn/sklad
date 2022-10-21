# Generated by Django 4.1.2 on 2022-10-19 23:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('nomenclature', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='BankDetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('account', models.IntegerField(verbose_name='Номер счета')),
                ('bank_name', models.CharField(max_length=100, verbose_name='Наименование банка')),
            ],
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Фамилия Имя Отчество')),
                ('email', models.EmailField(max_length=254, verbose_name='Email')),
                ('phone', models.IntegerField(verbose_name='Телефон')),
            ],
        ),
        migrations.CreateModel(
            name='Vendor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Наименование')),
                ('address', models.CharField(max_length=100, verbose_name='Адрес')),
                ('bank_details', models.OneToOneField(on_delete=django.db.models.deletion.DO_NOTHING, to='contactor.bankdetails', verbose_name='Банковские реквизиты')),
                ('categories', models.ManyToManyField(to='nomenclature.category', verbose_name='Категории')),
                ('contact_person', models.OneToOneField(on_delete=django.db.models.deletion.DO_NOTHING, to='contactor.person', verbose_name='Контактное лицо')),
            ],
            options={
                'verbose_name': 'Поставщик',
                'verbose_name_plural': 'Поставщики',
            },
        ),
        migrations.CreateModel(
            name='Buyer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('person', models.OneToOneField(on_delete=django.db.models.deletion.DO_NOTHING, to='contactor.person', verbose_name='Покупатель')),
            ],
            options={
                'verbose_name': 'Покупатель',
                'verbose_name_plural': 'Покупатели',
            },
        ),
    ]
