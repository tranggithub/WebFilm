# Generated by Django 3.2.15 on 2022-12-01 16:30

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('movie', '0056_remove_movie_trailer_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='reply',
            field=models.ManyToManyField(related_name='comnent_reply', to=settings.AUTH_USER_MODEL),
        ),
    ]
