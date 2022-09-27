# Generated by Django 4.1.1 on 2022-09-26 03:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Buyer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fio', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254)),
                ('phone', models.IntegerField()),
            ],
            options={
                'verbose_name': 'Покупатель',
                'verbose_name_plural': 'Покупатели',
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Nomenclature',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('article', models.IntegerField()),
                ('amount', models.IntegerField()),
                ('price', models.IntegerField()),
            ],
            options={
                'verbose_name': 'Номенклатура',
                'verbose_name_plural': 'Номенклатура',
            },
        ),
        migrations.CreateModel(
            name='Vendor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('address', models.CharField(max_length=100)),
                ('fio', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254)),
                ('phone', models.IntegerField()),
                ('category', models.ManyToManyField(to='sklad.category')),
            ],
            options={
                'verbose_name': 'Поставщик',
                'verbose_name_plural': 'Поставщики',
            },
        ),
        migrations.CreateModel(
            name='SubCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sklad.category')),
            ],
        ),
        migrations.CreateModel(
            name='Shipment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.IntegerField()),
                ('status', models.CharField(choices=[('vl', 'На проверке'), ('fi', 'Завершен'), ('ca', 'Отменен')], default='vl', max_length=2)),
                ('date', models.DateTimeField()),
                ('qr', models.CharField(max_length=100)),
                ('buyer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sklad.buyer')),
                ('content', models.ManyToManyField(to='sklad.nomenclature')),
            ],
            options={
                'verbose_name': 'Отгрузка',
                'verbose_name_plural': 'Отгрузки',
            },
        ),
        migrations.AddField(
            model_name='nomenclature',
            name='subcategory',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sklad.subcategory'),
        ),
        migrations.CreateModel(
            name='Delivery',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.IntegerField()),
                ('status', models.CharField(choices=[('vl', 'На проверке'), ('fi', 'Завершен'), ('ca', 'Отменен')], default='vl', max_length=2)),
                ('date', models.DateTimeField()),
                ('content', models.ManyToManyField(to='sklad.nomenclature')),
                ('vendor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sklad.vendor')),
            ],
            options={
                'verbose_name': 'Поставка',
                'verbose_name_plural': 'Поставки',
            },
        ),
    ]
