# Generated by Django 4.1.2 on 2022-11-28 16:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movie', '0046_remove_movie_trailer'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='category',
            name='movie',
        ),
        migrations.AddField(
            model_name='movie',
            name='categogies',
            field=models.ManyToManyField(to='movie.category', verbose_name='category'),
        ),
    ]
