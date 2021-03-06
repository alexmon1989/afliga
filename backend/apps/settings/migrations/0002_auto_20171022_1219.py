# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-22 09:19
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('settings', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='footersettings',
            options={'verbose_name': 'Footer', 'verbose_name_plural': 'Footer'},
        ),
        migrations.AlterField(
            model_name='footersettings',
            name='contacts_block_html',
            field=models.TextField(blank=True, null=True, verbose_name='Текст блока "Контактная информация" (html)'),
        ),
        migrations.AlterField(
            model_name='footersettings',
            name='copyrights_block_html',
            field=models.TextField(blank=True, null=True, verbose_name='Текст блока копирайта (html)'),
        ),
        migrations.AlterField(
            model_name='footersettings',
            name='information_block_text',
            field=models.TextField(blank=True, null=True, verbose_name='Текст блока'),
        ),
    ]
