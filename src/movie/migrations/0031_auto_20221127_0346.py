# Generated by Django 3.2.15 on 2022-11-26 20:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('movie', '0030_comment'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='avatar',
            field=models.ImageField(default='user_profile/anonymous.PNG', upload_to=''),
        ),
        migrations.AddField(
            model_name='comment',
            name='name',
            field=models.CharField(default=' ', max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='comment',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='publisher', to='movie.profile'),
        ),
    ]
