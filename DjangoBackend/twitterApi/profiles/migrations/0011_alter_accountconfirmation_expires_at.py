# Generated by Django 4.2.1 on 2023-05-27 18:19

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0010_alter_accountconfirmation_expires_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='accountconfirmation',
            name='expires_at',
            field=models.DateTimeField(default=datetime.datetime(2023, 5, 28, 18, 19, 44, 527502, tzinfo=datetime.timezone.utc)),
        ),
    ]
