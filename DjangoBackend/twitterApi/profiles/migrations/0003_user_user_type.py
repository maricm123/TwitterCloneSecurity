# Generated by Django 4.1.7 on 2023-03-25 18:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0002_user_is_staff'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='user_type',
            field=models.CharField(blank=True, choices=[('default', 'Default User'), ('business', 'Business User')], max_length=10, null=True),
        ),
    ]
