# Generated by Django 3.0.7 on 2020-08-07 14:01

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_music_db', '0002_auto_20200806_2139'),
    ]

    operations = [
        migrations.AlterField(
            model_name='song',
            name='cdYear',
            field=models.CharField(blank=True, max_length=4, validators=[django.core.validators.MinLengthValidator(4)]),
        ),
    ]
