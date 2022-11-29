# Generated by Django 3.2.15 on 2022-11-29 06:59

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('movie', '0050_auto_20221129_0740'),
    ]

    operations = [
        migrations.AddField(
            model_name='movie',
            name='history',
            field=models.ManyToManyField(related_name='movie_history', to=settings.AUTH_USER_MODEL),
        ),
    ]
