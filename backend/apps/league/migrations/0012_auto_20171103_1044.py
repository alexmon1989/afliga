# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-11-03 08:44
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('league', '0011_auto_20171030_1333'),
    ]

    operations = [
        migrations.AddField(
            model_name='match',
            name='goals_team_1',
            field=models.IntegerField(blank=True, default=None, null=True, verbose_name='Голов забила команда хозяев'),
        ),
        migrations.AddField(
            model_name='match',
            name='goals_team_2',
            field=models.IntegerField(blank=True, default=None, null=True, verbose_name='Голов забила команда гостей'),
        ),
    ]