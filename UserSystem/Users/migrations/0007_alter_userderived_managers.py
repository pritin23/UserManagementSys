# Generated by Django 4.0.6 on 2022-07-25 05:25

import django.contrib.auth.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Users', '0006_alter_userderived_managers'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='userderived',
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
    ]
