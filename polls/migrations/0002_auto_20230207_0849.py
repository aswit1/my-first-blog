# Generated by Django 3.2.16 on 2023-02-07 13:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='poll',
            old_name='votes',
            new_name='vote1',
        ),
        migrations.AddField(
            model_name='poll',
            name='vote2',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='poll',
            name='vote3',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='poll',
            name='vote4',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='poll',
            name='option1',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='poll',
            name='option2',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='poll',
            name='option3',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='poll',
            name='option4',
            field=models.CharField(max_length=200),
        ),
    ]
