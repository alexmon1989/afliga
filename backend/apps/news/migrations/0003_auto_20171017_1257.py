# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-17 09:57
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0002_auto_20171013_1120'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='news',
            options={'verbose_name': 'Новость', 'verbose_name_plural': 'Новости'},
        ),
        migrations.AddField(
            model_name='news',
            name='image',
            field=models.ImageField(null=True, upload_to='', verbose_name='Изображение'),
        ),
        migrations.AddField(
            model_name='news',
            name='is_visible',
            field=models.BooleanField(default=True, verbose_name='Включено'),
        ),
    ]