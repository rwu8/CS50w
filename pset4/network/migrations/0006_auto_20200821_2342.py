# Generated by Django 3.0.8 on 2020-08-21 23:42

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0005_auto_20200811_2158'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='likes',
        ),
        migrations.AddField(
            model_name='like',
            name='currently_liked',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='post',
            name='total_likes',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='post',
            name='user_likes',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL),
        ),
    ]