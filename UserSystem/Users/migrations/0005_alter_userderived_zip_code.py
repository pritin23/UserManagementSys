# Generated by Django 4.0.6 on 2022-07-23 15:59

import Users.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Users', '0004_alter_userderived_password'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userderived',
            name='zip_code',
            field=models.CharField(max_length=6, validators=[Users.models.get_number]),
        ),
    ]
