# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-04-18 12:19
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0007_auto_20171031_2135'),
    ]

    operations = [
        migrations.AddField(
            model_name='bombardierspenaltiestablesettings',
            name='show_bombardiers',
            field=models.BooleanField(default=True, verbose_name='Показывать бомбардиров'),
        ),
        migrations.AddField(
            model_name='bombardierspenaltiestablesettings',
            name='show_penalties',
            field=models.BooleanField(default=True, verbose_name='Показывать штрафников'),
        ),
        migrations.AddField(
            model_name='bombardierspenaltiestablesettings',
            name='show_table',
            field=models.BooleanField(default=True, verbose_name='Показывать турнирную таблицу'),
        ),
    ]
