# Generated by Django 4.0.6 on 2022-07-25 05:34

import Users.manager
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Users', '0007_alter_userderived_managers'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='userderived',
            managers=[
                ('objects', Users.manager.CustomAccountManager()),
            ],
        ),
    ]
