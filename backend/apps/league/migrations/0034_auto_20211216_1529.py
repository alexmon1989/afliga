# Generated by Django 3.2.9 on 2021-12-16 13:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('league', '0033_coach'),
    ]

    operations = [
        migrations.AddField(
            model_name='match',
            name='coach_team_1',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='coach_team_1', to='league.coach', verbose_name='Тренер команды 1'),
        ),
        migrations.AddField(
            model_name='match',
            name='coach_team_2',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='coach_team_2', to='league.coach', verbose_name='Тренер команды 2'),
        ),
    ]