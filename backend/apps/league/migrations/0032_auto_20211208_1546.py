# Generated by Django 3.2.9 on 2021-12-08 13:46

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('league', '0031_match_stadium'),
    ]

    operations = [
        migrations.CreateModel(
            name='Referee',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='ФИО судьи')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Создано')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Обновлено')),
            ],
            options={
                'verbose_name': 'Судья',
                'verbose_name_plural': 'Судьи',
            },
        ),
        migrations.AddField(
            model_name='stadium',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now, verbose_name='Создано'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='stadium',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, verbose_name='Обновлено'),
        ),
        migrations.AddField(
            model_name='match',
            name='main_referee',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='main_referee', to='league.referee', verbose_name='Главный судья'),
        ),
        migrations.AddField(
            model_name='match',
            name='other_referees',
            field=models.ManyToManyField(blank=True, to='league.Referee', verbose_name='Помощники судьи'),
        ),
    ]
