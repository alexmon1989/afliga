# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-04-18 12:43
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0008_auto_20180418_1519'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bombardierspenaltiestablesettings',
            name='tournament',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='league.Tournament', verbose_name='Турнир'),
            preserve_default=False,
        ),
    ]
