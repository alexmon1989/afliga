# Generated by Django 2.2.24 on 2021-11-24 15:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('league', '0025_auto_20211124_1343'),
    ]

    operations = [
        migrations.AddField(
            model_name='matchlineup',
            name='team',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='league.Team', verbose_name='Команда'),
        ),
    ]
