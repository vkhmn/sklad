# Generated by Django 4.1.2 on 2022-10-20 04:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contactor', '0005_alter_bankdetails_account'),
    ]

    operations = [
        migrations.RenameField(
            model_name='person',
            old_name='name',
            new_name='full_name',
        ),
    ]
