# Generated by Django 3.2.16 on 2023-03-13 12:33

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('blog', '0008_reply_message'),
    ]

    operations = [
        migrations.AddField(
            model_name='direct_message',
            name='marked_as_new',
            field=models.ManyToManyField(related_name='marked_as_new', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='direct_message',
            name='new_messages',
            field=models.BooleanField(default=True),
        ),
    ]
