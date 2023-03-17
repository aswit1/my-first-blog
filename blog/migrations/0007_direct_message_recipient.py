# Generated by Django 3.2.16 on 2023-03-03 13:41

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('blog', '0006_direct_message'),
    ]

    operations = [
        migrations.AddField(
            model_name='direct_message',
            name='recipient',
            field=models.ManyToManyField(related_name='recipient', to=settings.AUTH_USER_MODEL),
        ),
    ]