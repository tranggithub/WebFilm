# Generated by Django 3.2.15 on 2022-11-26 20:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movie', '0031_auto_20221127_0346'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='name',
            field=models.CharField(blank=True, default=' ', max_length=255, null=True),
        ),
    ]