# Generated by Django 3.2.16 on 2023-03-06 14:01

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('blog', '0007_direct_message_recipient'),
    ]

    operations = [
        migrations.CreateModel(
            name='Reply_Message',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField()),
                ('send_date', models.DateTimeField(blank=True, null=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('recipient', models.ManyToManyField(related_name='reply_recipient', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
