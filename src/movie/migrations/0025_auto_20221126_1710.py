# Generated by Django 3.2.15 on 2022-11-26 10:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movie', '0024_alter_profile_avatar'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='avatar',
            field=models.ImageField(blank=True, null=True, upload_to='user_profile'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='birthday',
            field=models.DateField(blank=True, default='2022-01-01', null=True),
        ),
    ]