# Generated by Django 3.2.16 on 2023-01-10 14:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_manager', '0002_userprofile_phone_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='email_updates',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='text_updates',
            field=models.BooleanField(default=True),
        ),
    ]
